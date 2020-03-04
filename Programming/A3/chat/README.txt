Server
[ec2-user@ip-172-31-47-168 ~]$ python3 chatServer.py                                                              [0/1932]
Chat server started on port 9009                                                                                          
Client (18.222.165.98, 49654) connected
Client (18.222.248.233, 53584) connected      


Client 1
[ec2-user@ip-172-31-40-147 ~]$ python3 chatClient.py 3.21.76.176 9009
Connected to remote host. You can start sending messages
[Me]: [18.222.248.233:53584] entered our chatting room
[Me]: hello
[ ('18.222.248.233', 53584) ] how are you?
[Me]: 


Client 2
[ec2-user@ip-172-31-38-57 ~]$ python3 chatClient.py 3.21.76.176 9009
Connected to remote host. You can start sending messages
[ ('18.222.165.98', 49654) ] hello
[Me]: how are you?
[Me]: 

