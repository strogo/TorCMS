# -*- coding: utf-8

from openpyxl.reader.excel import load_workbook

wb = load_workbook(filename='dic_schema.xlsx')
sheet_ranges = wb['Sheet1']

class_arr = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
sig_name_arr = []


def gen_html_dic():
    fo = open('xxtmp_html_dic.py', 'w')
    # sig_name_arr = []
    for jj in class_arr:

        cc_val = sheet_ranges['{0}1'.format(jj)].value
        if cc_val and cc_val != '':
            (qian, hou) = cc_val.split(':')
            c_name, e_name = qian.split(',')
            sig_name_arr.append(e_name)
            tags1 = hou.split(',')
            tags1 = [x.strip() for x in tags1]
            tags_dic = {}

            if len(tags1) == 1:
                tags_dic[1] = hou
                ctr_type = 'text'
            else:
                for ii in range(len(tags1)):
                    tags_dic[ii + 1] = tags1[ii].strip()
                ctr_type = 'select'
            print(tags1)

            fo.write('''html_{0} = {{
                'en': 'tag_{0}',
                'zh': '{1}',
                'dic': {2},
                'type': '{3}',
                }}\n'''.format(e_name, c_name, tags_dic, ctr_type))
    fo.close()


def uu():
    fo_edit = open('xxtmp_array_add_edit_view.py', 'w')

    # 父类索引
    papa_index = 1
    # 子类索引
    c_index = 1
    papa_id = 0
    uid = ''

    p_dic = {}


    # 逐行遍历
    for row_num in range(2, 50):
        # 父类
        if sheet_ranges['B{0}'.format(row_num)].value and sheet_ranges['B{0}'.format(row_num)].value != '':
            c_index = 1

            papa_id = papa_index
            papa_index += 1
            print(papa_id)
            u_dic = {}
            u_dic['uid'] = 'adfd'
            u_dic['name'] = sheet_ranges['B{0}'.format(row_num)].value
            u_dic['arr'] = []

            p_dic = {
                'uid': '0{0}'.format(papa_id),
                'name': sheet_ranges['B{0}'.format(row_num)].value,
                'u_arr': [],
            }
            for ii, jj in zip(class_arr, sig_name_arr):
                cell_val = sheet_ranges['{0}{1}'.format(ii, row_num)].value
                if cell_val == 1:
                    print('=' * 40)
                    u_dic['arr'].append('{0}'.format(jj))
            print(u_dic)
            print('=' * 40)
            fo_edit.write('dic_0{0}00 = {1}\n'.format(papa_id, u_dic['arr']))


        # 子类
        c_cell_val = sheet_ranges['C{0}'.format(row_num)].value
        if c_cell_val and c_cell_val != '':
            u_dic = {}

            app_uid = '0{0}0{1}'.format(papa_id, c_index)
            p_dic['u_arr'].append(app_uid)
            u_dic['uid'] = app_uid
            u_dic['name'] = sheet_ranges['C{0}'.format(row_num)].value
            u_dic['arr'] = []

            for ii, jj in zip(class_arr, sig_name_arr):
                cell_val = sheet_ranges['{0}{1}'.format(ii, row_num)].value
                if cell_val == 1:
                    u_dic['arr'].append('{0}'.format(jj))
            print(u_dic)
            fo_edit.write('dic_{0} = {1}\n'.format(app_uid, u_dic['arr']))

            c_index += 1

    fo_edit.close()


if __name__ == '__main__':
    gen_html_dic()
    uu()
