from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd


class text_editor:
    # varibles required
    fts = [("Text File", "*.txt"), ("All Files", "*.*")]
    filename = "Untitled.txt"
    filestate = "UNSAVED"
    root = Tk()
    sbv = Scrollbar(root, orient=VERTICAL)
    input = Text(root, height=root.winfo_screenheight(
    ), width=root.winfo_screenwidth(), wrap=WORD, yscrollcommand=sbv.set, undo=True)
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    editmenu = Menu(menubar, tearoff=0)
    helpmenu = Menu(menubar, tearoff=0)

    def __init__(self):

        self.root.title(self.filename + " - Text Editor")
        self.root.geometry("1060x560")

        # defining a protocol handler for closing the window
        self.root.protocol("WM_DELETE_WINDOW", self.handle)

        # 1.File Menu
        self.filemenu.add_command(
            label="New", command=self.newfile)
        self.filemenu.add_command(
            label="Open", command=self.openfile)
        self.filemenu.add_command(
            label="Save", accelerator='Ctrl+S', command=self.savefile)
        self.filemenu.add_command(
            label="Save as", command=self.savefileas)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Close", command=self.handle)

        # 2.Edit Menu

        self.editmenu.add_command(label="Undo", accelerator='Ctrl+Z', command=self.input.edit_undo)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Cut", accelerator='Ctrl+X',
                                  command=self.input.event_generate("<<Cut>>"))
        self.editmenu.add_command(label="Copy", accelerator='Ctrl+C',
                                  command=self.input.event_generate("<<Copy>>"))
        self.editmenu.add_command(label="Paste", accelerator='Ctrl+V',
                                  command=self.input.event_generate("<<Paste>>"))
        self.editmenu.add_command(
            label="Clear All", accelerator='Shift+Del', command=lambda: self.input.delete("1.0", "end-1c"))
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Find and Replace",
                                  accelerator='Ctrl+F', command=self.findPrompt)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Select All", accelerator="Ctrl+A",
                                  command=lambda: self.input.tag_add('sel', '1.0', 'end'))

        # 3. Help Menu
        self.helpmenu.add_command(label="About", command=self.about)

        # Adding all Child Menus to The Parent Menu
        self.menubar.add_cascade(
            label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        # Config the scrollbar to change with the input
        self.sbv.config(command=self.input.yview)

        # keybinds
        self.input.bind('<Control-s>', lambda event: self.savefile())
        self.input.bind('<Shift-Delete>', lambda event: self.input.delete("1.0", "end-1c"))
        self.input.bind('<Control-f>', lambda event: self.findPrompt())

        self.sbv.pack(side=RIGHT, fill=Y)
        self.input.pack()
        # making menubar as the menu of the entire window
        self.root.config(menu=self.menubar)

    def about(self):
        def close():
            self.root.focus_set()
            a.destroy()

        a = Tk()
        a.title("About Text Editor")
        a.geometry("420x200")

        info = Label(a)
        info.config(text="""This Text Editor was programmed for a Minor Project.


        Version : 1.0
        Author : Tejasvee
        Technology : Python
        """)
        a.attributes("-topmost", True)
        ok = Button(a, text="OK", command=close)
        info.pack()
        ok.pack()
        a.focus_force()
        a.mainloop()

    def newfile(self):
        # if the file is already empty no prompt is needed
        if len(self.input.get("1.0", "end-1c")) > 0:
            var = messagebox.askquestion(
                title="Warning", message="Discard the current File data?")
            if var == "yes":
                self.input.delete("1.0", "end")
        else:
            self.input.delete("1.0", "end")

    def openfile(self):
        # if the file is already empty no prompt is needed
        if len(self.input.get("1.0", "end-1c")) > 0:
            var = messagebox.askquestion(
                title="Warning", message="The current File data will be lost, Save file?")
            if var == "yes":
                fd.asksaveasfilename(
                    title="Save File", initialdir="/", filetypes=self.fts)
            else:
                self.input.delete("1.0", "end-1c")

        fname = fd.askopenfile(
            title="Open File", initialdir="/", mode='r+', filetypes=self.fts)
        if fname is not None:
            self.filename = fname.name
            self.root.title(self.filename + " - Text Editor")
        # home, ext = os.path.splitext(filename.name) #to get the path and extension of file
        # if(ext not in fts):
        #       messagebox.showwarning(title="Warning", message="File may not work")
        try:
            # if file is not readable or of unknown type prompt a error.
            content = fname.read()
            self.input.insert(END, content)
        except:
            messagebox.showerror(message="File cannot be opened!")

    def savefile(self):
        if self.filename == "Untitled.txt":
            fname = fd.asksaveasfile(
                title="Save As", initialdir="/", filetypes=self.fts, defaultextension=self.fts)
            if fname is not None:
                fname = fname.name
                self.filename = fname
        else:
            fname = self.filename

        if fname is not None:
            file = open(fname, "w")
            c = self.input.get("1.0", "end-1c")
            file.write(c)
            file.close()
            self.filestate = "SAVED"

        if self.filestate == "SAVED":
            messagebox.showinfo(title="Task", message="Filed Saved!")
            self.root.title(self.filename + " - Text Editor")
        else:
            messagebox.showerror(title="Error", message="File Not Saved!")

    def savefileas(self):
        fname = fd.asksaveasfilename(
            title="Save As", initialdir="/", filetypes=self.fts, defaultextension=self.fts)
        if fname is not None:
            self.filestate = "SAVED"
            f = open(fname, "w")
            c = self.input.get("1.0", "end-1c")
            f.write(c)
            f.close()

        if self.filestate == "SAVED":
            messagebox.showinfo(title="Task", message="Filed Saved!")
            self.root.title(self.filename + " - Text Editor")
        else:
            messagebox.showerror(title="Error", message="File Not Saved!")

    def handle(self):
        if len(self.input.get("1.0", "end-1c")) > 0:
            if self.filestate == "UNSAVED":
                if messagebox.askyesno(title="Warning",
                                       message="Do You Want to save the changes made to " + self.filename):
                    self.savefile()
                else:
                    self.root.destroy()
        try:
            self.root.destroy()
        except:
            print()

    def findPrompt(self):
        def close():
            self.input.tag_remove('found', '1.0', END)
            prompt.destroy()

        def findtext():
            self.input.tag_remove('found', '1.0', END)
            findInput = findEntry.get()
            if findInput:
                idx = '1.0'
                while 1:
                    idx = self.input.search(
                        findInput, idx, nocase=1, stopindex=END, exact=False)

                    if not idx:
                        break

                    lastidx = '%s+%dc' % (idx, len(findInput))
                    self.input.tag_add('found', idx, lastidx)
                    idx = lastidx
                self.input.tag_config('found', foreground='black', background='yellow')

        def replacetext():
            findInput = findEntry.get()
            replaceInput = replaceEntry.get()
            if replaceInput and findInput:
                idx = '1.0'
                while 1:
                    idx = self.input.search(
                        findInput, idx, nocase=1, stopindex=END, exact=False)

                    if not idx:
                        break

                    lastidx = '%s+%dc' % (idx, len(findInput))

                    self.input.delete(idx, lastidx)
                    self.input.insert(idx, replaceInput)
                    idx = lastidx
                self.input.tag_config('found', foreground='black', background='yellow')

        prompt = Toplevel()
        findLabel = Label(prompt, text="Find :", font="TkHeadingFont")
        replaceLabel = Label(prompt, text="Replace :", font="TkHeadingFont")
        findEntry = Entry(prompt, width=25)
        replaceEntry = Entry(prompt, width=25)
        findButton = Button(prompt, text="Find")
        replaceButton = Button(prompt, text="Replace")

        prompt.focus_force()

        findButton.config(command=findtext)
        replaceButton.config(command=replacetext)

        prompt.title("Find And Replace")
        prompt.geometry("250x100")
        findLabel.grid(row=3, column=2)
        replaceLabel.grid(row=4, column=2)
        findEntry.grid(row=3, column=3)
        replaceEntry.grid(row=4, column=3)
        findButton.grid(row=5, column=3)
        replaceButton.grid(row=6, column=3)

        prompt.protocol("WM_DELETE_WINDOW", close)

    def run(self):
        self.root.mainloop()


notepad = text_editor()
notepad.run()
