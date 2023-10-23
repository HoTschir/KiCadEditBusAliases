# KiCadEditBusAliases
Simple tool for easy editing of Bus Aliases across hierarchical sheets.

## installation
* install python3
* install kiutils
  ```
  pip3 install kiutils
  ```
Copy KiCadEditBusAliases.py to a directory, your PATH-variable points to.

## Usage
* Pass root schematic file of your KiCad project as a parameter for the script.
  ```
  KiCadEditBusAliases.py <eeschema_file_name.kicad_sch>
  ```
* Do the changes you want (see pictures below).
* Press "save and exit" to make changes permanent to *.kicad_sch files.
  (Please keep in mind: If one Bus Alias is _not_ assigned to any file, it will _not_ be saved in any way.) 

## Screen shots
![Main window](KicadEditBusAliases_Main_edited.png) Main window

![Window to edit members of a Bus Alias](KicadEditBusAliases_Members_edit.png) Window to edit members of a Bus Alias

![Insert a new Bus Alias](KicadEditBusAliases_NewBus.png) Insert a new Bus Alias


