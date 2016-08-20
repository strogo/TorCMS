__author__ = 'ycb'

from xxtmp_array_add_edit_view import *
from xxtmp_html_dic import *
from func_to_html_add_edit_view import *
import os
from base_crud import crud_path

if __name__ == '__main__':
    out_dir = os.path.join(os.getcwd(), crud_path )
    bianliang_arr = globals().copy().keys()
    for bianliang in bianliang_arr:
        if bianliang.startswith('dic_') and (not bianliang.endswith('00')):
            filesig = bianliang.split('_')[1]
            add_file = os.path.join(out_dir, 'add', 'add_' + filesig + '.html')
            edit_file = os.path.join(out_dir, 'edit', 'edit_' + filesig + '.html')
            view_file = os.path.join(out_dir, 'view', 'view_' + filesig + '.html')

            add_widget_arr = []
            var_dic = eval(bianliang)
            for sig in var_dic:
                html_sig = '_'.join(['html', sig])
                # print(html_sig)
                var_html = eval(html_sig)
                if var_html['type'] == 'text':
                    tp = (gen_input_add(var_html))
                if var_html['type'] == 'select':
                    tp = (gen_select_add(var_html))
                if var_html['type'] == 'radio':
                    tp = (gen_radio_add(var_html))
                if var_html['type'] == 'checkbox':
                    tp = (gen_checkbox_add(var_html))
                if var_html['type'] == 'file':
                    tp = (gen_file_add(var_html))
                add_widget_arr.append(tp)
            with open(add_file, 'w') as fo:
                fo.write(open('tpl_add.tpl').read().replace('xxxxxx', ''.join(add_widget_arr)))

            view_widget_arr = []
            var_dic = eval(bianliang)
            for sig in var_dic:
                html_sig = '_'.join(['html', sig])
                # print(html_sig)
                var_html = eval(html_sig)
                if var_html['type'] == 'text':
                    tp = (gen_input_view(var_html))
                if var_html['type'] == 'select':
                    tp = (gen_select_view(var_html))
                if var_html['type'] == 'radio':
                    tp = (gen_radio_view(var_html))
                if var_html['type'] == 'checkbox':
                    tp = (gen_checkbox_view(var_html))
                if var_html['type'] == 'file':
                    tp = (gen_file_view(var_html))
                view_widget_arr.append(tp)
            with open(view_file, 'w') as fo:
                fo.write(open('tpl_view.tpl').read().replace('xxxxxx', ''.join(view_widget_arr)))

            edit_widget_arr = []
            var_dic = eval(bianliang)
            for sig in var_dic:
                html_sig = '_'.join(['html', sig])
                # print(html_sig)
                var_html = eval(html_sig)
                if var_html['type'] == 'text':
                    tp = (gen_input_edit(var_html))
                if var_html['type'] == 'select':
                    tp = (gen_select_edit(var_html))
                if var_html['type'] == 'radio':
                    tp = (gen_radio_edit(var_html))
                if var_html['type'] == 'checkbox':
                    tp = (gen_checkbox_edit(var_html))
                if var_html['type'] == 'file':
                    tp = (gen_file_edit(var_html))
                edit_widget_arr.append(tp)
            with open(edit_file, 'w') as fo:
                fo.write(open('tpl_edit.tpl').read().replace('xxxxxx', ''.join(edit_widget_arr)))
