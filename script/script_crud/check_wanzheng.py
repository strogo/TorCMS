# -*- coding: utf-8 -*-

__author__ = 'bukun'

'''
完整性检测
必须保证list中的，为add中存在的。

'''

from pytpl_array_add_edit_view import *
from pytpl_array_list import *

all_var_str = globals().copy()

for var_str in all_var_str:
    if var_str.startswith('tlist') and (not (var_str.endswith('00'))):

        sig = var_str.split('_')[1]
        var = eval(var_str)
        com_list = eval('_'.join(['dic', sig]))
        for x in var:
            if x in com_list:
                pass
            else:
                print('-' * 20)
                print(var_str)
                print(x)


# Todo: 所有一级类的选择，必须在所有的二级类中都有
