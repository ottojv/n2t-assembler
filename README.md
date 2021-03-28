# ASM Assembler

## About
This was built for the Nand 2 Tetris course.

Translates .asm (assembly machine language) files following the standard from the course into .hack (hack binary code) files.
Won't check for spelling errors but will translate correct programs correctly.

## Usage
```shell
python assembler.py asmfile [hackfile] # if hackfile is ommited the program will create a new file 
                                       # with the same name as the asmfile 
                                       # ending with .hack in the folder the script was run on
```
