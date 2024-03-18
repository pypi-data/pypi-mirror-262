from os import system,name,urandom
from time import sleep 
import sys
import hashlib
import string
import random
import socket
import pythonping
from ping3 import ping
import ipaddress
try:
	hostName = socket.gethostname()
	__IP__ = socket.gethostbyname(hostName)
except:
	pass

def clearShell():
	system('cls')

def type(message, interval=""):
    for i in message:
        sys.stdout.write(i)
        sys.stdout.flush()
        if interval:
            sleep(float(interval))
        else:
            sleep(0.01)
            
def list_directory():
    system('dir')
def wait(milliseconds):
    sleep(milliseconds)
def salt(chars, unencoded):
    salt = urandom(chars)
    if unencoded == True:
        return str(salt)
    elif unencoded == False:
        saltEncoded = str(salt)
        saltEncoded2 = saltEncoded.encode()
        return saltEncoded2
        
def hash(string,method=""):
    stringRaw = str(string).encode(encoding="utf-8")
    if method == "sha256":
        algorithm = hashlib.sha256()
    elif method == "md5":
        algorithm = hashlib.md5()
    else:
        raise ValueError("Invalid Algorithm")
    algorithm.update(stringRaw)
    return stringRaw,algorithm.hexdigest()


class Pinging:
    def pingServer(servername, print=False):
        if print == True:
            pingServer = pythonping.ping(servername, verbose=True)
            return pingServer
        else:
            pingServer = str(pythonping.ping(servername, verbose=False))
            pingServerRawText = ReplaceString(pingServer)
            replaceList = ["Reply from ", " ","ms",]
            replacedText = pingServerRawText.replaceAll(replaceList)
            finalText = replacedText.replace(' bytes in ', ',')
            return finalText
    def pingSweep(IPRANGE, unreachables=True, timeout = 1):
        network = ipaddress.ip_network(IPRANGE, strict=False)
        for ip in network.hosts():
            ipString = str(ip)
            response = ping(ipString, timeout=timeout)
            if response is not None:
                print(f"[IP:{ip}] is reachable ({response} seconds)")
            else:
                if unreachables == True:
                    print(f"[IP:{ip}] is unreachable")
                else:
                    continue
class ReplaceString:
    def __init__(self, string):
        self.string = string
        
    def replaceAll(self,substrings, replacefor=''):
        passed_string = self.string
        for i in substrings:
            passed_string = passed_string.replace(i,replacefor)

                
        return passed_string
            

class pyRandom:
    def string(case=""):
        if case == "lowercase":
            return random.choice(string.ascii_lowercase)
        elif case == "uppercase":
            return random.choice(string.ascii_uppercase)
        else:
            return random.choice(string.ascii_letters)
    def number(LowerNumber,HigherNumber):
        return random.randint(LowerNumber,HigherNumber)
    def charRandom():
        charList = ['!','@','#','$','%','^','&','*','*','(',')','-', '_','=','+','`','~',',','<','.','>',';',':','{','}','[',']','|']
        return random.choice(charList)
    
class pyHelp:
    def all():
        print("Brief List of some functions and classes: ")
        print("__IP__: Your IP address")
        print("hostName: Your host name")
        print("clearShell(): clears shell\nlist_directory(): Lists directories within the active directory")
        print("type(text): Only accepts 1 argument and replaces 'print' with a type writer effect")
        print("wait(seconds): same as sleep() but saves the importing of time")
        print("salt(amountOfCharacters, [encoded?] True | False)")
        print("hash(string, method), hashes string with the supported methods: md5, sha256")
        print("pyRandom Class")
        print("---------------")
        print("string([optional] case= uppercase | lowercase)")
        print("number(firstNumber, secondNumber): generates one random number between the two argued numbers")
        print("charRandom: returns random generated symbol [utf-8]")

