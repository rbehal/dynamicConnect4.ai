# Modified Dynamic Connect-4 - Rahul Behal (260773885)

The following code serves to be an implementation of the alphabeta pruning and minimax algorithms to play a modified version of the game Connect-4. The rules and guidelines for the game can be found in the assignment specifications for ECSE 526: Artificial Intelligence - Assignment #1. 
<br />
## Game Server
The code is meant to be run on this [game server](http://www.cim.mcgill.ca/~jer/courses/ai/assignments/gameserver.tgz).

<br />

In the gserver directory there is a file entitled DC4Server.jar. The default port running is 12345, but this can be changed in the Java file. In order to run the server, navigate to the gserver directory and run the following command. 

~~~
java -jar DC4Server.jar
~~~

## Client
In order to have the client play the game, launch the main.py file with the command below. There are four required arguments for this file outlined below. Additionally, ensure that Game.py, Player.py, init.txt, algorithms.py, and main.py are all in the same directory. Navigate to that directory and run the following command. 

~~~
python main.py -c <colour> -p <port> <serverIP> <gameID>
~~~

An explanation of the parameters is in the following table: 

| Parameter | Value                                                         |
|-----------|---------------------------------------------------------------|
| colour    | Must be "white" or "black" indicating the role of the player. |
| port      | Port of the server. Default Java file uses 12345.             |
| serverIP  | IP of the server. For this class: 156TRLinux.ece.mcgill.ca    |
| gameID    | ID of the game to create or join.                             |

## Initial Gamestate
The initial gamestate is defined in the init.txt file. This file must be modified to change the initial gamestate. The format is as follows:

~~~
 ,X,X, ,O, , 
 , , , , , ,X
O, , , , , , 
O, , , , , ,O
 , , , , , ,O
X, , , , , , 
 , ,O, ,X,X, 
~~~

There should be 7 rows of 13 characters (6 of the commas) with a newline charachter at the end of every row *except* the last one. 
