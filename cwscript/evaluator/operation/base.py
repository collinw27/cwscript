from cwscript.evaluator.value import *

class StackOperation:

	def __init__(self, line, value_type, eval_vars):

		self._line = line
		self._value_type = value_type
		self._eval_vars = eval_vars

	def get_line(self):

		return self._line

	# A simple wrapper to type-check the return value and evaluate variables
	# This prevents all inherited classes from needing to do this,
	# making the code slightly more readable

	def evaluate_and_check(self, evaluator, last_value):

		output = self._evaluate(evaluator, last_value)
		if (output is not None):
			if (self._eval_vars and isinstance(output, VariableValue)):
				output = output.get_var_value(evaluator)
			return evaluator.assert_type(output, self._value_type)
		else:
			return None

	def _evaluate(self, evaluator, last_value):

		raise NotImplementedError()

	# Overwrite to handle interrupt
	# Default behavior is to not handle anything

	def handle_interrupt(self, evaluator, interrupt):

		pass

class StackBlock (StackOperation):

	def __init__(self, value, line, value_type, eval_vars):

		# Value type isn't checked until execution is finished
		# even though it's technically predetermined (null)
		# This is intentional: if a block is used in a statement, the block should be
		# ran before the statement is evaluated and any type-related errors are thrown
		# StackList uses the same method

		super().__init__(line, value_type, eval_vars)
		self._statements = value
		self._pc = 0

	def _evaluate(self, evaluator, last_value):

		if (self._pc >= len(self._statements)):
			return NullValue(evaluator)
		self._line = self._statements[self._pc].get_line()
		evaluator.request_value(self._statements[self._pc], ScriptValue)
		self._pc += 1

class StackList (StackOperation):

	def __init__(self, value, line, value_type, eval_vars):

		super().__init__(line, value_type, eval_vars)
		self._values = value
		self._output = []

	def _evaluate(self, evaluator, last_value):

		if (last_value is not None):
			self._output.append(last_value)
		if (len(self._values) == len(self._output)):
			return ListValue(evaluator, self._output)
		evaluator.request_value(self._values[len(self._output)], ScriptValue)

# Class for evaluating arguments and performing an operation on them
# Contains some methods to reduce boilerplate
# Some statements (usually control flow) need more control than this
# class provides, in which case they should inherit StackOperation directly 
# and define their own implementation of _evaluate()

# Also note that some statements don't need to perform any operations that
# could potentially rely on other operations (ex. PiStatement, FunctionStatement, etc.),
# in which case they should inherit StackOperation directly and run _evaluate()
# in a single go

class StackBasicOperation (StackOperation):

	def __init__(self, args, line, value_type, eval_vars):

		super().__init__(line, value_type, eval_vars)
		self._args = args
		self._args_evaluated = []
		self._arg_requests = self._define_args()

	def _evaluate(self, evaluator, last_value):

		if (last_value is not None):
			self._args_evaluated.append(last_value)
		if (len(self._args_evaluated) == len(self._args)):
			return self._finish(evaluator, self._args_evaluated)
		else:
			req = self._arg_requests[len(self._args_evaluated)]
			evaluator.request_value(self._args[req.name], req.value_type, req.eval_vars)

	def _define_args(self):

		raise NotImplementedError()

	def _finish(self, evaluator, args):

		raise NotImplementedError()

# Used in statement and operator definitions for reducing boilerplate

class _ArgRequest:

	def __init__(self, name, value_type, eval_vars = True):

		self.name = name
		self.value_type = value_type
		self.eval_vars = eval_vars