#[Class]:
	#MAIN
#[Name]:
	#templateAlphaGUI
#[Author]:
	#Kevin Kandzorra
#[DateUpdated]:
	#31/07/2020
#[Purpose]:
	#The base framework for the ModularToolkit. All scripts will be seen and run from here

#Notes:
"""
This is the alpha code for the application. This will generate the base window, tabs, lists and buttons
according to the size and files found within the "MODULES" directory, and its sub directories.

By doing so, users can add new directories with folders, and the code will adapt to the new size and 
content found within. 

All scriptModules, within their respectove subDirectory, will need to be run using a TOP-WINDOW function
to avoid clashing with the main window of the application. 
"""

"""////////////////////
		Setup
////////////////////"""

#Imports:
import os											#Gives access to OS 
from os import listdir										#Gathering directory information
from os.path import isfile, isdir, join								#File checking 

import tkinter as tk										#Main TK library to control GUI
from tkinter import ttk										#Notebook widget and ComboBoxes
from tkinter.filedialog import askopenfilename, asksaveasfilename				#Command for opening/saving files

import pathlib
from pathlib import Path									#Used to gather the path and its parent

#Handlers/Functions:

def getBtnRunList(tList,dList):
	#This will generate the RunButtons for each tab based on the tabList(tList) and directory list (dList)
	brList = [ttk.Button(tList[x],text="Run",command=runScript) for x in range(len(dList))]
	return brList

def getComboboxList(tList,cOptions,dList):
	#This will generate ttkCombobox objects for the given tabList(tList), comboOptions(cOptions) for the given size of the directory list (dList)
	cbList = [ttk.Combobox(tList[x],value=cOptions[x],justify="left") for x in range(len(dList))]
	return cbList
	
def getCurrentDir():
	#This will grab the current directory name and return it
	dir = os.path.dirname(os.path.realpath(__file__))
	return dir

def getDirList(inputDir):
	#Get a specific list of directories from the given location (inputDir)
	directoryList = [dir for dir in os.listdir(inputDir) if os.path.isdir(os.path.join(inputDir,dir))]
	return directoryList
	
def getTabList(inputDir):
	#This will generate ttkFRAME tab for each object in the given directory list (inputDir)
	tList = [ttk.Frame(tabControl,relief=tk.SUNKEN) for x in range(len(inputDir))]
	return tList
	
def getPyFiles(dir):
	#This will filter all the .py files from within a given directory (dir)
	pyFiles = [ file for file in listdir(dir) if file.endswith(".py") if isfile(join(dir,file)) ]
	return pyFiles
	
def gridComboBox(cbList):
	#This will be used to GRID all the comboboxes to their respective tab
	for x in range(len(cbList)):
		cbList[x].grid(row=0,column=0)

def gridRunBtn(btnList):
	#This will be used to GRID all the runButtons to their respective tab
	for x in range(len(btnList)):
		btnList[x].grid(row=1,column=0,sticky="w")

def selected(event,x,dir):
	#Whenever a combobox selects a new file, this value will be changed to that name, and return its value
	global currentFileValue
	currentFileValue = "Modules/"+str(dir)+"/"+str(comboBoxList[x].get())
	return(currentFileValue)

def runScript():
	print("Running: "+currentFileValue)
	exec(open(str(currentFileValue)).read())

def startToolkit():
	root.mainloop()

def close(name):
	name.destroy()
	#exec(close(str(currentFileValue)))	

#Variables:
searchDir = 'Modules'							#This is the main ModularToolkit folder which will hold all modules for scripts
searchDirSlash = 'Modules/'						#Main folder name with a "/" character for indepth searching
dirList = []								#List holding all "Modules" names
dirList = getDirList(searchDir)						#Executing command to fill with Modules
bindVal = 0								#This will be used as a place holder, to bind the correct comboBox object to its function (selected)



#Windows:
root = tk.Tk()								#Main window, this is the parent widget
root.title("Modular Toolkit - Alpha")					#The title you see on the TOP-LEFT when running
root.geometry('350x150')						#Starting size of the applicaiton
root.rowconfigure(0,minsize=100,weight=1)				#Minimum row configuration (Stretches Horizontally, stacks vertically)
root.columnconfigure(0,minsize=100,weight=1)				#Minimum column configuration (Stretched vertically, stacks horizontally)
	
	

#TabControl:
tabControl = ttk.Notebook(root)						#The parent tab controller. This will hold all the generated tabs
	
	
	
#Frames/Tabs:
tabList = []								#List holding all ttkFrame objects (aka:Tabs)
tabList = getTabList(dirList)						#Executing command to fill with ttkFrame tabs

for x in range(len(tabList)):
	#This sets the tabs into the tabControl parent, with the names of the modules found in the dirList
	tabControl.add(tabList[x], text=dirList[x])


	
#ComboBoxes:
comboOptions = []							#List which will contain all "options", which will be all .py files in a directory
comboOptions = [[] for x in range(len(dirList))]			#Will generate a List-of-Lists, since there will be multiple files in multiple directories
	
for x in range(len(dirList)):
	#This loop sets all the .py files filtered, into the respective list
	comboOptions[x] = getPyFiles(searchDirSlash+dirList[x])

	

comboBoxList = []							#List which will contain ttkComboBox objects that will hold the options
comboBoxList = getComboboxList(tabList,comboOptions,dirList)		#Executing command to fill with ttkComboBox objects

for x in comboBoxList:
	#This loop binds all the comboBoxList objects to the command SELECTED() with their respective event and bindOption
	x.bind("<<ComboboxSelected>>", lambda event, cur=bindVal, dir=dirList[bindVal]: selected(event,cur,dir))
	bindVal +=1
	
	

#Labels:
	#Renaming tabs and buttons/etc...

	
	

#Buttons:

btnRunList = []								#List holding all ttkButton objects
btnRunList = getBtnRunList(tabList,dirList)				#Executing command to fill with ttkBtn objects




"""////////////////////
		MainCode
////////////////////"""
#Layout

tabControl.grid(sticky="nesw",row=0,column=0)				#Grid the main parent tab onto Root
gridComboBox(comboBoxList)						#Grid comboBoxList to their parents
gridRunBtn(btnRunList)							#Grid btnRUnList to their parents

startToolkit()								#Loop required to being displaying and running the applicaiton 
