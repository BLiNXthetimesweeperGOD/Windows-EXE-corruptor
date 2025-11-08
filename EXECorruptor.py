#x86 corruptor
from libraries.FileIO import *
from libraries.simpleGUI import *
from libraries.generateInstructionList import *
import random

#Feel free to customize this. Be careful! Some instructions are be more dangerous than others.
targets = ["fmul", "fsub", "fadd", "fdiv", "fld", "fst", "fstp", "fsqrt",
           "addps", "mulps", "subps", "divps", "sqrtps"]
file = None
amount = 30
seed = ""

def openFile():
    global file
    global instructions
    file = dialog("file").paths
    if file:
        instructionList = file.replace("exe", "txt")
        
        if not os.path.exists(instructionList): #Generate an instruction list
            instructionListGenerator(file)
            
        instructions = []

        with open(instructionList, "r") as listLoader:
            lines = listLoader.readlines()
            for line in lines:
                entry = line.split()
                if len(entry) >= 3:
                    offset = int(entry[0], 16)
                    size = int(entry[1], 16)
                    name = entry[2]
                    
                    if any(target in name for target in targets):
                        instructions.append([name, size, offset])

        #Create a backup (this also restores the backup if one already exists)
        backupFile(file, 0, os.getcwd()+"/backups/", extension=".exe")
    else:
        return None

def update():
    global amount
    if intensityBox.get() != "":
        try:
            amount=int(intensityBox.get())
        except:
            amount=5
    intensityDisplay.config(text=f"Intensity: {amount}")
    
def restoreBackup():
    if file:
        backupFile(file, 0, os.getcwd()+"/backups/", extension=".exe")
    
def corrupt():
    if useSeed.var.get():
        random.seed(seed.get())
    else:
        seed.delete(0, tk.END)
        seed.insert(0, str(random.randint(0, 99999999)))
        random.seed(seed.get())
        
    if file:
        #Restore the file before corrupting
        backupFile(file, 0, os.getcwd()+"/backups/", extension=".exe")
        
        #Corrupt the file
        intensity = min(amount, len(instructions))
        usedOffsets = set()

        with open(file, "r+b") as corruptor:
            for i in range(intensity):
                instruction = random.choice(instructions)
                name, size, offset = instruction

                if offset in usedOffsets or offset < 0x500:
                    continue
                    
                usedOffsets.add(offset)
                corruptor.seek(offset)
                corruptor.write(b'\x90' * size)

#Sorry for the mess...
GUI = simpleGUI(title="EXE Corruptor", size="640x360")

openFileButton = GUI.button("Open a file", xPosition=140, yPosition=200, command=openFile)
corruptFileButton = GUI.button("Corrupt file", yPosition=200, command=corrupt)
restoreFileButton = GUI.button("Restore file", xPosition = 500, yPosition=200, command=restoreBackup)

updateIntensityButton = GUI.button("Update intensity", yPosition=280, command=update)

intensityBox = GUI.entry(xPosition=500, yPosition=120)
intensityBox.insert(0, "30")

useSeedText = GUI.text("Use seed?", xPosition=140)
useSeed = GUI.checkBox(xPosition=140, yPosition=120)

seedText = GUI.text("Seed")
seed = GUI.entry(yPosition=120)

intensityDisplay = GUI.text(f"Intensity: {amount}", xPosition=500)

GUI.root.mainloop()
