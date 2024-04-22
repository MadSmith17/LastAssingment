from fastapi import FastAPI, HTTPException
from typing import List
from course import CourseManager, Course
from user import UserManager

app = FastAPI()
course_manager = CourseManager()
user_manager = UserManager()

@app.get("/")
def welcome():
    return "Welcome to our miniCanvas!"

@app.post("/courses/{coursecode}")
def create_a_course(coursecode: str, 
                    semester: str, 
                    teacher_id_list: List[int]) -> int:
    # Check if teacher IDs are provided
    if not teacher_id_list:
        raise HTTPException(status_code=400, detail="No teacher IDs provided.")

    # Find users with provided IDs
    teacher_list = user_manager.find_users(teacher_id_list)
    if not teacher_list:
        raise HTTPException(status_code=404, detail="No teachers found with provided IDs.")
    
    # Create course
    try:
        course_id = course_manager.create_a_course(coursecode, semester, teacher_list, "admin")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    return course_id

@app.put("/courses/{courseid}/students")
def import_students(courseid: int,
                    student_id_list: List[int]) -> None:
    # Check if student IDs are provided
    if not student_id_list:
        raise HTTPException(status_code=400, detail="No student IDs provided.")

    # Find course
    course = course_manager.find_a_course(courseid)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")
    
    # Find users with provided IDs
    student_list = user_manager.find_users(student_id_list)
    if not student_list:
        raise HTTPException(status_code=404, detail="No students found with provided IDs.")
    
    # Import students to the course
    try:
        course.import_students(student_list)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    
    return None