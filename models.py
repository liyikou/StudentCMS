from . import settings
from .utils.pickle_utils import load_pickle_file, update_pickle_file
from .utils.public_utils import format_print, is_id_card_valid, is_phone_number_valid


# 存储结构
class Person:
    required_attrs = ('name', 'gender', 'age')  # 不需要变的数据用元组比较好
    optional_attrs = ('id_card', 'phone_number', 'address')
    
    def __init__(self, name, gender, age, **kwargs):
        self.name = name
        self.gender = gender  # 0: male; 1: female
        self.age = age
        # 实例化其他任意个可选属性
        for k, v in kwargs.items():
            if k in Person.optional_attrs:
                setattr(self, k, v)
                
    def __str__(self) -> str:
        return f'{self.name.title()} -- {self.gender_display}'
    
    @property
    def gender_display(self):
        return 'Female' if self.gender else 'Male'
    
    def is_valid_property(self, key: str):
        if key in [*Person.required_attrs, *Person.optional_attrs]:
            return True
        return False

        
class Student(Person):  # 继承
    def __init__(self, name, gender, age, **kwargs):
        super().__init__(name, gender, age, **kwargs)  # 调用父类的初始化，先把父类这些 实例属性 初始化
        self.id = self.get_new_unique_stu_id()

    def __str__(self) -> str:  # 重构
        desc1 = f'{self.id}'
        desc2 = super().__str__()
        return ' -- '.join((desc1, desc2))  # 字符串拼接
             
    @staticmethod
    def get_new_unique_stu_id() -> int:  # 从pickle获取唯一id
        pickle_data = load_pickle_file(settings.DATA_PICKLE_PATH)
        student_id = pickle_data.get('student_id')
        if not student_id:
            student_id = 1
        pickle_data['student_id'] = student_id + 1
        update_pickle_file(settings.DATA_PICKLE_PATH, pickle_data)           
        return student_id
    
    def print_student_info(self):
        print(f'Student ID: {self.id}\tName: {self.name}\tGender: {self.gender_display}\tAge: {self.age}')  # 调用父类自定义属性 self.gender_display
        
    def check_valid_input(self, key: str, value) -> tuple[bool, str]:
        key = key.lower()
        if not self.is_valid_property(key):
            return False, f'{key} is not a valid property.'
        else:
            if key in ['name', 'address']:
                if value == '':
                    return False, f'{key} cannot be blank.'
            elif key == 'gender':
                if value not in (0, 1):
                    return False, f'{value} is not valid.'
            elif key == 'age':
                if value < 3 or value > 123:
                    return False, f'{value} is not valid.'
            elif key == 'id_card':
                if not is_id_card_valid(value):
                    return False, f'{value} is not valid.'
            elif key == 'phone_number':
                if not is_phone_number_valid(value):
                    return False, f'{value} is not valid.'
            return True, ''

class Course:
    def __init__(self, course_name, teacher):
        self.id = self.get_new_unique_course_id()
        self.name = course_name
        self.teacher = teacher
        
    def __str__(self) -> str:
        return f'{self.id} -- {self.name} -- {self.teacher}'
    
    @staticmethod
    def get_new_unique_course_id() -> int:
        pickle_data = load_pickle_file(settings.DATA_PICKLE_PATH)
        course_id = pickle_data.get('course_id')
        if not course_id:
            course_id = 1
        pickle_data['course_id'] = course_id + 1
        update_pickle_file(settings.DATA_PICKLE_PATH, pickle_data)           
        return course_id

    def print_course_info(self):        
        print(f'Course ID: {self.id}\tCourse Name: {self.name}\tTeacher: {self.teacher}')


class StudentCourseScore:
    def __init__(self, student_id, course_id, score):
        self.student_id = student_id
        self.course_id = course_id
        self.score = score


class StudentList:
    def __init__(self):
        self.stu_list = []
        self.length = 0

    # 增
    def add_student(self, student: Student):
        self.stu_list.append(student)
        self.length += 1

    # 删    
    def delete_student(self, key='id', value=None):
        if not value:
            format_print('ERROR', f'Please populate the value of the key {key}')
        else:
            if key == 'id':
                self.delete_student_by_id(value)
            elif key == 'name':
                self.delete_student_by_name(value)
            else:
                format_print('ERROR', f'Student only can deleted by id or name, not {key}')

    def delete_student_by_id(self, stu_id: int):        
        student = self.get_student_by_id(stu_id)
        if student:
            self.stu_list.remove(student)
            return True
        return False

    def delete_student_by_name(self, name: str):
        students = []
        count = 0
        for stu in self.stu_list:
            if stu.name == name:
                students.append(stu)
                count += 1
        if count == 0:
            format_print('DELETE', f'{name} is not found.')
        elif count == 1:
            self.delete_student_by_id(students[0].id)
        else:
            format_print('DELETE', f'There are more than one student named {name}, check one to delete.')
            for i, stu in enumerate(students, 1):
                print(f'{i} -- student info:\n')
                self.show_student_info_by_id(stu.id)
            option = int(input("Input: "))
            if option <= i:  # 谨慎使用循环后的i变量
                self.delete_student_by_id(stu[option-1])
            else:
                format_print('DELETE', 'Please enter valid values.')

    # 查            
    def get_student_by_id(self, stu_id: int):
        for stu in self.stu_list:
            if stu.id == stu_id:  # TODO: 二分查找 优化，因为 stu_list id 有序
                return stu
        return None

    def show_student_info_by_id(self, stu_id):
        student = self.get_student_by_id(stu_id)
        if student:
            student.print_student_info()
        else:
            format_print('GET', f'Student with student_id {stu_id} is not found.')

    def show_all_student_info(self):  # TODO: 分页; show 选课和课程成绩信息；
        for student in self.stu_list:
            student.print_student_info()

    # 改
    def update_student_info_by_id(self, stu_id):
        student = self.get_student_by_id(stu_id)
        if student:
            student.print_student_info()
            # 选择属性去修改
            while True:
                option = input('Please enter the property you want to change: ')
                if option.lower() in Person.required_attrs or option in Person.optional_attrs:
                    value = input('Please enter the value you want to populate: ')
                    is_valid, msg = student.check_valid_input(option, value)
                    if not is_valid:
                        format_print('UPDATE', msg)
                    else:
                        setattr(student, option, value)
                        format_print('UPDATE', f'Update student {student.name} {option} successfully!')
                option = input('Continue update? (y)/n')
                if option.lower() == 'n':
                    break
        else:
            format_print('GET', f'Student with student_id {stu_id} is not found.')


class CourseList:
    def __init__(self):
        self.course_list = []
        self.length = 0
        
    def add_course(self):
        pass
    
    def delete_course(self):
        pass
    
    def get_course(self):
        pass
    
    def update_course(self):
        pass


class StudentCourseList:
    def __init__(self):
        self.stu_course_list = []
        self.length = 0
