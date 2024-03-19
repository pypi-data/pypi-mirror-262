"""
yaml2md - Galaxie YAML to MarkDown utility
"""

from argparse import ArgumentParser
from enum import Enum
from re import sub

from glxdocs.libs.file import File


class State(Enum):
    """
    State class, consist of an ``Enum`` class heritage and a set of constants

    where: TEXT=0 and YAML=1
    """
    TEXT = 0
    YAML = 1


class Yaml2Md:
    """
    Yaml2Md class
    """

    def __init__(self):
        self.file_input = File()
        self.file_output = File()
        self.file_output.mode = "w"
        self.strip_regex = r"\s*(:?\[{3}|\]{3})\d?$"
        self.__state = None
        self.state = None

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value: State):
        if value is None:
            value = State.TEXT

        if value and not isinstance(value, State):
            raise TypeError("state property 'value' must be int type or None")
        if self.state != value:
            self.__state = value

    def convert_lines(self, lines):
        """
        That function is call by ``convert_file`` function, the hard work is done by it function:

        The ``lines`` argv will be estimated inside a loop, the text will be clean, and commentary estimated for get
        the Markdown information.

        :param lines: A lines list to convert in to Yaml
        :type lines: list
        :return: Converted lines iterator
        :rtype: str
        """
        self.state = State.TEXT
        last_text_line = ""
        for line in lines:
            # Remove any white spaces at the end of the string
            line = line.rstrip()

            # Cleaning
            if not line:
                # do not change state if the line is empty
                pass
            elif line == "---":
                # ignore yaml tags
                pass

            # Yaml or not Yaml what is the question
            elif line.startswith("# ") or line == "#":
                if self.state != State.TEXT:
                    yield "```"
                    yield ""

                line = last_text_line = sub(self.strip_regex, "", line)[2:]
                self.state = State.TEXT
                yield line
            else:
                if self.state != State.YAML:
                    if not last_text_line.endswith("```"):
                        yield ""
                        yield "``` yaml"

                line = sub(self.strip_regex, "", line)
                yield line
                self.state = State.YAML

        # If last line was a YAML section open
        if self.state == State.YAML:
            if not last_text_line.endswith("```"):
                yield "```"

    def convert_file(self) -> None:
        """
        After have set ``file_input.path`` ``file_output.path`` properties value, that function can be call.

        The function open input file as read only and output file with write permission.
        For each line inside input file a conversion is done and write in to output file.

        Note: If the output file do not exist it will be created, but the parent directory must exist.
        """
        with self.file_input.smart_open() as input_file, self.file_output.smart_open() as output_file:
            for line in self.convert_lines(input_file.readlines()):
                output_file.write(line.rstrip())
                output_file.write("\n")
                output_file.flush()


def main():  # pragma: no cover
    """
    The entry point of ``yaml2md``, it is use by setup-tools as console script.
    Tha function define the CLI parser and the Yaml2Md class object
    """
    parser = ArgumentParser(
        description="Galaxie Docs - YAML to Markdown", epilog="Developed under GPLv3+ license"
    )
    parser.add_argument(
        "source_file", metavar="source_file",
        nargs='?',
        help="A pathname of an YAML input file. "
             "If no file operands are specified, the standard input shall be used. "
             "If a file is '-', the utility read from the standard input at that point in the sequence."
    )
    parser.add_argument(
        "target_file", metavar="target_file",
        nargs='?',
        help="A pathname of an target file. "
             "If no file operands are specified, the standard output shall be used. "
             "If a file is '-', the utility write to the standard output at that point in the sequence."
    )
    parser.add_argument(
        "--strip-regex",
        metavar="strip_regex",
        default=r"\s*(:?\[{3}|\]{3})\d?$",
        help=(
            "Regex which will remove everything it matches. "
            "Can be used e.g. to remove fold markers from headings. "
            "Example to strip out [[[,]]] fold markers use: "
            r"'\s*(:?\[{3}|\]{3})\d?$'. "
            "Check the README for more details."
        ),
    )

    args = parser.parse_args()

    yaml2md = Yaml2Md()
    yaml2md.file_input.path = args.source_file
    yaml2md.file_output.path = args.target_file
    yaml2md.strip_regex = rf"{args.strip_regex}"

    yaml2md.convert_file()
