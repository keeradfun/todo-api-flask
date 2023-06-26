from .controller import TaskCreate, TaskFindById, AllTasks, UpdateTask, DeleteTask


def define_urls(api):
    api.add_resource(TaskCreate, '/task/create')
    api.add_resource(TaskFindById, '/task/find/<int:id>')
    api.add_resource(AllTasks, '/task/find-all')
    api.add_resource(UpdateTask, '/task/update/<int:id>')
    api.add_resource(DeleteTask, '/task/delete/<int:id>')
