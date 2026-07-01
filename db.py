import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",   # Replace with your MySQL password if you have one
    database="threat_detection"
)

cursor = conn.cursor()