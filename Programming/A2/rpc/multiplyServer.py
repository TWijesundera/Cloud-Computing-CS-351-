"""RPC Server that multiplies 2 numbers and send answer to client"""
# Thisara Wijesundera
# CS 351
# RPC Assignment 2

import sys

from xmlrpc.server import SimpleXMLRPCServer

def mutiply_nums(num_1: int, num_2: int) -> int:
    """Mutiplies 2 numbers

        Args:
            num_1 (int): number given to the server
            num_2 (int): number given to the server

        Returns:
            Two given numbers multiplied together
    """
    return num_1 * num_2

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USAGE: python3 <port_num>\n")
        sys.exit()
    else:
        try:
            SERVER = SimpleXMLRPCServer(("0.0.0.0", int(sys.argv[1])))
            SERVER.register_introspection_functions()
            SERVER.register_function(mutiply_nums, "mul")

            print("Press CTRL+C to stop server\n")
            SERVER.serve_forever()

        except ValueError as err:
            print("Incorrect port number\nERROR: {}\n".format(err))

        except PermissionError as err:
            print("Port in use\nERROR: {}\n".format(err))

        except KeyboardInterrupt:
            print('\n')
