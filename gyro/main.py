from __future__ import print_function
import serial
import json
from gyro.device import Board


board = Board(firmware="teeti-MPU9250-firmware")
print(board)
board.upload()

with serial.Serial(board.upload_port, 38400) as com:
    log_buffer = ""
    while True:
        this_line = com.readline()
        # this_line = this_line.decode('utf-8')
        try:
            if log_buffer:
                print(log_buffer)
                log_buffer = ""
            json_from_serial = json.loads(this_line)
            print(json_from_serial)

        except ValueError:
            if this_line is not "\n":
                log_buffer += this_line.replace("\n", "")

        except Exception as e:
            print(e)

