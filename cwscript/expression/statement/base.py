from cwscript.expression.dynamic import DynamicExpression

class StatementExpression (DynamicExpression):

	# Called by StackOperation, values are passed from runner
	# Arguments are received in the same order they were passed to get_stack()

	@staticmethod
	def evaluate(runner, args):

		raise NotImplementedError()