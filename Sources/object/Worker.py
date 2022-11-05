import mysql.connector

class Worker:
    def __init__(self, id, name, on_working_shift, workingTime, specialization, assemblyId):
        self.id = id,
        self.name = name
        self.on_working_shift = on_working_shift
        self.workingTime = workingTime
        self.specialization = specialization
        self.assemblyId = assemblyId

        #init sql client
        self.mydb = mysql.connector.connect(
            host = "sql12.freesqldatabase.com",
            user = "sql12532759",
            password = "L7cn3eESyz",
            database="sql12532759"
        )
        self.mycursor = self.mydb.cursor()

    
    
    

