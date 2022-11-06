"""
Ref link: https://www.pythontutorial.net/python-concurrency/python-threading/
"""
import threading
import mysql.connector
import logging

from object.Assembly import Assembly
from object.Worker import Worker


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


list_car_type = {"SUV", "SEDAN", "MINIVAN"}

worker_available_list = []
assembly_available_list = []

assembly_working_list = []

def get_worker_available():
    sql = "SELECT * FROM workers where workingShift = 'ON_SHIFT'"
    mycursor.execute(sql)
    query_return = mycursor.fetchall()
    for worker_info in query_return:
        worker_available_list.append(Worker(id = worker_info[worker_column_dict["id"]],
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
        assembly_available_list.append(Assembly(id = assembly_info[assembly_column_dict["id"]], 
                                        category = assembly_info[assembly_column_dict["category"]],
                                        productId = assembly_info[assembly_column_dict["productId"]],
                                        workerId = assembly_info[assembly_column_dict["workerId"]],
                                        status = assembly_info[assembly_column_dict["status"]]))
    # print(assembly_available_list)
    # for x in assembly_available_list:
    #     print(f"Assembly(x).id {x.id}")


def fetch_local_database():
    global worker_available_list 
    worker_available_list = []
    global assembly_available_list
    assembly_available_list = []

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
    
    for car_type in list_car_type:
        
        while(1):
            worker = None
            assembly = None
            # if worker and assembly are on free
            for x in worker_available_list:
                if x.specialization == car_type and x.workingShift == 'ON_SHIFT' and x.assemblyId == None:
                    worker = x
                    break
            if(worker == None):
                break
            
            for x in assembly_available_list:
                if x.category == car_type and x.workerId == None and x.status == 'STOPPED':
                    assembly = x
                    break
            if(assembly == None):
                break
            
            print(f"process {worker.id} {assembly.id}")
            assembly.workerId = 1
            worker.assemblyId = assembly.id

            # update db
            commit_to_database(worker = worker, assembly = assembly)
            fetch_local_database()


def get_assembly_working():
    sql = "SELECT * FROM assemblyLines where status ='PREPARING'"
    mycursor.execute(sql)
    query_return = mycursor.fetchall()
    # print(query_return)
    for assembly_info in query_return:
        assembly_working_list.append(Assembly(id = assembly_info[assembly_column_dict["id"]], 
                                        category = assembly_info[assembly_column_dict["category"]],
                                        productId = assembly_info[assembly_column_dict["productId"]],
                                        workerId = assembly_info[assembly_column_dict["workerId"]],
                                        status = assembly_info[assembly_column_dict["status"]]))

def assembly_running(assembly):
    assembly.assembly_manufacturing()

def process_assembly():
    threads = []
    for assembly in assembly_working_list:
        # creating threads: 
        t = threading.Thread(target=assembly_running, args=(assembly,))
        threads.append(t)
        t.start()
        logging.info(f"assembly {assembly.id} start running")

        sql = f"UPDATE assemblyLines SET  status = 'RUNNING' WHERE id = '{assembly.id}'"
        mycursor.execute(sql)
        mydb.commit()

    #wait to finish
    for t in threads:
        t.join()


def main():
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
    logging.info("START")

    fetch_local_database()
    assign_worker_to_assembly()

    get_assembly_working()
    process_assembly()

if __name__=='__main__':
    main()
    
