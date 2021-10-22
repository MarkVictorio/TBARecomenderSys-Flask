import math, statistics
from flaskblog.models import Question, Quiz_user_answer, Quiz_user_taken
from flaskblog import db

class Student():
	def __init__(self, name, scores):
		self.name = name
		self.scores = scores # This is a list, ideally.
		self.expectedScores = None
		self.result = None # The actual score for the quiz.
		self.expectedResult = None # Collaborative filtering exclusive. Will use eventually.

	def compute_result(self):
		self.result = 0
		for score in self.scores:
			if score != -1:
				self.result += score

def get_euclidean_similarity(targetStudent, student, targetScore):
	euclideanDistance = 0
	for score in range(len(targetStudent.scores)):
		if score != targetScore:
			euclideanDistance += (targetStudent.scores[score] - student.scores[score])**2
	euclideanDistance = math.sqrt(euclideanDistance)

	euclideanSimilarity = 1 / (1 + euclideanDistance)

	return euclideanSimilarity

def collabFilter():
    percentErrors = []
    absoluteErrors = []
    variancesResult = []
    variancesExpected = []
    student_count = Quiz_user_taken.query.count()
    students = []
    for x in range(student_count):
        answerList = []
        answers = Quiz_user_answer.query.filter_by(user_id = x+1)
        for j in answers:
            if j.is_correct == True:
                answerList.append(1)
            elif j.is_correct == False:
                answerList.append(0)
        students.append(Student(x+1,answerList))
        students[x].compute_result()
    
    for targetStudent in students:
        expectedScores = []
        expectedResult = 0
        for targetScore in range(len(targetStudent.scores)):
            expectedScore = 0
            expectedScoreAbove = 0
            expectedScoreBelow = 0
            for student in students:
                if student is not targetStudent:
                    expectedScoreAbove += get_euclidean_similarity(targetStudent,student,targetScore)*student.scores[targetScore]
                    expectedScoreBelow += get_euclidean_similarity(targetStudent,student,targetScore)
            expectedScore = expectedScoreAbove / expectedScoreBelow
            expectedScore = int(round(expectedScore,0))
            expectedScores.append(expectedScore)
            expectedResult += expectedScore
            
        targetStudent.expectedResult = expectedResult
        targetStudent.expectedScores = expectedScores

    for student in students:
        for i in range(len(student.expectedScores)):
            cf_expect = Quiz_user_answer.query.filter_by(user_id = student.name).filter_by(question_id = i+1).first()
            cf_expect.expected = student.expectedScores[i]
            db.session.commit()

    print()
    print("Student Raw Score Matrix")

    for student in students:
        student.compute_result()
        print(student.name,"\t| Scores:",student.scores,"\t| Result:",student.result)

    print()
    print("Student Expected Score Matrix")

    for student in students:
        print(student.name,"\t| Expected Scores:",student.expectedScores," | Expected Result:",student.expectedResult)
            
    allExpectedResults = []
    allResults = []
    for student in students:
        allExpectedResults.append(student.expectedResult)
        allResults.append(student.result)
    
    print("\nClass Minimum:",min(allResults),"| Class Maximum:",max(allResults),"| Class Mean:",statistics.mean(allResults))
    print("Minimum Expected:",min(allExpectedResults),"| Maximum Expected:",max(allExpectedResults),"| Mean Expected:",statistics.mean(allExpectedResults))

    variancesResult.append(statistics.variance(allResults))
    variancesExpected.append(statistics.variance(allExpectedResults))
    percentErrors.append((abs(statistics.mean(allResults) - statistics.mean(allExpectedResults)) / statistics.mean(allResults))*100)
    absoluteErrors.append(abs(statistics.mean(allResults) - statistics.mean(allExpectedResults)))

    print("\nResult Variance:",round(statistics.mean(variancesResult),4))
    print("Expected Result Variance:",round(statistics.mean(variancesExpected),4))
    print("\nPercent Error of Both Means:",round(statistics.mean(percentErrors),4),"%")
    print("Absolute Error of Both Means:",round(sum(absoluteErrors)/len(absoluteErrors),4))

    print()