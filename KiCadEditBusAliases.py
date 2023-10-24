#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  
#  KiCad_EditBusAliases.py
#
#  Copyright 2023 Horst Tschirke
#  
#  this has been tested with eeschema files of KiCad version 6.0
# 
#  2023-10-20  v0.1   - - start developing, output of existing configuration in terminal
#  2023-10-22  v0.2   - - gui
#                       - complete load-edit-save
#                       - language to English
#  2023-10-23  v0.3   - - BusAliases window modal visible - position: besides main window
#                       - remove debugging code
#                       - new BusAlias-Button
#  2023-10-23  v0.4   - - first published version
#  2023-10-24  v0.5   - - bugfix: in main window: member count not updated, when members-window is closed

#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#  
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the  nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  


import os
from tkinter import Tk, Label, Canvas, Button, Text, Frame, Checkbutton, BooleanVar, Toplevel, NONE, END
from pathlib import Path
import operator

from tkinter import simpledialog

from kiutils.schematic import Schematic       
from kiutils.items.schitems import BusAlias   

ListOfFilenames = []
ListOfBusAliases = []


class clBusAlias():

    def __init__(self, name):
        self.name = name
        self.members = []
        self.assignedto = []
        self.keep_sorted = 1

    def __str__(self):
        return self.name

    def append_member(self,member):
      if not member in self.members:
        self.members.append(member)
        if (self.keep_sorted == 1):
          self.members.sort()

    def append_assignedto(self,fn):
      if not fn in self.assignedto:
        self.assignedto.append(fn)
        if (self.keep_sorted == 1):
          self.assignedto.sort()
    
    def remove_assignedto(self,fn):
      if fn in self.assignedto:
        self.assignedto.remove(fn)



class BusCheckbox(Checkbutton):
  def __init__(self, parent, ba, fn):
    Checkbutton.__init__(self, parent)
    self.ticked = BooleanVar()  
    self['variable'] = self.ticked
    self['indicatoron'] = True
    self['command'] = self.on_checkbutton_toggle
    self.ba = ba
    self.fn = fn
      
  def on_checkbutton_toggle(self):
    if self.ticked.get():
      self.ba.append_assignedto(self.fn)
    else:
      self.ba.remove_assignedto(self.fn)


def LoadDatafromFile(fn):
  print("load "+fn)

  ThisSchematic = Schematic().from_file(fn)
  
  if not fn in ListOfFilenames:
    ListOfFilenames.append(fn)

  for ThisBusAlias in ThisSchematic.busAliases:
  
    if not any(x.name == ThisBusAlias.name for x in ListOfBusAliases):
     
      ba = clBusAlias(ThisBusAlias.name)
     
      ba.assignedto.append(fn)
     
      for member in ThisBusAlias.members:
        ba.append_member(member)
      ListOfBusAliases.append(ba)
    else:
      ba = next((x for x in ListOfBusAliases if x.name == ThisBusAlias.name), None)
      ba.append_assignedto(fn)
      for member in ThisBusAlias.members:
        if not member in ba.members:
          ba.members.append(member)

 
  for HSheet in ThisSchematic.sheets:
    if not HSheet.fileName.value in ListOfFilenames:  
                                                      
      if os.path.exists(HSheet.fileName.value):
        LoadDatafromFile(HSheet.fileName.value)
      else:
        print("File: "+HSheet.fileName.value+" not found, skipped")                                    
         
def GetBaNameStr(ba):
  return ba.name+" ("+str(len(ba.members))+")"
  
def BusWindow(event, canvas, text, ba, posX, posY):

  def save_member_changes(aliaslist):
    ba.members.clear()
    for alias in aliaslist:
       if (alias != ""):
         ba.append_member(alias)
    top.destroy()
    canvas.itemconfig(text, text=GetBaNameStr(ba))


  top = Toplevel()
  top.title("BusAlias: "+ba.name)
  top.geometry("290x640")  
  lbl = Label(top, text="defined bus members:")
  lbl.place(x=20, y=10)
  txt = Text(top, height="32", width="30", wrap=NONE)  
  txt.place(x=20, y=40)
  for m in ba.members:
    txt.insert(END,m+"\n")
  
    
  cancelBtn = Button(top, text="cancel", command=top.destroy)
  cancelBtn.place(x=20, y=600)
  okBtn = Button(top, text="take changes", width=15, command=lambda: save_member_changes(txt.get('1.0', END).splitlines()))
  okBtn.place(x=135, y=600)
  
  top.geometry("+"+str(posX)+"+"+str(posY))
  top.wait_visibility()
  top.grab_set()
    
     
def saveBusaliases(): 
 
  for fn in ListOfFilenames:
    ThisSchematic = Schematic().from_file(fn)  
    ThisSchematic.busAliases.clear()
    ThisSchematic.to_file(fn)
 
  for ba in ListOfBusAliases:
    for fn in ba.assignedto:
      ThisSchematic = Schematic().from_file(fn)  
      ThisBa = BusAlias(ba.name, ba.members)
      ThisSchematic.busAliases.append(ThisBa)
      ThisSchematic.to_file(fn)
 
    
aw = 250             
ah = 160             
dw = 60              
dh = 40              
guiposX = 200
guiposY = 80

def main(args):

  def setGuiGeometry(window, lenBA, lenFN):
    guiwidth = aw+dw*lenBA+20
    guiheight = ah+dh*lenFN+120
    window.geometry(str(guiwidth)+"x"+str(guiheight)+"+"+str(guiposX)+"+"+str(guiposY))
    window.update()
        
  def do_save_and_exit(): 
    saveBusaliases()
    gui.destroy()

  def createCheckbox(parent, ba, fn, i, k): 
    cb = BusCheckbox(parent, ba, fn) 
    cb.parent = parent
    cb.place(x = aw-5+(dw)*k, y=ah+30+(dh)*i)  
    if fn in ba.assignedto:
      cb.select()

  def createBusCanvas(parent, ba, nbr, posX, posY):
    h = ah-10
    w = dw-10
    canvas = Canvas(parent, width = w, height = h)
    canvas.grid(row = 0, column = 0)
    canvas.place(x = aw+(dw)*nbr, y=20)
    canvastxt = canvas.create_text(6, h-10, text = GetBaNameStr(ba), angle = 80, anchor = "w",  fill = 'blue')  
    canvas.bind("<Button-1>", lambda event: BusWindow(event, canvas, canvastxt, ba, posX, posY))
      
  def createFileCanvas(parent, fn, nbr):
    h = dh-10
    w = aw-10
    basisfn = Path(fn).stem 
    canvas = Canvas(parent, width = w, height = h)
    canvas.grid(row = 0, column = 0)
    canvas.place(x = 20, y=ah+20+(dh)*nbr)
    canvas.create_text(w-40, h-10, text = basisfn, angle = 0, anchor = "e")  
    
  def createMatrix(parent):
    matrix = Frame(parent)
    matrix.place(x=5, y=5, width=parent.winfo_width()-10, height=parent.winfo_height()-60)
    
   
    i = 0
    for fn in  ListOfFilenames:
     
      createFileCanvas(matrix, fn, i)
      k = 0
      for ba in  ListOfBusAliases:
        createCheckbox(matrix, ba, fn, i, k)
        k += 1
      i += 1
   
    k = 0
    for ba in  ListOfBusAliases:
      createBusCanvas(matrix, ba, k, guiposX+parent.winfo_width()+10, guiposY)
      k += 1
   
    return matrix
      
  def NewBusAlias(parent, matrix, btn):
    ba_name =simpledialog.askstring("new Busalias", "Give the name of new BusAlias:", parent=parent) 
    if (ba_name != None):               
      if (len(ba_name) > 0):            
        ba = clBusAlias(ba_name)
        ListOfBusAliases.append(ba) 
        matrix.destroy()
        setGuiGeometry(parent, len(ListOfBusAliases), len(ListOfFilenames))
        matrix = createMatrix(parent) 
        btn.tkraise()     
    return matrix
       
    
  if len(args) < 2:
    print("call this script: KiCadEditBusAliases.py <eeschema_file_name.kicad_sch>")
  else:
    if os.path.exists(args[1]):
      LoadDatafromFile(args[1])
    else:
      print("File: "+args[1]+" not found, exit")                 
      quit()
    
  ListOfFilenames.sort()      
  ListOfBusAliases.sort(key = operator.attrgetter('name'))

 
  
 
  gui = Tk()
  gui.title("BusAliases of "+args[1])
  setGuiGeometry(gui, len(ListOfBusAliases), len(ListOfFilenames))
   
  matrix = createMatrix(gui)

  guicancel = Button(gui, text="close without saving", width=25, command=gui.destroy)  
  guicancel.place(x=75, y=gui.winfo_height()-50)
  
  guisaveexit = Button(gui, text="save and exit", width=25, command=do_save_and_exit)  
  guisaveexit.place(x=320, y=gui.winfo_height()-50)
  
  nbabtn = Button(gui, text="new BusAlias", width=15, command=lambda: NewBusAlias(gui, matrix, nbabtn))  
  nbabtn.place(x=80, y=ah-30)
  
  gui.mainloop()

  return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
