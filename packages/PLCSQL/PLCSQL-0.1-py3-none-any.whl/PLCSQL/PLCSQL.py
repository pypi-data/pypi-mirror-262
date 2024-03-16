import mysql.connector

def CD(text, mydb):
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE " + text)

def CT(text, mydb):
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE " + text)

def IV(text, text1, text2, mydb):
    num_columns = text1.count(',') + 1
    placeholders = ','.join(['%s'] * num_columns)
    sqlFormula = "INSERT INTO " + text + " (" + text1 + ") VALUES (" + placeholders + ")"

    mycursor = mydb.cursor()
    mycursor.execute(sqlFormula, text2)
    mydb.commit()

def IVM(text, text1, text2, mydb):
    num_columns = text1.count(',') + 1
    placeholders = ','.join(['%s'] * num_columns)
    sqlFormula = "INSERT INTO " + text + " (" + text1 + ") VALUES (" + placeholders + ")"

    mycursor = mydb.cursor()
    mycursor.executemany(sqlFormula, text2)
    mydb.commit()



def SA(text, mydb):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM " + text)
    results = mycursor.fetchall()
    for x in results:
        print(x)

def DB(text, mydb):
    mycursor = mydb.cursor()
    mycursor.execute("DROP DATABASE " + text)

def DT(text, mydb):
    mycursor = mydb.cursor()
    mycursor.execute("DROP TABLE " + text)

def STBC(text1, text, mydb):
    mycursor = mydb.cursor()
    sql_query = "SELECT " + text1 + " FROM " + text
    mycursor.execute(sql_query)
    results = mycursor.fetchall()
    for row in results:
        print(row[0])

def STBW(table_name, condition, mydb):
    mycursor = mydb.cursor()
    sql_query = "SELECT * FROM " + table_name + " WHERE " + condition
    mycursor.execute(sql_query)
    results = mycursor.fetchall()
    for row in results:
        print(row[0])

def STBWL(table_name, column, condition, mydb):
    mycursor = mydb.cursor()
    sql_query = "SELECT * FROM " + table_name + " WHERE " + column + " LIKE %s"
    mycursor.execute(sql_query, (condition,))
    results = mycursor.fetchall()
    for row in results:
        print(row[0])

def UTBW(table_name, value, condition, mydb):
    mycursor = mydb.cursor()
    sql_query = "UPDATE " + table_name + " SET " + value + " WHERE " + condition
    mycursor.execute(sql_query)
    mydb.commit()

def STBR(condition, mydb):
    mycursor = mydb.cursor()
    sql_query = "SELECT * FROM " + condition
    mycursor.execute(sql_query)
    results = mycursor.fetchall()
    for row in results:
        print(row)

def STBO(table, field, mydb):
    mycursor = mydb.cursor()
    sql_query = "SELECT * FROM " + table + " ORDER BY " + field
    mycursor.execute(sql_query)
    results = mycursor.fetchall()
    for row in results:
        print(row)

def STBOAD(table, field, ad, mydb):
    mycursor = mydb.cursor()
    sql_query = "SELECT * FROM " + table + " ORDER BY " + field + " " + ad
    mycursor.execute(sql_query)
    results = mycursor.fetchall()
    for row in results:
        print(row)

def MCDT(table_name, column_name, new_datatype, mydb):
    mycursor = mydb.cursor()
    sql_query = f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} {new_datatype}"
    
    try:
        mycursor.execute(sql_query)
        mydb.commit()
        print(f"Column '{column_name}' in table '{table_name}' datatype successfully modified to '{new_datatype}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def MCP(table_name, column_name, after_column_name, mydb):
    mycursor = mydb.cursor()
    sql_query = f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} VARCHAR(100) AFTER {after_column_name}"
    
    try:
        mycursor.execute(sql_query)
        mydb.commit()
        print(f"Column '{column_name}' in table '{table_name}' moved after '{after_column_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def ATBF(table_name, new_column_name, column_definition, mydb):
    mycursor = mydb.cursor()
    sql_query = f"ALTER TABLE {table_name} ADD {new_column_name} {column_definition}"
    
    try:
        mycursor.execute(sql_query)
        mydb.commit()
        print(f"Field '{new_column_name}' added to table '{table_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
