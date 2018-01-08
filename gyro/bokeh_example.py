# myplot.py
from __future__ import print_function
from bokeh.plotting import figure, curdoc
from bokeh.driving import linear, count
import random


import serial
import json
from gyro.device import Board
import numpy as np
import pyqtgraph as pg


board = Board(firmware="teeti-MPU9250-firmware")
print(board)
# board.upload()

board.connect()

p = figure(plot_width=400, plot_height=400)
r1 = p.line(np.arange(100), np.zeros(100), color="firebrick", line_width=2)
r2 = p.line(np.arange(100), np.zeros(100), color="navy", line_width=2)

ds1 = r1.data_source
ds2 = r2.data_source


@count()
def update(step):

    ds1.data['y'] = board.read_z()
    # ds1.data['y'].append(random.randint(0,100))
    # ds2.data['x'].append(step)
    # ds2.data['y'].append(random.randint(0,100))
    ds1.trigger('data', ds1.data, ds1.data)
    ds2.trigger('data', ds2.data, ds2.data)

curdoc().add_root(p)

# Add a periodic callback to be run every 500 milliseconds
curdoc().add_periodic_callback(update, 100)


