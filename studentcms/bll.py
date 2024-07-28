# Business Logic Lever
from .models import Person, Student, StudentList, CourseList, StudentCourseList  # noqa


class StudentManager(StudentList):
    def __init__(self):
        super().__init__()
