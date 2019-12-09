from transitions.extensions import GraphMachine

from utils import send_text_message

import random


class TocMachine(GraphMachine):
	def __init__(self, **machine_configs):
		self.guesstimes = 0
		self.target = [0,0,0,0]
		self.machine = GraphMachine(model=self, **machine_configs)
	
	def is_going_to_state1(self, event):
		text = event.message.text
		return text.lower() == "new game"
	
	def is_going_to_state2(self, event):
		text = event.message.text
		self.guess = event.message.text
		if len(text) != 4:
			return False
		return text == str(self.target)
		
	def is_going_to_state3(self, event):
		text = event.message.text
		self.guess = event.message.text
		if len(text) != 4:
			return False
		if text == self.target:
			return False
		return text.isdigit()
	
	def is_going_to_state4(self, event):
		text = event.message.text
		return len(text) != 4 | text.isdigit() == True
		
	def is_going_to_state5(self, event):
		text = event.message.text
		return self.guesstimes <= 0
	
	def on_enter_state1(self, event):
		print("I'm entering state1")
		arr = [0,1,2,3,4,5,6,7,8,9]
		for num in range(0,4):
			ran = random.randint(0,9-num)
			self.target[num] = arr[ran]
			arr[ran] = arr[9-num]
		self.guesstimes = 9
		reply_msg = "start your guess\n" + str(self.target)
		reply_token = event.reply_token
		send_text_message(reply_token, reply_msg)
		self.go_back()
	
	def on_exit_state1(self):
		print("Leaving state1")
	
	def on_enter_state2(self, event):
		print("I'm entering state2")
		reply_msg = "You got it!!\nenter \"new game\"to start a new game."
		reply_token = event.reply_token
		send_text_message(reply_token, reply_msg)
		self.go_back()
	
	def on_exit_state2(self):
		print("Leaving state2")
	
	def on_enter_state3(self, event):
		print("I'm entering state3")
		nA = 0
		nB = 0
		cpy = self.target
		for num in range(0,4):
			if self.guess[num] == str(cpy[num]):
				cpy[num] = -1
				nA = nA + 1
		for num in range(0,4):
			for num2 in range(0,4):
				if self.guess[num] == str(cpy[num2]):
					cpy[num2] = -1
					nB = nB + 1
		self.guesstimes = self.guesstimes - 1
		reply_msg = "nice try\n" + str(nA) + "A" + str(nB) + "B"
		reply_token = event.reply_token
		send_text_message(reply_token, reply_msg)
		self.go_back()
	
	def on_exit_state3(self):
		print("Leaving state3")
	
	def on_enter_state4(self, event):
		print("I'm entering state4")
		reply_msg = "maybe you should try a 4-digit number without repeat."
		reply_token = event.reply_token
		send_text_message(reply_token, reply_msg)
		self.go_back()
	
	def on_exit_state4(self):
		print("Leaving state4")
	
	def on_enter_state5(self, event):
		print("I'm entering state5")
		reply_msg = "Enter \"new game\"to start a new game."
		reply_token = event.reply_token
		send_text_message(reply_token, reply_msg)
		self.go_back()
	
	def on_exit_state5(self):
		print("Leaving state5")
	
	