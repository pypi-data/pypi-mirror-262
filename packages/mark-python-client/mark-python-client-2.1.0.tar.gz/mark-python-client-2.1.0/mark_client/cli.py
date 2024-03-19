"""
Cli for mark_python_client
"""
import inspect
import ast
from mark_client.ncurse import MenuCurses


def run_command(func, parameters):
    """
    convert the parameters given in str 
    to correct format and launch the methode
    """
    parameters = list(parameters)
    args_info = inspect.getfullargspec(func)
    parameters[:0] = [None]
    args = ()
    for a, parameter in  zip(args_info.args, parameters):
        if a == 'self':
            continue
        annotation = args_info.annotations.get(a, "str")
        if annotation == float:
            args += (float(parameter),)
        elif annotation == int:
            args += (int(parameter),)
        elif annotation == dict:
            args += (ast.literal_eval(parameter),)
        else:
            args += (parameter,)
    return str(func(*args))

def interactif_main(mark_client):
    """
    interactif view of the mark_client
    """
    # get the functions to interact with
    functions_list = [getattr(mark_client, func)
                      for func in dir(mark_client)
                      if not func.startswith("_") and callable(getattr(mark_client, func))]
    # set up the menu
    menu = {
        "Title":"mark_client",
        "Desc":"",
        "option":[
            {
                "name":"toggle logging_level",
                "info":{
                    "type":"function",
                    "function":lambda :f"verbse set to {mark_client.toggle_logging_level()}"
                }
            },
            {
            "name":"set server",
            "info":{
                 "type":"function",
                 "function":lambda url :f"{mark_client.set_server_url(url) or 'set'}",
                 "params":["server"]
                }
            }
        ] + [
                {
                "name":f.__name__ , 
                "info":{
                    "type":"function",
                    "function":lambda *arg, function=f:run_command(function, arg),
                    "params":
                        inspect.getfullargspec(f).args[1:]
                            if len(inspect.getfullargspec(f).args) > 1 else []
                    }
                } for f in functions_list
            ]
    }
    # init the menu
    interactif_menu = MenuCurses()
    interactif_menu.run(menu)

def static_main(command_name, parameters, mark_client):
    """
    interactif view of the client
    """
    found = False
    for function in dir(mark_client):
        if function == command_name:
            found = True
            if parameters:
                print(run_command(getattr(mark_client, function), parameters))
            else:
                print(getattr(mark_client, function)())
            break
    if not found:
        print("please provide command")
