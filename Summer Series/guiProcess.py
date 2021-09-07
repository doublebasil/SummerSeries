import tkinter as tk

class guiThread():
    def __init__(self):
        global graphSetting
        print(graphSetting)
        self.graphSettingSelected = 0
        # self.checkRunningPeriod = 1000 # ms
        self.root = tk.Tk()
        self.mainFrame = tk.Frame(self.root)
        self.mainFrame.pack()
        self.stopButton = tk.Button(self.mainFrame, text = "STOP ALL", fg = "white", bg = "red", height = 5, width = 5, command = self.stopAll)
        self.stopButton.pack()

        self.buttonSelected = tk.IntVar()

        tk.Radiobutton(self.mainFrame, variable = self.buttonSelected, value = 0, text = "All graphs", command = self.setGraph0).pack(anchor = tk.W)
        tk.Radiobutton(self.mainFrame, variable = self.buttonSelected, value = 1, text = "Humidity", command = self.setGraph1).pack(anchor = tk.W)

        # Check if the program is running every 1000 ms
        # self.root.after(self.checkRunningPeriod, self.checkRunning)
        self.root.mainloop()
    def setGraph0(self):
        global graphSetting
        self.graphSettingSelected = 0
    def setGraph1(self):
        global graphSetting
        self.graphSettingSelected = 1
    def stopAll(self):
        # global runSerial
        global runMain
        # runPlotter = False
        self.root.destroy()
        # runSerial = False
        runMain = False
    # def checkRunning(self):
    #     if (runGui == False):
    #         print("guiThread :: runGui is False")
    #         self.root.destroy()
    #     else:
    #         self.root.after(self.checkRunningPeriod, self.checkRunning)