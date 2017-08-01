from subprocess import Popen, PIPE
import os
import configparser as cfgp

submodule_path = os.path.dirname(__file__)
module_path = os.path.dirname(submodule_path)
abs_path = os.path.dirname(module_path)


class Board(object):
    def __init__(self, **kwargs):

        self.firmware_path = kwargs.pop("firmware_path", None)
        if not self.firmware_path:
            self.firmware = kwargs.pop("firmware", "Serial_to_I2C")
            self.firmware_path = os.path.join(module_path, "firmwares", self.firmware)
        print(self.firmware_path)
        self.environment = kwargs.pop("environment", "uno")
        self.upload_port = kwargs.pop("upload_port", None)
        self.env_parser = cfgp.ConfigParser()
        if not self.upload_port:
            try:
                with open(os.path.join(self.firmware_path, "platformio.ini"), "r") as pio_ini:
                    self.env_parser.read_file(pio_ini)

                self.upload_port = self.env_parser.get("env:{}".format(self.environment), "upload_port")

            except Exception as e:
                print("No configurable upload_port", e)

    def upload(self, **kwargs):

        folder_path = kwargs.pop("firmware_path", self.firmware_path)
        env = kwargs.pop("environment", self.environment)

        arguments = [
            "platformio", "run",
            "-t", "upload",
            "-d", folder_path,
            "-e", env,
        ]

        platformio_process = Popen(arguments, stdout=PIPE)
        platformio_process.wait()
        out = platformio_process.stdout.read()
        platformio_process.stdout.close()
        return out

    def check(self):
        # TODO check that port exists, etc.
        pass



