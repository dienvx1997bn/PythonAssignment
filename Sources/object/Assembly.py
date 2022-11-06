import threading
import time
import uuid
import logging
import random
from datetime import datetime

import mysql.connector
from object.Product import Product


column_dict = {
    "id":0,
    "name":1,
    "cost":2,
    "vendor":3,
    "amount":4,
    "quantityPerUnit":5
}

class Assembly:

    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.category = kwargs["category"]
        self.productId = kwargs["productId"]
        self.workerId = kwargs["workerId"]
        self.status = kwargs["status"]
        self.production_list = []
        self.production_current = None
        
        # Creating lock for threads
        self.lock_for_take_component = threading.Lock()

    def connect_sql(self):
        #init sql client
        self.mydb = mysql.connector.connect(
            host = "sql12.freesqldatabase.com",
            user = "sql12532759",
            password = "L7cn3eESyz",
            database="sql12532759"
        )
        self.mycursor = self.mydb.cursor()
    
    def get_requirements(self):
        sql = f"SELECT * FROM requirements where category ='{self.category}'"
        self.mycursor.execute(sql)
        self.requirements = self.mycursor.fetchall()
        self.requirements = self.requirements[0] #get the first element due to the sql return tuple 
        # print(self.query_return)

    def take_componments(self, materials):
        materials_dict = dict(eval(materials))
        err = 0
        # enter blocking
        self.lock_for_take_component.acquire()
        # check
        for id, num in materials_dict.items():
            sql = f"SELECT * FROM materials where id ='{id}'"
            self.mycursor.execute(sql)
            query_return = self.mycursor.fetchall()
            material_available  = query_return[0][4]
            if material_available < num:
                err = err + 1
        
        if err != 0:
            self.lock_for_take_component.release()
            return False
        
        # take and update
        for id, num in materials_dict.items():
            sql = f"SELECT * FROM materials where id ='{id}'"
            self.mycursor.execute(sql)
            query_return = self.mycursor.fetchall()
            material_available  = query_return[0][4]

            sql = f"UPDATE materials SET amount = {material_available - num} WHERE id = '{id}'"
            self.mycursor.execute(sql)
            self.mydb.commit()
        # exit blocking
        self.lock_for_take_component.release()
        return True


    def prepare_new_product(self):
        #new product, update table
        self.timeNedded = self.requirements[5]
        product = Product(id = str(uuid.uuid4())[0:8], 
                            name = self.requirements[2], 
                            materials = self.requirements[3], 
                            category = self.category,
                            cost = 0,   # TODO: caculate
                            produceTime = 0,
                            price = 0,
                            progress = 'WAITING',
                            qcStatus = None,
                            assemblyId = self.id,
                            workerId = self.workerId)
        self.production_current = product
        self.production_list.append(self.production_current)
        sql = "INSERT INTO products (id, name, materials, category, progress, assemblyId, workerId) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (product.id, product.name, product.materials, product.category, product.progress, product.assemblyId, product.workerId)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

        logging.info(f"assembly {self.id} has new product {product.id}")
        #processing, update table
        product.product_start_manufacturing()

    def processing_new_product(self):
        # wait for processing
        time.sleep(self.timeNedded)
    
    def finish_new_product(self):
        self.production_current.product_end_manufacturing()

    def qa_check(self):
        magic_num = random.randrange(1, 100)
        if(magic_num < 25):
            self.production_current.qc_check("FAIL")
        else:
            self.production_current.qc_check("PASS")


    def assembly_manufacturing(self):
        self.connect_sql()
        self.get_requirements()

        while(True):    # loop for manufacturing
            # take componments
            if self.take_componments(self.requirements[3]):
                self.prepare_new_product()
                self.processing_new_product()
                self.qa_check()
                self.finish_new_product()
                
            else: 
                logging.info(f"assembly {self.id} finish all product")
                sql = f"UPDATE assemblyLines SET  status = 'FINISH' WHERE id = '{self.id}'"
                self.mycursor.execute(sql)
                self.mydb.commit()
                break
