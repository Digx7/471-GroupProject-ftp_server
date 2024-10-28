# 471-GroupProject-ftp_server
For our 471 Computer Communications class we had to make a simple FTP server
Last Edited 10/27/2024


# How to use
This section goes over how to run this file

## Prerequisites:
 Have python installed in the path

## 1. Open Terminals
Open up two seperate terminals

## 2. Navigate Terminals
Navitage both terminals to the location of the python directory in this project

## 3. Run python
In one terminal run `python sendfileserv.py`
This will set up the reciving terminal

In the other terminal `run python sendfilecli.py ..\filesToSend\[FILETOSEND]`
In the `[FILETOSEND]` incluce the `.txt` or any other extensions

## 4. Watch
Watch the output of both terminals
In the `sendfilecli.py` terminal you should see the following output
`Sent  [NUM]  bytes.`
Wher `[NUM]` is some number of bytes

In the `sendfileserv.py` terminal you should see the following output
```
The file size is  [NUM]
The file data is:
[FILE]
Waiting for connections...
```

# Output explained
This section what appear to be a few discrepencies between the `sendfilecli.py` and the `sendfileserv.py`

## Differences in file size
You may notice that the `sendfilecli.py` always reports sending 10 bytes more than what `sendfileserv.py` recieves.
This is because the first 10 bytes sent by `sendfilecli.py` are used to tell `sendfileserv.py` the size of the file it is sending

## How to validate the output of the Lorem files
Under the `/filesToSend` you will find multiple `Lorem_` files.  These are text files filled with giberish known as Lorem Ipsum.
The Lorem Ipsum generator we used can be found [here](https://loremipsum.io/generator?n=100&t=p)

For ease of validation we have included the all caps words `START` and `END` at the beginning and end of the files for easy validation
At the moment the only one that fails is `/filesToSend/Lorem_SuperLong_v2.txt`

## What is with the /r's and /n's in the output
Those are the return and endof line tokens your computer usually hides.
They are technically in all text files, they are just rarely diplayed
The output showing them is a good thing, it means that even the hidden charcters are being sent

# Whats left to work on?
At the time of writing we have these following task that need to be worked on
- Make it so `sendfilecli.py` breaks up the file into multiple packets if the file is to large
- Make it so `sendfileserv.py` can receive multiple packets and reassemble the file correctly
- Make it so `sendfileserv.py` stores the file somewhere (after all it need to be able to send this file back)
- Make it so we can specify the port number when setting up `sendfilecli.py` and the `sendfileserv.py`
- Make it so the user can establish a connection between a client and a sever then enter any of the following commands 
    - `get <file name> (downloads file <file name> from the server)`
    - `put <filename> (uploads file <file name> to the server)`
    - `ls(lists files on the server)`
    - `quit (disconnects from the server and exits)`
- Make it so the client an server use 2 connections at all times 1 for sending data and 1 for sending commands

If there are any futher questions check the assignment pdf `CPSC471_Fall 2024_Programming Assignment(1).pdf`