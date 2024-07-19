from datetime import datetime
import re
import csv


# 深层递归更新字典的值
def update_dict_values(origin_dict, new_dict):
    for k, v in new_dict.items():
        if k in origin_dict:
            if isinstance(origin_dict[k], set):
                if isinstance(v, list) or isinstance(v, set):
                    origin_dict[k].update(v)
                else:
                    origin_dict[k].add(v)
            elif isinstance(origin_dict[k], list):
                if isinstance(v, list) or isinstance(v, set):
                    origin_dict[k].extend(v)
                    origin_dict[k] = list(set(origin_dict[k]))
                else:
                    origin_dict[k].update(v)
            elif isinstance(origin_dict[k], dict):
                update_dict_values(origin_dict[k], v)
            else:
                origin_dict.update({k: v})
        else:
            origin_dict.update({k: v})
            

def format_print(action: str, message):
    # 格式化输出
    """
    一般用datetime，更适合日期相关的处理；time 适合于基本的时间相关操作；
    转换时间格式的，用strftime和f-sting 都可以
    """
    # from time import localtime, strftime
    # print(f'{strftime('%Y-%m-%d %H:%M:%S', localtime())} [{action.upper()}] {message}')
    # print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [{action.upper()}] {message}')
    print(f'{datetime.now(): %Y-%m-%d %H:%M:%S} [{action.upper()}] {message}')  # f-string 可以直接转换 datetime 类型的数据
   
    
def format_result(code, message, data=None):
    return {'code': code, 'message': message, 'data': data}


def is_id_card_valid(id_number: str):
    # 正则表达式验证身份证号格式
    pattern = r"^\d{17}[\dXx]$"
    if not re.match(pattern, id_number):
        return False
    
    # 加权因子
    weight_factor = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    # 校验码
    check_code = "10X98765432"
    
    # 计算校验位(中国身份证号最后一位是校验位，它是根据前面17位数字经过特定算法计算得出的)
    sum = 0
    for i in range(17):
        sum += int(id_number[i]) * weight_factor[i]
    if id_number[17] in ['x', 'X']:
        id_number = id_number[:17] + '10'
    else:
        id_number = id_number[:17] + id_number[17]
    calc_code = check_code[sum % 11]

    # 校验身份证号
    if calc_code == id_number[17]:
        return True
    else:
        return False
    
    
def is_phone_number_valid(phone_number: str):
    # 正则表达式验证手机号格式
    pattern = r"^1\d{10}$"
    if re.match(pattern, phone_number):
        return True
    else:
        return False
    
    
def is_name_valid(name: str):
    chinese_pattern = r"^[\u4e00-\u9fa5]{2,4}$"  # 2-4个中文字符
    english_pattern = r"^[A-Z][a-z]+(?:[-\s][A-Z][a-z]+)*$"  # eg. "John Doe"
    if re.match(chinese_pattern, name) or re.match(english_pattern, name):
        return True
    else:
        return False


def handle_keyboard_interrupt(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            format_print('GET', 'Get canceled.')
            return False
    return wrapper


def save_data_to_csv(objs, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'name', 'age'])  # 写入列名
        for obj in objs:
            writer.writerow([obj.id, obj.name, obj.age])


def load_data_from_csv(filename, Obj):
    with open(filename, mode='r') as file:
        csv_rows = csv.DictReader(file)
        for row in csv_rows:
            # Obj(int(row['id']), row['name'], int(row['age']))
            pass  # TODO: Obj.add_item(Obj(int(row['id']), row['name'], int(row['age'])))
    return
