# -*- coding: utf-8 -*-
import abc, six
import zmq
import random
from evaluate import ffwd_to_img
import subprocess


class StyleTransfer(object):
	def __init__(self):
		self.port = "5556"
		self.input_location = "/home/jammu55048/polaroid/backend/fast-style-transfer/"
		self.output_location = "/home/jammu55048/polaroid/backend/fast-style-transfer/outputs/"
		self.checkpoint_dir = "/home/jammu55048/polaroid/backend/fast-style-transfer/models/la_muse.ckpt"
		self.device = "/gpu:0"
		print("before serve")
		self.serve()

	def apply_style(self, arguments):
		print("inside apply style")
		id = arguments['id']
		subprocess.call([
			"python", 
			"evaluate.py", 
			"--checkpoint", 
			"models/la_muse.ckpt", 
			"--in-path", 
			"{}.jpeg".format(id), 
			"--out-path", 
			"outputs/", 
			"--device", 
			"/gpu:0"
			])
		return {"status": "success"}

	def serve(self):
		print("entered serve function")
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.REP)
		self.socket.bind("tcp://*:%s" % self.port)
		print("Serving {} on tcp://*:{}".format(type(self).__name__, self.port))
		while True:
			print("inside while look")
			arguments = self.socket.recv_json()
			response = self.apply_style(arguments)
			self.socket.send_json(response)
print("pre-instantiation")
StyleTransfer()