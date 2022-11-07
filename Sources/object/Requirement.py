"""
For saving requirements
"""
class Requirement:
    def __init__(self, **kwargs):
        self.assembly_id = kwargs["id"]
        self.category = kwargs["category"]
        self.name = kwargs["name"]
        self.material = kwargs["material"]
        self.time_needed = kwargs["time_needed"]


    def requirement_update(self):
        """TODO"""
        print("TODO")

    def requirement_commit(self):
        """TODO"""
        print("TODO")
