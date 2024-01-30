import pymysql

name = ""

def setName(x):
    name = x

def insertData(emp_id, name, photo):
    print("Inserting data into table")
    try:
        connection = pymysql.connect(host='localhost',
                                     db='be_project_db',
                                     user='root',
                                     password='test')

        print("DB Connection Success")
        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO python_employee
                          (id, name, photo, biodata) VALUES (%s,%s,%s)"""

        empPicture = convertToBinaryData(photo)

        # Convert data into tuple format
        insert_blob_tuple = (emp_id, name, empPicture)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Image and file inserted successfully as a BLOB into python_employee table", result)

    except pymysql.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
