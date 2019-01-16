import os 
import subprocess
import psutil   
import math
from bs4 import BeautifulSoup
from flask import Flask, url_for, render_template

#Instantiate app
app = Flask(__name__, template_folder='templates')
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
print partis
#App routes
@app.route('/')
def proc():
    return render_template('index.html', memory=memory, memory_mb=memory_mb, swap=swap, swap_mb=swap_mb, c=c, cpurange=cpurange, cpucount=cpucount, cpu=cpu, frequency=frequency, disk_usage=disk_usage)
