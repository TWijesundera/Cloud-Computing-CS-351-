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
            for line in file:
                splited = line.split()
                output.append((splited[0], [int(x) for x in splited[1:]]))
        return output
    except FileNotFoundError as err:
        print("ERROR: {}\n".format(err))
        sys.exit()


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Please provide all arguments\n")
        sys.exit()
    else:
        ADD_HOST = sys.argv[1]
        ADD_PORT = sys.argv[2]

        MUL_HOST = sys.argv[3]
        MUL_PORT = sys.argv[4]
        operations = read_file(sys.argv[5])

        try:
            ADD_CONN = xmlrpc.client.ServerProxy('http://{}:{}'.format(ADD_HOST, ADD_PORT))
            MUL_CONN = xmlrpc.client.ServerProxy('http://{}:{}'.format(MUL_HOST, MUL_PORT))

            for opr in operations:
                num_1 = opr[1][0]
                num_2 = opr[1][1]

                if opr[0] == 'A':
                    print("{} + {} = {}"
                          .format(num_1, num_2, ADD_CONN.add(num_1, num_2)))
                elif opr[0] == 'M':
                    print("{} * {} = {}"
                          .format(num_1, num_2, MUL_CONN.mul(num_1, num_2)))
                else:
                    print("Unsupported operand!\n")

        except ConnectionRefusedError as err:
            msg = ("The connection was refused."
                   "Check outbound rules of sec group and port number")
            print("{}\nERROR: {}\n".format(msg, err))

        except OSError as err:
            print("Hostname or port invalid\nERROR: {}\n".format(err))

        except KeyboardInterrupt:
            print("\n")
