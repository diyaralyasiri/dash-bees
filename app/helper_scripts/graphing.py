import pandas as pd 
from bokeh.plotting import figure, show, curdoc
from bokeh.palettes import Spectral11, colorblind, Inferno, BuGn, brewer
from bokeh.models import HoverTool, value, LabelSet, Legend, ColumnDataSource,LinearColorMapper,BasicTicker, PrintfTickFormatter, ColorBar, DatetimeTickFormatter, NumeralTickFormatter, DatePicker
from bokeh.layouts import gridplot, column, row
from bokeh.models.widgets import Button
from datetime import datetime
from SQL_helper_functions import DatabaseManager
import timeit
import sqlite3

# print(timeit.timeit(get_data, number=3))

### Functions #######

def get_data_update():##  function attempting to only read 3 latest entries in DB and send to datasource, doesnt work tho 
   
    
    conn = sqlite3.connect("Bee_Telemetry_Database.db")

    df_telemetry = pd.read_sql_query("SELECT Timestamp, Temperature, Wieght, Humidity FROM Telemetry_Data_Table ORDER BY id DESC LIMIT 3", 
        conn,
        parse_dates=['Timestamp'],
        )
          
    conn.close()
    
    # print(df_telemetry)
    # print(df_telemetry.info())
       
    return df_telemetry
def get_data():
    conn = sqlite3.connect("Bee_Telemetry_Database.db")
    df_telemetry = pd.read_sql_query("SELECT Timestamp, Temperature, Wieght, Humidity FROM Telemetry_Data_Table", conn,parse_dates=['Timestamp'])
    conn.close()


    # print(df_telemetry)
    # print(df_telemetry.info())
       
    return df_telemetry
def get_data_dict(): 
    """Function to read SQL data into a python dictionary"""
    dbObj=DatabaseManager()
    df_telemetry = list(zip(*dbObj.read_db_record("SELECT Timestamp, Temperature, Wieght, Humidity FROM Telemetry_Data_Table ")))
    df_dict = {'Timestamp': [df_telemetry[0]],'Temperature': [df_telemetry[1]],'Wieght':[df_telemetry[2]], 'Humidity': [df_telemetry[2]]}
    del dbObj
       
    return df_dict
def get_data_filtered(t1,t2):
    """Function to get time filtered data from SQL database to pandas dataframe"""
    
    conn = sqlite3.connect("Bee_Telemetry_Database.db")

    df_telemetry = pd.read_sql_query("SELECT Timestamp, Temperature, Wieght, Humidity FROM Telemetry_Data_Table where Timestamp >= (?)  and Timestamp <= (?) ",
        conn, params=(t1,t2),
        parse_dates=['Timestamp'],
    )
          
    conn.close()
    
    # print(df_telemetry)
    # print(df_telemetry.info())
       
    return df_telemetry
def plotgraphs(data_source):
    """Function that performs all plotting"""


    t_plot = figure(x_axis_type="datetime", title="Temperature Timeseries", sizing_mode="stretch_width", plot_height=250,name="t_plot")

    t_plot.background_fill_color="#f5f5f5"
    t_plot.grid.grid_line_color="white"
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

    t_plot.line('Timestamp', 'Temperature', source=data_source ,line_width=2, color='#66CCCC')
        
    t_plot.add_tools(HoverTool(
        tooltips=[
            ( 'Temperature',   '@Temperature °C'),
            ( 'Timestamp',  '@Timestamp{%Y/%m/%d %H:%M:%Ss}'),
        ],

        formatters={
            '@Temperature': 'numeral',  
            '@Timestamp' : 'datetime',                                
        },
        mode='vline'
    ))

    h_plot = figure(x_axis_type="datetime",title="Humidity Timeseries", sizing_mode="stretch_width", plot_height=250)

    h_plot.background_fill_color="#f5f5f5"
    h_plot.grid.grid_line_color="white"
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


    h_plot.line('Timestamp', 'Humidity', source=data_source,line_width=2, color='#66CCCC')


    h_plot.add_tools(HoverTool(
        tooltips=[
            ( 'Humidity',   '@Humidity %'),
            ( 'Timestamp',  '@Timestamp{%Y/%m/%d %H:%M:%Ss}'),
        ],

        formatters={
            '@Humidity'        : 'numeral',  
            '@Timestamp' : 'datetime',                                
        },
        mode='vline'
    ))

    w_plot = figure(x_axis_type="datetime",title="Wieght Timeseries", sizing_mode="stretch_width", plot_height=250)
    w_plot.background_fill_color="#f5f5f5"
    w_plot.grid.grid_line_color="white"
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

    w_plot.line('Timestamp', 'Wieght', source=data_source,line_width=2, color='#66CCCC')
        
    w_plot.add_tools(HoverTool(
        tooltips=[
            ( 'Wieght',   '@Wieght Kg'),
            ( 'Timestamp',  '@Timestamp{%Y/%m/%d %H:%M:%Ss}'),
        ],

        formatters={
            '@Wieght': 'numeral',  
            '@Timestamp' : 'datetime',                                
        },
        mode='vline'
    ))

    return t_plot

    
    # show(t_plot)
    # show(gridplot([[t_plot],[h_plot],[w_plot]], sizing_mode="scale_width", plot_height=250))
    # return t_plot, h_plot, w_plot
def renderer_added(attr, old, new):
    """This is supposed to show when a new glyph is rendered on the plot but hasnt worked yet"""
    # print(f"attribute '{attr}' changed")
def update_xaxis():
    """Supposed to update axis but hasnt worked yet"""
    
    ## change data source here 
    print(datepicker_start)
    print(datepicker_end)

    # Calculate time delta from reference time in seconds
    # timestamp_start = (datetime.combine(datepicker_start.value, datetime.min.time())
    #                     - datetime(1970, 1, 1)) / timedelta(seconds=1)
    # timestamp_end = (datetime.combine(datepicker_end.value, datetime.min.time())
    #                     - datetime(1970, 1, 1)) / timedelta(seconds=1)
    # t_plot.x_range.start = int(timestamp_start)*1e3  # Multiply by 1e3 as JS timestamp is in milliseconds
    # t_plot.x_range.end   = int(timestamp_end)*1e3  # Multiply by 1e3 as JS timestamp is in milliseconds
def get_data_dict():
    """Gets data into list of lists"""
    dbObj= DatabaseManager()

    Timestamp, Temperature, Weight, Humidity= list(zip(*dbObj.read_db_record("SELECT Timestamp, Temperature, Wieght, Humidity FROM Telemetry_Data_Table")))

    data = [Timestamp, Temperature, Weight, Humidity]

    # source.data = dict(x_time=[], x_only_time=[], ...)

    return data
def callback():
    """Function used to refresh plot with new data, called back continuously"""
    # data_source = ColumnDataSource(empty_dataframe)
    data_source.stream(get_data(),rollover=500)

# column_names = ["Timestamp", "Temperature", "Wieght","Humidity"]
# empty_dataframe = pd.DataFrame(columns = column_names)


bokeh_doc = curdoc()
datepicker_start = DatePicker(title='Start Date')
datepicker_end = DatePicker(title='End Date')
button = Button(label='Set Date')
button.on_click(update_xaxis)

### Time inputs for testing 
current_time = datetime.now()
t1= "2020-04-25 16:50:14"
t2= current_time.strftime("%Y-%m-%d %H:%M:%S")
# df_telemetry_filtered= get_data_filtered(t1,t2)

data = get_data_filtered(t1,t2)

data_source = ColumnDataSource(data)
print(str(data_source))
plot = plotgraphs(data_source)

# show(plot)

bokeh_doc.add_root(column([plot, column( datepicker_start,datepicker_end,button, align='center', max_width=200)],sizing_mode="scale_width"))
bokeh_doc.add_periodic_callback(callback, 500)
bokeh_doc.title="graphing"
# plot.on_change("renderers", renderer_added)




