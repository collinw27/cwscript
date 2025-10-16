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

	def __init__(self, args, line, value_type, eval_vars):

		super().__init__(line, value_type, eval_vars)

	def _evaluate(self, evaluator, last_value):

		return evaluator.get_function_scope()

class GlobalScopeStatement (StackOperation):

	def __init__(self, args, line, value_type, eval_vars):

		super().__init__(line, value_type, eval_vars)

	def _evaluate(self, evaluator, last_value):

		return evaluator.get_global_scope()

class IfStatement (StackOperation):

	def __init__(self, args, line, value_type, eval_vars):

		super().__init__(line, value_type, eval_vars)
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

	def __init__(self, args, line, value_type, eval_vars):

		super().__init__(line, value_type, eval_vars)
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

	def __init__(self, args, line, value_type, eval_vars):

		super().__init__(line, value_type, eval_vars)
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

	def __init__(self, args, line, value_type, eval_vars):

		super().__init__(line, value_type, eval_vars)

	def _evaluate(self, evaluator, last_value):

		evaluator.raise_interrupt(ContinueInterrupt())
		return NullValue(evaluator)

class BreakStatement (StackOperation):

	def __init__(self, args, line, value_type, eval_vars):

		super().__init__(line, value_type, eval_vars)

	def _evaluate(self, evaluator, last_value):

		evaluator.raise_interrupt(BreakInterrupt())
		return NullValue(evaluator)

class LengthStatement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('value', ScriptValue)
		]

	def _finish(self, evaluator, args):

		if (isinstance(args[0], StringValue)):
			return IntValue(evaluator, len(args[0].get_value()))
		elif (isinstance(args[0], ListValue)):
			return IntValue(evaluator, len(args[0].get_list()))
		elif (isinstance(args[0], ObjectValue)):
			return IntValue(evaluator, len(args[0].get_dict()))
		else:
			evaluator.unmatched_type_error(args[0], [StringValue, ContainerValue])

class SliceStatement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('value', ScriptValue),
			ArgRequest('start', IntegralValue),
			ArgRequest('end', IntegralValue)
		]

	def _finish(self, evaluator, args):

		# Like Python, this function doesn't care about bounds checking

		if (isinstance(args[0], StringValue)):
			return StringValue(evaluator, args[0].get_value()[args[1].get_value():args[2].get_value()])
		elif (isinstance(args[0], ListValue)):
			return ListValue(evaluator, args[0].get_list()[args[1].get_value():args[2].get_value()])
		else:
			evaluator.unmatched_type_error(args[0], [StringValue, ListValue])

class SliceAfterStatement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('value', ScriptValue),
			ArgRequest('start', IntegralValue)
		]

	def _finish(self, evaluator, args):

		# Like Python, this function doesn't care about bounds checking

		if (isinstance(args[0], StringValue)):
			return StringValue(evaluator, args[0].get_value()[args[1].get_value():])
		elif (isinstance(args[0], ListValue)):
			return ListValue(evaluator, args[0].get_list()[args[1].get_value():])
		else:
			evaluator.unmatched_type_error(args[0], [StringValue, ListValue])

# String & list: try to find index, return -1 if cannot
# Object: try to find key (arbitrary choice if multiple), otherwise return null

class FindStatement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('source', ScriptValue),
			ArgRequest('value', ScriptValue)
		]

	def _finish(self, evaluator, args):

		if (isinstance(args[0], StringValue)):
			evaluator.assert_type(args[1], StringValue)
			return IntValue(evaluator, args[0].get_value().find(args[1].get_value()))
		elif (isinstance(args[0], ListValue)):
			for i, value in enumerate(args[0].get_list()):
				if (value.is_equal(evaluator, args[1])):
					return IntValue(evaluator, i)
			return IntValue(evaluator, -1)
		elif (isinstance(args[0], ObjectValue)):
			for key, value in args[0].get_dict().items():
				if (value.is_equal(evaluator, args[1])):
					return StringValue(evaluator, key)
			return NullValue(evaluator)
		else:
			evaluator.unmatched_type_error(args[1], [StringValue, ContainerValue])

class StringReplaceStatement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('source', StringValue),
			ArgRequest('old', StringValue),
			ArgRequest('new', StringValue)
		]

	def _finish(self, evaluator, args):

		return StringValue(evaluator, args[0].get_value().replace(args[1].get_value(), args[2].get_value()))

class StringUpperCaseStatement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('source', StringValue)
		]

	def _finish(self, evaluator, args):

		return StringValue(evaluator, args[0].get_value().upper())

class StringLowerCaseStatement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('source', StringValue)
		]

	def _finish(self, evaluator, args):

		return StringValue(evaluator, args[0].get_value().lower())

class ListMergeStatement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('list_1', ListValue),
			ArgRequest('list_2', ListValue)
		]

	def _finish(self, evaluator, args):

		return ListValue(evaluator, args[0].get_list() + args[1].get_list())

# Pops value from list/object, returning the removed value

class ContainerPopStatement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('source', ContainerValue),
			ArgRequest('index', ScriptValue)
		]

	def _finish(self, evaluator, args):

		if (isinstance(args[0], ListValue)):
			evaluator.assert_type(args[1], IntegralValue)
			size = len(args[0].get_list())
			if not (-size <= args[1].get_value() < size):
				raise CWRuntimeError("List index '%s' out of bounds" % args[1].get_value(), evaluator.get_line())
			return args[0].get_list().pop(args[1].get_value())
		else:
			evaluator.assert_type(args[1], StringValue)
			if (args[1].get_value() not in args[0].get_dict()):
				raise CWRuntimeError("Invalid variable '%s'" % args[1].get_value(), evaluator.get_line())
			return args[0].get_dict().pop(args[1].get_value())

class RangeStatement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('end', IntegralValue)
		]

	def _finish(self, evaluator, args):

		return ListValue(evaluator, [IntValue(evaluator, a) for a in range(args[0].get_value())])

class AdvancedRangeStatement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('start', IntegralValue),
			ArgRequest('end', IntegralValue),
			ArgRequest('step', IntegralValue)
		]

	def _finish(self, evaluator, args):

		# Returns nothing if the iterator will never terminate
		# (i.e. step direction goes away from end value)
		# Luckily, Python already works like this

		range_iter = range(args[0].get_value(), args[1].get_value(), args[2].get_value())
		return ListValue(evaluator, [IntValue(evaluator, a) for a in range_iter])

# In the previous iteration of this project
# functions were automatically 'bound' to the current object
# Since I'm not sure how 'binding' functions will work in the future,
# they're left out of this class for now

class FunctionStatement (StackOperation):

	def __init__(self, args, line, value_type, eval_vars):

		super().__init__(line, value_type, eval_vars)
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

	def __init__(self, args, line, value_type, eval_vars):

		super().__init__(line, value_type, eval_vars)
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

# Creates an empty object and runs a code block on it
# This is the intended replacement for dictionaries

class ObjectStatement (StackOperation):

	def __init__(self, args, line, value_type, eval_vars):

		super().__init__(line, value_type, eval_vars)
		self._args = args
		self._step = 0

	def _evaluate(self, evaluator, last_value):

		if (self._step == 0):
			self._obj = ObjectValue(evaluator)
			evaluator.add_function_scope(self._obj)
			evaluator.request_value(self._args['body'], ScriptValue)
		else:
			evaluator.pop_function_scope()
			return self._obj
		self._step += 1

	# Return can be used in objects
	# The return value will be ignored, however

	def handle_interrupt(self, evaluator, interrupt):

		if (isinstance(interrupt, ReturnInterrupt)):
			evaluator.handle_interrupt()
		elif (isinstance(interrupt, ContinueInterrupt)):
			raise CWRuntimeError("Invalid use of continue", evaluator.get_line())
		elif (isinstance(interrupt, BreakInterrupt)):
			raise CWRuntimeError("Invalid use of break", evaluator.get_line())

class ObjectKeysStatement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('object', ObjectValue)
		]

	def _finish(self, evaluator, args):

		return ListValue(evaluator, [StringValue(evaluator, key) for key in args[0].get_dict().keys()])

class ObjectValuesStatement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('object', ObjectValue)
		]

	def _finish(self, evaluator, args):

		return ListValue(evaluator, list(args[0].get_dict().values()))

class MaxStatement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('value_1', NumericValue),
			ArgRequest('value_2', NumericValue)
		]

	def _finish(self, evaluator, args):

		return args[0] if (args[0].get_value() > args[1].get_value()) else args[1]

class MinStatement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('value_1', NumericValue),
			ArgRequest('value_2', NumericValue)
		]

	def _finish(self, evaluator, args):

		return args[0] if (args[0].get_value() < args[1].get_value()) else args[1]