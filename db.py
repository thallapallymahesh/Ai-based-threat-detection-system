import mysql.connector

try:
    conn = mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        port=3306,
        user="sql12832834",
        password="yrZ8Zxg9mv",
        database="sql12832834",
        autocommit=True,
        connection_timeout=30
    )

    cursor = conn.cursor()
    print("Connected successfully!")

except Exception as e:
    print(e)