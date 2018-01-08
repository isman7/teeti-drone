from __future__ import print_function
import serial
from gyro.device import Board
import numpy as np

board = Board(firmware="teeti-MPU9250-firmware")
print(board)
board.upload()

board.connect()

with serial.Serial(board.upload_port, 38400) as com:
    log_buffer = ""

    z = np.zeros(100, dtype=float)

    while True:
        board.read_z()

