from .controller import UserRegister, UserLogin, UserManager, PasswordUpdate


def define_urls(api):
    api.add_resource(UserRegister, '/user/register')
    api.add_resource(UserLogin, "/user/login")
    api.add_resource(UserManager, "/user/profile")
    api.add_resource(PasswordUpdate, "/user/new-password")
