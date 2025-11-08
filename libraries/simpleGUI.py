#This is here because I want to avoid pip as much as possible and tkinter is kind of awful to set up and use as-is.
import tkinter as tk
class simpleGUI:
    def __init__(self, title="You forgot to enter a name! This window needs a name.", size="640x480", color="#3A56AD"):
        self.color = color
        self.width = int(size.split("x")[0])
        self.height = int(size.split("x")[1])
        
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(size)
        self.root.config(bg=color)
    def testCommand(self):
        print(f"Hello there! You're either testing this or forgot to enter a command.\nThe window color is {self.color} by the way.")
        
    def text(self, message="Please enter a message", font="Arial", size=20, textColor="black", xPosition=None, yPosition=80):
        if xPosition == None:
            xPosition = self.width//2
        if yPosition == None:
            yPosition = self.height//2
            
        label = tk.Label(
            self.root,
            text=message,
            font=(font, size),
            fg=textColor,
            bg=self.color)
        label.place(x=xPosition, y=yPosition, anchor="center")
        return label
        
    def button(self, message="Please enter a message", command=None, font="Arial", size=20, buttonColor="lightblue", textColor="black", xPosition=None, yPosition=80):
        if command == None:
            command = self.testCommand
        if xPosition == None:
            xPosition = self.width//2
        if yPosition == None:
            yPosition = self.height//2
            
        button = tk.Button(
            self.root,
            text=message,
            command=command,
            font=(font, size),
            fg=textColor,
            bg=buttonColor)
        button.place(x=xPosition, y=yPosition, anchor="center")
        return button
        
    def entry(self, font="Arial", size=20, textColor="black", boxColor="white", xPosition=None, yPosition=20, width=10):
        if xPosition == None:
            xPosition = self.width//2
        if yPosition == None:
            yPosition = self.height//2
            
        entry = tk.Entry(
            self.root,
            font=(font, size),
            fg=textColor,
            bg=boxColor,
            width=width)
        entry.place(x=xPosition, y=yPosition, anchor="center")
        return entry
    def checkBox(self, font="Arial", size=20, textColor="black", xPosition=None, yPosition=80):
        if xPosition == None:
            xPosition = self.width//2
        if yPosition == None:
            yPosition = self.height//2
            
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(
            self.root,
            variable=var,
            font=(font, size),
            fg=textColor,
            bg=self.color,
            selectcolor=self.color)
        checkbox.place(x=xPosition, y=yPosition, anchor="center")
        checkbox.var = var
        return checkbox
