import pickle
import os
from typing import Dict

from .public_utils import update_dict_values
from .. import settings


# # TODO: 现在做到设计model，然后想到了用pickle来存放各表最新的id值，然后写了一下pickle的实现；考虑一下保存方式，假如用csv呢？还需要用pickle来长期存储吗？
# def update_pickle_data(new_data: Dict, cover_update=True):
#     with open(settings.DATA_PICKLE_PATH, 'rb') as f:
#         data = pickle.load(f)
#     if cover_update:
#         data.update(new_data)      
#     else:
#         update_dict_values(data, new_data)
#     with open(settings.DATA_PICKLE_PATH, 'wb') as f:  # 'wb'覆盖写入
#         pickle.dump(data, f)
        
        
def init_pickle_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as fp:
            pickle.dump({}, fp)


def update_pickle_file(file_path, data):
    try:
        with open(file_path, 'wb') as fp:
            pickle.dump(data, fp)
    except Exception as e:
        print(f"[Error] Update pickle file occurred error: {e}")


def load_pickle_file(file_path):
    init_pickle_file(file_path)  # if file not exists, create file

    with open(file_path, 'rb') as fp:
        data = pickle.load(fp)
    return data


def remove_pickle_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
