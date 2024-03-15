
from dataclasses import dataclass
import logging
import typing


@dataclass(init=False)
class SprinkoCtx:
    code : typing.Dict[int, str]
    args : typing.List[typing.Dict[str, typing.Any]]
    gargs : typing.ClassVar[typing.Dict[str, typing.Any]] = {}

    @staticmethod
    def __parse_args(code : str):
        parsed = {}
        splitted = code.split(",")
        for raw in splitted:
            raw = raw.strip()
            x, y = raw.split("=")
            parsed[x] = eval(y, SprinkoCtx.gargs)

        return parsed

    def __init__(self, *codes) -> None:
        self.code = {}
        self.args = []
        self.gargs = {}
        index = 0

        for code in codes:
            if index >= len(self.args):
                self.args = self.args + [{} for _ in range(index - len(self.args))]

            code :str
            if code.startswith("[") and code.endswith("]"):
                self.args.append(SprinkoCtx.__parse_args(code))
            elif code.startswith("{") and code.endswith("}"):
                self.gargs.update(SprinkoCtx.__parse_args(code))
            else:
                self.code[index] = code
                index += 1

            if index >= len(self.args):
                self.args = self.args + [{} for _ in range(index - len(self.args))]
                
    def run(self):
        for index, code in sorted(self.code.items(), key=lambda x: x[0]):
            logging.debug(f"executing {index}")
            exec(code, self.gargs, self.args[index])