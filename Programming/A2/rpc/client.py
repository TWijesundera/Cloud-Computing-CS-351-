"""Client code for RPC assginment

    Args:
        ADD_HOST (str): Public IP address or DNS of addition server
        ADD_PORT (str): Port for connection to addition server
        MUL_HOST (str): Public IP address or DNS of multiplication server
        MUL_PORT (str): Port for connection to multiplication server

    Usage:
        python3 client.py <add_server_ip> <add_server_port>
        <multiplication_server_ip> <multiplication_server_port> <calcultor.txt>

    Notes:
        Must be run using python3
"""
# Thisara Wijesundera
# CS-351
# RPC Assignment 2

import xmlrpc.client
import sys

from typing import List

def read_file(input_file: str) -> List[tuple]:
    """Read the input file (calculator.txt)

        Args:
            input_file (str): The file path as a string

        Returns:
            List of tuples detailing operations for each RPC server
    """

    output = []

    try:
        with open(input_file) as file:
            """
                For every line remove the operation and convert
                    the numbers into and integer list
                Append it to list for returning
            """
            for line in file:
                splited = line.split()
                output.append((splited[0], [int(x) for x in splited[1:]]))
        return output
    except FileNotFoundError as err:
        print(f"ERROR: {err}\n")
        sys.exit()
    
    except IndexError as err:
        print(f"Operations file is empty\nERROR: {err}")
        sys.exit()


if __name__ == "__main__":
    if len(sys.argv) != 6:
        msg = ('USAGE: python3 <add_hostname/ip> <add_port>'
        ' <multiply_hostname/ip> <multiply_port> <operations_file>\n')
        print(msg)
        sys.exit()
    else:
        try:
            ADD_HOST = sys.argv[1]
            ADD_PORT = sys.argv[2]

            MUL_HOST = sys.argv[3]
            MUL_PORT = sys.argv[4]
            operations = read_file(sys.argv[5])

            ADD_CONN = xmlrpc.client.ServerProxy(f'http://{ADD_HOST}:{ADD_PORT}')
            MUL_CONN = xmlrpc.client.ServerProxy(f'http://{MUL_HOST}:{MUL_PORT}')

            for opr in operations:
                num_1 = opr[1][0]
                num_2 = opr[1][1]

                if opr[0] == 'A':
                    print(f"{num_1} + {num_2} = {ADD_CONN.add(num_1, num_2)}")
                elif opr[0] == 'M':
                    print(f"{num_1} * {num_2} = {MUL_CONN.mul(num_1, num_2)}")
                else:
                    print("Unsupported operand!\n")

        except ConnectionRefusedError as err:
            msg = ("The connection was refused."
                   "Check outbound rules of sec group and port number")
            print(f"{msg}\nERROR: {err}\n")

        except OSError as err:
            print(f"Hostname or port invalid\nERROR: {err}\n")

        except KeyboardInterrupt:
            print("\n")
