"""
For create new product
"""
import mysql.connector
from datetime import datetime


class Product:
    def __init__(self, **kwargs):
        self.product_id = kwargs["product_id"]
        self.name = kwargs["name"]
        self.materials = kwargs["materials"]
        self.category = kwargs["category"]
        self.cost = kwargs["cost"]
        self.price = kwargs["price"]
        self.progress = kwargs["progress"]
        self.qc_status = kwargs["qc_status"]
        self.assembly_id = kwargs["assembly_id"]
        self.worker_id = kwargs["worker_id"]
        self.start_time = ""
        self.end_time = ""

        #init sql client
        self.mydb = mysql.connector.connect(
            host = "sql12.freesqldatabase.com",
            user = "sql12532759",
            password = "L7cn3eESyz",
            database="sql12532759"
        )
        self.mycursor = self.mydb.cursor()

    def product_start_manufacturing(self):
        """product_start_manufacturing"""
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        self.start_time = formatted_date
        sql = f"UPDATE products \
                SET progress = 'PROCESSING', startTime = '{formatted_date}' \
                WHERE id = '{self.product_id}'"
        self.mycursor.execute(sql)
        self.mydb.commit()

    def product_end_manufacturing(self):
        """product_end_manufacturing"""
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        self.end_time = formatted_date
        sql = f"UPDATE products \
                SET progress = 'FINISHED', endTime = '{formatted_date}' \
                WHERE id = '{self.product_id}'"
        self.mycursor.execute(sql)
        self.mydb.commit()
        # close connection when done
        self.mycursor.close()
        self.mydb.close()

    def qc_check(self, qc_status):
        """update qc check result"""
        sql = f"UPDATE products SET qcStatus = '{qc_status}' WHERE id = '{self.product_id}'"
        self.mycursor.execute(sql)
        self.mydb.commit()
