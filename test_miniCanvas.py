import unittest
from user import UserManager, User
from course import CourseManager, Course
from assignment import Assignment, Submission


class TestUserManager(unittest.TestCase):
    def setUp(self):
        self.usermanager = UserManager()
        self.usermanager.create_a_user("Brianna", "pwd", "student")
        self.usermanager.create_a_user("Maddy", "pwd", "teacher")
        self.usermanager.create_a_user("Carolina", "pwd", "admin")

    def test_generate_id(self):
        # Arrange
        expected_id = 4

        # Act
        generated_id = self.usermanager.generate_id()

        # Assert
        self.assertEqual(generated_id, expected_id)

    def test_create_a_user(self):
        # Arrange
        initial_user_count = len(self.usermanager.user_list)
        new_user_name = "TestUser"
        new_user_type = "student"

        # Act
        self.usermanager.create_a_user(new_user_name, "pwd", new_user_type)
        updated_user_count = len(self.usermanager.user_list)

        # Assert
        self.assertEqual(updated_user_count, initial_user_count + 1)
        self.assertEqual(self.usermanager.user_list[-1].name, new_user_name)
        self.assertEqual(self.usermanager.user_list[-1].type, new_user_type)

    def test_find_users(self):
        # Arrange
        user_ids_to_find = [1, 2]
        expected_user_names = ["Brianna", "Maddy"]

        # Act
        found_users = self.usermanager.find_users(user_ids_to_find)

        # Assert
        self.assertEqual(len(found_users), len(user_ids_to_find))
        for i, user in enumerate(found_users):
            self.assertEqual(user.name, expected_user_names[i])


class TestUser(unittest.TestCase):
    def test_user_initialization(self):
        # Test valid user initialization
        user_id = 1
        name = "John"
        password = "pwd"
        user_type = "student"
        user = User(user_id, name, password, user_type)
        self.assertEqual(user.user_id, user_id)
        self.assertEqual(user.name, name)
        self.assertEqual(user.password, password)
        self.assertEqual(user.type, user_type)

        # Test invalid user ID
        with self.assertRaises(ValueError):
            User(-1, name, password, user_type)

        # Test invalid name
        with self.assertRaises(ValueError):
            User(user_id, "", password, user_type)

        # Test invalid password
        with self.assertRaises(ValueError):
            User(user_id, name, "", user_type)

        # Test invalid user type
        with self.assertRaises(ValueError):
            User(user_id, name, password, "")

        # Test invalid user type
        with self.assertRaises(ValueError):
            User(user_id, name, password, "invalid_type")

class TestCourseManager(unittest.TestCase):
    def setUp(self):
        self.course_manager = CourseManager()

    def test_create_a_course_valid_input(self):
        # Valid input: non-empty course code, semester, and teacher list
        course_code = "CS101"
        semester = "Spring 2024"
        teacher_list = ["John Doe", "Jane Smith"]
        
        # Create a new course
        course_id = self.course_manager.create_a_course(course_code, semester, teacher_list)

        # Verify that the course was created successfully
        self.assertTrue(course_id > 0)  # Course ID should be a positive integer
        self.assertEqual(len(self.course_manager.course_list), 1)  # Course list should contain one course

    def test_sync_with_database(self):
        self.course_manager.sync_with_database()

    def test_create_a_course_invalid_input(self):
        # Invalid input: empty course code
        course_code = ""
        semester = "Spring 2024"
        teacher_list = ["John Doe", "Jane Smith"]

        # Verify that ValueError is raised
        with self.assertRaises(ValueError):
            self.course_manager.create_a_course(course_code, semester, teacher_list)

        # Invalid input: empty semester
        course_code = "CS101"
        semester = ""
        teacher_list = ["John Doe", "Jane Smith"]

        # Verify that ValueError is raised
        with self.assertRaises(ValueError):
            self.course_manager.create_a_course(course_code, semester, teacher_list)

        # Invalid input: empty teacher list
        course_code = "CS101"
        semester = "Spring 2024"
        teacher_list = []

        # Verify that ValueError is raised
        with self.assertRaises(ValueError):
            self.course_manager.create_a_course(course_code, semester, teacher_list)

        # Invalid input: teacher list is not a list
        course_code = "CS101"
        semester = "Spring 2024"
        teacher_list = "John Doe"  # Not a list

        # Verify that ValueError is raised
        with self.assertRaises(ValueError):
            self.course_manager.create_a_course(course_code, semester, teacher_list)

        # Invalid input: teacher name in the list is not a string
        course_code = "CS101"
        semester = "Spring 2024"
        teacher_list = ["John Doe", 123]  # Int instead of string

        # Verify that ValueError is raised
        with self.assertRaises(ValueError):
            self.course_manager.create_a_course(course_code, semester, teacher_list)

        # Invalid input: teacher name in the list is an empty string
        course_code = "CS101"
        semester = "Spring 2024"
        teacher_list = ["John Doe", ""]  # Empty string

        # Verify that ValueError is raised
        with self.assertRaises(ValueError):
            self.course_manager.create_a_course(course_code, semester, teacher_list)


class TestCourse(unittest.TestCase):
    def setUp(self):
        self.teacher_list = [User(1, "Mark", "pwd", "teacher")]
        self.student_list = [User(2, "Anthony", "pwd", "student")]
        self.course = Course(1, "COSC381", "Winter", self.teacher_list)

    def test_import_students(self):
        # Arrange
        initial_student_count = len(self.course.student_list)

        # Act
        self.course.import_students(self.student_list)
        updated_student_count = len(self.course.student_list)

        # Assert
        self.assertEqual(updated_student_count, initial_student_count + len(self.student_list))
        self.assertEqual(self.course.student_list[-1].name, "Anthony")

    def test_create_an_assignment(self):
        # Arrange
        initial_assignment_count = len(self.course.assignment_list)
        due_date = "2024-04-21"

        # Act
        self.course.create_an_assignment(due_date)
        updated_assignment_count = len(self.course.assignment_list)

        # Assert
        self.assertEqual(updated_assignment_count, initial_assignment_count + 1)

class TestAssignment(unittest.TestCase):
    def test_assignment_initialization(self):
        # Test valid initialization
        assignment_id = 1
        due_date = "2024-04-21"
        course_id = 1
        assignment = Assignment(assignment_id, due_date, course_id)
        self.assertEqual(assignment.assignment_id, assignment_id)
        self.assertEqual(assignment.due_date, due_date)
        self.assertEqual(assignment.course_id, course_id)
        self.assertEqual(assignment.submission_list, [])

        # Test invalid assignment ID
        with self.assertRaises(ValueError):
            Assignment(-1, due_date, course_id)

        # Test invalid due date
        with self.assertRaises(ValueError):
            Assignment(assignment_id, None, course_id)

        # Test invalid course ID
        with self.assertRaises(ValueError):
            Assignment(assignment_id, due_date, -1)

    def test_submit_method(self):
        assignment = Assignment(1, "2024-04-21", 1)
        submission = Submission(1, "Content")

        # Test valid submission
        assignment.submit(submission)
        self.assertEqual(len(assignment.submission_list), 1)
        self.assertEqual(assignment.submission_list[0], submission)

        # Test invalid submission (not an instance of Submission)
        with self.assertRaises(ValueError):
            assignment.submit("Not a submission")


class TestSubmission(unittest.TestCase):
    def test_submission_initialization(self):
        # Test valid initialization
        student_id = 1
        content = "Content"
        submission = Submission(student_id, content)
        self.assertEqual(submission.student_id, student_id)
        self.assertEqual(submission.submission, content)
        self.assertIsNone(submission.grade)

        # Test invalid student ID
        with self.assertRaises(ValueError):
            Submission(-1, content)

        # Test invalid content
        with self.assertRaises(ValueError):
            Submission(student_id, None)


if __name__ == "__main__":
    unittest.main()