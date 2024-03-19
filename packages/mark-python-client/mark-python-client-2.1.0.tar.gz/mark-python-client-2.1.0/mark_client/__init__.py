import argparse
import logging
from .mark_python_client import MarkClient
from .cli import interactif_main, static_main

name = "mark_python_client"

def main():
    '''
    entry point for the cli
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--set-server", action="store", required=True)
    parser.add_argument("-c","--command", required=False, help="")
    parser.add_argument("-p","--parameters",action="extend", required=False, nargs="+")
    parser.add_argument("-I", "--interactif", action="store_true")
    parser.add_argument("-l", "--logging_level", action="store")
    parser.add_argument("--proxy", action="store", required=False)
    parser.add_argument("-i", "--client_id", action="store", required=False, type=int, default=1234)
    arguments = parser.parse_args()
    if arguments.logging_level == "none":
        lvl = logging.NOTSET
    elif arguments.logging_level == "info":
        lvl = logging.INFO
    else:
        lvl = logging.DEBUG
    client = MarkClient(server_url=arguments.set_server,
                        logging_level=lvl,
                        proxy=arguments.proxy,
                        client_id=arguments.client_id)
    if arguments.interactif:
        interactif_main(client)
    elif arguments.command:
        static_main(arguments.command, arguments.parameters, client)
    else:
        print("please provide either a command (-c) or set the interactif flag (-I)")
