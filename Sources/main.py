"""
Main function, running this file
"""
import threading
import logging
import mysql.connector

from object.Assembly import Assembly
from object.Worker import Worker


ASSEMBLY_COLUMN_DICT = {
    "id":0,
    "category":1,
    "productId":2,
    "workerId":3,
    "status":4
}

#init sql client
mydb = mysql.connector.connect(
    host="sql12.freesqldatabase.com",
    user="sql12532759",
    password="L7cn3eESyz",
    database="sql12532759"
)
mycursor = mydb.cursor()


list_car_type = {"SUV", "SEDAN", "MINIVAN"}

worker_available_list = []
assembly_available_list = []

assembly_working_list = []

def get_worker_available():
    """query workers are ready to work"""
    sql = "SELECT * FROM workers where workingShift = 'ON_SHIFT'"
    mycursor.execute(sql)
    query_return = mycursor.fetchall()
    for worker_info in query_return:
        worker_available_list.append(Worker(worker_id=worker_info[0],
                                            name=worker_info[1],
                                            specialization=worker_info[2],
                                            working_shift=worker_info[3],
                                            working_time=worker_info[4],
                                            assembly_id=worker_info[5]))

def get_assembly_available():
    """query assembly lines are ready to work"""
    sql = "SELECT * FROM assemblyLines where status ='STOPPED'"
    mycursor.execute(sql)
    query_return = mycursor.fetchall()
    # print(query_return)
    for assembly_info in query_return:
        global assembly_available_list
        assembly_available_list.append(Assembly(assembly_id=assembly_info[0],
                                                category=assembly_info[1],
                                                product_id=assembly_info[2],
                                                worker_id=assembly_info[3],
                                                status=assembly_info[4]))


def fetch_local_database():
    """get all workers and assemblys status"""
    global worker_available_list
    worker_available_list = []
    global assembly_available_list
    assembly_available_list = []
    get_worker_available()
    get_assembly_available()


def commit_assignment_to_database(worker, assembly):
    """update assignment to database"""
    sql = f"UPDATE workers \
            SET assemblyId = '{assembly.assembly_id}' \
            WHERE id = '{worker.worker_id}'"
    mycursor.execute(sql)
    mydb.commit()
    sql = f"UPDATE assemblyLines SET \
            workerId = '{worker.worker_id}', status = 'PREPARING' \
            WHERE id = '{assembly.assembly_id}'"
    mycursor.execute(sql)
    mydb.commit()


def assign_worker_to_assembly():
    """map worker to assembly"""
    for car_type in list_car_type:
        while True:
            worker = None
            assembly = None
            # if worker and assembly are on free
            for worker_available in worker_available_list:
                if (worker_available.specialization == car_type
                        and worker_available.working_shift == 'ON_SHIFT'
                        and worker_available.assembly_id is None):
                    worker = worker_available
                    break
            if worker is None:
                break
            for assembly_available in assembly_available_list:
                if (assembly_available.category == car_type
                        and assembly_available.worker_id is None
                        and assembly_available.status == 'STOPPED'):
                    assembly = assembly_available
                    break
            if assembly is None:
                break
            print(f"process {worker.worker_id} {assembly.assembly_id}")
            assembly.worker_id = 1
            worker.assembly_id = assembly.assembly_id
            # update db
            commit_assignment_to_database(worker=worker, assembly=assembly)
            fetch_local_database()


def get_assembly_working():
    """get the assembly line are ready to process product"""
    sql = "SELECT * FROM assemblyLines where status ='PREPARING'"
    mycursor.execute(sql)
    query_return = mycursor.fetchall()
    # print(query_return)
    for assembly_info in query_return:
        assembly_working_list.append(Assembly(assembly_id=assembly_info[0],
                                              category=assembly_info[1],
                                              product_id=assembly_info[2],
                                              worker_id=assembly_info[3],
                                              status=assembly_info[4]))

def assembly_running(assembly):
    """assembly on running state"""
    assembly.assembly_manufacturing()

def process_assembly():
    """start processing"""
    threads = []
    for assembly in assembly_working_list:
        # creating threads:
        thread = threading.Thread(target=assembly_running, args=(assembly,))
        threads.append(thread)
        thread.start()
        logging.info("assembly %s start running", assembly.assembly_id)

        sql = f"UPDATE assemblyLines SET  status = 'RUNNING' WHERE id = '{assembly.assembly_id}'"
        mycursor.execute(sql)
        mydb.commit()
    #wait to finish
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
    logging.info("START")
    fetch_local_database()
    assign_worker_to_assembly()
    get_assembly_working()
    process_assembly()
