#For the file dialogs
import tkinter as tk
from tkinter import filedialog

#For the backup function
import hashlib

#For the eventual pathHandler class
import os

#These simplify unpacking integers
def BE_Integer(data):
    value = 0
    for byte in data:
        value = (value << 8) | byte
    return value

def LE_Integer(data):
    value = 0
    index = 0
    for byte in data:
        value |= (byte << (8 * index))
        index+=1
    return value

#To-do: Write floating point value decoders as well

def getFileContents(filePath):
    with open(filePath, "rb") as file:
        return file.read()

def genHash(data):
    algorithm = hashlib.sha256()
    algorithm.update(data)
    return algorithm.hexdigest()

#When I write tools, I'll often need to auto-generate backups.
#The original code is from my BLiNX: the Time Sweeper randomizer.
def backupFile(file, offset, rootDirectory, tag="_BACKUP", extension=".bin"):
    with open(file, "r+b") as stream:
        stream.seek(offset)
        fileData = stream.read(0x140)
        fileHash = genHash(fileData)
        backupPath = rootDirectory

        if not os.path.exists(backupPath):
            os.makedirs(backupPath)
            
        backupPath += fileHash + tag + extension
        
        if os.path.exists(backupPath):
            stream.seek(offset)
            stream.write(getFileContents(backupPath))
        else:
            
            with open(backupPath, "w+b") as backup:
                stream.seek(offset)
                backup.write(stream.read())

        return backupPath

#Simpler file dialog class that utilizes Python classes correctly
class dialog:
    def __init__(self, mode):
        self.root = tk.Tk()
        self.root.withdraw()
        self.paths = ""
        if mode.lower() == "file":
            self.file()
        elif mode.lower() == "files":
            self.files()
        elif mode.lower() == "folder":
            self.folder()
        else:
            print("You entered an invalid mode. Please enter one of the following:\nfile\nfiles\nfolder")

    def file(self):
        self.paths = filedialog.askopenfilename()
        self.root.destroy()
    
    def files(self):
        self.paths = filedialog.askopenfilenames()
        self.root.destroy()

    def folder(self):
        self.paths = filedialog.askdirectory()
        self.root.destroy()

def checkSignature(file, signatureToCheckFor):
    with open(file, "rb") as signatureCheck:
        signature = signatureCheck.read(len(signatureToCheckFor)).decode("utf-8")
        
        if signature == signatureToCheckFor:
            return True
        else:
            return False
