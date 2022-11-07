"""
For create new assembly line
"""
import threading
import time
import uuid
import logging
import random

import mysql.connector
from .Product import Product
from .Material import Material
from .Requirement import Requirement


class Assembly:
    # Creating lock for query
    lock_for_take_component = threading.Lock()

    def __init__(self, **kwargs):
        self.assembly_id = kwargs["assembly_id"]
        self.category = kwargs["category"]
        self.product_id = kwargs["product_id"]
        self.worker_id = kwargs["worker_id"]
        self.status = kwargs["status"]
        self.production_list = []
        self.production_current = None
        self.product_material_current = []
        self.requirements_current = None
        self.requirements_list = []

        #init sql client
        self.mydb = mysql.connector.connect(
            host="sql12.freesqldatabase.com",
            user="sql12532759",
            password="L7cn3eESyz",
            database="sql12532759"
        )
        self.mycursor = self.mydb.cursor()


    def get_requirements(self):
        """query requirement of list material"""
        sql = f"SELECT * FROM requirements where category ='{self.category}'"
        self.mycursor.execute(sql)
        queryreturn = self.mycursor.fetchall()

        for requirement in queryreturn:
            self.requirements_list.append(Requirement(id=requirement[0], category=requirement[1],
                                                 name=requirement[2], material=eval(requirement[3]),
                                                 time_needed=requirement[5]))


    def take_componments(self, materials_dict):
        """
        take material and then update database
        need blocking for query to avoid conflict
        """
        err = 0
        # enter blocking
        self.lock_for_take_component.acquire()
        # check
        for material_id, num in materials_dict.items():
            sql = f"SELECT * FROM materials where id ='{material_id}'"
            self.mycursor.execute(sql)
            query_return = self.mycursor.fetchall()
            material_available = query_return[0][4]
            if material_available < num:
                err = err + 1
        if err != 0:
            self.lock_for_take_component.release()
            return False
        # take and update
        for material_id, num in materials_dict.items():
            sql = f"SELECT * FROM materials where id ='{material_id}'"
            self.mycursor.execute(sql)
            query_return = self.mycursor.fetchall()
            material_available = query_return[0][4]

            sql = f"UPDATE materials \
                    SET amount = {material_available - num} \
                    WHERE id = '{material_id}'"
            self.mycursor.execute(sql)
            self.mydb.commit()

            self.product_material_current.append(Material(material_id=material_id,
                                                          name=query_return[0][1],
                                                          cost=query_return[0][2],
                                                          vendor=query_return[0][3],
                                                          quantity_per_unit=query_return[0][5]))
        # exit blocking
        self.lock_for_take_component.release()
        return True


    def prepare_new_product(self):
        """new product, update table"""
        product = Product(product_id=str(uuid.uuid4())[0:8],
                          name=self.requirements_current.name,
                          materials=self.requirements_current.material,
                          category=self.category,
                          cost = 0,
                          price = 0,
                          progress='WAITING',
                          qc_status=None,
                          assembly_id=self.assembly_id,
                          worker_id=self.worker_id)
        # caculate cost and price
        product.cost = sum(material.cost for material in self.product_material_current)
        product.price = product.cost * 3

        self.production_current = product
        self.production_list.append(self.production_current)
        sql = "INSERT INTO products \
               (id, name, materials, category, progress, assemblyId, workerId, cost, price) \
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (product.product_id, product.name, str(product.materials), product.category,
               product.progress, product.assembly_id, product.worker_id, int(product.cost),
               int(product.price))
        self.mycursor.execute(sql, val)
        self.mydb.commit()

        logging.info("assembly %s has new product %s", self.assembly_id, product.product_id)
        #processing, update table
        product.product_start_manufacturing()


    def processing_new_product(self):
        """wait for processing"""
        time.sleep(self.requirements_current.time_needed)


    def finish_new_product(self):
        """finish_new_product"""
        self.production_current.product_end_manufacturing()


    def qa_check(self):
        """qa check"""
        magic_num = random.randrange(1, 100)
        if magic_num < 25:
            self.production_current.qc_check("FAIL")
        else:
            self.production_current.qc_check("PASS")


    def assembly_manufacturing(self):
        """assembly main function"""
        self.get_requirements()

        while True:
            # take componments
            err = False
            for self.requirements_current in self.requirements_list:
                if self.take_componments(self.requirements_current.material):
                    self.prepare_new_product()
                    self.processing_new_product()
                    self.qa_check()
                    self.finish_new_product()
                    err = False
                    break
                else:
                    err = True
            if err == True:
                break

        logging.info("assembly %s finish all product", self.assembly_id)
        sql = f"UPDATE assemblyLines SET  status = 'FINISH' WHERE id = '{self.assembly_id}'"
        self.mycursor.execute(sql)
        self.mydb.commit()
