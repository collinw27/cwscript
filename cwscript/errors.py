
# Represents an error that I'm too lazy to categorize

class CWError (Exception):

    def __init__(self, type_, message):

        super().__init__(message)
        self._message = message
        self._type = type_

    def __str__(self):

        return f"{self._type}: {self._message}"

class CWLexError (CWError):

    def __init__(self, message):

        super().__init__("Lex error", message)

class CWParseError (CWError):

    def __init__(self, message):

        super().__init__("Parse error", message)