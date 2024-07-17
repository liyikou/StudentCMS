# UI lever
import sys
import os
from bll import StudentManager


class UserInterfaceManager:
    OPTIONS = {
        '1': 'Show all students',
        '2': 'Add students',
        '3': 'Delete students',
        '4': 'Find students',
        '5': 'Update students',
        '6': 'Student course score statistics',
        'q': 'Quit'
    }
    BOUNDARY_CHAR = '-'
    BOUNDARY_LENGTH = 50
    
    def __init__(self):
        # 将 manager 设置为实例属性，而不是类属性，以便每个实例可以管理不同的 StudentManager 实例
        self.manager = StudentManager()
        
    
    def display_menu(self):
        for key, value in self.OPTIONS.items():
            self.format_print(f'{key}. {value}')
        self.print_boundary()

    def format_print(self, text):
        text_len = len(text)
        placeholder = self.BOUNDARY_CHAR * (int((self.BOUNDARY_LENGTH - text_len) / 2) - 2)
        print(placeholder, text, placeholder, sep=' ')
        
    def print_boundary(self):
        print(self.BOUNDARY_CHAR * self.BOUNDARY_LENGTH)
        
    def run(self):
        while True:
            os.system('cls')  # 清屏
            self.display_menu()
            option = input('Please choose an option: ')
            option = option.strip().lower()
            if option == '1':  # TODO: 在内部操作也设置上输入q和ctrl c 退出
                self.manager.show_all_student_info()
                os.system('pause')
            elif option == '2':
                self.manager.add_student()  # TODO: 不需要返回值，error需要print
                os.system('pause')
            elif option == '3':
                self.manager.delete_student()
                os.system('pause')
            elif option == '4':
                self.manager.get_student()
                os.system('pause')
            elif option == '5':
                self.manager.update_student_info()
                os.system('pause')
            elif option == '6':
                self.manager.student_course_score_statistics()  # TODO: 这个需要做完 Course 相关才能进行成绩统计
                os.system('pause')
            elif option == 'q':
                print('Quitting...')
                break
            else:
                print('Invalid option, please try again.')
                os.system('pause')
        return
                
        
    
    
    