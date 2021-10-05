import sqlite3
from constants import *

class DataBase:

    def __init__(self, name, fields, types):
        self.name = name
        self.fields = fields
        self.types = types

    def createTable(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        sql_command = f'''CREATE TABLE IF NOT EXISTS {self.name} ('''
        for i in range(0, len(self.fields) - 1):
            sql_command += f'''\n\t{self.fields[i]} {self.types[i]}, '''

        sql_command += f'''\n\t{self.fields[-1]} {self.types[-1]}\n)'''

        cursor.execute(sql_command)
        conn.commit()
        conn.close()

    def addData(self, data):
        # when passes a list of dictionaries, will add data in dictionaries to the given table in the database only if
        # dictionary key is within the 'fields' of the table
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        for i in range(0, len(data)):
            insert_data = f"""INSERT INTO {self.name}\n("""

            for ii in range(0, len(list(data[i].keys()))):
                if list(data[i].keys())[ii] in self.fields:
                    # add that line to the INSERT
                    insert_data += f"""{list(data[i].keys())[ii]},"""
                else:
                    # print(f'Unrecognised Field Name on line {i+1} of input')
                    pass
            insert_data = insert_data[:-1]  # delete last comma
            insert_data += f""") \nVALUES ("""

            additions = []
            for ii in range(0, len(list(data[i].keys()))):
                if list(data[i].keys())[ii] in self.fields:
                    # add that line to the INSERT
                    insert_data += f"""\n\t?,"""
                    additions.append(f"{data[i][list(data[i].keys())[ii]]}")
                else:
                    pass
            insert_data = insert_data[:-1]  # delete last comma
            insert_data += f"""\n)"""
            cursor.execute(insert_data, additions)
            conn.commit()

        conn.close()

    def getAllData(self):
        # read contents of given table into list of dictionaries, each key is defined by the corresponding field entry
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        sql_command = f'''SELECT * FROM {self.name}'''
        cursor.execute(sql_command)
        rows = cursor.fetchall()

        data = []

        for row in rows:
            data_row = {}
            for i in range(0, len(row)):
                data_row[f'{self.fields[i]}'] = row[i]

            data.append(data_row)

        conn.commit()
        conn.close()

        return data

    # def findMatchingID(self, User_Input):
    #     User_Input_List = [User_Input]
    #
    #     conn = sqlite3.connect(DATABASE)
    #     cursor = conn.cursor()
    #     sql_command = f'''SELECT * FROM {self.name}'''
    #     sql_command += f'''\nWHERE {self.fields[0]}=?'''
    #     cursor.execute(sql_command, User_Input_List)
    #     rows = cursor.fetchall()
    #
    #     data = []
    #     for row in rows:
    #         data_row = {}
    #         for i in range(0, len(row)):
    #             data_row[f'{self.fields[i]}'] = row[i]
    #
    #         data.append(data_row)
    #     conn.commit()
    #     conn.close()
    #
    #     return data

    # def editData(self, user_edit, ID):
    #     conn = sqlite3.connect(DATABASE)
    #     cursor = conn.cursor()
    #     edits = []
    #     sql_command = f"""UPDATE {self.name}"""
    #     sql_command += f"""\nSET """
    #
    #     for i in range(1, len(user_edit)+1):
    #         sql_command += f"""{self.fields[i]}=?, """
    #         edits.append(f"{user_edit[f'{self.fields[i]}']}")
    #
    #     sql_command = sql_command[:-2]
    #     sql_command += f"""\nWHERE {self.fields[0]} = {ID};"""
    #
    #     cursor.execute(sql_command, edits)
    #     conn.commit()
    #     conn.close

    # def editAvailable(self, crement, ID):
    #     conn = sqlite3.connect(DATABASE)
    #     cursor = conn.cursor()
    #
    #     data = self.findMatchingID(ID)
    #     currentVal = int(data[0]['Available'])
    #
    #     sql_command = f"""UPDATE {self.name}"""
    #     sql_command += f"""\nSET """
    #     sql_command += f"""{self.fields[4]}={str((crement*1)+currentVal)}"""
    #     sql_command += f"""\nWHERE {self.fields[0]} = {ID};"""
    #
    #     cursor.execute(sql_command)
    #     conn.commit()
    #     conn.close()