

import re


sample = "int * __usercall Moho::UNIT_IssueCommand@<eax>(moho_set *a2@<edx>, int moho, Moho::SSTICommandIssueData *a4, char a5)"


REGISTERS_32 = {
    "eax": "a",
    "ebx": "b",
    "ecx": "c",
    "edx": "d",
    "esi": "S",
    "edi": "D",
}


FUNC_R = r"^([a-zA-Z0-9\:_]+\*?\s+\*?)\s*__user(call|purge)\s+([a-zA-Z0-9\:_]+)(@<([a-z0-9]+)>)?\((.+)\)$"

FUNC_ARGS = re.compile(
    r"((([a-zA-Z0-9\:_]+\*?\s+\*?)([a-zA-Z0-9_]+)(@<([a-z0-9]+)>)?)(\,\s+)?)")


def check_register(reg: str):
    if reg != "" and reg not in REGISTERS_32:
        raise Exception(f"unknown register {reg}")


class Arg:

    def __init__(self, arg_data) -> None:
        self.type: str = arg_data[2].replace(" ", "")
        self.name: str = arg_data[3]
        self.register: str = arg_data[5]

        check_register(self.register)


class Function:

    def __init__(self, s) -> None:
        match = re.match(FUNC_R, s)
        if match is None:
            raise Exception("Invalid input string")
        groups = match.groups()
        self.type: str = groups[0].replace(" ", "")
        self.need_stack_clear: bool = groups[1] == "call"
        self.name: str = groups[2]
        self.register: str = groups[4]

        check_register(self.register)

        args = groups[5]
        self.args: list[Arg] = [Arg(arg) for arg in FUNC_ARGS.findall(args)]

    def convert_args(self) -> str:
        return ", ".join([f"{arg.type} {arg.name}" for arg in self.args])

    def make_output(self) -> str:
        if self.type == "void":
            return ""
        if self.register == "":
            raise Exception("Return register must be specified")
        return f"\"={REGISTERS_32[self.register]}\" (__result)"

    def make_input(self) -> str:
        return ", ".join([f"[{arg.name}] \"{REGISTERS_32[arg.register] if arg.register != "" else "g"}\" ({arg.name})" for arg in self.args])

    def make_instructions(self) -> str:
        instructions = []
        for arg in self.args[::-1]:
            if arg.register == "":
                instructions.append(f"\"push %[{arg.name}];\"")
        instructions.append("\"call ADDRESS;\"")
        if self.need_stack_clear:
            stack_args = len([arg for arg in self.args if arg.register == ""])
            if stack_args != 0:
                instructions.append(f"\"add esp, 0x{stack_args*4:x}\"")

        return "\n".join(instructions)

    def make_asm(self) -> str:
        return f"asm(\n{self.make_instructions()}\n: {self.make_output()}\n: {self.make_input()}\n:\n);"

    def make_header(self) -> str:
        return f"{self.type} {self.name} ({self.convert_args()})"

    def make_body(self) -> str:
        if self.type == "void":
            return f"{{\n{self.make_asm()}\n}}"

        return f"{{\n{self.type} __result;\n{self.make_asm()}\nreturn __result;\n}}"

    def convert(self) -> str:
        return f"{self.make_header()}\n{self.make_body()}"


def main(s: str):
    fn = Function(s)
    print(fn.convert())


if __name__ == "__main__":
    main(input().strip())
