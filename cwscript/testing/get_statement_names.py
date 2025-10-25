from cwscript import rules

# Used for formatting in Sublime syntax file

if (__name__ == '__main__'):
	print('|'.join(rules.get_statement_names() + ['else']))