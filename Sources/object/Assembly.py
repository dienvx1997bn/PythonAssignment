import threading
import time

import mysql.connector

column_dict = {
    "id":0,
    "name":1,
    "cost":2,
    "vendor":3,
    "amount":4,
    "quantityPerUnit":5
}

class Assembly:

    def __init__(self, id, category, productId, hasWorker, hasProduct, status):
        self.id = id
        self.category = category
        self.productId = productId
        self.hasWorker = hasWorker
        self.hasProduct = hasProduct
        self.status = status
        
        #global variable
        self.car_type = None
        self.query_return = ""
        self.sedan_produced = 0
        self.sedan_fail = 0
        # Creating lock for threads
        self.lock_for_take_component = threading.Lock()

        #init sql client
        self.mydb = mysql.connector.connect(
            host = "sql12.freesqldatabase.com",
            user = "sql12532759",
            password = "L7cn3eESyz",
            database="sql12532759"
        )
        self.mycursor = self.mydb.cursor()


    def get_requirements(self):
        sql = "SELECT * FROM requirements WHERE category =%s"
        val = (self.car_type,)
        self.mycursor.execute(sql, val)
        self.query_return = self.mycursor.fetchall()
        # print(self.query_return)


    def check_and_take_component(self, product_requirement):
        is_available = False
        material_dict = dict(eval(product_requirement[3]))
        # print(material_dict)
        # for i in material_dict.keys():
        #     print(i)
        self.lock_for_take_component.acquire()
        error = 0
        for component in material_dict.keys():
            sql = f"SELECT * FROM materials WHERE id ='{component}'"
            # print(f"sql {sql}")
            self.mycursor.execute(sql)
            query_return = self.mycursor.fetchall()
            # print(query_return)
            query_return = query_return[0] # unpacking
            if(query_return[column_dict["amount"]] > query_return[column_dict["quantityPerUnit"]]):
                pass
            else:
                error = error + 1
        
        # if have all the things needed, take and update databae
        if(error == 0):
            for component in material_dict.keys():
                sql = f"SELECT * FROM materials WHERE id ='{component}'"
                self.mycursor.execute(sql)
                query_return = self.mycursor.fetchall()
                query_return = query_return[0] # unpacking

                amout_new = query_return[column_dict["amount"]] - query_return[column_dict["quantityPerUnit"]]
                sql = f"UPDATE materials SET amount = {amout_new} WHERE id ='{component}"
                self.mycursor.execute(sql)
                self.mydb.commit()
            is_available = True
        self.lock_for_take_component.release()
        return is_available

    def assembly_running(self, product_requirement):

        while(True):
            if self.check_and_take_component(product_requirement):
                continue
            else:
                break
        
        #start process
        xtime = time.perf_counter()
        time.sleep(3)
        #end process
        xtime = time.perf_counter()
        self.sedan_produced += 1


    def assembly_manufacturing(self, car_type):
        self.car_type = car_type
        self.get_requirements()
        
        # # start production line
        start_time = time.perf_counter()
        threads = []
        requirement_list = self.query_return
        for product_requirement in requirement_list:
            # creating threads: 
            t = threading.Thread(target=self.assembly_running, args=(product_requirement, ))
            threads.append(t)
            t.start()
        
        #wait to finish
        for t in threads:
            t.join()

        end_time = time.perf_counter()
        print(f'It took {end_time- start_time: f} second(s) to complete. {self.car_type}')
