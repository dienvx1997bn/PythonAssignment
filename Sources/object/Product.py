import mysql.connector
from datetime import datetime

column_dict = {
    "id":0,
    "name":1,
    "materials":2,
    "category":3,
    "cost":4,
    "produceTime":5,
    "price":6,
    "progress":7,
    "qcStatus":8,
    "assemblyId":9,
    "workerId":10
}

class Product:
    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.materials = kwargs["materials"]
        self.category = kwargs["category"]
        self.cost = kwargs["cost"]
        self.produceTime = kwargs["produceTime"]
        self.price = kwargs["price"]
        self.progress = kwargs["progress"]
        self.qcStatus = kwargs["qcStatus"]
        self.assemblyId = kwargs["assemblyId"]
        self.workerId = kwargs["workerId"]

        #init sql client
        self.mydb = mysql.connector.connect(
            host = "sql12.freesqldatabase.com",
            user = "sql12532759",
            password = "L7cn3eESyz",
            database="sql12532759"
        )
        self.mycursor = self.mydb.cursor()

    def product_start_manufacturing(self):
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        self.startTime = formatted_date
        sql = f"UPDATE products SET progress = 'PROCESSING', startTime = '{formatted_date}' WHERE id = '{self.id}'"
        self.mycursor.execute(sql)
        self.mydb.commit()

    def product_end_manufacturing(self):
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        self.endTime = formatted_date
        sql = f"UPDATE products SET progress = 'FINISHED', endTime = '{formatted_date}' WHERE id = '{self.id}'"
        self.mycursor.execute(sql)
        self.mydb.commit()
        # close connection when done
        self.mycursor.close()
        self.mydb.close()
    
    def qc_check(self, qcStatus):
        sql = f"UPDATE products SET qcStatus = '{qcStatus}' WHERE id = '{self.id}'"
        self.mycursor.execute(sql)
        self.mydb.commit()
