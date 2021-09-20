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

def get_recommendation(student):
	if student.result >= (round(len(student.scores)/2)):
		print("You passed the test!")
	elif student.result < (round(len(student.scores)/2)):
		print("You failed the test...")

	if student.result >= student.expectedResult:
		print("Congratulations! You have reached our expectations!")
	elif student.result < student.expectedResult:
		print("Overall, you did not meet expectations...")

	for question in range(len(student.scores)):

		if student.expectedScores[question] == 1:
			print(" Expected result: CORRECT")
		elif student.expectedScores[question] == 0:
			print(" Expected result: INCORRECT")

		if student.scores[question] != 0 and student.expectedScores[question] != 0: # RCEC
			print("> We expected you to get this question correctly and you got the question correctly! Good job!")
		elif student.scores[question] != 0 and student.expectedScores[question] == 0: # RCEW
			print("> We expected you to get this question wrong but you got the question correctly! Good job!")
			print("  However, we still recommend you to review this question.")
		elif student.scores[question] == 0 and student.expectedScores[question] != 0: # RWEC
			print("> We expected you to get this question correctly however you got the question wrong.")
			print("  We highly recommend that you review this question and similar questions to it.")
		if student.scores[question] == 0 and student.expectedScores[question] == 0: #RWEW
			print("> We expected you to get this question wrong. Unfortunately, you did get the question wrong.")
			print("  We highly recommend that you review this question and similar questions to it.")

def collabFilter():
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
            
    allExpectedResults = []
    allResults = []
    for student in students:
        allExpectedResults.append(student.expectedResult)
        allResults.append(student.result)

    currentStudent = 1

    for student in students:
        print(student.name,"\t| Scores:",student.scores,"| Expected Scores:",student.expectedScores,"| Results:",student.result,"\t| Expected Result:",student.expectedResult)
    
    print("\nClass Minimum:",min(allResults),"| Class Maximum:",max(allResults),"| Class Mean:",statistics.mean(allResults))
    print("Minimum Expected:",min(allExpectedResults),"| Maximum Expected:",max(allExpectedResults),"| Mean Expected:",statistics.mean(allExpectedResults))

    print("\nRecommendation for",students[currentStudent-1].name)
    print("Your result:",students[currentStudent-1].result,"| Expected result:",students[currentStudent-1].expectedResult)

    get_recommendation(students[currentStudent-1]) # THIS IS IMPORTANT
    print()

