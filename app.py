import psutil   
import re
import math
import pygal
import mimetypes
import datetime
from flask import Flask, url_for, render_template, make_response

#Instantiate app
app = Flask(__name__, template_folder='templates')
#Local machine time
uptime = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

#Battery status
#Convert seconds to hours
def secs2hours(secs):
    mm, ss = divmod(secs, 60)   
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)
battery = psutil.sensors_battery()

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

pmemory = {
    'Total': round(mem.total / (1024.0 ** 3), 2),
    'Used': round(mem.used / (1024.0 ** 3), 2),
    'Available': round(mem.available / (1024.0 ** 3), 2),
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

pswap = {
    'Total': round(swp.total / (1024.0 ** 3), 2),
    'Used': round(swp.used / (1024.0 ** 3), 2),
    'Free' : round(swp.free / (1024.0 ** 3), 2),
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
    dparts[key]=re.findall(r'\((.*?)\)', str(value))[0]

#Running processes
"""pinfo = dict()
rproc = dict()
rcount = 0
for process in psutil.process_iter(attrs=['pid', 'name', 'username']):
    pinfo[process] = process.as_dict(attrs = ['pid', 'name', 'username'])
    rcount += 1
    for key in range(rcount):
        rproc[key] = pinfo[process]
        print rproc[key]
"""

#Network if_addresses
ifa = psutil.net_if_addrs()
for i, v in ifa.items():
    ifa[i] = re.findall(r'\((.*)\)', str(v))[0].replace(")", "").replace("(", "").replace("'", "")

sockets = []    
#Socket connections
socket_cons = psutil.net_connections()
for i in socket_cons:
    sockets = re.findall(r'\((.*?)\)', str(socket_cons))[0].replace("(", "").replace("'", "")
#App routes
@app.route('/')
def proc():
    return render_template('index.html', uptime=uptime, memory=memory, memory_mb=memory_mb, swap=swap, swap_mb=swap_mb, c=c, cpurange=cpurange, cpucount=cpucount, cpu=cpu, frequency=frequency, disk_usage=disk_usage, dparts=dparts, ifa=ifa, sockets=sockets)

@app.route('/graphs')
def graph():
    #Bar chart for CPU usage
    bar_chart = pygal.Bar(width=500, height=400, explicit_size=True, range=(0, 100))
    bar_chart.title = 'CPU usage per core (%)'
    for i, v in cpu.items():
        bar_chart.add('Core' + str(i), v)
    chart= bar_chart.render_data_uri()
    #Pie chart for disk usage
    pie_chart = pygal.Pie(width=500, height=400, explicit_size=True)
    pie_chart.title = 'Disk usage (GB)'
    for key, value in disk_usage.items():
        pie_chart.add(key, value)
    dchart = pie_chart.render_data_uri()
    #H-bar for memory and swap memory
    hbar = pygal.HorizontalBar(width=500, height=400, explicit_size=True)
    hbar.title = 'Memory usage (GB)'
    for key, value in pmemory.items():
        hbar.add(key, value)
    hbarchart = hbar.render_data_uri()

    hbarswap = pygal.HorizontalBar(width=500, height=400, explicit_size=True)
    hbarswap.title = 'Swap memory usage (GB)'
    for key, value in pswap.items():
        hbarswap.add(key, value)
    hbarswapchart = hbarswap.render_data_uri()

    return render_template('graphs.html', chart=chart, dchart=dchart, hbarchart=hbarchart, hbarswapchart=hbarswapchart)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
