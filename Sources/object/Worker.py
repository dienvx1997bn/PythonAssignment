"""
for saving worker state
"""
class Worker:
    def __init__(self, **kwargs):
        self.worker_id = kwargs["worker_id"]
        self.name = kwargs["name"]
        self.working_shift = kwargs["working_shift"]
        self.working_time = kwargs["working_time"]
        self.specialization = kwargs["specialization"]
        self.assembly_id = kwargs["assembly_id"]


    def worker_relax(self):
        """TODO"""
        print("TODO")

    def worker_assignment(self):
        """TODO"""
        print("TODO")
