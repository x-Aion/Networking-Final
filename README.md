# Networking-Final
This is the final project for our COMP-3670 class

Include in the git  is a CLI and a GUI implementation of TicTacToe 

Users are able to play the game over the network, for non local games the server must be ran in a port-forwared environment

### CLI

To run the CLI do the following steps:

* Run the file **ServerClient.py**
* First select 1 starting the server and copy the IP it gives you
* In a new process run **ServerClient.py** again but select 2
* Fill in the required information including the IP you copied and have fun!

To generate an output file the client must quit by typing quit when prompted
otherwise the outfile will not save properly

### GUI

To run the GUI do the following steps:

* Run the file **TicTacServer.py** and select start
* Take note of the IP address displayed at the top
* Run the file **TicTacClient.py** and input required information
* Press connect

When 2 clients have connected the game will start


### Authors and maintainers
Harpreet Dhamarait, Ryan Dreise, Sawyer King, Jack Pistagnesi, and Ikenna Uduh
