from .controller import UserRegister,UserLogin

def define_urls(api):
    api.add_resource(UserRegister, '/user/register')
    api.add_resource(UserLogin,"/user/login")