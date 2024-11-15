from . import settings
from .utils.pickle_utils import load_pickle_file, update_pickle_file
from .utils.public_utils import is_name_valid, is_id_card_valid, is_phone_number_valid, \
    is_student_number_valid


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
    required_attrs = ('student_number', ) + Person.required_attrs  # 元组内不可变，但是两个元组可以拼接
    
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
                if not func:
                    return False, f'Invalid {key}'
                elif not func(value):
                    return False, f"{value} is an invalid {cls.display_attr(key)}."
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
        
    @classmethod
    def display_attr(cls, attr: str):
        return attr.replace('_', ' ').title()
        

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
    """
    顺序表
    1. is_empty: 判空
    2. append_item: 尾插入元素
    3. get_item_by_key_value: 根据 键值对 查询元素
    4. delete_item: 按值删除元素 
    5. delete_item_by_key_value: 根据 键值对 删除元素 
    6. _update_item_attr_by_index: 根据 索引 更新元素属性
    """
    def __init__(self, Item):
        self.model = Item
        self.sq_list: list[Item] = []
        self.length = 0
        #
        self.check_key_value = getattr(Item, 'check_data', lambda x, y, z=None: (False, 'Item has no check_data method.'))

    def is_empty(self):
        return self.length == 0
    
    def _is_index_valid(self, i: int):
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
    
    def append_item(self, item):
        """Add item to list."""
        self.sq_list.append(item)
        self.length += 1
        return {"status": True, "msg": f"{self.model.__name__} {item} added."}
    
    def _add_item_by_index(self, i: int, item):  # maybe not used
        """Add item to list with index."""
        success, msg = self._is_index_valid(i)
        if not success:
            return success, msg
        self.sq_list.insert(i, item)
        self.length += 1
        return {"status": True, "msg": f"{self.model.__name__} {item} added."}
    
    def _get_item_index_by_key_value(self, key: str, value):  # TODO: 查询结果有两个怎么办
        """
        Used to get the index of item in sq_list.
        Will be used before updating or deleting item.
        """
        if key != 'id':
            success, msg = self.check_key_value(key, value)
            if not success:
                return {"status": False, "msg": msg, "data": {"index": -2}}
        for i, item in enumerate(self.sq_list):  # i begins from 0.
            attr = getattr(item, key)
            if attr == value:
                return {"status": True, "msg": "OK", "data": {"index": i}}  # This index do not need to do _is_index_valid().
        return {"status": False, "msg": f"{self.model.__name__} with {key}={value} not found.", "data": {"index": -1}}
    
    def get_item_by_key_value(self, key: str, value):  # TODO: 调用这个的需要改
        """Get item by key-value."""
        res = self._get_item_index_by_key_value(key, value)
        if not res["status"]:
            return res
        res["data"]["item"] = self.sq_list[res["data"]["index"]]
        return res
        
    def delete_item(self, item):
        """Delete item from list."""
        if self.is_empty():
            return {"status": False, "msg": "List is empty."}
        try:
            self.sq_list.remove(item)
            self.length -= 1
        except ValueError:
            return {"status": False, "msg": f"{self.model.__name__} {item} not found."}
        else:
            return {"status": True, "msg": f"{self.model.__name__} {item} deleted."}  # try没有异常时执行，也可以直接放到try中，取消else部分
        
    def _delete_item_by_index(self, i: int, need_check_index=True):
        if need_check_index:
            success, msg = self._is_index_valid(i)
            if not success:
                return {"status": False, "msg": msg}
        item = self.sq_list.pop(i)
        self.length -= 1
        return {"status": True, "msg": f"{self.model.__name__} {item} deleted."}
    
    def delete_item_by_key_value(self, key, value):
        """Delete item by key-value."""
        res = self._get_item_index_by_key_value(key, value)
        if not res["status"]:
            return res
        else:
            return self._delete_item_by_index(res["data"]["index"], False)
    
    def _replace_item_by_index(self, i: int, new_item, need_check_index=True):  # to be deleted.
        if need_check_index:
            success, msg = self._is_index_valid(i)
            if not success:
                return {"status": False, "msg": msg}
        self.sq_list[i] = new_item
        return {"status": True, "msg": f"{self.model.__name__} {new_item} updated."}
    
    def _update_item_attr_by_index(self, i: int, attr: str, new_value, need_check_index=True, need_check_key=True):
        if need_check_index:
            success, msg = self._is_index_valid(i)
            if not success:
                return {"status": False, "msg": msg}
        # Used to check if new_value is valid in UPDATE, need_check_index == True means that index is get from _get_item_index_by_key_value, which means it is valid.
        success, msg = self.check_key_value(attr, new_value, need_check_key)
        if not success:
            return {"status": False, "msg": msg}
        setattr(self.sq_list[i], attr, new_value)
        return {"status": True, "msg": f"{self.model.__name__} {attr} updated."}
    
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
