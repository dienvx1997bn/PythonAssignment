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

    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.category = kwargs["category"]
        self.productId = kwargs["productId"]
        self.workerId = kwargs["workerId"]
        self.status = kwargs["status"]
        
        #global variable
        self.car_type = None
        self.query_return = ""
        self.sedan_produced = 0
        self.sedan_fail = 0
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
