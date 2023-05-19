# Sorry-Multiplayer

This game follows the rules of the original board game, which can be found here: https://www.hasbro.com/common/instruct/sorry.pdf

## Controls:
Selecting a color: Follow the click icons and select a color. Once you have selected one, the center visual will change and there will be a confirm button to select to lock in your choice. By hitting confirm, this color becomes greyed out for other players, and they can not select it. Once all players have selected a color and confirmed it, the game will start.

Drawing a card: When it is your turn, there will be a message announcement that appears on the screen. Once it fades, there will be a draw button that appears around the center of the board. After clicking it, a card visual will be displayed representing your card drawn. 

Movement: After drawing a card, if there is a possible move then the pieces that can be moved will have icons on them. Select a piece by clicking on it. If there is only one end position for the piece, it will automatically move to that position. If there are multiple positions that the piece can move with the given card, then the possible end positions are highlighted and the user is prompted to select one by clicking on it. After the piece has finished moving, then the turn ends.

## What you'll need
Clone of the main repository
Python interpreter version 3.9 or greater https://www.python.org/downloads/ (May work on other versions, but 3.9 is the lowest version texted)
Python environment (not required, but would make your life easier) Suggestion: Pycharm, https://www.jetbrains.com/pycharm/download/#section=windows
Install the pygame library (add it to the project as a package in an environment, or perform "pip install pygame" via the console)
Set-up
Works on multiple devices on the same network, or you may run it with multiple sessions on one device. This repository will need to be cloned on all devices that are being used. First, one person must decide to be the host, they are the only person who needs to run server.py

Before the host runs server.py, everyone will need to change line 2 of constants.py and replace the 'numbers.numbers.number.numbers' with a string of the hosts IP. The host can find this by opening command prompt and typing "ipconfig" and entering the IPv4 address displayed, and relaying this information to the participating parties.

After that, run the server file. If it is successful you will see "Waiting for a connection, Server Started" in the terminal.

Once the server is running, each player can run the main.py file to load the game. The game will start when all players connected have selected and confirmed their character.

## Want to play the game with friends online?
There are several ways to go about this, but I suggest trying out Hamachi https://vpn.net/. Hamachi allows you to create a virtual server, allowing up to 5 people to join the server for free. If you go this route, Hamachi will need to be installed on all participating devices, and one player will need to create a server.

Once created, all participating members should join the server created. This can be done by selecting Network > Join existing network ...

Continue through the set-up instructions, when it comes to the changing line 2 of constants.py, enter the servers IPv4 address in this location.
