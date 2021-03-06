"""
name
"""
from db.dbtable import Rps, Sps, Xps, Template

x_file_pattern = '"XPS (*.xps, *.x, *.XPS, *.X )"'
s_file_pattern = '"SPS (*.sps, *.s, *.SPS, *.S )"'
r_file_pattern = '"RPS (*.rps, *.r, *.RPS, *.R )"'
db_file_pattern = '"SQLite (*.sqlite )"'

'''
table config
'''
point_table_content = '''(
                        line real NOT NULL,
                        point real NOT NULL,
                        idx int NOT NULL,
                        easting real NOT NULL,
                        northing real NOT NULL,
                        elevation real NOT NULL,
                        PRIMARY KEY(line, point, idx)'''

table_dict = {'R': point_table_content,
              'S': point_table_content,
              'X': point_table_content,
              }

table_class = {'R': Rps,
               'S': Sps,
               'X': Xps,
               'template': Template
               }
point_table = ['R', 'S']

# SQL_CREATE_TABLE = """ CREATE TABLE IF NOT EXISTS  {}{}
# ); """.format(list(table_dict.keys())[0], table_dict[list(table_dict.keys())[0]])
#
# print(SQL_CREATE_TABLE)
