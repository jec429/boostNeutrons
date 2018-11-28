import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt

from featureUtils import *

#test = readTXT('trainDump.csv')

#data = readCSV('trainDump.csv')
#data = readTXT('trainDump.csv')
fname = 'trainDump.csv'
fnameHDF = 'testDump'
fstatus = initStatus(fnameHDF)
hindex = 0
tindex = 0


LARGE_FONT= ("Verdana", 12)

class FeaturesGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Neutron features")
        
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand = True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        #container.pack()
        
        self.frames = {}

        for F in (StartPage, PageOne, TablePage, PlotPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def show_Table(self, cont):
        frame = TablePage(self.container, self)
        self.frames[TablePage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button2 = tk.Button(self, text="Table Page", command=lambda: controller.show_Table(TablePage))
        button2.configure(height = 2, width = 20)
        button2.place(relx=.35, rely=0.4, anchor="c")
        
        button3 = tk.Button(self, text="Plots Page",
                            command=lambda: controller.show_frame(PlotPage))
        button3.configure(height = 2, width = 20)
        button3.place(relx=.65, rely=0.4, anchor="c")

        button4 = tk.Button(self, text="Quit",
                            command=self.quit)
        button4.configure(height = 2, width = 40)
        button4.place(relx=.5, rely=.5, anchor="c")
        
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(TablePage))
        button2.pack()


class TablePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="TABLE", font=LARGE_FONT)
        label.pack(pady=5,padx=5)

        self.controller = controller
        self.parent = parent
        self.treeview = None

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button3 = ttk.Button(self, text="Plots Page",
                            command=lambda: controller.show_frame(PlotPage))
        button3.pack()

        buttonN = ttk.Button(self, text="Next",
                             command=lambda: self.nextTable())
        buttonN.pack()

        buttonP = ttk.Button(self, text="Previous",
                             command=self.previousTable)
        buttonP.pack()
        
        buttonPrint = ttk.Button(self, text="Print Table",
                             command=self.printTable)
        buttonPrint.pack()
        
        buttonQ = ttk.Button(self, text="Quit",
                            command=self.quit)
        buttonQ.pack(pady=5,padx=5)

        self.CreateUI()
        self.LoadTable(tindex)
        
    def CreateUI(self):
        if self.treeview:
            self.treeview.destroy()
        tv = ttk.Treeview(self)
        tv['columns'] = ('index', 'mean', 'std', 'status')
        tv.heading("#0", text='Feature', anchor='w')
        tv.column("#0", anchor="w")
        tv.heading('index', text='Index')
        tv.column('index', anchor='center', width=50)
        tv.heading('mean', text='Mean')
        tv.column('mean', anchor='center', width=100)
        tv.heading('std', text='STD')
        tv.column('std', anchor='center', width=100)
        tv.heading('status', text='Status')
        tv.column('status', anchor='center', width=50)
        tv.pack(fill="both", expand=True)
        self.treeview = tv

    def LoadTable(self, tindex):
        global fstatus
        ldata = readDataHDFBlock(fnameHDF,tindex)
        #print(ldata[17])
        for i,d in enumerate(ldata):
            fstatus[tindex*20 + i] = 0 if np.std(d[1:]) == 0 else 1
            self.treeview.insert('', 'end', text=d[0], values=(tindex*20 + i, '%.3f' %np.mean(d[1:]), '%.3f' %np.std(d[1:]), u'\u2705' if fstatus[tindex*20 + i] == 1 else u'\u274C'))

    def nextTable(self):
        global tindex
        tindex += 1
        self.DeleteUI()
        self.CreateUI()
        self.LoadTable(tindex)
    
    def previousTable(self):
        global tindex
        if tindex == 0: return
        tindex -= 1
        self.DeleteUI()
        self.CreateUI()
        self.LoadTable(tindex)

    def DeleteUI(self):
        self.treeview.delete()

        
    def printTable(self):
        '''
        print('Table printed')        
        f = open('prunedDump.csv','w')
        string = 'class,'
        dt =  np.array(data[-1][1])[np.newaxis].T
        for n in data[:-1]:
            if n[2] == 1:
                string += n[0]
                string += ','
                na = np.array(n[1])[np.newaxis]
                dt = np.concatenate((dt,na.T),axis=1)

        string = string[:-1]+'\n'
        for d in dt:
            for e in d:
                string += str(e)+','
            string = string[:-1]+'\n'
        f.write(string+'\n')
        f.close()
        '''
        print("NOT IMPLEMENTED")
        
            
class PlotPage(tk.Frame):

    def __init__(self, parent, controller):
        global fstatus
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="", font=LARGE_FONT)
        label.pack(pady=120,padx=10)

        self.widget = None
        if self.widget:
            self.widget.destroy()

        #names = [n[0] for n in data]
        h = histoFeature(fnameHDF,hindex,fstatus)            
        canvas = FigureCanvasTkAgg(h, self)
        canvas.draw()
        self.widget = canvas.get_tk_widget()

        self.widget.pack(fill=tk.BOTH)                

        
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.place(relx=.4, rely=0.05, anchor="n")
        buttonQ = ttk.Button(self, text="Quit", command=self.quit)
        buttonQ.place(relx=.6, rely=0.05, anchor="n")

        buttonT = ttk.Button(self, text="Table Page",
                            command=lambda: controller.show_Table(TablePage))
        buttonT.place(relx=.5, rely=0.1, anchor="n")

        button2 = ttk.Button(self, text="Next >",
                             command=self.nextFeature)
        button2.place(relx=.6, rely=0.15, anchor="n")

        button3 = ttk.Button(self, text="< Previous",
                             command=self.previousFeature)
        button3.place(relx=.4, rely=0.15, anchor="n")

        button4 = ttk.Button(self, text="<< First",
                             command=self.firstFeature)
        button4.place(relx=.4, rely=0.2, anchor="n")

        button5 = ttk.Button(self, text="Last >>",
                             command=self.lastFeature)
        button5.place(relx=.6, rely=0.2, anchor="n")

        labelF = tk.Label(self, text="Feature index=", font=LARGE_FONT)
        labelF.place(relx=.35, rely=0.255, anchor="n")
        self.entry = tk.Entry(self,width=10)
        self.entry.insert(0,'0')
        self.entry.place(relx=.5, rely=0.25, anchor="n")
        button6 = tk.Button(self, text="Get", command=self.jumpToFeature)
        button6.place(relx=.6, rely=0.255, anchor="n")
        
        button7 = tk.Button(self, text="Change status", command=self.changeStatus)
        button7.place(relx=.6, rely=0.3, anchor="n")

        button8 = tk.Button(self, text="Get status", command=self.getStatus)
        button8.place(relx=.4, rely=0.3, anchor="n")
        

        self.Status = tk.Label(self, text="Feature status %d" %(fstatus[hindex]))
        #self.Status = tk.Label(self, text="Feature status %d" %(0))
        h = 0

    def changeStatus(self):
        if self.entry.get() is not '':
            hhindex = int(self.entry.get())
        else:
            hhindex = 0
        fstatus[hhindex] = 1 if fstatus[hhindex] == 0 else 0
        print("Feature status=",fstatus[hhindex])
        self.Status.destroy()
        self.Status = tk.Label(self, text="Feature status %d" %(fstatus[hhindex]))
        self.Status.place(relx=.5, rely=0.35, anchor="n")
        
        
    def getStatus(self):
        
        #hhindex = int(self.entry.get())
        print("Feature status=",fstatus[hindex])
        self.Status.destroy()
        self.Status = tk.Label(self, text="Feature status %d" %(fstatus[hindex]))
        self.Status.place(relx=.5, rely=0.35, anchor="n")
        
        
    def jumpToFeature(self):
        global hindex
        global fstatus
        global tindex
        #print(self.entry.get())
        hindex = int(self.entry.get())
        tindex = int(hindex/20)
        self.Status.destroy()
        self.Status = tk.Label(self, text="Feature status %d" %(fstatus[hindex]))
        print("Feature status=",fstatus[hindex])
        h = histoFeature(fnameHDF,hindex,fstatus)            
        if self.widget:
            self.widget.destroy()
        canvas = FigureCanvasTkAgg(h, self)
        canvas.draw()
        self.widget = canvas.get_tk_widget()
        self.Status.place(relx=.5, rely=0.35, anchor="n")
        self.widget.pack(fill=tk.BOTH)
        plt.close('all')

        
    def nextFeature(self):
        global hindex
        global fstatus
        #print(hindex)
        hindex = hindex + 1
        h = histoFeature(fnameHDF,hindex,fstatus)            
        if self.widget:
            self.widget.destroy()
        canvas = FigureCanvasTkAgg(h, self)
        canvas.draw()
        self.widget = canvas.get_tk_widget()
        self.widget.pack(fill=tk.BOTH)
        plt.close('all')
        self.Status = tk.Label(self, text="Feature status %d" %(fstatus[hindex]))

    def previousFeature(self):
        global hindex
        global fstatus
        #print(hindex)
        if hindex == 0: return
        hindex = hindex - 1
        h = histoFeature(fnameHDF,hindex,fstatus)            
        if self.widget:
            self.widget.destroy()
        canvas = FigureCanvasTkAgg(h, self)
        canvas.draw()
        self.widget = canvas.get_tk_widget()
        self.widget.pack(fill=tk.BOTH)
        plt.close('all')
        self.Status = tk.Label(self, text="Feature status %d" %(fstatus[hindex]))


    def firstFeature(self):
        global hindex
        global fstatus
        hindex = 0
        h = histoFeature(fnameHDF,hindex,fstatus)            
        if self.widget:
            self.widget.destroy()
        canvas = FigureCanvasTkAgg(h, self)
        canvas.draw()
        self.widget = canvas.get_tk_widget()
        self.widget.pack(fill=tk.BOTH)
        plt.close('all')
        self.Status = tk.Label(self, text="Feature status %d" %(fstatus[hindex]))


    def lastFeature(self):
        global hindex
        global fstatus
        #print(hindex)
        hindex = -1
        h = histoFeature(fnameHDF,hindex,fstatus)            
        if self.widget:
            self.widget.destroy()
        canvas = FigureCanvasTkAgg(h, self)
        canvas.draw()
        self.widget = canvas.get_tk_widget()
        self.widget.pack(fill=tk.BOTH)
        plt.close('all')
        self.Status = tk.Label(self, text="Feature status %d" %(fstatus[hindex]))

        
app = FeaturesGUI()
app.mainloop()


#fig = histoFeature(data,'neutron3d_time_0')
