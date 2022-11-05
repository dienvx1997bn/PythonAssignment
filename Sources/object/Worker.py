import mysql.connector

class Worker:
    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.workingShift = kwargs["workingShift"]
        self.workingTime = kwargs["workingTime"]
        self.specialization = kwargs["specialization"]
        self.assemblyId = kwargs["assemblyId"]
        


