"""
Ref link: https://www.pythontutorial.net/python-concurrency/python-threading/
"""
import threading
import mysql.connector
import uuid

from object.Assembly import Assembly
from object.Worker import Worker
from object.Product import Product


worker_column_dict = {
    "id":0,
    "name":1,
    "specialization":2,
    "workingShift":3,
    "workingTime":4,
    "assemblyId":5
}

assembly_column_dict = {
    "id":0,
    "category":1,
    "productId":2,
    "workerId":3,
    "status":4
}

#init sql client
mydb = mysql.connector.connect(
    host = "sql12.freesqldatabase.com",
    user = "sql12532759",
    password = "L7cn3eESyz",
    database="sql12532759"
)
mycursor = mydb.cursor()


list_car_type = {"SUV"}

worker_list = []
assembly_list = []
product_list = []

def create_assembly(car_type):
    assembly = Assembly()
    # assembly.assembly_manufacturing(car_type)

def get_worker_available():
    sql = "SELECT * FROM workers where workingShift = 'ON_SHIFT'"
    mycursor.execute(sql)
    query_return = mycursor.fetchall()
    for worker_info in query_return:
        worker_list.append(Worker(id = worker_info[worker_column_dict["id"]],
                        name = worker_info[worker_column_dict["name"]],
                        specialization = worker_info[worker_column_dict["specialization"]],
                        workingShift = worker_info[worker_column_dict["workingShift"]],
                        workingTime = worker_info[worker_column_dict["workingTime"]],
                        assemblyId = worker_info[worker_column_dict["assemblyId"]]))

def get_assembly_available():
    sql = "SELECT * FROM assemblyLines where status ='STOPPED'"
    mycursor.execute(sql)
    query_return = mycursor.fetchall()
    # print(query_return)
    for assembly_info in query_return:
        assembly_list.append(Assembly(id = assembly_info[assembly_column_dict["id"]], 
                                        category = assembly_info[assembly_column_dict["category"]],
                                        productId = assembly_info[assembly_column_dict["productId"]],
                                        workerId = assembly_info[assembly_column_dict["workerId"]],
                                        status = assembly_info[assembly_column_dict["status"]]))
    # print(assembly_list)
    # for x in assembly_list:
    #     print(f"Assembly(x).id {x.id}")


def fetch_local_database():
    global worker_list 
    worker_list = []
    global assembly_list
    assembly_list = []

    get_worker_available()
    get_assembly_available()

def commit_to_database(worker, assembly):
    sql = f"UPDATE workers SET assemblyId = '{assembly.id}' WHERE id = '{worker.id}'"
    mycursor.execute(sql)
    mydb.commit()

    sql = f"UPDATE assemblyLines SET workerId = '{worker.id}', status = 'PREPARING' WHERE id = '{assembly.id}'"
    mycursor.execute(sql)
    mydb.commit()


def assign_worker_to_assembly():
    # process assembly
    threads = []

    #remember to add lock for threading

    for car_type in list_car_type:
        
        while(1):
            worker = None
            assembly = None
            # if worker and assembly are on free
            for x in worker_list:
                if x.specialization == car_type and x.workingShift == 'ON_SHIFT' and x.assemblyId == None:
                    worker = x
                    break
            if(worker == None):
                break
            
            for x in assembly_list:
                if x.category == car_type and x.workerId == None and x.status == 'STOPPED':
                    assembly = x
                    break
            if(assembly == None):
                break
            
            print(f"process {worker.id} {assembly.id}")
            assembly.workerId = 1
            worker.assemblyId = assembly.id

            commit_to_database(worker = worker, assembly = assembly)
            fetch_local_database()


        # if(car_type == worker.category for worker in worker_list) and (car_type == assembly.category for assembly in assembly_list):
    #         # creating threads: 
    #         t = threading.Thread(target=create_assembly, args=(car_type,))
    #         threads.append(t)
    #         t.start()
    
    # #wait to finish
    # for t in threads:
    #     t.join()


def main():
    fetch_local_database()
    assign_worker_to_assembly()

if __name__=='__main__':
    main()
    
