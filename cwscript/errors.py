
class CWError (Exception):

    def __init__(self, type_, message, line):

        super().__init__(message)
        self._message = message
        self._type = type_
        self._line = line
        self._context = None

    def __str__(self):

        if (self._context is None):
            return f"\n\n>>> {self._type} at [UNKNOWN LINE]: {self._message}"
        else:
            return f"\n\n{self._context}\n>>> {self._type} at line {self._line + 1}: {self._message}"

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

# Represents an error that I'm too lazy to categorize

class CWMiscError (CWError):

    def __init__(self, message, line):

        super().__init__("Error", message, line)