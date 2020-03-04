Server

[ec2-user@ip-172-31-47-168 ~]$ python3 Server.py 
Chat server started on port 9009

Client ('18.222.165.98', 49658) connected

Client ('18.222.248.233', 53588) connected


Client X

ec2-user@ip-172-31-40-147 ~]$ python3  chatClient.py 3.21.76.176 9009                                                    
Connected to remote host. You can start sending messages                                                                  
[Me]: You are an X player                                                                                                 
[Me]: ('18.222.248.233', 53588) entered the chat room                                                                     
[Me]: [server]:Let's begin tic tac toe                                                                                    
ROW                                                          
  9  -  -  -  -  -  -  -  -  -                        
  8  -  -  -  -  -  -  -  -  -                               
  7  -  -  -  -  -  -  -  -  -                               
  6  -  -  -  -  -  -  -  -  -                               
  5  -  -  -  -  -  -  -  -  -                               
  4  -  -  -  -  -  -  -  -  -      
  3  -  -  -  -  -  -  -  -  -                                                                                            
  2  -  -  -  -  -  -  -  -  -                                                                                            
  1  -  -  -  -  -  -  -  -  -    
COL  1  2  3  4  5  6  7  8  9              
[server]: It's your turn X                                   
[('18.222.248.233', 53588)]: hello             
[Me]: hi                                                     
[Me]: (1,1)                                                  
[Me]:                                                                                                                     
ROW                                                          
  9  -  -  -  -  -  -  -  -  -                                                                                            
  8  -  -  -  -  -  -  -  -  -                              
  7  -  -  -  -  -  -  -  -  - 
  6  -  -  -  -  -  -  -  -  - 
  5  -  -  -  -  -  -  -  -  - 
  4  -  -  -  -  -  -  -  -  - 
  3  -  -  -  -  -  -  -  -  - 
  2  -  -  -  -  -  -  -  -  - 
  1  X  -  -  -  -  -  -  -  - 
COL  1  2  3  4  5  6  7  8  9 
[Me]: It's your turn O
[Me]: ERROR: There is already a symbol in that position
[('18.222.248.233', 53588)]: (1,1)
[Me]: ERROR: Unable to access that location
[('18.222.248.233', 53588)]: (12,1)
[Me]: 
ROW
  9  O  -  -  -  -  -  -  -  - 
  8  -  -  -  -  -  -  -  -  - 
  7  -  -  -  -  -  -  -  -  - 
  6  -  -  -  -  -  -  -  -  - 
  5  -  -  -  -  -  -  -  -  - 
  4  -  -  -  -  -  -  -  -  - 
  3  -  -  -  -  -  -  -  -  - 
  2  -  -  -  -  -  -  -  -  - 
  1  X  -  -  -  -  -  -  -  - 
COL  1  2  3  4  5  6  7  8  9 
[Me]: It's your turn X
[Me]: (1,2)
[Me]: 
ROW
  9  O  -  -  -  -  -  -  -  - 
  8  -  -  -  -  -  -  -  -  - 
  7  -  -  -  -  -  -  -  -  - 
  6  -  -  -  -  -  -  -  -  - 
  5  -  -  -  -  -  -  -  -  - 
  4  -  -  -  -  -  -  -  -  - 
  3  -  -  -  -  -  -  -  -  - 
  2  -  -  -  -  -  -  -  -  - 
  1  X  X  -  -  -  -  -  -  - 
COL  1  2  3  4  5  6  7  8  9 
[Me]: It's your turn O
[Me]: 
ROW
  9  O  -  -  -  -  -  -  -  - 
  8  -  O  -  -  -  -  -  -  - 
  7  -  -  -  -  -  -  -  -  - 
  6  -  -  -  -  -  -  -  -  - 
  5  -  -  -  -  -  -  -  -  - 
  4  -  -  -  -  -  -  -  -  - 
  3  -  -  -  -  -  -  -  -  - 
  2  -  -  -  -  -  -  -  -  - 
  1  X  X  -  -  -  -  -  -  - 
COL  1  2  3  4  5  6  7  8  9 
[Me]: It's your turn X
[Me]: (1,3)
[Me]: 
ROW
  9  O  -  -  -  -  -  -  -  - 
  8  -  O  -  -  -  -  -  -  - 
  7  -  -  -  -  -  -  -  -  - 
  6  -  -  -  -  -  -  -  -  - 
  5  -  -  -  -  -  -  -  -  - 
  4  -  -  -  -  -  -  -  -  - 
  3  -  -  -  -  -  -  -  -  - 
  2  -  -  -  -  -  -  -  -  - 
  1  X  X  X  -  -  -  -  -  - 
COL  1  2  3  4  5  6  7  8  9 
[Me]: The winner is X
Ending server now
[Me]: 
Disconnected from chat server

Client O

[ec2-user@ip-172-31-38-57 ~]$ python3 chatClient.py 3.21.76.176 9009                                             [60/1905]
Connected to remote host. You can start sending messages                                                                  
[Me]: You are an O player                                                                                                 
[Me]: [server]:Let's begin tic tac toe                                                                                    
ROW                                                                                                                       
  9  -  -  -  -  -  -  -  -  -                                                                                            
  8  -  -  -  -  -  -  -  -  -                                                                                            
  7  -  -  -  -  -  -  -  -  -                                                                                            
  6  -  -  -  -  -  -  -  -  -                                                                                            
  5  -  -  -  -  -  -  -  -  -                                                                                            
  4  -  -  -  -  -  -  -  -  -                                                                                            
  3  -  -  -  -  -  -  -  -  -                                                                                            
  2  -  -  -  -  -  -  -  -  -                                                                                            
  1  -  -  -  -  -  -  -  -  -                                                                                            
COL  1  2  3  4  5  6  7  8  9                               
[Me]: hello                                                  
[('18.222.165.98', 49658)]: hi                                                                                            
[Me]:                                                                                                                     
ROW                                                          
  9  -  -  -  -  -  -  -  -  -                               
  8  -  -  -  -  -  -  -  -  -     
  7  -  -  -  -  -  -  -  -  -                                                                                            
  6  -  -  -  -  -  -  -  -  -                                                                                            
  5  -  -  -  -  -  -  -  -  -                          
  4  -  -  -  -  -  -  -  -  -    
  3  -  -  -  -  -  -  -  -  -                               
  2  -  -  -  -  -  -  -  -  -                               
  1  X  -  -  -  -  -  -  -  -                               
COL  1  2  3  4  5  6  7  8  9     
[Me]: It's your turn O                                                                                                    
[Me]: (1,1)                                                                                                               
[Me]: ERROR: There is already a symbol in that position
[Me]: (12,1)
[Me]: ERROR: Unable to access that location
[Me]: (9,1)
[Me]: 
ROW
  9  O  -  -  -  -  -  -  -  - 
  8  -  -  -  -  -  -  -  -  - 
  7  -  -  -  -  -  -  -  -  - 
  6  -  -  -  -  -  -  -  -  - 
  5  -  -  -  -  -  -  -  -  - 
  4  -  -  -  -  -  -  -  -  - 
  3  -  -  -  -  -  -  -  -  - 
  2  -  -  -  -  -  -  -  -  - 
  1  X  -  -  -  -  -  -  -  - 
COL  1  2  3  4  5  6  7  8  9 
[Me]: It's your turn X
[Me]: 
ROW
  9  O  -  -  -  -  -  -  -  - 
  8  -  -  -  -  -  -  -  -  - 
  7  -  -  -  -  -  -  -  -  - 
  6  -  -  -  -  -  -  -  -  - 
  5  -  -  -  -  -  -  -  -  - 
  4  -  -  -  -  -  -  -  -  - 
  3  -  -  -  -  -  -  -  -  - 
  2  -  -  -  -  -  -  -  -  - 
  1  X  X  -  -  -  -  -  -  - 
COL  1  2  3  4  5  6  7  8  9 
[Me]: It's your turn O
[Me]: (8,2)
[Me]: 
ROW
  9  O  -  -  -  -  -  -  -  - 
  8  -  O  -  -  -  -  -  -  - 
  7  -  -  -  -  -  -  -  -  - 
  6  -  -  -  -  -  -  -  -  - 
  5  -  -  -  -  -  -  -  -  - 
  4  -  -  -  -  -  -  -  -  - 
  3  -  -  -  -  -  -  -  -  - 
  2  -  -  -  -  -  -  -  -  - 
  1  X  X  -  -  -  -  -  -  - 
COL  1  2  3  4  5  6  7  8  9 
[Me]: It's your turn X
[Me]: 
ROW
  9  O  -  -  -  -  -  -  -  - 
  8  -  O  -  -  -  -  -  -  - 
  7  -  -  -  -  -  -  -  -  - 
  6  -  -  -  -  -  -  -  -  - 
  5  -  -  -  -  -  -  -  -  - 
  4  -  -  -  -  -  -  -  -  - 
  3  -  -  -  -  -  -  -  -  - 
  2  -  -  -  -  -  -  -  -  - 
  1  X  X  X  -  -  -  -  -  - 
COL  1  2  3  4  5  6  7  8  9 
[Me]: The winner is X
Ending server now
[Me]: 
Disconnected from chat server
