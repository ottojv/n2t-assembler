from enum import Enum


class CommandType(Enum):
    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3


class Parser:
    def __init__(self, asm):
        self.asmfile = None
        self.current_command = None
        self.line = None
        self.command_type = None

        try:
            self.asmfile = open(asm, "r")
        except:
            print("Error when opening " + asm + " for reading")

    def hasMoreCommands(self):
        while True:
            try:
                self.line = self.asmfile.readline()
            except EOFError:
                return False

            if self.line == "":
                return False

            self.line = self.line.strip()

            if self.line.startswith("//") or self.line == "":
                continue
            else:
                if "//" in self.line:
                    self.line = self.line.split("//")[0].strip()

                return True

    def advance(self):
        self.current_command = self.line

    def commandType(self):
        if self.current_command[0] == "@":
            return CommandType.A_COMMAND
        elif self.current_command[0] == "(":
            return CommandType.L_COMMAND
        else:
            return CommandType.C_COMMAND

    def symbol(self):
        return self.current_command.strip("@()")

    def dest(self):
        if "=" in self.current_command:
            return self.current_command.split("=")[0]
        else:
            return ""

    def comp(self):
        if "=" in self.current_command:
            if ";" in self.current_command:
                return self.current_command.split("=")[1].split(";")[0]
            else:
                return self.current_command.split("=")[1]
        else:
            if ";" in self.current_command:
                return self.current_command.split(";")[0]
            else:
                return self.current_command

    def jump(self):
        if ";" in self.current_command:
            return self.current_command.split(";")[1]
        else:
            return ""

    def close(self):
        self.asmfile.close()

    def restart(self):
        self.current_command = None
        self.line = None
        self.command_type = None
        self.asmfile.seek(0)
