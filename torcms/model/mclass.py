# # -*- coding:utf-8 -*-
#
#
# from torcms.model.core_tab import CabCatalog
# from torcms.model.msingle_table import MSingleTable
#
#
# class MClass(MSingleTable):
#     def __init__(self):
#         self.tab = CabCatalog
#         try:
#             self.tab.create_table()
#         except:
#             pass
#
#     def update(self, uid, post_data, update_time=False):
#
#         if update_time:
#             entry = self.tab.update(
#                 name=post_data['name'][0],
#                 slug=post_data['slug'][0],
#                 order=post_data['order'][0],
#             ).where(self.tab.uid == uid)
#         else:
#             entry = self.tab.update(
#                 name=post_data['name'][0],
#                 slug=post_data['slug'][0],
#                 order=post_data['order'][0],
#             ).where(self.tab.uid == uid)
#         entry.execute()
#
#
#     def insert_data(self, id_post, post_data):
#         uu = self.get_by_id(id_post)
#         if uu is None:
#             pass
#         else:
#             return (False)
#
#         entry = self.tab.create(
#             name=post_data['name'][0],
#             slug=post_data['slug'][0],
#             order=post_data['order'][0],
#             uid=id_post,
#         )
#         return (entry.uid)
#
#
#
