"""RPC server that adds 2 numbers and send content to client"""
# Thisara Wijesundera
# CS 351
# RPC Assignment 2

import sys

from xmlrpc.server import SimpleXMLRPCServer

def add_nums(num_1: int, num_2: int) -> int:
    """Adds numbers that are given

        Args:
            num_1 (int): number given to the server
            num_2 (int): number given to the server

        Returns:
            Two given numbers added together
    """
    return num_1 + num_2

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USAGE: python3 <port_num>")
        sys.exit()
    else:
        try:
            SERVER = SimpleXMLRPCServer(("0.0.0.0", int(sys.argv[1])))
            SERVER.register_introspection_functions()

            SERVER.register_function(add_nums, "add")

            print("Press CTRL+C to stop server\n")
            SERVER.serve_forever()

        except ValueError as err:
            print("Incorrect port number\nERROR: {}\n".format(err))

        except PermissionError as err:
            print("Port in use\nERROR: {}\n".format(err))

        except KeyboardInterrupt:
            print('\n')
