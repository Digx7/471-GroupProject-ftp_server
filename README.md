# 471-GroupProject-ftp_server
For our 471 Computer Communications class we had to make a simple FTP server
Last Edited 11/24/2024


## Group Members
- Everette Webber edwebber@csu.fullerton.edu
- Michael Martinez ???@csu.fullerton.edu
- Gregory Dorfman ???@csu.fullerton.edu
- Sepehr Nourbakhsh ???@csu.fullerton.edu

## Program Language Used
Python

## How To Start
To run you will need two computers, one for the `server`, and one for the `client`.

First follow the instructions below to setup the `server`.
Second follow the instrucitons below to setup the `client`.

*(You can use the same computer for both for demonstration purposes.  Just run the `server` and the `client` in seperate terminals.)*

### Setting up the Server
1. Open a terminal
2. Navigate to the following directory `..\application\Server\`
3. Run the following command in the terminal `python .\pythonserv.py <PORT-NUMBER>`
4. Watch the output and remember the address that it is waiting for a connection on.
    The address will have the following format `(<IP-ADDRESS>, <PORT-NUMBER>)`.
    This will be used to connect the client to it

### Setting up the Client
1. Open a terminal
2. Naviage to the following directory `..\application\Client\`
3. Run the following command in the terminal `python .\cli.py <IP-ADDRESS> <PORT-NUMBER>`
    `<IP-ADDRESS>` can be found on the server once it is setup
    `<PORT-NUMBER>` can be found on the server once it is setup

## More Info
You can read the `Application Layer Protocol.pdf` to view a full breakdown of the protocol we built
The github repository for this project can be found here: https://github.com/Digx7/471-GroupProject-ftp_server 