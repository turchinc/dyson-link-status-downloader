#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" simple script to subscribe to and serialize status messages from a dyson link device for later processing """
from datetime import datetime
from configparser import ConfigParser as configparser
from paho.mqtt import client as mqtt
import threading
import os, json
import  sys, getopt
import re

# to get your username and password, see the excellent - japanese - tutorial at:
# http://aakira.hatenablog.com/entry/2016/08/12/012654 
# (google translate is quite readable, but don't copy and paste the code afterwards!!!)
# short summary: tPacketCapture on android to create the pcap file and wireshark to analyse packets and extract required data
username = ''
password = ''
host = ''

#device id: information obtainable in the packets in wireshark
# - 475 dyson pure cool link, 
# - 455 dyson pure hot+cool link 
device_id = 455
client = mqtt.Client (protocol = mqtt.MQTTv311)

def bn():
	""" defines the base name for the queues """
	return str(device_id) + '/' + username 

def	 on_connect (client, userdata, flags, response_code):
	""" subscribe to relevant queues - could be extended """
	print ( 'Status:' + str(response_code))	
	topics = [
		bn() + '/status/current',
		bn() + '/status/summary']
	for topic in topics:
		client.subscribe(topic)

def	 on_message (client, userdata, msg):
	""" handle message received in subscribed queue """
	print ( '-----' + msg.topic + '-----' )
	payload = msg.payload.decode('UTF-8')
	print (payload)
	save_data(msg.topic, payload)

def clean(filename):
	""" clean filenames """
	#2016-10-31T17:00:37.412Z
	return re.sub(':', '', filename)

def	save_data(topic, payload):
	""" extract key info from json then save off to file for processing """
	json_msg = json.loads(payload)
	msg_dir = clean(json_msg['msg']) 
	msg_filename = clean(json_msg['time']) + '.json'
	if not os.path.exists(msg_dir):
		os.makedirs(msg_dir)
	with open (os.path.join(msg_dir, msg_filename), mode="w+") as file:
		json.dump(json_msg, file)
	
def get_status():
	""" send a message requesting status update """
	now = datetime.utcnow().isoformat()[:-3] + 'Z'
	payload = '{"msg":"REQUEST-CURRENT-STATE","time":"' + now + '"}'
	topic = bn() + '/command'
	print (topic + '\n\n' + payload)
	client.publish(topic, payload)  

def set_interval(func, sec):
	""" simple background threading """
	def func_wrapper():
		set_interval(func, sec)
		func()
	t = threading.Timer(sec, func_wrapper)
	t.daemon = True
	t.start()
	return t
	
def start_client(host, username, password, port, interval):
	""" start the mqtt client and issue the first status request also start the thread for further udpates """
	#print("starting " , host, username, password, port, interval)
	client.username_pw_set (username, password)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host, port = port, keepalive = 60 )
	get_status()
	set_interval(get_status, interval)
	client.loop_forever()
	
def help():
	script = os.path.basename(sys.argv[0])
	print(script + ' -c <cfg-file>')
	sys.exit()

def main(argv):
	global username, password, host, device_id
	try:
	  opts, args = getopt.getopt(argv,"hc:",["config="])
	except getopt.GetoptError:
		help()
	for opt, arg in opts:
		if opt == '-c':
			cfg = arg
			config = configparser()
			config.read_file(open(cfg))
			username = config['dysondata']['username']
			password = config['dysondata']['password']
			host = config['dysondata']['host']
			device_id = config['dysondata']['device_id']
			port = config.getint('dysondata','port')
			interval = config.getint('dysondata','interval')
			start_client(host, username, password, port, interval)
		else:
			help()
			
if __name__ == "__main__":
   main(sys.argv[1:])
