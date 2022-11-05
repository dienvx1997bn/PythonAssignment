
column_dict = {
    "id":0,
    "name":1,
    "materials":2,
    "category":3,
    "cost":4,
    "produceTime":5,
    "price":6,
    "progress":7,
    "qcStatus":8,
    "assemblyId":9,
    "workerId":10
}

class Product:
    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.materials = kwargs["materials"]
        self.category = kwargs["category"]
        self.cost = kwargs["cost"]
        self.produceTime = kwargs["produceTime"]
        self.price = kwargs["price"]
        self.progress = kwargs["progress"]
        self.qcStatus = kwargs["qcStatus"]
        self.assemblyId = kwargs["assemblyId"]
        self.workerId = kwargs["workerId"]

