
class CWError (Exception):

    def __init__(self, type_, message, line):

        super().__init__(message)
        self._message = message
        self._type = type_
        self._line = line
        self._context = None

    def __str__(self):

        return "\n\n" + self.str()

    def str(self):

        if (self._context is None):
            return f">>> {self._type} at [UNKNOWN LINE]: {self._message}"
        else:
            return f">>> {self._type} at line {self._line + 1}: {self._message}\n{self._context}"

    def get_line(self):

        return self._line

    def set_context(self, snippet):

        self._context = snippet

class CWLexError (CWError):

    def __init__(self, message, line):

        super().__init__("Lex error", message, line)

class CWParseError (CWError):

    def __init__(self, message, line):

        super().__init__("Parse error", message, line)

class CWRuntimeError (CWError):

    def __init__(self, message, line):

        super().__init__("Runtime error", message, line)

# Represents an error that I'm too lazy to categorize

class CWMiscError (CWError):

    def __init__(self, message, line):

        super().__init__("Error", message, line)

# A special error that will be caught by the evaluator
# and raised as an exception the user can catch

class CatchableError (Exception):

    def __init__(self, e_type, body):

        self.type = e_type
        self.body = body