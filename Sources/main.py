"""
Ref link: https://www.pythontutorial.net/python-concurrency/python-threading/
"""
import threading
import mysql.connector

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
    "hasWorker":3,
    "hasProduct":4,
    "status":5
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

def create_assembly(car_type):
    assembly = Assembly()
    # assembly.assembly_manufacturing(car_type)

def get_worker_available():
    sql = "SELECT * FROM workers where workingShift = 'ON_SHIFT'"
    mycursor.execute(sql)
    query_return = mycursor.fetchall()
    for worker_info in query_return:
        worker_list.append(Worker(id=worker_info[worker_column_dict["id"]],
                        name=worker_info[worker_column_dict["name"]],
                        specialization=worker_info[worker_column_dict["specialization"]],
                        on_working_shift=worker_info[worker_column_dict["id"]],
                        workingTime=worker_info[worker_column_dict["workingTime"]],
                        assemblyId=worker_info[worker_column_dict["assemblyId"]])
                        )

def get_assembly_available():
    sql = "SELECT * FROM assemblyLines where status ='STOPPED'"
    mycursor.execute(sql)
    query_return = mycursor.fetchall()
    print(query_return)
    for assembly_info in query_return:
        assembly_list.append(Assembly(id = assembly_info[assembly_column_dict["id"]], 
                                        category = assembly_info[assembly_column_dict["category"]],
                                        productId = assembly_info[assembly_column_dict["productId"]],
                                        hasWorker = assembly_info[assembly_column_dict["hasWorker"]],
                                        hasProduct = assembly_info[assembly_column_dict["hasProduct"]],
                                        status = assembly_info[assembly_column_dict["status"]],))
    print(assembly_list)

def assign_worker_to_assembly():
    pass


def main():
    #get worker available
    # get_worker_available()

    #assign worker to assembly
    get_assembly_available()

    #create assembly
    # threads = []
    # for car_type in list_car_type:
    #     # creating threads: 
    #     t = threading.Thread(target=create_assembly, args=(car_type,))
    #     threads.append(t)
    #     t.start()
    
    # #wait to finish
    # for t in threads:
    #     t.join()

if __name__=='__main__':
    main()
    
