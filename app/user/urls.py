from .controller import UsersManager, LoginManager, UserManager


def define_urls(api):
    api.add_resource(UsersManager, '/users/')
    api.add_resource(LoginManager, '/users/login')
    api.add_resource(UserManager, '/user/<int:id>')
