import re


class JackTokenizer:
    def __init__(self, filePath):
        self.file = open(filePath)
        self.text = self.file.read()  # read entire source file
        self.file.close()
        self.tokens = []

        self.preproccess()
        self.currentToken = ''
        self.currentTokenType = ''
        self.tokenCounter = 0
        self.keywords = ['class', 'constructor', 'function', 'method', 'field',
                         'static', 'var', 'int', 'char', 'boolean', 'void', 'true',
                         'false', 'null', 'this', 'let', 'do', 'if', 'else',
                         'while', 'return']
        self.symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+',
                        '-', '*', '/', '&', '|', '<', '>', '=', '~']

    def removeCommentsFromInput(self):
        pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
        # first group captures quoted strings (double or single)
        # second group captures comments (//single-line or /* multi-line */)
        regex = re.compile(pattern, re.MULTILINE|re.DOTALL)

        def _replacer(match):
            # if the 2nd group (capturing comments) is not None,
            # it means we have captured a non-quoted (real) comment string.
            if match.group(2) is not None:
                return "" # so we will return empty to remove the comment
            else: # otherwise, we will return the 1st group
                return match.group(1) # captured quoted-string

        self.text = regex.sub(_replacer, self.text)

    def preproccess(self):
        """General method that takes the raw input and tokenizes it.\n
           Removes comments' splits into list and removes whitespace.
        """
        self.removeCommentsFromInput()
        self.tokens = re.split('([(;})\[\]~{.,-])| ', self.text)
        self.tokens = [item for item in self.tokens if item is not None]
        self.tokens = [item.strip() for item in self.tokens]
        self.tokens = [item for item in self.tokens if item != '']
        self.fixStrings()

    def fixStrings(self):
        """Smushes together adjacent substrings in the tokens lists, that are part of the same string constant.
        """
        string = False
        appendedString = ""
        newlist = []
        for line in self.tokens:
            if "\"" in line and string == False:
                string = True
                appendedString = line
            elif string == True and "\"" in line:
                string = False
                appendedString += " " + line
                newlist.append(appendedString)
            elif string == True:
                appendedString += " " + line

            elif line.startswith("-") and len(line) > 1:
                newlist.append("-")
                newlist.append(line[1:])
            else:
                newlist.append(line)
        self.tokens = newlist

    def hasMoreTokens(self):
        return self.tokenCounter < len(self.tokens)

    def advance(self):
        self.currentToken = self.tokens[self.tokenCounter]
        self.tokenCounter += 1

        self.currentTokenType = self.tokenType()
        if self.currentTokenType == 'KEYWORD':
            self.currentToken = self.keyword()
        elif self.currentTokenType == 'IDENTIFIER':
            self.currentToken = self.identifier()
        elif self.currentTokenType == 'INT_CONST':
            self.currentToken = self.intVal()
        elif self.currentTokenType == 'SYMBOL':
            self.currentToken = self.symbol()
        elif self.currentTokenType == 'STRING_CONST':
            self.currentToken = self.stringVal()

    def tokenType(self):
        current = self.currentToken

        if re.match('[a-zA-Z_]', current):
            if current in self.keywords:
                return 'KEYWORD'
            else:
                return 'IDENTIFIER'
        elif current in self.symbols:
            return 'SYMBOL'
        elif current.isnumeric():
            return 'INT_CONST'
        elif current.startswith('\"') and current.endswith('\"'):
            return 'STRING_CONST'
        else:
            print('ERROR: invalid token: ' + current)
            exit()

    def keyword(self):
        return self.currentToken

    def symbol(self):
        return self.currentToken

    def identifier(self):
        return self.currentToken

    def intVal(self):
        return self.currentToken

    def stringVal(self):
        return self.currentToken.strip('\"')
