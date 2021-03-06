import sqlite3
from sqlite3 import Error
from configure import config


class Table:
    table_dict = config.table_dict

    def __init__(self, db_file: str):
        self.db_file = db_file

    def create_connection(self):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
        finally:
            if conn:
                return conn

    def create_table(self, conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
            c.execute("select name from sqlite_master where type='table'")
            tab_name = c.fetchall()
            tab_name = [line[0] for line in tab_name]
            print(tab_name)
            col_names = []
            for line in tab_name:
                c.execute('pragma table_info({})'.format(line))
                col_name = c.fetchall()
                col_name = [x[1] for x in col_name]
                col_names.append(col_name)
                col_name = tuple(col_name)
            print(col_name)
        except Error as e:
            print(e)

    def table_crate(self):
        conn = self.create_connection()
        for key in config.table_dict.keys():
            SQL_CREATE_TABLE = """ CREATE TABLE IF NOT EXISTS  {}{} 
            ); """.format(key, config.table_dict[key])
            print(SQL_CREATE_TABLE)
            self.create_table(conn, SQL_CREATE_TABLE)

    def choose_table(self, data_file):
        with open(data_file) as sps:
            line = sps.readline()
            while line:
                if line[0:1] not in config.table_dict.keys():
                    pass
                else:
                    break
                line = sps.readline()
        sps.close()
        return line[0:1]

    def db_point_update(self, conn, DB_TABLE, sps_data):
        line = sps_data[1]
        point = sps_data[2]
        idx = sps_data[3]
        easting = sps_data[10]
        northing = sps_data[11]
        elevation = sps_data[12]
        if elevation == None:
            elevation = 0
        c = conn.cursor()
        sql_insert = "INSERT OR REPLACE INTO " + DB_TABLE + " (line, point, idx, easting, northing, elevation) VALUES (?, ?, ?, ?, ?, ?);"
        data = (line, point, idx, easting, northing, elevation)
        c.execute(sql_insert, data)
        # print(sql_insert, data)
        # conn.commit()
        c.close()

    def get_record_for_point(self, conn, DB_TABLE, key_list: list):
        """
        :param conn:
        :param key_list:
        :return:
        """
        c = conn.cursor()
        c.execute("SELECT * FROM " + DB_TABLE + " WHERE line =? and point = ? and idx = ?",
                  (key_list[0], key_list[1], key_list[2]))
        rows = c.fetchall()
        if len(rows) > 0:
            data = rows[0]  # [rows[0][0], rows[0][1], rows[0][2], rows[0][3], rows[0][4], rows[0][5]]
            return data

    def clear(self, conn, DB_TABLE):
        # conn = self.create_connection(db_file)
        c = conn.cursor()
        sql = "DELETE from " + DB_TABLE
        c.execute(sql)
        conn.commit()
        conn.close()

# def get_record_for_point(conn, DB_TABLE, sps_point):
#     """
#     :param conn:
#     :param Point sps_point:
#     :return:
#     """
#     print(DB_TABLE)
#     c = conn.cursor()
#     print(sps_point[1], sps_point[2])
#     c.execute("SELECT * FROM " + DB_TABLE + " WHERE line =? and point = ?", (sps_point[1], sps_point[2]))
#     rows = c.fetchall()
#     print(rows)
#     if len(rows) > 0:
#         data = [rows[0][0], rows[0][1], rows[0][2], rows[0][3], rows[0][4]]
#         print(data)
#         return data
#
#     # return None
#
#
# def count_db_records(db_file, DB_TABLE):
#     conn = create_connection(db_file)
#     sql = "SELECT COUNT(*) FROM " + DB_TABLE
#     c = conn.cursor()
#     c.execute(sql)
#     count = c.fetchone()[0]
#     conn.close()
#
#     return count
#
#
# def clear(db_file, DB_TABLE):
#     conn = create_connection(db_file)
#     c = conn.cursor()
#     sql = "DELETE from " + DB_TABLE
#     # print(sql)
#     c.execute(sql)
#     conn.commit()
#     conn.close()
