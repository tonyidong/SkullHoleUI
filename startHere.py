from Tkinter import *
from tkFileDialog import askopenfilename

import numpy

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

        self.areaButton = Button(self, text = "Get Area", command = self.getArea)
        self.areaButton.grid(row = 7, column = 5)

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

    def getArea(self):
        fileObj = open(self.urlLabel["text"], 'r')
        # print fileObj
        pointList = []
        self.sum = 0

        for line in fileObj:
            brokeDown = line.split()
            if brokeDown[0] == "v":
                pointList.append(brokeDown)
            if brokeDown[0] == "f":
                # print brokeDown
                # print pointList

                subArea = self.areaForTriangle(pointList[int(brokeDown[1])-1], pointList[int(brokeDown[2])-1], pointList[int(brokeDown[3])-1])
                self.sum += float(subArea)

        self.messageLabel.configure(text = self.sum)

    def areaForTriangle(self, p1, p2, p3):
        ary1 = numpy.array((float(p1[1]), float(p1[2]), float(p1[3])))
        ary2 = numpy.array((float(p2[1]), float(p2[2]), float(p2[3])))
        ary3 = numpy.array((float(p3[1]), float(p3[2]), float(p3[3])))

        d1 = numpy.linalg.norm(ary1-ary2)
        d2 = numpy.linalg.norm(ary2-ary3)
        d3 = numpy.linalg.norm(ary3-ary1)

        s = (d1 + d2 + d3) / 2

        return (s*(s-d1)*(s-d2)*(s-d3)) ** 0.5



root = Tk()
root.title("Skull Holes Interface")
# root.geometry("500x306")
root.config(height = 500, width = 306, bg = "#C2C2D6")

app = Application(root)

root.mainloop()

