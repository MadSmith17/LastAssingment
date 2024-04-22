class Assignment:
    def __init__(self, assignment_id, due_date, course_id):
        # Input validation
        if not isinstance(assignment_id, int) or assignment_id <= 0:
            raise ValueError("Assignment ID must be a positive integer.")
        
        if not due_date:
            raise ValueError("Due date cannot be empty.")
        
        if not isinstance(course_id, int) or course_id <= 0:
            raise ValueError("Course ID must be a positive integer.")
        
        self.assignment_id = assignment_id
        self.due_date = due_date
        self.course_id = course_id
        self.submission_list = []

    def submit(self, submission):
        if not isinstance(submission, Submission):
            raise ValueError("Submission must be an instance of the Submission class.")
        
        self.submission_list.append(submission)

class Submission:
    def __init__(self, student_id, content):
        # Input validation
        if not isinstance(student_id, int) or student_id <= 0:
            raise ValueError("Student ID must be a positive integer.")
        
        if not content:
            raise ValueError("Submission content cannot be empty.")
        
        self.student_id = student_id
        self.submission = content
        self.grade = None  # Initially set to None