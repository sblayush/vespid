from abc import ABC, abstractmethod


class VUIAppInterface(ABC):
	def __init__(self):
		self.actions = {}
	
	@abstractmethod
	def load(self):
		pass
	