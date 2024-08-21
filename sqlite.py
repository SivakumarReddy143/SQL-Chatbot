import sqlite3

connection=sqlite3.connect("student.db")
cursor=connection.cursor()
table_info="""
create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),MARKS INT, SECTION VARCHAR(25))
"""
cursor.execute(table_info)

cursor.execute("""INSERT INTO STUDENT VALUES('SIVA','CSE',45,'B')""")
cursor.execute("""INSERT INTO STUDENT VALUES('KUMAR','DATA SCIENCE',67,'A')""")
cursor.execute("""INSERT INTO STUDENT VALUES('REDDY','AI',89,'A')""")
data=cursor.execute("""SELECT * FROM STUDENT""")
for row in data:
    print(row)
connection.commit()
connection.close()