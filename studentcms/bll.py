# Business Logic Lever
from .models import Student, StudentList, CourseList, StudentCourseList  # noqa
from .utils.public_utils import format_print, handle_keyboard_interrupt


class StudentManager(StudentList):

    @handle_keyboard_interrupt
    def handle_input(self, prompt, key):
        """ 处理用户输入 """
        user_input = input(prompt)
        processed_input = self.process_input(key, user_input)
        return processed_input
    
    @handle_keyboard_interrupt
    def prompt_and_get_option(self, prompt, options_mapping) -> str:
        """ 选项输入模块 """
        option_items = [f"'{key}': {self.display_attr(value)}" for key, value in options_mapping.items()]
        options_str = '\n'.join(option_items) + '\n\'Q(q)\': Cancel and Return to Menu\n' + 'Enter your choice: '
        prompt += '\n' + options_str
        while True:
            option = input(prompt)
            if option in options_mapping or option.lower() == 'q':
                return option.lower()
            else:
                print('Invalid option. Please enter again: ')

    def add_student(self):
        """ 添加学生信息 """
        print("Please enter student's information:")
        input_data = {}
        for attr in self.all_attrs:
            prompt = f"{self.display_attr(attr)}{'(Optional)' if attr in self.optional_attrs else ''}: "
            processed_input = self.handle_input(prompt, attr)
            input_data[attr] = processed_input  # 动态创建变量方式：1. global()[attr] 2. 字典
            success, msg = self.check_data(attr, input_data[attr], False)
            if not success:
                format_print(action="Add student", message=msg)
                return {"status": False, "msg": msg}
        return super().append_item(Student(**input_data))
    
    '''
    def __delete_student(self):  # Deprecated
        """ 删除学生信息 """
        """ 
        发现这个不符合逻辑，没有确认删除。
        但是如果加上确认删除，就需要先展示学生信息，就需要get_student ，那先get到学生数据了都，再去查一遍进行删除，那还不如直接用remove，
        也就是delete_student_2的逻辑。 """
        option_key_map = {
            '1': 'student_number',
            '2': 'name',
        }
        option = self.prompt_and_get_option('Which way do you want to delete?', option_key_map)
        if not option or option == 'q':
            return
        key = option_key_map[option]
        processed_data = self.handle_input(f"Enter student\' {self.display_attr(key)}: ", key)
        res = super().delete_item_by_key_value(key, processed_data)
        format_print(f"DELETE {'FAILED' if not res['status'] else 'SUCCESS'}", res["msg"])
    '''
    
    def get_student(self):
        """ 查找学生信息 """
        if self.is_empty():
            format_print("GET", "There is no student.")
            return
        option_key_map = {
            '1': 'student_number',
            '2': 'name',
        }
        option = self.prompt_and_get_option('Which way do you want to get?', option_key_map)
        if not option or option == 'q':
            return
        key = option_key_map[option]
        processed_data = self.handle_input(f'Enter student\'s {self.display_attr(key)}: ', key)
        res = super().get_item_by_key_value(key, processed_data)
        if res["status"]:
            student = res["data"]["item"]
            format_print('GET', 'Here are the student info:')
            student.print_student_info()
            return student
        else:
            format_print('GET', res["msg"])
            return
    
    def delete_student(self):
        """ 删除学生信息 """
        student = self.get_student()
        if student:
            option = input("Confirm to delete? [y/n] ")
            if option.lower() == "y":
                res = self.delete_item(student)
                format_print(f"DELETE {'FAILED' if not res["status"] else 'SUCCESS'}", res["msg"])
            else:
                print('Canceled.')
            
    def show_all_student_info(self):  # TODO: 分页; show 选课和课程成绩信息；
        """ 显示所有学生信息 """
        if self.is_empty():
            format_print('Show Students', 'There is no student.')
            return
        self.print_columns_name()
        for student in self.student_list:
            student.print_student_info_simply()

    """
    def __update_student_info(self):  # noqa: C901; [Deprecated]
        '''
        更新学生信息 
        但是不能用封装的get_student()，因为其是封装好的查询+print。
        get_item_by_key_value() 返回一个Student对象，而该系统的理念是先获取 index 然后进行 update，故也不能用。
        只能用_get_item_index_by_key_value() + _update_item_attr_by_index()
        '''
        update = get + reset
        
        options_mapping = {
            '1': 'student_number',
            '2': 'name',
        }
        option = self.prompt_and_get_option('Which way do you want to update?', options_mapping)
        if not option or option == 'q':
            return
        key = options_mapping[option]
        value = self.handle_input(f'Enter student\'s {key}: ', key)
        res = super()._get_item_index_by_key_value(key, value)
        if not res["status"]:
            format_print('UPDATE', res.get("msg"))
            return
        else:
            # TODO: show old student info
            options_mapping = {
                '1': 'name',
                '2': 'age',
                '3': 'gender',
                '4': 'student_number',  # TODO: id_number
                # '5': 'phone_number',
                '5': 'else',
                '6': 'all'
            }
            option = self.prompt_and_get_option('Please enter the property you want to change,', options_mapping)
            if not option or option == 'q':
                return
            elif option in ['1', '2', '3']:
                attr_name = options_mapping[option]
                new_attr_value = self.handle_input(f'Please enter the new {attr_name}: ', attr_name)
                success, msg = self.check_data(attr_name, new_attr_value, False)
                if not success:
                    format_print(action='update failed', message=msg)
                    return
                res = super()._update_item_attr_by_index(res["data"]["index"], attr_name, new_attr_value, False, False)
                format_print(f"UPDATE {'SUCCESS' if res["status"] else 'FAILED'}", res["msg"])
            elif option == '4':  # TODO: 继续修改 while循环
                key = input('Please enter the property you want to change: ')
                value = self.handle_input(f'Please enter the student\'s {key}: ', key)
                success, msg = self.check_data(key, value, False)
                if not success:
                    format_print(action='update failed', message=msg)
                    return False, msg
                res = super()._update_item_attr_by_index(res["data"]["index"], key, value, False, True)
                format_print(f"UPDATE {'SUCCESS' if res["status"] else 'FAILED'}", res["msg"])
            elif option == '5':
                for key in self.all_attrs:  # TODO: 这里不应该一个个update？但这也不是数据库，应该也可以
                    new_attr_value = self.handle_input(f'Please enter the new {key}: ', key)  # TODO: 输入回车，是覆盖，还是跳过？
                    success, msg = self.check_data(key, new_attr_value, False)
                    if not success:
                        format_print(action='update failed', message=msg)
                        return False, msg
                    res = super()._update_item_attr_by_index(res["data"]["index"], key, new_attr_value, False, False)
                    format_print(f"UPDATE {'SUCCESS' if res["status"] else 'FAILED'}", res["msg"])
        
    """
                
    def update_student(self):
        """ 更新学生信息 """
        student = self.get_student()
        if not student:
            return False, 'No student found'
        options_mapping = {
            '1': 'name',
            '2': 'age',
            '3': 'gender',
            '4': 'student_number',
            '5': 'else',
            '6': 'all'
        }
        option = self.prompt_and_get_option('Please enter the property you want to change,', options_mapping)
        need_check_key = False
        if not option or option == 'q':
            return
        elif option in ['1', '2', '3', '4']:
            to_update_attrs = [options_mapping[option]]
        elif option == '5':
            to_update_attrs = [input('Please enter the property you want to change: ')]
            need_check_key = True
        else:
            to_update_attrs = self.all_attrs
        for attr_name in to_update_attrs:
            new_attr_value = self.handle_input(f'Please enter the new {self.display_attr(attr_name)}: ', attr_name)
            success, msg = self.check_data(attr_name, new_attr_value, need_check_key)
            if not success:
                format_print(action='update failed', message=msg)
                return False, msg
            setattr(student, attr_name, new_attr_value)  # Update attribute
            format_print(f"UPDATE {'SUCCESS' if success else 'FAILED'}", msg)

    def student_course_score_statistics(self):
        pass
