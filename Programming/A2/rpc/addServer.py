"""RPC server that adds 2 numbers and send content to client"""
# Thisara Wijesundera
# CS 351
# RPC Assignment 2

def addNumbers(n1: int, n2: int) -> int:
    """Adds numbers that are given

        Args:
            n1 (int): number given to server
            n2 (int): number given to server
        
        Returns:
            Two given numbers added together
    """
    return n1 + n2

if __name__ == "__main__":
    """Do rpc stuff"""
    pass