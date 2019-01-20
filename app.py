import os 
import psutil   
import re
import math
import pygal
import mimetypes
from time import sleep
import datetime
from bs4 import BeautifulSoup
from flask import Flask, url_for, render_template, make_response

#Instantiate app
app = Flask(__name__, template_folder='templates')
#Local machine time
uptime = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
#Fetch memory info
mem = psutil.virtual_memory()
#Create dictionary of desired memory info, change to Gigabytes and round to 2 digits.
memory = {
    'Total': round(mem.total / (1024.0 ** 3), 2),
    'Used': round(mem.used / (1024.0 ** 3), 2),
    'Available': round(mem.available / (1024.0 ** 3), 2),
    'Percentage': round(mem.percent, 2),
    'Free' : round(mem.free / (1024.0 ** 3), 2),
    'Buffers': round(mem.buffers / (1024.0 ** 3), 2),
    'Cached': round(mem.cached / (1024.0 ** 3), 2),
    'Shared': round(mem.shared  / (1024.0 ** 3), 2),
}

memory_mb = {
    'Total': round(mem.total / (1024.0 ** 2), 2),
    'Used': round(mem.used / (1024.0 ** 2), 2),
    'Available': round(mem.available / (1024.0 ** 2), 2),
    'Percentage': round(mem.percent, 2),
    'Free' : round(mem.free / (1024.0 ** 2), 2),
    'Buffers': round(mem.buffers / (1024.0 ** 2), 2),
    'Cached': round(mem.cached / (1024.0 ** 2), 2),
    'Shared': round(mem.shared  / (1024.0 ** 2), 2),
}

#Fetch swap info
swp = psutil.swap_memory()
#Create dicitionary of swap memory info, change to GB and round to 2 digits
swap = {
    'Total': round(swp.total / (1024.0 ** 3), 2),
    'Used': round(swp.used / (1024.0 ** 3), 2),
    'Free' : round(swp.free / (1024.0 ** 3), 2),
    'Percentage': round(swp.percent, 2),
}

swap_mb = {
    'Total': round(swp.total / (1024.0 ** 2), 2),
    'Used': round(swp.used / (1024.0 ** 2), 2),
    'Free' : round(swp.free / (1024.0 ** 2), 2),
    'Percentage': round(swp.percent, 2),
}
#Fetch CPU info
c = psutil.cpu_percent(interval=1, percpu=True)
cpucount = psutil.cpu_count()
cpurange = range(cpucount)
cpu = dict()
#CPU dictionary
for i in cpurange:
    cpu[i] = c[i]

#Fetch cpu frequency
freq = psutil.cpu_freq()
#Frequency dictionary
frequency = {
    'Current': round(freq.current, 2),
    'Min': freq.min,
    'Max': freq.max,
}
#Disk usage
dusg = psutil.disk_usage('/')

disk_usage = {
    'Total': round(dusg.total / (1024.0 ** 3), 2),
    'Used': round(dusg.used / (1024.0 ** 3), 2),
    'Free': round(dusg.free / (1024.0 ** 3), 2),
    'Percentage': dusg.percent,
}

#Disk partitions
partis = psutil.disk_partitions(all=False)
dparts = dict()

count = 0
for i in partis:
    dparts[count] = i
    count += 1

for key, value in dparts.items():
    dparts[key]=re.findall(r'\((.*?)\)', str(value))
#Running processes
pinfo = dict()
rproc = dict()
for process in psutil.process_iter(attrs=['pid', 'name', 'username']):
    pinfo[process] = process.as_dict(attrs = ['pid', 'name', 'username'])


    




    
#App routes
@app.route('/')
def proc():
    return render_template('index.html', uptime=uptime, memory=memory, memory_mb=memory_mb, swap=swap, swap_mb=swap_mb, c=c, cpurange=cpurange, cpucount=cpucount, cpu=cpu, frequency=frequency, disk_usage=disk_usage, dparts=dparts)

@app.route('/graphs')
def graph():
    pie_chart = pygal.Pie(width=500, height=400, explicit_size=True)
    pie_chart.title = 'Browser usage in February 2012 (in %)'
    pie_chart.add('IE', 19.5)
    pie_chart.add('Firefox', 36.6)
    pie_chart.add('Chrome', 36.3)
    pie_chart.add('Safari', 4.5)
    pie_chart.add('Opera', 2.3)
    chart= pie_chart.render_data_uri()
    return render_template('graphs.html', chart=chart)
