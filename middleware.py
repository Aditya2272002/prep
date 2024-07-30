from flask import g, request


# def check_token():
#     if request.path.startswith("/test") and request.method == "POST":
#         print("ARGS", request.args)
#         id = request.view_args.get('id')
#         if id == "1":
#             g.allowed = "yes"
#         else:
#             g.allowed = "no"


def check_token_decorator(f):
    def wrapper(*args, **kwargs):
        id = request.view_args.get('id')
        if id == "1":
            g.allowed = "yes"
        else:
            g.allowed = "no"
        return f(*args, **kwargs)
    wrapper.__name__= f.__name__
    return wrapper
