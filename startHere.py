from Tkinter import *
import tkMessageBox
from tkFileDialog import askopenfilename

import numpy

import os

class Application(Frame):

    def __init__(self, master, **options):
        # Initialize the Frame
        Frame.__init__(self, master, options)
        self.padx = 10
        self.pady = 10

        self.grid()

        self.url = NO
        self.create_widgets(master)

        self.pwd = os.getcwd()

    def create_widgets(self, master):
        #Label(master, text="First").grid(row=0)
        #Label(master, text="Second").grid(row=1)

        #e1 = Entry(master)
        #e2 = Entry(master)

        #e1.grid(row=0, column=1)
        #e2.grid(row=1, column=1)

        # Create Instruction Label
        self.instructionLabel = Label(self, \
            text = "Please click \"Specify Hole\" to select the hole from mesh\nOr browse the curve and calculate area", \
            font = "Arial 10", justify = LEFT, height = 3, bg = "white")
        self.instructionLabel.grid(row = 0, column = 0, columnspan = 2, padx = self.padx, pady = self.pady)

        self.drawLineButton = Button(self, text = "Specify Hole", \
            font = ("Arial Black", 16), \
            command = self.start3DViewer, width = 12, height = 2)
        self.drawLineButton.grid(row = 1, column = 0, padx = self.padx, pady = self.pady)

        
        # Create Browser Button
        self.browseButton = Button(self, text = "Browse File", \
            font = ("Arial Black", 16), \
            command = self.openFile, width = 12, height = 2)
        self.browseButton.grid(row = 1, column = 1, padx = self.padx, pady = self.pady)

        self.areaButton = Button(self, text = "Get Area", \
            font = ("Arial Black", 16), \
            command = self.runScripts, width = 12, height = 2)
        self.areaButton.grid(row = 2, column = 1, padx = self.padx, pady = self.pady)

        # Create Message Label
        self.messageLabel = Label(self, text = "Status: wait for user input", height = 4, font = "Helvetica 8", bg = "white")
        self.messageLabel.grid(row = 5, column = 0, columnspan = 2, sticky = W)



    def openFile(self):
        filename = askopenfilename()
        self.url = filename
        self.messageLabel.configure(text = "Status: " + filename + " is been selected")

    def runScripts(self):
        if not self.url:
            tkMessageBox.showwarning(
            "Error",
            "Please select a valid \".curve \" first."
            )
            return 

        if not self.url.endswith(".curve"):
            tkMessageBox.showwarning(
            "Error", 
            "\"" + self.url + " \" is not a valid \".curve \" first."
            )
            return 


        #run connecting script
        self.messageLabel.configure(text = "Status: now connecting the curves")
        curve = self.url
        filename = 'python ' + self.pwd + '\\scripts\\findHole.py ' + curve
        os.system(filename)

        #run TriMultPoly
        self.messageLabel.configure(text = "Status: now triangulate the curve")
        cCurve = curve[:-6] + ".continous"
        filename = self.pwd + '\\TriMultPoly\\TMP.exe ' + cCurve + ' 1 1 0 0 1 0 1 0'
        os.system(filename)

        #get Area
        dynObj = cCurve + "_dyn.obj"
        area = self.getArea(dynObj)

        tkMessageBox.showwarning(
        "Area", 
        "The hole area is " + str(area)
        )

        self.messageLabel.configure(text = "Stauts: finished")

    def getArea(self, url):
        lines = open(url, 'r')

        pointList = []
        area = 0

        for line in lines:
            brokeDown = line.split()
            if brokeDown[0] == "v":
                pointList.append(brokeDown)
            if brokeDown[0] == "f":
                subArea = self.areaForTriangle(pointList[int(brokeDown[1])-1], pointList[int(brokeDown[2])-1], pointList[int(brokeDown[3])-1])
                area += float(subArea)

        return area

    def areaForTriangle(self, p1, p2, p3):
        ary1 = numpy.array((float(p1[1]), float(p1[2]), float(p1[3])))
        ary2 = numpy.array((float(p2[1]), float(p2[2]), float(p2[3])))
        ary3 = numpy.array((float(p3[1]), float(p3[2]), float(p3[3])))

        d1 = numpy.linalg.norm(ary1-ary2)
        d2 = numpy.linalg.norm(ary2-ary3)
        d3 = numpy.linalg.norm(ary3-ary1)

        s = (d1 + d2 + d3) / 2

        return (s*(s-d1)*(s-d2)*(s-d3)) ** 0.5

    def start3DViewer(self):
        filename = self.pwd + '\\meshdrawing\\MeshDrawing.exe'
        os.system(filename)




root = Tk()
root.resizable(False, False)
root.title("Skull Holes Interface")

root.update()
scnWidth = root.winfo_screenwidth()
scnHeight = root.winfo_screenheight()
tmpcnf = '%dx%d+%d+%d' %(420 , 320, (scnWidth-420)/2, (scnHeight-320)/2)
root.geometry(tmpcnf)

app = Application(root, bg = 'white')

root.mainloop()

