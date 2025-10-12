
from cwscript.value.primitive import VariableValue

# For now, stack items do not have runtime type checking
# This will be fixed after I get the basic structure working

class StackItem:

	pass

class StackValueRequest (StackItem):

	def __init__(self, value, eval_vars = True):

		self._value = value
		self._eval_vars = eval_vars

	def evaluate(self, runner):

		return self._value.get_stack(runner, self._eval_vars)

class StackValue (StackItem):

	def __init__(self, value):

		self.value = value

class StackOperation (StackItem):

	def __init__(self, op_class, num_args, eval_vars):

		self._op_class = op_class
		self._eval_vars = eval_vars
		self.num_args = num_args

	# Variable evaluation is performed after the operation's value is returned
	# This way, the operation doesn't need to have any knowledge of `eval_vars`

	def evaluate(self, runner, args):

		# return runner.assert_type(self._op_class.evaluate(runner, args, self._eval_vars), self._value_type)
		value = self._op_class.evaluate(runner, args)
		if (isinstance(value, VariableValue) and self._eval_vars):
			value = value.get_var_value(runner)
		return StackValue(value)

# Stores a state variable that is passed into each `evaluate()` call
# This is used for operations that need to run a block as part of
# their evaluation (function calls, loops, etc.), since running a block
# requires exiting the function and adding to the stack

class StackInterruptableOperation (StackOperation):

	def __init__(self, op_class, num_args, eval_vars, state = {}):

		super().__init__(op_class, num_args, eval_vars)
		self._state = state.copy()

	# Instead of a ScriptValue, a StackBlock can be returned
	# to trigger an interrupt

	def evaluate(self, runner, args):

		value = self._op_class.evaluate(runner, args, self._state)
		if (isinstance(value, StackBlock)):
			return value
		if (isinstance(value, VariableValue) and self._eval_vars):
			value = value.get_var_value(runner)
		return StackValue(value)

# Runs all expressions in a block in sequence
# Operations are responsible for flagging when to execute blocks

class StackBlock (StackItem):

	def __init__(self, block):

		self._block = block
		self._pc = 0

	def has_started(self):

		return self._pc != 0

	def pop_next(self):

		# `get_expression()` performs bounds checking and returns None if necessary

		self._pc += 1
		return self._block.get_expression(self._pc - 1)

class StackList (StackItem):

	def __init__(self, num_items):

		self.num_items = num_items