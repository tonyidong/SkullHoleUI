from Tkinter import *
from tkFileDialog import askopenfilename

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
        self.executeButton = Button(self, text = "Execute", command = self.executeExternal)
        self.executeButton.grid(row = self.executeButtonRow, column = self.executeButtonCol)

    def openFile(self):
        filename = askopenfilename()
        self.urlLabel.configure(text = filename)
        self.url = YES

    def executeExternal(self):
        if self.url:
            self.messageLabel.configure(text = "Now Executing")
        else:
            self.messageLabel.configure(text = "Please Select a File First")


root = Tk()
root.title("Skull Holes Interface")
# root.geometry("500x306")
root.config(height = 500, width = 306, bg = "#C2C2D6")

app = Application(root)

root.mainloop()

