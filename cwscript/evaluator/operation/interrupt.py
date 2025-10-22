
class Interrupt:

	pass

class ReturnInterrupt:

	def __init__(self, value):

		self.value = value

class BreakInterrupt:

	def __init__(self):

		pass

class ContinueInterrupt:

	def __init__(self):

		pass

class ExceptionInterrupt:

	def __init__(self, value):

		self.value = value