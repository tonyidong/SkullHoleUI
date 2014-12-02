from Tkinter import *
from tkFileDialog import askopenfilename

import os

class Application(Frame):

    def __init__(self, master):
        # Initialize the Frame
        self.instructionLabelRow = 0
        self.instructionLabelCol = 10
        self.instructionLabelSpan = 2

        self.messageLabelRow = 1
        self.messageLabelCol = 10
        self.messageLabelSpan = 2

        self.browseButtonRow = 2
        self.browseButtonCol = 10

        self.urlLabelRow = 3
        self.urlLabelCol = 10
        self.urlLabelSpan = 2

        self.executeButtonRow = 4
        self.executeButtonCol = 10


        Frame.__init__(self, master)
        self.grid()
        self.url = NO
        self.create_widgets()

    def create_widgets(self):
        # Create Instruction Label
        self.instructionLabel = Label(self, text = "Please Click on 'Browse File' to Select a File", font = "Helvetica 16 bold italic")
        self.instructionLabel.grid(row = self.instructionLabelRow, column = self.instructionLabelCol, columnspan = self.instructionLabelSpan)

        # Create Message Label
        self.messageLabel = Label(self, text = "Message Will Be Displayed here", fg = "blue")
        self.messageLabel.grid(row = self.messageLabelRow, column = self.messageLabelCol, columnspan = self.messageLabelSpan)

        # Create Browser Button
        self.browseButton = Button(self, text = "Browse File", command = self.openFile, justify = CENTER)
        self.browseButton.grid(row = self.browseButtonRow, column = self.browseButtonCol)

        # Create Url Label
        self.urlLabel = Label(self, text = "No File Selected yet")
        self.urlLabel.grid(row = self.urlLabelRow, column = self.urlLabelCol, columnspan = self.urlLabelSpan)

        # Create Execute Button
        self.executeButton = Button(self, text = "Execute", command = self.run3DViewer)
        self.executeButton.grid(row = self.executeButtonRow, column = self.executeButtonCol)

    def openFile(self):
        filename = askopenfilename()
        self.urlLabel.configure(text = filename)
        self.url = YES

    def run3DViewer(self):
        pwd = os.getcwd()

        self.messageLabel.configure(text = "Now Circling the hole")
        # run 3D viewer
        filename = pwd + '\\meshdrawing\\MeshDrawing.exe'
        os.system(filename)        

        #run connecting script
        self.messageLabel.configure(text = "Now Connecting the curves")
        ply = self.urlLabel.cget("text")
        curve = ply[:-4] + ".curve"
        filename = 'python ' + pwd + '\\scripts\\findHole.py ' + curve
        os.system(filename)

        #run TriMultPoly
        self.messageLabel.configure(text = "Now Triangulate the curve")
        cCurve = curve[:-6] + ".continous"
        filename = pwd + '\\TriMultPoly\\TMP.exe ' + cCurve + ' 1 1 0 0 1 0 1 0'
        print filename
        os.system(filename)

        self.messageLabel.configure(text = "Finished")

    def run3DViewer2(self):
        if self.url:
            self.messageLabel.configure(text = "Now Executing")

            #print self.urlLabel.cget("text")
        else:
            self.messageLabel.configure(text = "Please Select a File First")


root = Tk()
root.title("Skull Holes Interface")
# root.geometry("500x306")
root.config(height = 500, width = 306, bg = "#C2C2D6")

app = Application(root)

root.mainloop()

