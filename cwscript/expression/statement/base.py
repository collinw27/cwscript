from cwscript.expression.dynamic import DynamicExpression
from cwscript.value import *

class StatementExpression (DynamicExpression):

	# Called by StackOperation, values are passed from runner
	# Arguments are received in the same order they were passed to get_stack()

	@staticmethod
	def evaluate(runner, args):

		raise NotImplementedError()

	# Use for interruptable operations that store a state

	@staticmethod
	def evaluate_special(runner, args, state):

		raise NotImplementedError()

	# Called by StackOperation, interrupt is passed from the runner
	# Attempt to handle the interrupt, should return NullValue if unable to

	@staticmethod
	def handle_interrupt(runner, interrupt):

		return NullValue(runner)

	@staticmethod
	def handle_interrupt_special(runner, interrupt, state):

		return NullValue(runner)