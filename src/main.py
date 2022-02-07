import time
import subprocess
import os
import requests
import warnings

#disable warning message if using self signed certs.  
warnings.filterwarnings('ignore',message='Unverified HTTPS request')

splunk_host=os.getenv('SPLUNK_HOST')
splunk_token=os.getenv('SPLUNK_TOKEN')
splunk_index=os.getenv('SPLUNK_INDEX')

balena_machine_name=os.getenv('BALENA_DEVICE_NAME_AT_INIT')
balena_device_type=os.getenv('BALENA_DEVICE_TYPE')

cmd = "hostname -I | cut -d' ' -f1"
balena_local_ip = subprocess.check_output(cmd, shell=True).decode("utf-8").rstrip()


host="testhost"

def splunkHec(splunk_host, host, splunk_token, target_index, load5min, DiskSize, DiskUsed, DiskUsedPct, UsedMem, TotalMem, UsedMemPct,balena_machine_name,balena_device_type,balena_local_ip):
	if not (splunk_host is None or splunk_token is None or splunk_index is None):
		try:
			print("Sending metrics to Splunk")
			splunk_token="Splunk "+splunk_token
			url='https://'+splunk_host+':8088/services/collector/event'
			authHeader = {'Authorization': splunk_token}
			jsonDict = { "time": epoch, "event": "metric", "source": "metrics", "sourcetype": "osperf", "host": host, "index": target_index, "fields": { "balena_machine_name": balena_machine_name, "balena_device_type": balena_device_type, "balena_local_ip": balena_local_ip, "metric_name:load5min": load5min, "metric_name:DiskSize": DiskSize, "metric_name:DiskUsed": DiskUsed, "metric_name:DiskUsedPct":DiskUsedPct, "metric_name:UsedMem": UsedMem, "metric_name:TotalMem": TotalMem, "metric_name:UsedMemPct": UsedMemPct  } }	 
			r = requests.post(url, headers=authHeader, json=jsonDict, verify=False)
			print(r.text)
		except Exception as e:
			print("Splunk send failed. Error below:")
			print(e)
	else:
		print("Splunk OS variables not defined")

counter=0
while True:

	#get time as epoch
	epoch=int(round(time.time()))
	print(epoch," ",counter)
	# Shell scripts for system monitoring from here:
	# https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
	cmd = 'cut -f 1 -d " " /proc/loadavg'
	load5min = subprocess.check_output(cmd, shell=True).decode("utf-8").rstrip()
	cmd = "free -m | grep Mem"
	MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8").rstrip()
	MemUsage = MemUsage.split()
	TotalMem = MemUsage[1]
	UsedMem = MemUsage[2]
	UsedMemPct = round(int(UsedMem)*100/int(TotalMem),2)
	#get disk space only for / 
	cmd = 'df -h | awk \'$NF=="/"{printf "%d %d %s", $3,$2,$5}\''
	Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
	Disk = Disk.split()
	DiskSize = Disk[1]
	DiskUsed = Disk[0]
	DiskUsedPct = int(Disk[2].replace("%",""))/100
	print("load5min: "+load5min+" DiskSize: "+DiskSize+" DiskUsed: "+DiskUsed+" DiskUsedPct: "+str(DiskUsedPct)+" UsedMem: "+UsedMem+" TotalMem: "+TotalMem+" UsedMemPct: "+str(UsedMemPct))
	print("balena_machine_name: "+balena_machine_name+" balena_device_type: "+balena_device_type+" balena_local_ip: "+balena_local_ip)
	splunkHec(splunk_host,host,splunk_token,splunk_index, load5min,DiskSize,DiskUsed,DiskUsedPct,UsedMem,TotalMem,UsedMemPct,balena_machine_name,balena_device_type,balena_local_ip)
	counter=counter+1
	time.sleep(10)

