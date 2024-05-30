from time import localtime, strftime
import re


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
            

def format_print(action: str, message: str):
    print(f'{strftime('%Y-%m-%d %H:%M:%S', localtime())} [{action.upper()}] {message}')
    

def is_id_card_valid(id_number):
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
    
    
def is_phone_number_valid(phone_number):
    # 正则表达式验证手机号格式
    pattern = r"^1\d{10}$"
    if re.match(pattern, phone_number):
        return True
    else:
        return False