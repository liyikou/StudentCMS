from . import settings
from .utils.pickle_utils import load_pickle_file, update_pickle_file
from .utils.public_utils import format_print, is_name_valid, is_id_card_valid, is_phone_number_valid, \
    handle_keyboard_interrupt, is_student_number_valid


# 存储结构
class Person:
    required_attrs = ('name', 'gender', 'age')  # 不需要变的数据用元组比较好
    optional_attrs = ('id_card', 'phone_number', 'address')

    def __init__(self, name, gender, age, **kwargs):
        self.name = name
        self.gender = gender  # 0: female; 1: male
        self.age = age
        # 实例化其他任意个可选属性
        for k, v in kwargs.items():
            if k in Person.optional_attrs:
                setattr(self, k, v)

    def __str__(self) -> str:  # 类型注解，Python3.5 引入
        return f'{self.name.title()} -- {self.gender_display}'
    
    @property
    def gender_display(self):
        return 'Male' if self.gender else 'Female'
    
    @property
    def all_attrs(self):
        return self.required_attrs + self.optional_attrs
    
    @classmethod
    def is_attr_valid(cls, key: str):  # 类型注解
        if key in [*cls.required_attrs, *cls.optional_attrs]:  # *：展开；这里也可以直接元组相加会生成新元组
            return True
        return False
    
    @classmethod
    def is_attr_optional(cls, key: str):
        return key in cls.optional_attrs
    
    @classmethod
    def is_attr_required(cls, key: str):
        return key in cls.required_attrs

        
class Student(Person):  # 继承
    required_attrs = Person.required_attrs + ('student_number', )  # 元组内不可变，但是两个元组可以拼接
    
    def __init__(self, student_number, name, gender, age, **kwargs):
        super().__init__(name, gender, age, **kwargs)  # 调用父类的初始化，先把父类这些 实例属性 初始化
        self.id = self.get_new_unique_stu_id()  # 表id
        self.student_number = student_number  # 学号

    def __str__(self) -> str:  # 重构
        desc1 = f'{self.student_number}'
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
        # print(f'Student ID: {self.id}\tName: {self.name}\tGender: {self.gender_display}\tAge: {self.age}')  # 调用父类自定义属性 self.gender_display,不需要super().
        self.print_columns_name()
        self.print_student_info_simply()
        
    @classmethod
    def print_columns_name(cls):
        # print('\t\t'.join(self.all_attrs))
        print(f"{'Student Number':<15}{'Name':<20}{'Gender':<10}{'Age':<5}{'ID Card':<20}{'Phone Number':<20}{'Address':<20}")  # <:左对齐，>:右对齐，^:居中； 20:长度；
    
    def print_student_info_simply(self):
        """f-string 设置对齐效果比 \\t 和 print的%s 好 """
        # print('\t\t'.join([str(getattr(self, attr)) for attr in self.all_attrs if getattr(self, attr, None)]))
        optional_attrs_str = ''.join([f'{getattr(self, attr):<20}' if getattr(self, attr, None) else f"{'':<20}" for attr in self.optional_attrs])
        print(f"{self.student_number:<15}{self.name:<20}{self.gender_display:<10}{self.age:<5}{optional_attrs_str}")
    
    # @classmethod
    # def is_attr_valid(cls, key: str):
    #     return super().is_attr_valid(key) or key in ('id',)  # TODO: 每个表都应该有id 和 xxx_id（stu_id, course_id, ...), id是保密的，所以这里注释掉了，在_get_item...方法里也跳过了对id的检查
    
    @classmethod
    def check_data(cls, key: str, value, need_check_key=True) -> tuple[bool, str]:
        key = key.lower()
        if need_check_key and not cls.is_attr_valid(key):  # 调用继承的类方法
            return False, f'{key} is not a valid attribute.'
        else:
            if cls.is_attr_required(key) or value:  # attr is required OR value is not blank
                check_func_map = {
                    'student_number': is_student_number_valid,
                    'name': is_name_valid,
                    'gender': lambda x: x in (0, 1),
                    'age': lambda x: x >= 6 and x <= 123,
                    'id_card': is_id_card_valid,
                    'phone_number': is_phone_number_valid,
                    'address': lambda _: True  # TODO: 让address成为选项，Choice那种
                }
                func = check_func_map.get(key)
                if func and not func(value):
                    return False, f'{value} is an invalid {key.capitalize()}.'
            return True, ''
    
    @classmethod
    def process_input(cls, key: str, value):
        try:
            if key in ('gender', 'age'):
                return int(value)
            else:
                return value
        except ValueError:
            return value
        

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


class SqList:
    def __init__(self, Item: type):
        self.model = Item
        self.sq_list: list[Item] = []
        self.length = 0
        #
        self.check_key_value = getattr(Item, 'check_data', lambda x, y, z=None: (False, 'Item has no check_data method.'))

    def is_empty(self):
        return self.length == 0
    
    def is_index_valid(self, i: int):
        """Check if index is valid.

        Args:
            i (int): index

        Returns:
            bool: True if index is valid, False otherwise.
        """
        if self.is_empty():
            return False, 'List is empty.'
        if i < 0 or i >= self.length:
            return False, f'Index--{i} out of list.'
        return True, ''
    
    def add_item(self, item):
        """Add item to list."""
        self.sq_list.append(item)
        self.length += 1
        return True, f'{self.model.__name__} {item} added.'
    
    def add_item_by_index(self, i: int, item):  # maybe not used
        """Add item to list with index."""
        success, msg = self.is_index_valid(i)
        if not success:
            return success, msg
        self.sq_list.insert(i, item)
        self.length += 1
        return True, f'{self.model.__name__} {item} added.'
    
    def _get_item_index_by_key_value(self, key: str, value):  # TODO: 查询结果有两个怎么办
        """
        Used to get the index of item in sq_list.
        Will be used before updating or deleting item.
        """
        if key != 'id':
            success, msg = self.check_key_value(key, value)
            if not success:
                return False, msg
        for i, item in enumerate(self.sq_list):  # i begins from 0.
            attr = getattr(item, key)
            if attr == value:
                return True, i  # This index do not need to do is_index_valid().
        return False, f'{self.model.__name__} with {key}={value} not found.'
    
    def get_item_by_key_value(self, key: str, value):
        """Get item by key-value."""
        success, i_or_msg = self._get_item_index_by_key_value(key, value)
        if not success:
            return success, i_or_msg
        if not isinstance(i_or_msg, int):  # without this check, self.sq_list[i_or_msg] will show error.
            return False, i_or_msg
        return True, self.sq_list[i_or_msg]
        
    def delete_item(self, item):
        """Delete item from list."""
        if self.is_empty():
            return False, 'List is empty.'
        try:
            self.sq_list.remove(item)
            self.length -= 1
        except ValueError:
            return False, f'{self.model.__name__} {item} not found.'
        else:
            return True, f'{self.model.__name__} {item} deleted.'
        
    def _delete_item_by_index(self, i: int, need_check_index=True):
        if need_check_index:
            success, msg = self.is_index_valid(i)
            if not success:
                return success, msg
        self.sq_list.pop(i)
        self.length -= 1
        return True, f'{self.model.__name__} deleted.'
    
    def delete_item_by_key_value(self, key, value):
        """Delete item by key-value."""
        success, i_or_msg = self._get_item_index_by_key_value(key, value)
        if not success:
            return success, i_or_msg
        else:  # i_or_msg is a int index
            return self._delete_item_by_index(i_or_msg, False)    # type: ignore
    
    def _update_item_by_index(self, i: int, new_item, need_check_index=True):  # to be deleted.
        if need_check_index:
            success, msg = self.is_index_valid(i)
            if not success:
                return success, msg
        self.sq_list[i] = new_item
        return True, f'{self.model.__name__} {new_item} updated.'
    
    def _update_item_attr_by_index(self, i: int, attr: str, new_value, need_check_index=True, need_check_key=True):
        if need_check_index:
            success, msg = self.is_index_valid(i)
            if not success:
                return success, msg
        # Used to check if new_value is valid in UPDATE, need_check_index == True means that index is get from _get_item_index_by_key_value, means it is valid.
        success, msg = self.check_key_value(attr, new_value, need_check_key)
        if not success:
            return False, msg
        setattr(self.sq_list[i], attr, new_value)
        return True, f'{self.model.__name__} {attr} updated.'
    
    # def update_item_by_key_value(self, key, value, new_value):  # to be deleted, UPDATE must DIY in StudentList. 因为用户先输入要修改的学生信息，然后查到学生，再去修改。用户的输入是穿插在其中的，而且需求设计上不支持用id name之外的属性去查学生。所以无法直接形成整体
    #     """Update item by key-value."""
    #     success, i_or_msg = self._get_item_index_by_key_value(key, value)
    #     if not success:
    #         return success, i_or_msg
    #     if not isinstance(i_or_msg, int):
    #         return False, i_or_msg
    #     return self._update_item_attr_by_index(i_or_msg, key, new_value, False)
    
    
class StudentList(SqList, Student):  # TODO: 添加了Student Number,修改一下逻辑
    def __init__(self):
        super().__init__(Student)  # 根据 MRO 顺序，会执行 SqList.__init__()
        self.student_list = self.sq_list  # 引用 SqList 的 sq_list
    
    def handle_input(self, prompt, key):
        user_input = input(prompt)
        processed_user_input = self.process_input(key, user_input)
        return processed_user_input

    def add_student(self):  # ps. 因为之前的for循环设计，这个add方法不需要改了。👍
        print("Please enter student information:")
        input_data = {}
        for attr in super(SqList, self).all_attrs:  # 根据 MRO 顺序，super(SqList, self) == Student
            prompt = f'{attr.capitalize()}{"(Optional)" if attr in super(SqList, self).optional_attrs else ""}: '
            processed_input = self.handle_input(prompt, attr)
            input_data[attr] = processed_input  # 动态创建变量方式：1. global()[attr] 2. 字典
            success, msg = self.check_data(attr, input_data[attr], False)
            if not success:
                format_print(action='Add student', message=msg)
                return False, msg
        return super().add_item(Student(**input_data))
    
    def delete_student(self):
        option_key_map = {
            '1': 'id',
            '2': 'name',
        }
        option = input('Which way do you want to delete? (1) by id; (2) by name; (3) cancel: ')  # TODO: pack to function
        while option not in ['1', '2', '3']:
            option = input('Invalid option. Please enter again: ')
        else:
            if option == '3':
                format_print('DELETE', 'Delete canceled.')
            else:
                key = option_key_map[option]
                processed_data = self.handle_input(f'Enter student {key}: ', key)
                success, msg = super().delete_item_by_key_value(key, processed_data)
                format_print(f"DELETE {'FAILED' if not success else 'SUCCESS'}", msg)
    
    @handle_keyboard_interrupt  # TODO: 给所有有input的都加上
    def get_student(self):
        option_key_map = {  # TODO: 查找逻辑，需要封装一下，很多地方在用
            '1': 'id',
            '2': 'name',
        }
        option = input('Which way do you want to get? (1) by id; (2) by name; (3) cancel: ')
        while option not in ['1', '2', '3']:
            option = input('Invalid option. Please enter again: ')
        if option == '3':
            format_print('GET', 'Get canceled.')
        else:
            key = option_key_map[option]
            processed_data = self.handle_input(f'Enter student {key}: ', key)
            success, student_or_msg = super().get_item_by_key_value(key, processed_data)
        if success and isinstance(student_or_msg, Student):
            format_print('GET', 'Here are the student info:')
            student_or_msg.print_student_info()
        elif isinstance(student_or_msg, str):
            format_print('GET', student_or_msg)
            
    def show_all_student_info(self):  # TODO: 分页; show 选课和课程成绩信息；
        if self.is_empty():
            format_print('Show Students', 'There is no student.')
            return
        self.print_columns_name()
        for student in self.student_list:
            student.print_student_info_simply()

    def update_student_info(self):  # TODO: 2024/7/14 继续修改，优化现在的逻辑
        """
        update = get + reset
        但是不能用封装的get_student()，因为其是封装好的查询+print。
        get_item_by_key_value() 返回一个Student对象，而该系统的理念是先获取 index 然后进行 update，故也不能用。
        只能用_get_item_index_by_key_value() + _update_item_attr_by_index()
        """
        options_mapping = {
            '1': 'id',
            '2': 'name',
        }
        option = input('Which way do you want to update? (1) by id; (2) by name; (3) cancel: ')
        while option not in ['1', '2', '3']:
            option = input('Invalid option. Please enter again: ')
        else:
            if option in ['1', '2']:
                key = options_mapping[option]
                value = self.handle_input(f'Enter student\'s {key}: ', key)
                success, i_or_msg = super()._get_item_index_by_key_value(key, value)
            else:
                format_print('UPDATE', 'Update canceled.')
                return
        if not success:
            format_print('UPDATE', i_or_msg)
            return
        elif isinstance(i_or_msg, int):  # success == True does mean i_or_msg is index, use isinstance for type checking
            options_mapping = {
                '1': 'name',
                '2': 'age',
                '3': 'gender',
                # '4': 'id_number',  # TODO: id_number
                # '5': 'phone_number',
                '4': 'else',
                '5': 'all'
            }
            option = input('Please enter the property you want to change: (1) name (2) age (3) gender (4) else (5) all (6) cancel: ')  # TODO: 更新输入的数据没有进行校验
            while option not in options_mapping:  # dict可以直接用in来判断key 是否存在
                option = input('Invalid option. Please enter again: ')
            else:
                if option in ['1', '2', '3']:
                    attr_name = options_mapping[option]
                    new_attr_value = self.handle_input(f'Please enter the new {attr_name}: ', attr_name)
                    success, msg = super()._update_item_attr_by_index(i_or_msg, attr_name, new_attr_value, False, False)
                    format_print(f"UPDATE {'SUCCESS' if success else 'FAILED'}", msg)
                elif option == '4':  # TODO: 继续修改 while循环
                    key = input('Please enter the property you want to change: ')
                    value = self.handle_input(f'Please enter the student\'s {key}: ', key)
                    success, msg = super()._update_item_attr_by_index(i_or_msg, key, value, False, True)
                    format_print(f"UPDATE {'SUCCESS' if success else 'FAILED'}", msg)
                elif option == '5':
                    for key in self.all_attrs:  # TODO: 这里不应该一个个update？但这也不是数据库，应该也可以
                        new_attr_value = self.handle_input(f'Please enter the new {key}: ', key)  # TODO: 输入回车，是覆盖，还是跳过？
                        success, msg = super()._update_item_attr_by_index(i_or_msg, key, new_attr_value, False, False)
                        format_print(f"UPDATE {'SUCCESS' if success else 'FAILED'}", msg)
                    
    def student_course_score_statistics(self):
        pass
                    

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


if __name__ == '__main__':
    m = StudentList()
    m.add_student()
    m.show_all_student_info()
