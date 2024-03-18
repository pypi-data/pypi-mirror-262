import mysql.connector
import mariadb

def CD(text, mydb):
    try:
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE " + text)
        print("Your Database created successfully.")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

def CT(text, mydb):
    try:
        mycursor = mydb.cursor()
        mycursor.execute("CREATE TABLE " + text)
        print("Table created successfully.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def IV(text, text1, text2, mydb):
    try:
        num_columns = text1.count(',') + 1
        placeholders = ','.join(['%s'] * num_columns)
        sqlFormula = "INSERT INTO " + text + " (" + text1 + ") VALUES (" + placeholders + ")"
        mycursor = mydb.cursor()
        mycursor.execute(sqlFormula, text2)
        mydb.commit()
        print("Data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")

def IVM(text, text1, text2, mydb):
    try:
        num_columns = text1.count(',') + 1
        placeholders = ','.join(['%s'] * num_columns)
        sqlFormula = "INSERT INTO " + text + " (" + text1 + ") VALUES (" + placeholders + ")"
        mycursor = mydb.cursor()
        mycursor.executemany(sqlFormula, text2)
        mydb.commit()
        print("Multiple data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting multiple data: {err}")

def SA(text, mydb):
    try:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM " + text)
        results = mycursor.fetchall()
        for x in results:
            print(x)
    except mysql.connector.Error as err:
        print(f"Error selecting data: {err}")

def DB(text, mydb):
    try:
        mycursor = mydb.cursor()
        mycursor.execute("DROP DATABASE " + text)
        print("Database dropped successfully.")
    except mysql.connector.Error as err:
        print(f"Error dropping database: {err}")

def DT(text, mydb):
    try:
        mycursor = mydb.cursor()
        mycursor.execute("DROP TABLE " + text)
        print("Table dropped successfully.")
    except mysql.connector.Error as err:
        print(f"Error dropping table: {err}")

def STBC(text1, text, mydb):
    try:
        mycursor = mydb.cursor()
        sql_query = "SELECT " + text1 + " FROM " + text
        mycursor.execute(sql_query)
        results = mycursor.fetchall()
        for row in results:
            print(row[0])
    except mysql.connector.Error as err:
        print(f"Error executing SELECT query: {err}")

def STBW(table_name, condition, mydb):
    try:
        mycursor = mydb.cursor()
        sql_query = "SELECT * FROM " + table_name + " WHERE " + condition
        mycursor.execute(sql_query)
        results = mycursor.fetchall()
        for row in results:
            print(row[0])
    except mysql.connector.Error as err:
        print(f"Error executing SELECT query with condition: {err}")

def STBWL(table_name, column, condition, mydb):
    try:
        mycursor = mydb.cursor()
        sql_query = "SELECT * FROM " + table_name + " WHERE " + column + " LIKE %s"
        mycursor.execute(sql_query, (condition,))
        results = mycursor.fetchall()
        for row in results:
            print(row[0])
    except mysql.connector.Error as err:
        print(f"Error executing SELECT query with LIKE condition: {err}")

def UTBW(table_name, value, condition, mydb):
    try:
        mycursor = mydb.cursor()
        sql_query = "UPDATE " + table_name + " SET " + value + " WHERE " + condition
        mycursor.execute(sql_query)
        mydb.commit()
        print("Update successful.")
    except mysql.connector.Error as err:
        print(f"Error executing UPDATE query: {err}")

def STBR(condition, mydb):
    try:
        mycursor = mydb.cursor()
        sql_query = "SELECT * FROM " + condition
        mycursor.execute(sql_query)
        results = mycursor.fetchall()
        for row in results:
            print(row)
    except mysql.connector.Error as err:
        print(f"Error executing SELECT query with dynamic table name: {err}")

def STBO(table, field, mydb):
    try:
        mycursor = mydb.cursor()
        sql_query = "SELECT * FROM " + table + " ORDER BY " + field
        mycursor.execute(sql_query)
        results = mycursor.fetchall()
        for row in results:
            print(row)
    except mysql.connector.Error as err:
        print(f"Error executing SELECT query with ORDER BY: {err}")

def STBOAD(table, field, ad, mydb):
    try:
        mycursor = mydb.cursor()
        sql_query = "SELECT * FROM " + table + " ORDER BY " + field + " " + ad
        mycursor.execute(sql_query)
        results = mycursor.fetchall()
        for row in results:
            print(row)
    except mysql.connector.Error as err:
        print(f"Error executing SELECT query with ORDER BY and direction: {err}")

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
