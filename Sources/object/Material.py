"""
For saving materials
"""
class Material:
    def __init__(self, **kwargs):
        self.material_id = kwargs["material_id"]
        self.name = kwargs["name"]
        self.cost = kwargs["cost"]
        self.vendor = kwargs["vendor"]
        self.quantity_per_unit = kwargs["quantity_per_unit"]


    def material_update(self):
        """TODO"""
        print("TODO")

    def material_commit(self):
        """TODO"""
        print("TODO")
