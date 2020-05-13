import re

input= "2020-02-04T02:02"

def parse_input_time(input):

    date =  re.search("....-..-..", input)
    time =  re.search("(?<=T).....", input)
 
    datetime = date.group() + " " + time.group() + ":00"
    return datetime

t1= "2020-04-25 16:50:14"