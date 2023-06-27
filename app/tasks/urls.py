from .controller import TasksManager, TaskManager, Filter


def define_urls(api):
    api.add_resource(TasksManager, '/tasks/')
    api.add_resource(Filter, '/tasks/filter')
    api.add_resource(TaskManager, '/task/<int:id>')
