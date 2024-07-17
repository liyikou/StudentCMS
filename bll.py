# Business Logic Lever
from models import Person, Student, StudentList, CourseList, StudentCourseList
from utils.public_utils import format_print


class StudentManager(StudentList):
    def __init__(self):
        super().__init__()

