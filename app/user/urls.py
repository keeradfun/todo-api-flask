from .controller import UserRegister,UserLogin,UserManager

def define_urls(api):
    api.add_resource(UserRegister, '/user/register')
    api.add_resource(UserLogin,"/user/login")
    api.add_resource(UserManager,"/user/<int:id>")