import mysql.connector
import os
import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="jeddevne_ccbalance",
    password=os.environ.get("MYSQL_PASSWORD"),
    database="jeddevne_ccbalance"
)

mycursor = mydb.cursor()


def approve(user_id, name, email):
    mydb = mysql.connector.connect(
        host="localhost",
        user="jeddevne_ccbalance",
        password=os.environ.get("MYSQL_PASSWORD"),
        database="jeddevne_ccbalance"
    )

    mycursor = mydb.cursor()
    sql = "INSERT INTO users (id, name, email) VALUES (%s, %s, %s)"
    val = (user_id, name, email)
    mycursor.execute(sql, val)
    mydb.commit()


def is_verified(user_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="jeddevne_ccbalance",
        password=os.environ.get("MYSQL_PASSWORD"),
        database="jeddevne_ccbalance"
    )

    mycursor = mydb.cursor()
    sql = "SELECT * FROM users WHERE id = %s"
    val = (user_id,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    if len(myresult) > 0:
        return True
    else:
        return False


def name_from_id(user_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="jeddevne_ccbalance",
        password=os.environ.get("MYSQL_PASSWORD"),
        database="jeddevne_ccbalance"
    )

    mycursor = mydb.cursor()
    sql = "SELECT name FROM users WHERE id = %s"
    val = (user_id,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    return myresult[0]


def check_day():
    mydb = mysql.connector.connect(
        host="localhost",
        user="jeddevne_ccbalance",
        password=os.environ.get("MYSQL_PASSWORD"),
        database="jeddevne_ccbalance"
    )

    mycursor = mydb.cursor()
    day = datetime.date.today()
    day = str(day)
    sql = "SELECT day from days WHERE day = %s"
    val = (day,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    if myresult is None:
        sql = "INSERT INTO days (day) VALUES (%s)"
        mycursor.execute(sql, val)
        sql = "UPDATE vars SET requests_today = 0 WHERE requests_today > 0"
        mycursor.execute(sql)


def set_max(max):
    mydb = mysql.connector.connect(
        host="localhost",
        user="jeddevne_ccbalance",
        password=os.environ.get("MYSQL_PASSWORD"),
        database="jeddevne_ccbalance"
    )

    mycursor = mydb.cursor()
    sql = "UPDATE vars SET max_requests = %s WHERE max_requests != -1" % max
    mycursor.execute(sql)


def get_max():
    mydb = mysql.connector.connect(
        host="localhost",
        user="jeddevne_ccbalance",
        password=os.environ.get("MYSQL_PASSWORD"),
        database="jeddevne_ccbalance"
    )

    mycursor = mydb.cursor()
    sql = "SELECT max_requests FROM vars"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    return myresult


def get_daily():
    mydb = mysql.connector.connect(
        host="localhost",
        user="jeddevne_ccbalance",
        password=os.environ.get("MYSQL_PASSWORD"),
        database="jeddevne_ccbalance"
    )

    mycursor = mydb.cursor()
    sql = "SELECT requests_today FROM vars"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    return myresult


def increase_daily():
    mydb = mysql.connector.connect(
        host="localhost",
        user="jeddevne_ccbalance",
        password=os.environ.get("MYSQL_PASSWORD"),
        database="jeddevne_ccbalance"
    )

    mycursor = mydb.cursor()
    sql = "UPDATE vars SET requests_today = requests_today + 1 WHERE requests_today != -1"
    mycursor.execute(sql)


def re_init():
    mydb = mysql.connector.connect(
        host="localhost",
        user="jeddevne_ccbalance",
        password=os.environ.get("MYSQL_PASSWORD"),
        database="jeddevne_ccbalance"
    )

    mycursor = mydb.cursor()
