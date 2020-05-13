import pandas as pd
from bokeh.plotting import figure, curdoc
from bokeh.models import HoverTool, ColumnDataSource, DatetimeTickFormatter, DatePicker
from bokeh.layouts import column
from bokeh.models.widgets import Button
from datetime import datetime
from app.data_analysis.SQL_helper_functions import DatabaseManager
import timeit
import sqlite3
import re
from sqlalchemy import create_engine
engine = create_engine('postgres://qeirlxsntkwbkn:4a53f53c6fd6d1b91f30a520a97e821364ca2c71b94c67711d2e5aaaced2c6dc@ec2-54-247-79-178.eu-west-1.compute.amazonaws.com:5432/ddqb75j223tb8c')


from bokeh.server.server import Server
from tornado.ioloop import IOLoop


def parse_input_time(input):

    date =  re.search("....-..-..", input)
    time =  re.search("(?<=T).....", input)
 
    datetime = date.group() + " " + time.group() + ":00"
    return datetime

def get_data():
    # conn = sqlite3.connect("app/data_analysis/Bee_Telemetry_Database.db")
    df_telemetry = pd.read_sql_query('SELECT timestamp, temperature, weight, humidity FROM telemetry_data_table ORDER BY id DESC LIMIT 100', con=engine,
                                     parse_dates=['timestamp'])
    # conn.close()

    return df_telemetry

def plotgraphs(data_source):
    """Function that performs all plotting"""

    t_plot = figure(x_axis_type="datetime", title="Temperature Timeseries", sizing_mode="stretch_width",
                    plot_height=250, name="t_plot", tools="save")

    t_plot.background_fill_color = "#f5f5f5"
    t_plot.grid.grid_line_color = "white"
    t_plot.xaxis.axis_label = 'Date and Time'
    t_plot.yaxis.axis_label = 'Temperature/ °C'
    t_plot.axis.axis_line_color = None

    t_plot.xaxis.formatter = DatetimeTickFormatter(days=["%m/%d %H:%M"],
                                                   months=["%m/%d %H:%M"],
                                                   years=["%m/%d %H:%M"],
                                                   hours=["%m/%d %H:%M"],
                                                   hourmin=["%m/%d %H:%M"],
                                                   minutes=["%m/%d %H:%M"],
                                                   minsec=["%m/%d %H:%M:%Ss"],
                                                   milliseconds=["%M:%Ss"],
                                                   seconds=["%m/%d %H:%M:%Ss"])

    t_plot.line('timestamp', 'temperature', source=data_source, line_width=2, color='#66CCCC')

    t_plot.add_tools(HoverTool(
        tooltips=[
            ('Temperature', '@temperature °C'),
            ('Timestamp', '@timestamp{%Y/%m/%d %H:%M:%Ss}'),
        ],

        formatters={
            '@temperature': 'numeral',
            '@timestamp': 'datetime',
        },
        mode='vline'
    ))

    h_plot = figure(x_axis_type="datetime", title="Humidity Timeseries", sizing_mode="stretch_width", plot_height=250,tools="save")

    h_plot.background_fill_color = "#f5f5f5"
    h_plot.grid.grid_line_color = "white"
    h_plot.xaxis.axis_label = 'Date and Time'
    h_plot.yaxis.axis_label = 'Humidity/%'
    h_plot.axis.axis_line_color = None

    h_plot.xaxis.formatter = DatetimeTickFormatter(days=["%m/%d %H:%M"],
                                                   months=["%m/%d %H:%M"],
                                                   years=["%m/%d %H:%M"],
                                                   hours=["%m/%d %H:%M"],
                                                   hourmin=["%m/%d %H:%M"],
                                                   minutes=["%m/%d %H:%M"],
                                                   minsec=["%m/%d %H:%M:%Ss"],
                                                   milliseconds=["%M:%Ss"],
                                                   seconds=["%m/%d %H:%M:%Ss"])

    h_plot.line('timestamp', 'humidity', source=data_source, line_width=2, color='#66CCCC')

    h_plot.add_tools(HoverTool(
        tooltips=[
            ('Humidity', '@humidity %'),
            ('Timestamp', '@timestamp{%Y/%m/%d %H:%M:%Ss}'),
        ],

        formatters={
            '@humidity': 'numeral',
            '@timestamp': 'datetime',
        },
        mode='vline'
    ))

    w_plot = figure(x_axis_type="datetime", title="Weight Timeseries", sizing_mode="stretch_width", plot_height=250, tools="save")
    w_plot.background_fill_color = "#f5f5f5"
    w_plot.grid.grid_line_color = "white"
    w_plot.xaxis.axis_label = 'Date and Time'
    w_plot.yaxis.axis_label = 'Weight/ Kg'
    w_plot.axis.axis_line_color = None

    w_plot.xaxis.formatter = DatetimeTickFormatter(days=["%m/%d %H:%M"],
                                                   months=["%m/%d %H:%M"],
                                                   years=["%m/%d %H:%M"],
                                                   hours=["%m/%d %H:%M"],
                                                   hourmin=["%m/%d %H:%M"],
                                                   minutes=["%m/%d %H:%M"],
                                                   minsec=["%m/%d %H:%M:%Ss"],
                                                   milliseconds=["%M:%Ss"],
                                                   seconds=["%m/%d %H:%M:%Ss"])

    w_plot.line('timestamp', 'weight', source=data_source, line_width=2, color='#66CCCC')

    w_plot.add_tools(HoverTool(
        tooltips=[
            ('Wieght', '@weight Kg'),
            ('Timestamp', '@timestamp{%Y/%m/%d %H:%M:%Ss}'),
        ],

        formatters={
            '@weight': 'numeral',
            '@timestamp': 'datetime',
        },
        mode='vline'
    ))

    # return t_plot

    # show(t_plot)
    # show(gridplot([[t_plot],[h_plot],[w_plot]], sizing_mode="scale_width", plot_height=250))
    return t_plot, h_plot, w_plot

def get_data_filtered(t1, t2):
    """Function to get time filtered data from SQL database to pandas dataframe"""

    # conn = sqlite3.connect("app/data_analysis/Bee_Telemetry_Database.db")

    df_telemetry = pd.read_sql_query(
        "SELECT timestamp, temperature, weight, humidity FROM telemetry_data_table where Timestamp >= %s  and Timestamp <= %s ",
        con=engine, params=[t1, t2],
        parse_dates=['timestamp']
        )

    # conn.close()

    return df_telemetry

def filtered_graphs(t1,t2):
    
    data = get_data_filtered(t1,t2)
    # data = get_data()
    data_source = ColumnDataSource(data)
    t_plot, h_plot, w_plot = plotgraphs(data_source)

    return t_plot, h_plot, w_plot

def bees_app(doc):
    
    data = get_data()
    # print(data)
    data_source = ColumnDataSource(data)
    t_plot, h_plot, w_plot = plotgraphs(data_source)

    def callback():
        data_source.stream(get_data(), rollover=100)


    doc.add_root(column([t_plot, h_plot, w_plot],
                        sizing_mode="scale_width"))
    doc.add_periodic_callback(callback, 500)
    doc.title = "graphing"

def bokeh_worker():
    server = Server({'/bees': bees_app}, io_loop=IOLoop(),
                    allow_websocket_origin=["localhost:5000", "127.0.0.1:5000"])
                    # allow_websocket_origin=["diyartest.herokuapp.com"])
    server.start()
    print(server.port)
    server.io_loop.start()

