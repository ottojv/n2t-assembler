from parser import Parser
from parser import CommandType
from code import Code
from symbol_table import SymbolTable
import sys


class Assembler:
    def __init__(self, asm, hack):
        self.address = 0
        self.parser = Parser(asm)
        self.code = Code()
        self.symbol_table = SymbolTable()
        try:
            self.hackfile = open(hack, "w")
        except:
            self.parser.close()
            print("Error when opening " + hack + " for writing")
            sys.exit(1)

    def first_pass(self):
        while self.parser.hasMoreCommands():
            self.parser.advance()
            if self.parser.commandType() == CommandType.L_COMMAND:
                if not self.symbol_table.contains(self.parser.symbol()):
                    self.symbol_table.addEntry(
                        self.parser.symbol(), self.address)
            else:
                self.address += 1  # ROM position

    def second_pass(self):
        self.parser.restart()
        self.address = 16  # RAM position

        while self.parser.hasMoreCommands():
            self.parser.advance()
            if self.parser.commandType() == CommandType.A_COMMAND:
                if not self.parser.symbol().isdigit():
                    if not self.symbol_table.contains(self.parser.symbol()):
                        self.symbol_table.addEntry(
                            self.parser.symbol(), self.address)
                        self.address += 1
                    self.hackfile.write("{0:016b}\n".format(
                        self.symbol_table.GetAddress(self.parser.symbol())))
                else:
                    self.hackfile.write("{0:016b}\n".format(
                        int(self.parser.symbol())))
            elif self.parser.commandType() == CommandType.C_COMMAND:
                self.hackfile.write("111" + self.code.comp(self.parser.comp()) +
                                    self.code.dest(self.parser.dest()) +
                                    self.code.jump(self.parser.jump()) + "\n")
        self.close()

    def close(self):
        self.parser.close()
        self.hackfile.close()


if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: ./assembler.py asmfile [hackfile]")
    sys.exit(1)

asmfile = sys.argv[1]
try:
    hackfile = sys.argv[2]
except IndexError:
    hackfile = asmfile.split("/")[-1].split(".")[0] + ".hack"

assembler = Assembler(asmfile, hackfile)
assembler.first_pass()
assembler.second_pass()
print(asmfile + " has been compiled to " + hackfile)
