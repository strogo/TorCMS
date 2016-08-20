__author__ = 'bukun'
import os
crud_path = os.path.abspath('../../templates/autogen')


if __name__ == '__main__':
    tag_arr = ['add', 'edit', 'view', 'list', 'infolist']
    path_arr = [os.path.join(crud_path, x) for x in tag_arr]
    for wpath in path_arr:
        if os.path.exists(wpath):
            continue
        os.makedirs( wpath )

