"""
Ref link: https://www.pythontutorial.net/python-concurrency/python-threading/
"""

import json
import threading
import time
import timeit

#global variable
sedan_produced = 0
sedan_completed = False

# Creating lock for threads
lock_sedan = threading.Lock()

def sedan_thread_running(thread_id, sedan_db, lock_sedan):

    while(True):
        lock_sedan.acquire()
        if (sedan_db['components']['wheel'] > 4) and (sedan_db['components']['chassis'] > 0) and (sedan_db['components']['engine'] > 0):
            sedan_db['components']['wheel'] -= 4
            sedan_db['components']['chassis'] -=1
            sedan_db['components']['engine'] -= 1
        else:
            print("thread_id {0} not engough components".format(thread_id))
            lock_sedan.release()
            break
        lock_sedan.release()

        time.sleep(1)
        global sedan_produced
        sedan_produced += 1
        print("thread_id {0} sedan_produced {1}".format(thread_id, sedan_produced))


def sedan_manufacturing(database):
    for type in database['materials']:
        if type['car_type'] == "SEDAN":
            sedan_db = type.copy()
    print('{}'.format(sedan_db))
    
    # start production line
    start_time = time.perf_counter()
    num = int(sedan_db['max_production_line'])
    threads = []

    for i in range(num):
        # creating threads: 
        t = threading.Thread(target=sedan_thread_running, args=(i, sedan_db, lock_sedan,))
        threads.append(t)
        t.start()
    
    #wait to finish
    for t in threads:
        t.join()
    end_time = time.perf_counter()
    print(f'It took {end_time- start_time: f} second(s) to complete.')


def suv_manufacturing(database):
    pass


def main():
    #load database
    with open('database/materials.json') as f:
        database = json.load(f)
    # print(database)
    #print("{}".format(database['materials'][0]))

    sedan_manufacturing(database)



if __name__=='__main__':
    main()
    
