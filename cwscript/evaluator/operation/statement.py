from cwscript.evaluator.operation.base import *
from cwscript.evaluator.operation.base import _ArgRequest as ArgRequest
from cwscript.evaluator.operation.interrupt import *
from cwscript.evaluator.value import *

class PrintStatement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('value', ScriptValue)
		]

	def _finish(self, evaluator, args):

		print(args[0].to_string(evaluator))
		return NullValue(evaluator)

class LocalScopeStatement (StackOperation):

	def __init__(self, args, value_type, eval_vars):

		super().__init__(value_type, eval_vars)

	def _evaluate(self, evaluator, last_value):

		return evaluator.get_function_scope()

class GlobalScopeStatement (StackOperation):

	def __init__(self, args, value_type, eval_vars):

		super().__init__(value_type, eval_vars)

	def _evaluate(self, evaluator, last_value):

		return evaluator.get_global_scope()

class IfStatement (StackOperation):

	def __init__(self, args, value_type, eval_vars):

		super().__init__(value_type, eval_vars)
		self._args = args
		self._step = 0

	def _evaluate(self, evaluator, last_value):

		# Request condition, then run if necessary

		if (self._step == 0):
			evaluator.request_value(self._args['condition'], ScriptValue)
		elif (self._step == 1):
			if (last_value.to_bool(evaluator)):
				evaluator.request_value(self._args['body'], ScriptValue)
			else:
				return BoolValue(evaluator, False)
		elif (self._step == 2):
			return BoolValue(evaluator, True)
		self._step += 1

class WhileLoopStatement (StackOperation):

	def __init__(self, args, value_type, eval_vars):

		super().__init__(value_type, eval_vars)
		self._args = args
		self._step = 0
		self._used_break = False

	def _evaluate(self, evaluator, last_value):

		# Request condition value
		# This will need to be performed before every loop iteration
		# to make sure it still should be run

		if (self._step % 2 == 0):
			evaluator.request_value(self._args['condition'], ScriptValue)
		elif (self._step % 2 == 1):

			condition = last_value.to_bool(evaluator)
			if (condition and not self._used_break):
				evaluator.request_value(self._args['body'], ScriptValue)

			# Returns whether the block ran at least once

			else:
				return BoolValue(evaluator, self._step > 1)

		self._step += 1

	# Handle break by exiting the loop on the next evaluation
	# Continue has already done its job by interruping the previous iteration

	def handle_interrupt(self, evaluator, interrupt):

		if (isinstance(interrupt, BreakInterrupt)):
			self._used_break = True
			evaluator.handle_interrupt()
		elif (isinstance(interrupt, ContinueInterrupt)):
			evaluator.handle_interrupt()

class ForLoopStatement (StackOperation):

	def __init__(self, args, value_type, eval_vars):

		super().__init__(value_type, eval_vars)
		self._args = args
		self._step = 0
		self._used_break = False

	def _evaluate(self, evaluator, last_value):

		# Request values

		if (self._step == 0):
			evaluator.request_value(self._args['iterator'], VariableValue, False)
		elif (self._step == 1):
			self._iterator = last_value
			evaluator.request_value(self._args['list'], ListValue)
		elif (self._step == 2):
			self._list = last_value

		# Third iteration and onward: Run the loop body

		if (self._step >= 2):

			# Finish when the iterator reaches the end of the list
			# Can also finish by using `break`
			# Returns whether the block was run

			if (self._step - 2 >= len(self._list.get_list()) or self._used_break):
				return BoolValue(evaluator, self._step > 2)

			# Increment iterator, then run the block

			self._iterator.set_var_value(evaluator, self._list.get_list()[self._step - 2])
			evaluator.request_value(self._args['body'], ScriptValue)

		self._step += 1

	# Handle break by exiting the loop on the next evaluation
	# Continue has already done its job by interruping the previous iteration

	def handle_interrupt(self, evaluator, interrupt):

		if (isinstance(interrupt, BreakInterrupt)):
			self._used_break = True
			evaluator.handle_interrupt()
		elif (isinstance(interrupt, ContinueInterrupt)):
			evaluator.handle_interrupt()

class ContinueStatement (StackOperation):

	def __init__(self, args, value_type, eval_vars):

		super().__init__(value_type, eval_vars)

	def _evaluate(self, evaluator, last_value):

		evaluator.raise_interrupt(ContinueInterrupt())
		return NullValue(evaluator)

class BreakStatement (StackOperation):

	def __init__(self, args, value_type, eval_vars):

		super().__init__(value_type, eval_vars)

	def _evaluate(self, evaluator, last_value):

		evaluator.raise_interrupt(BreakInterrupt())
		return NullValue(evaluator)

# In the previous iteration of this project
# functions were automatically 'bound' to the current object
# Since I'm not sure how 'binding' functions will work in the future,
# they're left out of this class for now

class FunctionStatement (StackOperation):

	def __init__(self, args, value_type, eval_vars):

		super().__init__(value_type, eval_vars)
		self._args = args

	def _evaluate(self, evaluator, last_value):

		parameters = self._args['parameters'].eval_as_parameters(evaluator)
		return FunctionValue(evaluator, parameters, self._args['body'])

class ReturnStatement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('value', ScriptValue)
		]

	def _finish(self, evaluator, args):

		evaluator.raise_interrupt(ReturnInterrupt(args[0]))
		return NullValue(evaluator)

class CallStatement (StackOperation):

	def __init__(self, args, value_type, eval_vars):

		super().__init__(value_type, eval_vars)
		self._args = args
		self._step = 0
		self._return_value = None

	def _evaluate(self, evaluator, last_value):

		# Request values

		if (self._step == 0):
			evaluator.request_value(self._args['function'], FunctionValue)
		elif (self._step == 1):
			self._func = last_value
			evaluator.request_value(self._args['args'], ListValue)

		# Third iteration: Run the function body

		elif (self._step == 2):

			# The number of arguments must match the number of parameters in the definition

			arg_values = last_value.get_list()
			parameters = self._func.get_parameters(evaluator)
			if (len(parameters) != len(arg_values)):
				raise CWRuntimeError("Wrong number of arguments for function call", evaluator.get_line())

			# Create a new variable scope, and initialize the function's variables within it

			scope = ObjectValue(evaluator)
			for i in range(len(parameters)):
				scope.set_field(evaluator, parameters[i], arg_values[i])
			evaluator.add_function_scope(scope)

			# Run the function's body

			evaluator.request_value(self._func.get_body(), ScriptValue)

		# This will be bypassed if a return statement is used
		# Another value can be set by a ReturnInterrupt

		else:
			evaluator.pop_function_scope()
			return NullValue(evaluator) if (self._return_value is None) else self._return_value

		self._step += 1

	# Exit on return interrupt
	# Error on continue/break interrupt, since
	# continue/break cannot propogate past function scope

	def handle_interrupt(self, evaluator, interrupt):

		if (isinstance(interrupt, ReturnInterrupt)):
			self._return_value = interrupt.value
			evaluator.handle_interrupt()
		elif (isinstance(interrupt, ContinueInterrupt)):
			raise CWRuntimeError("Invalid use of continue", evaluator.get_line())
		elif (isinstance(interrupt, BreakInterrupt)):
			raise CWRuntimeError("Invalid use of break", evaluator.get_line())

class MaxStatement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('value_1', NumericValue),
			ArgRequest('value_2', NumericValue)
		]

	def _finish(self, evaluator, args):

		return args[0] if (args[0].get_value() > args[1].get_value()) else args[1]