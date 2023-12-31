# KiCadEditBusAliases
Simple tool for easy edit of Bus Aliases across hierarchical sheets.

It is easy, because of:
* edit bus member names within a text-box (text-editor-like)
* assign/remove Bus Aliases to/from sheet by tick/untick a checkbox

It prevents you from ERC-error:
  ```
  [bus_definition_conflict]: Bus alias NAME has conflicting definitions on file1.kicad_sch and file2.kicad_sch
  ```
because of keeping the same bus members in alphabetical order for all assigned files.

Tested with: ![](https://img.shields.io/badge/V6-%20KiCad-blue)

## Installation
* install python3
* install kiutils
  ```
  pip3 install kiutils
  ```
Copy KiCadEditBusAliases.py to a directory, your PATH-variable points to.

## Usage
* Close and _!backup!_ your KiCad project.
* Pass root schematic file of your KiCad project as a parameter for the script.
  ```
  KiCadEditBusAliases.py <eeschema_file_name.kicad_sch>
  ```
* Do the changes you want (see pictures below). Don't forget to assign each and every Bus Alias to at least one file. Otherwise it will _not_ be saved.
* Press "save and exit" to make changes permanent to *.kicad_sch files.
* Open your KiCad project and continue editing using eeschema.

## Screen shots
![Main window](KicadEditBusAliases_Main_edited.png) Main window

![Window to edit members of a Bus Alias](KicadEditBusAliases_Members_edit.png) Window to edit members of a Bus Alias

![Insert a new Bus Alias](KicadEditBusAliases_NewBus.png) Insert a new Bus Alias


