from __future__ import print_function

from tornado.ioloop import IOLoop
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.server.server import Server
from bokeh.models import Slider
from bokeh.plotting import figure
from bokeh.driving import count
from bokeh.layouts import gridplot

import numpy as np
import pandas as pd
from gyro.device import Board


io_loop = IOLoop.current()

board = Board(firmware="teeti-MPU9250-firmware")
print(board)
board.upload()

board.connect()


def modify_doc(doc):
    plt_1 = figure(plot_width=400, plot_height=400)
    plt_2 = figure(plot_width=400, plot_height=400)
    plt_3 = figure(plot_width=400, plot_height=400)

    r1 = plt_1.line(np.arange(100), np.zeros(100), color="firebrick", line_width=2)
    plt_1.line(np.arange(100), np.zeros(100) + 1, color="black", line_width=1)
    plt_1.line(np.arange(100), np.zeros(100) - 1, color="black", line_width=1)

    r2 = plt_2.line(np.arange(100), np.zeros(100), color="navy", line_width=2)
    plt_2.line(np.arange(100), np.zeros(100) + 1, color="black", line_width=1)
    plt_2.line(np.arange(100), np.zeros(100) - 1, color="black", line_width=1)

    r3 = plt_3.line(np.arange(100), np.zeros(100), color="green", line_width=2)
    plt_3.line(np.arange(100), np.zeros(100) + 1, color="black", line_width=1)
    plt_3.line(np.arange(100), np.zeros(100) - 1, color="black", line_width=1)

    ds1 = r1.data_source
    ds2 = r2.data_source
    ds3 = r3.data_source

    window_size = 5

    # slider = Slider(start=0, end=25, value=window_size, step=1)
    #
    # doc.add_root(column(slider, the_plot))

    @count()
    def update(t):

        updated_dataframe = board.read()

        # z = pd.Series.rolling(updated_dataframe["acc"]["z"], window=slider.value).mean()

        ds1.data['y'] = np.array(updated_dataframe["acc"]["x"])
        ds2.data['y'] = np.array(updated_dataframe["acc"]["y"])
        ds3.data['y'] = np.array(updated_dataframe["acc"]["z"])

        ds1.trigger('data', ds1.data, ds1.data)
        ds2.trigger('data', ds2.data, ds2.data)
        ds3.trigger('data', ds3.data, ds3.data)

    grid = gridplot([[plt_1, plt_2, plt_3]])
    doc.add_root(grid)

    # Add a periodic callback to be run every 500 milliseconds
    doc.add_periodic_callback(update, 100)

bokeh_app = Application(FunctionHandler(modify_doc))

server = Server({'/': bokeh_app}, io_loop=io_loop)
server.start()

if __name__ == '__main__':
    print('Opening Bokeh application on http://localhost:5006/')
    io_loop.add_callback(server.show, "/")
    io_loop.start()