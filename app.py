import os 
import subprocess
import psutil   
import math
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
#Fetch swap info
swp = psutil.swap_memory()
#Create dicitionary of swap memory info, change to GB and round to 2 digits
swap = {
    'Total': round(swp.total / (1024.0 ** 3), 2),
    'Used': round(swp.used / (1024.0 ** 3), 2),
    'Free' : round(swp.free / (1024.0 ** 3), 2),
    'Percentage': round(swp.percent, 2),
}
#Fetch CPU info
c = psutil.cpu_percent(interval=1, percpu=True)
cpucount = psutil.cpu_count()
print cpucount

#CPU dictionary
cpu = {}


#App routes
@app.route('/')
def proc():
    return render_template('index.html', memory=memory, swap=swap)
