from __future__ import print_function
import os
import configparser as cfgp
from platformio.commands.run import cli
import pprint
import StringIO
from click.testing import CliRunner

submodule_path = os.path.dirname(__file__)
module_path = os.path.dirname(submodule_path)
abs_path = os.path.dirname(module_path)


class Board(object):
    def __init__(self, **kwargs):

        self.firmware_path = kwargs.pop("firmware_path", None)
        if not self.firmware_path:
            self.firmware = kwargs.pop("firmware", "sample")
            self.firmware_path = os.path.join(module_path, "firmwares", self.firmware)
        print(self.firmware_path)
        self.env_parser = cfgp.ConfigParser()
        self.pio_cli = cli

        INI_FILE_PATH = os.path.join(self.firmware_path, "platformio.ini")

        if os.path.isfile(INI_FILE_PATH):
            with open(INI_FILE_PATH, "r") as pio_ini:
                self.env_parser.read_file(pio_ini)

        else:
            print("No platformio.ini file found, upoload will fail.")

    def __repr__(self):
        properties_dict = {key: dict(item) for key, item in dict(self.env_parser).items()}
        # TODO custom better pretty print fuction...
        repr_stream = StringIO.StringIO()
        pretty_printer = pprint.PrettyPrinter(indent=4, stream=repr_stream)
        pretty_printer.pprint(properties_dict)
        repr_stream.seek(0)
        return "Board with build project: \n" + repr_stream.read()

    def upload(self):

        CURRENT_PATH = os.path.abspath(os.curdir)
        os.chdir(self.firmware_path)
        # TODO find what Python is CliRunner using.
        runner = CliRunner()
        result = runner.invoke(self.pio_cli, ["--target", 'upload'])
        print(result.output)
        os.chdir(CURRENT_PATH)



