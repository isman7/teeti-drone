from __future__ import print_function
import os
import configparser as cfgp
from platformio.commands.run import cli as run_cli
from platformio.commands.device import cli as device_cli
import pprint
import StringIO
import json
import serial
import numpy as np
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


        config_file_path = os.path.join(self.firmware_path, "platformio.ini")

        if os.path.isfile(config_file_path):
            with open(config_file_path, "r") as pio_ini:
                self.env_parser.read_file(pio_ini)

        else:
            raise Exception("No platformio.ini file found, upoload will fail.")

        self.run_cli = run_cli
        self.device_cli = device_cli
        self.runner = CliRunner()
        # self.runner_result = None

        self.runner_result = self.runner.invoke(self.device_cli, ["list", "--json-output"])
        devices_json = json.loads(self.runner_result.output)
        self.upload_port = devices_json[0]["port"]

        self.com = None
        self.log_buffer = ""
        self.z = np.zeros(100, dtype=float)

    def __repr__(self):
        properties_dict = {key: dict(item) for key, item in dict(self.env_parser).items()}
        # TODO custom better pretty print fuction...
        repr_stream = StringIO.StringIO()
        pretty_printer = pprint.PrettyPrinter(indent=4, stream=repr_stream)
        pretty_printer.pprint(properties_dict)
        repr_stream.seek(0)
        return "Board with build project: \n" + \
               repr_stream.read() + "\n" + \
               "Auto-detected port: " + self.upload_port

    def upload(self):

        CURRENT_PATH = os.path.abspath(os.curdir)
        os.chdir(self.firmware_path)

        # TODO find what Python is CliRunner using.
        self.runner_result = self.runner.invoke(self.run_cli, ["--target", 'upload'])
        print(self.runner_result.output)

        os.chdir(CURRENT_PATH)

    def connect(self, **kwargs):
        com_port = kwargs.pop("com_port", self.upload_port)
        try:
            self.com = serial.Serial(com_port, 38400)
            # self.com.open()
        except IOError as e:
            self.com = None
            print("Not able to connect, please specify manually a com port. Exception: {}".format(e))

    def read_z(self):
        this_line = self.com.readline()
        # this_line = this_line.decode('utf-8')
        try:
            if self.log_buffer:
                print(self.log_buffer)
                self.log_buffer = ""
            json_from_serial = json.loads(this_line)
            print(json_from_serial)

            self.z = np.roll(self.z, 1)
            self.z[0] = json_from_serial["acc"]["z"]

        except ValueError:
            if this_line is not "\n":
                self.log_buffer += this_line.replace("\n", "")

        return self.z[::-1]
