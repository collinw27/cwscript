
class Interrupt:

	def __init__(self, line):

		self._line = line

	def get_line(self):

		return self._line

class ReturnInterrupt (Interrupt):

	def __init__(self, line, value):

		super().__init__(line)
		self.value = value

class BreakInterrupt (Interrupt):

	pass

class ContinueInterrupt (Interrupt):

	pass

class ExceptionInterrupt (Interrupt):

	def __init__(self, line, value):

		super().__init__(line)
		self.value = value