import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt

from featureUtils import *

data = readCSV('trainDump.csv')
hindex = 0
tindex = 0


LARGE_FONT= ("Verdana", 12)

class FeaturesGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Neutron features")
                
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, TablePage, PlotPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        #button = ttk.Button(self, text="Visit Page 1",
        #                    command=lambda: controller.show_frame(PageOne))
        #button.pack()
        
        button2 = tk.Button(self, text="Table Page", command=lambda: controller.show_frame(TablePage))
        #button2.grid(row = 0, column = 0)
        button2.configure(height = 2, width = 20)
        button2.place(relx=.35, rely=0.4, anchor="c")
        
        button3 = tk.Button(self, text="Plots Page",
                            command=lambda: controller.show_frame(PlotPage))
        #button3.grid(row = 0, column = 1)
        button3.configure(height = 2, width = 20)
        button3.place(relx=.65, rely=0.4, anchor="c")

        button4 = tk.Button(self, text="Quit",
                            command=self.quit)
        #button4.grid(column=0, row=1, columnspan=2, rowspan=1, sticky=(tk.N, tk.S, tk.E, tk.W))
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
        for i,d in enumerate(data[tindex*20:(tindex+1)*20]):
            self.treeview.insert('', 'end', text=d[0], values=(tindex*20 + i, '%.3f' %np.mean(d[1]), '%.3f' %np.std(d[1]), u'\u2705' if d[2] == 1 else u'\u274C'))

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
        
        
            
class PlotPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #frame1 = tk.Frame(self,parent)
        label = tk.Label(self, text="PLOTS", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        buttonT = ttk.Button(self, text="Table Page",
                            command=lambda: controller.show_frame(TablePage))

        button2 = ttk.Button(self, text="Next",
                             command=self.updateFeature)
        #button2.pack()

        button3 = ttk.Button(self, text="Previous",
                             command=self.previousFeature)
        #button3.pack()

        button4 = ttk.Button(self, text="First",
                             command=self.firstFeature)
        #button4.pack()

        button5 = ttk.Button(self, text="Last",
                             command=self.lastFeature)
        #button5.pack()

        self.entry = tk.Entry(self)        
        #self.entry.pack()
        button6 = tk.Button(self, text="Get", command=self.jumpToFeature)
        #button6.pack()
        
        button7 = tk.Button(self, text="Change status", command=self.changeStatus)
        #button7.pack()
        
        buttonQ = ttk.Button(self, text="Quit", command=self.quit)
        #buttonQ.pack()

        self.Status = tk.Label(self, text="Feature status %d" %(data[hindex][2]))
        #self.Status.pack()

        self.widget = None
        if self.widget:
            self.widget.destroy()

        names = [n[0] for n in data]
        h = histoFeature(data,names[hindex])            
        canvas = FigureCanvasTkAgg(h, self)
        canvas.draw()
        self.widget = canvas.get_tk_widget()
        self.widget.pack(fill=tk.BOTH)

        h = 0

    def changeStatus(self):
        global data
        hhindex = int(self.entry.get())
        data[hhindex][2] = 1 if data[hhindex][2] == 0 else 0
        print("Feature status=",data[hhindex][2])
        self.Status.destroy()
        self.Status = tk.Label(self, text="Feature status %d" %(data[hhindex][2]))
        self.Status.pack()
        
        
    def jumpToFeature(self):
        #print(self.entry.get())
        hhindex = int(self.entry.get())
        self.Status.destroy()
        self.Status = tk.Label(self, text="Feature status %d" %(data[hhindex][2]))
        self.Status.pack()
        print("Feature status=",data[hhindex][2])
        names = [n[0] for n in data]
        h = histoFeature(data,names[hhindex])
        if self.widget:
            self.widget.destroy()
        canvas = FigureCanvasTkAgg(h, self)
        canvas.draw()
        self.widget = canvas.get_tk_widget()
        self.widget.pack(fill=tk.BOTH)
        plt.close('all')

        
    def updateFeature(self):
        global hindex
        #print(hindex)
        hindex = hindex + 1
        names = [n[0] for n in data]
        h = histoFeature(data,names[hindex])
        if self.widget:
            self.widget.destroy()
        canvas = FigureCanvasTkAgg(h, self)
        canvas.draw()
        self.widget = canvas.get_tk_widget()
        self.widget.pack(fill=tk.BOTH)
        plt.close('all')

    def previousFeature(self):
        global hindex
        #print(hindex)
        if hindex == 0: return
        hindex = hindex - 1
        names = [n[0] for n in data]
        h = histoFeature(data,names[hindex])
        if self.widget:
            self.widget.destroy()
        canvas = FigureCanvasTkAgg(h, self)
        canvas.draw()
        self.widget = canvas.get_tk_widget()
        self.widget.pack(fill=tk.BOTH)
        plt.close('all')
        self.Status = tk.Label(self, text="Feature status %d" %(data[hindex][2]))


    def firstFeature(self):
        global hindex
        #print(hindex)
        hindex = 0
        names = [n[0] for n in data]
        h = histoFeature(data,names[hindex])
        if self.widget:
            self.widget.destroy()
        canvas = FigureCanvasTkAgg(h, self)
        canvas.draw()
        self.widget = canvas.get_tk_widget()
        self.widget.pack(fill=tk.BOTH)
        plt.close('all')
        self.Status = tk.Label(self, text="Feature status %d" %(data[hindex][2]))


    def lastFeature(self):
        global hindex
        #print(hindex)
        hindex = len(data) - 1
        names = [n[0] for n in data]
        h = histoFeature(data,names[hindex])
        if self.widget:
            self.widget.destroy()
        canvas = FigureCanvasTkAgg(h, self)
        canvas.draw()
        self.widget = canvas.get_tk_widget()
        self.widget.pack(fill=tk.BOTH)
        plt.close('all')
        self.Status = tk.Label(self, text="Feature status %d" %(data[hindex][2]))

        
app = FeaturesGUI()
app.mainloop()


#fig = histoFeature(data,'neutron3d_time_0')
