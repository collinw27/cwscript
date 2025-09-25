
# String groups are split into lists so ('' in <list>) returns false

WHITESPACE = list(" \n\t\r")
QUOTES = list("'\"")
OPENING_GROUPINGS = list("({[")
CLOSING_GROUPINGS = list(")}]")
BOOLS = ["true", "false"]
NEWLINES = list('\n\r')

ALPHA = list('abcdefghijklmnopqrstuvwxyz')
NUMS = list('0123456789')

VAR_ALLOWED = ALPHA + NUMS + ['_']