from sshy_app.tasks import TaskBase

class CLI:
    def __init__(self, host, username, password) -> None:
        TaskBase.TaskBase(self, host=host, username=username, password=password).runDefaults()
    
    def log(self, message):
        print(message)