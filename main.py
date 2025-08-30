import os
import shutil
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

master = tk.Tk()
master.title("Find 'N Copy v0.1")

T = ''

def fileShow():
    global T
    root = tk.Tk()
    root.title("Copying Files")  
    S = tk.Scrollbar(root)
    T = tk.Text(root, height=10, width=70)
    S.pack(side=tk.RIGHT, fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    
def findNCopy():
    global T, thePath
    
    fileExtension = ext.get().strip()
    folderName = dirname.get().strip()
    
    
    if not thePath:
        messagebox.showerror("Error", "Please select a folder to search.")
        return
    
    if not fileExtension:
        messagebox.showerror("Error", "Please enter a file extension.")
        return
    
    if not folderName:
        messagebox.showerror("Error", "Please enter a folder name.")
        return
    
    if not fileExtension.startswith('*'):
        if not fileExtension.startswith('.'):
            fileExtension = '*.' + fileExtension
        else:
            fileExtension = '*' + fileExtension
    
    try:
        newPath = Path.home() / folderName
        newPath.mkdir(exist_ok=True)  
        
        fileShow()
        
        files_copied = 0
        for foldernames, subfolders, filenames in os.walk(thePath):
            folderPath = Path(foldernames)
            filesToCopy = list(folderPath.glob(fileExtension))
            for fileName in filesToCopy:
                try:
                    msg = f'Copying {fileName} to {newPath}\n'
                    T.insert(tk.END, msg)
                    T.see(tk.END) 
                    T.update()  
                    shutil.copy2(fileName, newPath) 
                    files_copied += 1
                except Exception as e:
                    errorMsg = f'Error copying {fileName}: {str(e)}\n'
                    T.insert(tk.END, errorMsg)
        
        completion_msg = f'\nCompleted! Copied {files_copied} files to {newPath}\n'
        T.insert(tk.END, completion_msg)
        messagebox.showinfo("Success", f"Copied {files_copied} files to {newPath}")
        
    except Exception as e:
        error_msg = f'Error: {str(e)}\n'
        if 'T' in globals():
            T.insert(tk.END, error_msg)
        messagebox.showerror("Error", str(e))

thePath = ''

def openFolder():
    global thePath
    selected_path = filedialog.askdirectory(
        initialdir=Path.home(), 
        title='Select folder you want to search for files'
    )
    if selected_path:  
        thePath = selected_path
        pathLabel.config(text=f"Selected: {thePath}")

menubar = tk.Menu(master)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=openFolder)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=master.quit)
menubar.add_cascade(label="File", menu=filemenu)
master.config(menu=menubar)

enterPath = tk.Label(master, text='Open the folder you want to search files')
enterPath.grid(row=0, column=0, sticky='w', padx=5, pady=5)

openButton = tk.Button(master, text='Open', command=openFolder)
openButton.grid(row=0, column=1, padx=5, pady=5)

pathLabel = tk.Label(master, text='No folder selected', fg='blue')
pathLabel.grid(row=1, column=0, columnspan=2, sticky='w', padx=5, pady=2)

enterExt = tk.Label(master, text='Enter the file extension of the files you want to copy:')
enterExt.grid(row=2, column=0, sticky='w', padx=5, pady=5)

ext = tk.Entry(master)
ext.grid(row=2, column=1, padx=5, pady=5)
ext.insert(0, "*.txt")  # Default example

enterDirname = tk.Label(master, text='Name the new folder:')
enterDirname.grid(row=3, column=0, sticky='w', padx=5, pady=5)

dirname = tk.Entry(master)
dirname.grid(row=3, column=1, padx=5, pady=5)
dirname.insert(0, "Copied_Files")  

quitButton = tk.Button(master, text='Quit', command=master.quit)
quitButton.grid(row=4, column=0, padx=5, pady=10)

findButton = tk.Button(master, text="Find and Copy", command=findNCopy)
findButton.grid(row=4, column=1, padx=5, pady=10)

master.resizable(True, True)

tk.mainloop()