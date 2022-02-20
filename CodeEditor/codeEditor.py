from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.messagebox import showinfo, showwarning, askokcancel
from tkinter.filedialog import asksaveasfilename, askopenfilename
from traceback import print_tb
from PIL import ImageTk, Image
import subprocess
import os

from sqlalchemy import column


class App(Tk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.config(bg='#999')
        self.title("Code Editor")
        self.filePath = ''

        self.outputhid = True
        self.sidemenu = False
        self.editorframe = Frame(self, width=200)
        self.editorframe.pack(side=RIGHT, fill=BOTH)
        # self.settingimg = PhotoImage('img/file.png')
        self.photosize = 40
        self.settingimg = Image.open('img/setting.png')
        self.settingimg = self.settingimg.resize(
            (self.photosize, self.photosize), Image.ANTIALIAS)
        self.settingimg = ImageTk.PhotoImage(self.settingimg)
        self.fileimg = Image.open('img/file.png')
        self.fileimg = self.fileimg.resize((40, 40), Image.ANTIALIAS)
        self.fileimg = ImageTk.PhotoImage(self.fileimg)

        self.activecolor = '#fff'


        self.morefilenumber = 0
        self.morefilelist = []


        self.iconbitmap('img/setting.png')
        self.cursors = [
            "arrow",
            "circle",
            "clock",
            "cross",
            "dotbox",
            "exchange",
            "fleur",
            "heart",
            "man",
            "mouse",
            "pirate",
            "plus",
            "shuttle",
            "sizing",
            "spider",
            "spraycan",
            "star",
            "target",
            "tcross",
            "trek"
        ]
        # for change curser style
        # self.config(cursor='fleur')
    def morefile(self):
        a = self.morefilenumber + 1
        self.morefileframe = Frame(self.editorframe)
        self.morefileframe.pack(anchor='nw')
        self.morefilelist.append(str(self.morefilenumber))
        self.morefilelist[self.morefilenumber] = Button(self.morefileframe,text=f'file{a}',borderwidth=0)
        self.morefilelist[self.morefilenumber].pack(side=RIGHT,fill=X)
        self.morefilenumber +=1


    def Editor(self):
        editorframe = Frame(self.editorframe)
        editorframe.pack()
        # self.editor = Text(self.editorframe,height=40)
        self.editor = Text(editorframe, height=41,
                           width=185, bg='#fff', fg='#000', spacing1=3)
        self.editor.pack(fill=BOTH, padx=1, pady=1,side=LEFT)
        scroll = Scrollbar(editorframe)
        scroll.pack(side=RIGHT,fill=Y)
        scroll.config(command= self.editor.yview)
        self.editor.config(yscrollcommand=scroll.set)

    def ScrollBar1(self):
        self.Scroll = Scrollbar(self.output)
        self.Scroll.pack(side=RIGHT, fill=Y)
        self.Scroll.config(command=self.output.yview)
        self.output.config(yscrollcommand=self.Scroll.set)

    def Menubar(self):
        def Save():
            if self.filePath != '':
                value = self.editor.get('1.0', 'end')
                with open(self.filePath, 'w') as f:
                    f.write(value)
            else:
                SaveAs()

        def SaveAs():
            path = pathSaveAs = asksaveasfilename(title="SaveAs")
            if path != '':
                value = self.editor.get('1.0', END)
                with open(path, 'w')as f:
                    f.write(value)
                self.filePath = path
            else:
                print("file is saved")

        def Open():
            path = askopenfilename(title='Open')
            if path != '':
                with open(path, 'r') as f:
                    value = f.read()
                self.editor.delete('1.0', 'end')
                self.editor.insert('1.0', value)

        def New():
            yn = askokcancel('Delete', 'You realy want to delete this page...')
            if yn:
                self.editor.delete('1.0', 'end')
                self.morefile()
            else:
                self.morefile()

        def Cut():
            self.editor.event_generate('<<Cut>>')

        def Paste():
            self.editor.event_generate('<<Paste>>')

        def Copy():
            self.editor.event_generate('<<Paste>>')

        def ClearOutput():
            try:
                self.output.delete('1.0', 'end')
            except:
                showinfo('Info', 'Output is Closed...')

        def recuernment():
            showinfo('Info', "Can't use Input in this ide")

        def About():
            showinfo('About', "This GUI made by AMAN")
            yn = askokcancel('Shorsh code', "Do you want to see Shors code")
            if yn:
                with open('shorscode.txt', 'r') as f:
                    value = f.read()
                    a = self.editor.get('1.0', 'end')
                    print(f'the value is {a}')
                    if a != '':
                        y = askokcancel(
                            'info', "You realy want to clear this page")
                        if y:
                            self.editor.insert('1.0', value)

        self.menu = Menu(self.editorframe)

        filemenu = Menu(self.menu, tearoff=0)
        filemenu.add_command(label="New File", command=New)
        filemenu.add_command(label="Save", command=Save)
        filemenu.add_command(label="Save As", command=SaveAs)
        filemenu.add_command(label="Open", command=Open)
        filemenu.add_command(label="Exit", command=quit)
        self.menu.add_cascade(label="File", menu=filemenu)

        editmenu = Menu(self.menu, tearoff=0)
        editmenu.add_command(label="Cut", command=Cut)
        editmenu.add_command(label="Copy", command=Copy)
        editmenu.add_command(label="Peste", command=Paste)
        self.menu.add_cascade(label="Edit", menu=editmenu)

        runmenu = Menu(self.menu, tearoff=0)
        runmenu.add_command(label="Run", command=self.Run)
        runmenu.add_separator()
        runmenu.add_command(label="Output", command=self.outputshow)
        runmenu.add_command(label='Clear Output', command=ClearOutput)
        self.menu.add_cascade(label="Run", menu=runmenu)
        AboutMenu = Menu(self.menu, tearoff=0)
        AboutMenu.add_command(label='Recuarnment', command=recuernment)
        AboutMenu.add_command(label='About', command=About)
        self.menu.add_cascade(label='About', menu=AboutMenu)

        self.config(menu=self.menu)

    def SideMenu(self):
        self.file = Frame(self, height=400)
        self.file.pack(side="left", anchor="n", fill=X)
        self.b1 = Button(self.file, image=self.fileimg, pady=20,
                         borderwidth=0, command=self.filemenu)
        self.b1.pack(side=TOP, pady=50)
        self.b2 = Button(self.file, image=self.settingimg,
                         pady=20, borderwidth=0, command=self.settingmenu, bd=0, activebackground=self.activecolor)
        self.b2.pack(pady=(550, 40))
        # self.b2.pack(side=BOTTOM, pady=250)

    def Run(self):
        self.stetasValue.set("Runing...")
        self.stetas.update()

        def run(path):
            p = subprocess.Popen(
                f'python {path}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, error = p.communicate()
            try:
                self.output.insert(END, out)
                self.output.insert(END, error)
            except:
                self.outputshow()
                self.output.insert(END, out)
                self.output.insert(END, error)

        if self.filePath != '':
            run(self.filePath)

        else:
            value = self.editor.get('1.0', END)
            with open('nano.py', 'w') as f:
                f.write(value)
            run('nano.py')
        self.stetasValue.set("Ready")
        self.stetas.update()

    def Output(self):
        self.outputframe = Frame(self.editorframe)
        self.outputframe.pack(side=LEFT)
        self.output = Text(self.outputframe, bg="#999")
        self.output.pack(side=LEFT)
        self.outscroll = Scrollbar(self.outputframe)
        self.outscroll.pack(side=RIGHT,fill=Y)
        self.outscroll.config(command=self.output.yview)
        self.output.config(yscrollcommand=self.outscroll.set)


    def StetasBar(self):
        self.stetasValue = StringVar()
        self.stetasValue.set("Ready")
        self.stetas = Button(
            self.editorframe, textvariable=self.stetasValue, anchor="w", borderwidth=0)
        self.stetas.pack(fill=X, side=BOTTOM)

    def outputshow(self):
        if self.outputhid:
            self.outputhid = False
            self.editor['height'] = 39
            # self.editor['height'] = 46.5
            self.outputframe.destroy()
            self.outscroll.destroy()
            # self.file.destroy()

        else:
            self.outputhid = True
            # self.editor['height'] = 35
            # self.editor['height'] = 40
            # self.SideMenu()
            self.Output()
            self.editor['height'] = 30
            self.output['height'] = 180
            if self.sidemenu:
                self.output['width'] = 170
            else:
                self.output['width'] = 183
            

    def SettingMenuIn(self):
        def setEditorColor():
            color = askcolor()
            self.editor['bg'] = color[1]
            self.stetas['bg'] = color[1]
            self.file['bg'] = color[1]
            self.menu['bg'] = color[1]
            self.activecolor = color[1]

        def changeCursor():
            def setcursor(event):
                value = event.widget.cget('text')
                self.editor['cursor'] = value

            def goBack():
                self.s1.destroy()
                self.SettingMenuIn()

            self.b1.destroy()
            self.editorcolorbutton.destroy()
            self.editorTextColor.destroy()
            self.cursorSetting.destroy()

            a = []
            i = 0
            for item in self.cursors:
                a.append(item)
                a[i] = Button(self.s1, text=item, borderwidth=0,
                              width=30, cursor=item)
                a[i].pack()
                a[i].bind('<Button-1>', setcursor)
            Button(self.s1, text='Back', width=30, borderwidth=0, command=goBack,
                   activebackground='black', activeforeground='white').pack()

        def setEditorTextColor():
            color = askcolor()
            self.editor['fg'] = color[1]
        self.s1 = Frame(self)
        self.s1.pack(side=BOTTOM)
        self.b1 = Button(self.s1, text="Setting menu", width=30, borderwidth=0)
        self.b1.pack()
        self.editorcolorbutton = Button(
            self.s1, text="Editor color", width=30, borderwidth=0, command=setEditorColor)
        self.editorcolorbutton.pack()
        self.editorTextColor = Button(
            self.s1, text='Ed0itor Text Color', width=30, borderwidth=0, command=setEditorTextColor)
        self.editorTextColor.pack()
        self.cursorSetting = Button(
            self.s1, text='Set Cursor', width=30, borderwidth=0, command=changeCursor)
        self.cursorSetting.pack()

    def settingmenu(self):

        if self.sidemenu:
            self.editor['width'] = 185
            try:
                self.output['width'] = 183
            except:
                pass
            self.sidemenu = False
            self.s1.destroy()
            try:
                self.fl1.destroy()
            except:
                self.filemenuin()
                self.fl1.destroy()

        else:
            self.editor['width'] = 170
            try:
                self.output['width'] = 170
            except:
                pass
            self.sidemenu = True
            self.SettingMenuIn()
            try:
                self.fl1.destroy()
            except:
                self.filemenuin()
                self.fl1.destroy()

    def filemenuin(self):

        def Sampel():
            # creating a back function for sampel file------------------------------------------------------------------
            def back():
                self.fl1.destroy()
                fl2.destroy()
                self.filemenuin()
            def fileopen(event):
                name = event.widget.cget('text')
                with open(f'SampelCode/{name}','r') as f:
                    value = f.read()
                self.editor.delete('1.0','end')
                self.editor.insert('1.0',value)

            self.fl1.destroy()
            # creatig a frame for sampel file---------------------------------------------------------------------
            self.fl1 = Frame(self)
            self.fl1.pack()
            Button(self.fl1,text='Go Back',borderwidth=0,width=30,command=back).pack()
            fl2 = Listbox(self.fl1,width=18)
            fl2.pack(fill=Y,side=LEFT)
            scrollbar = Scrollbar(self.fl1)
            scrollbar.pack(side=RIGHT,fill=Y)
            scrollbar.config(command=fl2.yview)
            fl2.config(yscrollcommand=scrollbar.set)

        # self.Scroll = Scrollbar(self.output)
        # self.Scroll.pack(side=RIGHT, fill=Y)
        # self.Scroll.config(command=self.output.yview)
        # self.output.config(yscrollcommand=self.Scroll.set)


            # sample code file list--------------------------------------------------------------------------------------
            list = os.listdir('SampelCode/')
            a = []
            i = 0
            for file in list:
                a.append(file)
                fl2.insert(END,file)
                i += 1

            
            
        # if user press a file to run this function------------------------------------------------------------------------
        def filepress(event):
            value = event.widget.cget('text')
            try:
                with open(value, 'r') as f:
                    text = f.read()
                self.editor.delete('1.0', END)
                self.editor.insert('1.0', text)
            except FileNotFoundError:
                showwarning('Warning', "File is missing...")

        # if user press a folder to run this function-------------------------------------------------------------------------
        def folderpress(event):
            showinfo('Info', "You can't open folder")
            
        # if usert click new file Button to run this function-----------------------------------------------------------------
        def newfile():
            def creatfile():
                # global new
                value = new.get()
                if value != '':
                    with open(value, 'w') as f:
                        f.write("")
                else:
                    showwarning('Worning', 'Plase Inter file name')

            def cansel():
                new.destroy()
                creat.destroy()
                cansel.destroy()

            new = Entry(self.fl1)
            new.pack()
            creat = Button(self.fl1, text='Creat', borderwidth=0,
                           width=30, command=creatfile)
            creat.pack()
            cansel = Button(self.fl1, text='Cansel',
                            borderwidth=0, width=30, command=cansel)
            cansel.pack()

        self.fl1 = Frame(self)
        self.fl1.pack()
        list = os.listdir()
        self.b1 = Button(self.fl1, text="file menu", width=30, borderwidth=0)
        self.b1.pack()
        self.sampel = Button(self.fl1,text='Sampel file',borderwidth=0,width=30,command=Sampel)
        self.sampel.pack()
        self.newfile = Button(self.fl1, text='New file',
                              borderwidth=0, width=30, command=newfile)
        self.newfile.pack()
        a = []
        i = 0
        for file in list:
            a.append(file)
            a[i] = Button(self.fl1, borderwidth=0,
                          width=30, text=file, anchor='w')
            a[i].pack()
            if os.path.isfile(file):
                a[i].bind('<Button-1>', filepress)

            else:
                a[i].bind('<Button-1>', folderpress)

            i += 1

    def filemenu(self):
        if self.sidemenu:
            self.sidemenu = False
            self.editor['width'] = 185
            try:
                self.output['width'] = 183
            except:
                pass
            try:
                self.s1.destroy()
            except:
                self.SettingMenuIn()
                self.s1.destroy()
            self.fl1.destroy()
        else:
            self.editor['width'] = 170
            self.sidemenu = True
            try:
                self.s1.destroy()
            except:
                self.SettingMenuIn()
                self.s1.destroy()
            try:
                self.output['width'] = 170
            except:
                pass
            self.filemenuin()


if __name__ == '__main__':
    app = App()
    app.morefile()
    app.morefile()
    app.Editor()
    app.Menubar()
    app.Output()
    app.output.destroy()
    app.StetasBar()
    app.SideMenu()
    app.outputshow()
    app.mainloop()
