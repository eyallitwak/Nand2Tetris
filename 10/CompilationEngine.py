import JackTokenizer


class CompilationEngine:

    def __init__(self, inputFilepath, outputFilepath):
        """Initializes a CompilationEngine object\n
        This also initiates the compilation, so no need to call any other method.

        Args:
            inputFilepath: path of .jack file to compile
            outputFilepath: path of .xml file that will be the output
        """
        self.tokenizer = JackTokenizer.JackTokenizer(inputFilepath)
        self.file = open(outputFilepath, "w+")
        self.indentCounter = 0
        self.types = ["int", "boolean", "char"]

        self.compileClass()  # THIS COMPILES

    def writeToken(self):
        escapes = {"<": "&lt;",
                   ">": "&gt;",
                   "\"": "&quot;",
                   "&": "&amp;"}

        token = self.tokenizer.currentToken
        token = escapes[token] if token in escapes.keys() else token
        typeDict = {'SYMBOL': 'symbol',
                    'IDENTIFIER': 'identifier',
                    'KEYWORD': 'keyword',
                    'STRING_CONST': 'stringConstant',
                    'INT_CONST': 'integerConstant'}
        type = typeDict[self.tokenizer.currentTokenType]

        print("  " * self.indentCounter +
              f"<{type}> {token} </{type}>", file=self.file)

    def checkToken(self, string):
        if self.tokenizer.currentToken in string:
            self.writeToken()
            self.tokenizer.advance()

    def checkTokenType(self, string):
        if self.tokenizer.currentTokenType in string:
            self.writeToken()
            self.tokenizer.advance()

    def checkVarType(self):
        if self.tokenizer.currentToken in self.types:
            self.writeToken()
            self.tokenizer.advance()

    def xmlOpenTag(self, tag):
        print("  " * self.indentCounter + "<" + tag + ">", file=self.file)
        self.indentCounter += 1

    def xmlCloseTag(self, tag):
        self.indentCounter -= 1
        print("  " * self.indentCounter + "</" + tag + ">", file=self.file)

    # Compiles a complete class.
    def compileClass(self):
        self.tokenizer.advance()
        self.xmlOpenTag("class")

        self.checkToken("class")
        self.checkTokenType("IDENTIFIER")
        self.checkToken("{")
        while self.tokenizer.currentToken not in {"}", "constructor", "function", "method", "void"}:
            self.compileClassVarDec()
        while self.tokenizer.currentToken != "}":
            self.compileSubroutine()

        self.writeToken()  # deals with the last token, which is always }
        self.xmlCloseTag("class")

    # Compiles a static or field declaration.
    def compileClassVarDec(self):
        self.xmlOpenTag("classVarDec")

        self.checkToken({"field", "static"})
        if self.tokenizer.currentTokenType == "IDENTIFIER":
            self.checkTokenType("IDENTIFIER")
        else:
            self.checkToken(self.types)
        self.checkTokenType("IDENTIFIER")
        while self.tokenizer.currentToken != ";":
            self.checkToken(",")
            self.checkTokenType("IDENTIFIER")
        self.checkToken(";")

        self.xmlCloseTag("classVarDec")

    # Compiles a complete method, function or constructor.
    def compileSubroutine(self):
        self.xmlOpenTag("subroutineDec")

        self.checkToken({"constructor", "function", "method", "void"})
        if self.tokenizer.currentTokenType == "IDENTIFIER":
            self.checkTokenType("IDENTIFIER")
        else:
            self.checkToken(self.types + ["void"])
        self.checkTokenType("IDENTIFIER")
        self.checkToken("(")
        self.compileParameterList()
        self.checkToken(")")
        self.compileSubroutineBody()

        self.xmlCloseTag("subroutineDec")

    # Compiles the boday of a method, function or constructor.
    def compileSubroutineBody(self):
        self.xmlOpenTag("subroutineBody")

        self.checkToken("{")
        while self.tokenizer.currentToken not in {"let", "if", "while", "do", "return"}:
            self.compileVarDec()
        self.compileStatements()
        self.checkToken("}")

        self.xmlCloseTag("subroutineBody")

    # Compiles a (possibly empty) parameter list, not including the enclosing"()".
    def compileParameterList(self):
        self.xmlOpenTag("parameterList")
        if self.tokenizer.currentToken != ")":

            if self.tokenizer.currentTokenType == "IDENTIFIER":
                self.checkTokenType("IDENTIFIER")
            else:
                self.checkToken(self.types)
            self.checkTokenType("IDENTIFIER")
            while self.tokenizer.currentToken != ")":
                self.checkToken(",")
                self.checkVarType()
                self.checkTokenType("IDENTIFIER")

        self.xmlCloseTag("parameterList")

    # Compiles a var declaration.
    def compileVarDec(self):
        self.xmlOpenTag("varDec")

        self.checkToken("var")
        if self.tokenizer.currentTokenType == "IDENTIFIER":
            self.checkTokenType("IDENTIFIER")
        else:
            self.checkToken(self.types)
        self.checkTokenType("IDENTIFIER")
        while self.tokenizer.currentToken != (";"):
            self.checkToken(",")
            self.checkTokenType("IDENTIFIER")
        self.checkToken(";")

        self.xmlCloseTag("varDec")

    # Compiles a sequence of statements, not including the enclosing "{}".
    def compileStatements(self):
        self.xmlOpenTag("statements")

        statementPrefixes = {
            "let": self.compileLet,
            "do": self.compileDo,
            "if": self.compileIf,
            "while": self.compileWhile,
            "return": self.compileReturn
        }
        while self.tokenizer.currentToken != ("}"):
            if self.tokenizer.currentToken in statementPrefixes:
                statementPrefixes[self.tokenizer.currentToken]()

        self.xmlCloseTag("statements")

    # Compiles a do statement.
    def compileDo(self):
        self.xmlOpenTag("doStatement")

        self.checkToken("do")
        self.compileExpression(True)
        self.checkToken(";")

        self.xmlCloseTag("doStatement")

    # Compiles a let statement.
    def compileLet(self):
        self.xmlOpenTag("letStatement")

        self.checkToken("let")
        self.checkTokenType("IDENTIFIER")
        if self.tokenizer.currentToken == "[":
            self.checkToken("[")
            self.compileExpression(False)
            self.checkToken("]")
        self.checkToken("=")
        self.compileExpression(False)
        self.checkToken(";")

        self.xmlCloseTag("letStatement")

    # Compiles a while statement.
    def compileWhile(self):
        self.xmlOpenTag("whileStatement")

        self.checkToken("while")
        self.checkToken("(")
        self.compileExpression(False)
        self.checkToken(")")
        self.checkToken("{")
        self.compileStatements()
        self.checkToken("}")

        self.xmlCloseTag("whileStatement")

    # Compiles a return statement.
    def compileReturn(self):
        self.xmlOpenTag("returnStatement")

        self.checkToken("return")
        if self.tokenizer.currentToken != ";":
            self.compileExpression(False)
        self.checkToken(";")

        self.xmlCloseTag("returnStatement")

    # Compiles an if statement, possibly with a trailing else clause.
    def compileIf(self):
        self.xmlOpenTag("ifStatement")

        self.checkToken("if")
        self.checkToken("(")
        self.compileExpression(False)
        self.checkToken(")")
        self.checkToken("{")
        self.compileStatements()
        self.checkToken("}")
        if self.tokenizer.currentToken == "else":
            self.checkToken("else")
            self.checkToken("{")
            self.compileStatements()
            self.checkToken("}")

        self.xmlCloseTag("ifStatement")

    # Compiles an expression.
    def compileExpression(self, insideDo):
        if not insideDo:
            self.xmlOpenTag("expression")

        self.compileTerm(insideDo)
        while self.tokenizer.currentToken not in {"]", ")", ";", ",", "("}:
            self.checkToken({"+", "-", "*", "/", "&", "|", ">", "<", "="})
            self.compileTerm(insideDo)

        if not insideDo:
            self.xmlCloseTag("expression")

    # Compiles a term.
    def compileTerm(self, insideDo):
        if not insideDo:
            self.xmlOpenTag("term")

        invalidKeywords = {"class", "constructor", "function", "method", "field",
                           "static", "var", "int", "char", "boolean", "void",
                           "let", "do", "if", "else", "while", "return"}

        if self.tokenizer.currentTokenType == "IDENTIFIER":
            self.checkTokenType("IDENTIFIER")
            if self.tokenizer.currentToken == "[":  # Identifier is an array
                self.checkToken("[")
                self.compileExpression(False)
                self.checkToken("]")
            # Identifier is a subroutine call
            elif self.tokenizer.currentToken in {"(", "."}:
                self.compileSubroutineCall()

        elif self.tokenizer.currentToken in {"-", "~"}:
            self.checkToken({"-", "~"})
            self.compileTerm(insideDo)

        elif self.tokenizer.currentToken == "(":
            self.checkToken("(")
            self.compileExpression(False)
            self.checkToken(")")

        elif self.tokenizer.currentToken not in invalidKeywords:
            self.writeToken()
            self.tokenizer.advance()

        if not insideDo:
            self.xmlCloseTag("term")

    def compileSubroutineCall(self):
        if self.tokenizer.currentToken == ".":
            self.checkToken(".")
            self.checkTokenType("IDENTIFIER")
        self.checkToken("(")
        self.compileExpressionList()
        self.checkToken(")")

    # Compiles a (possibily empty) comma-seperated list of expressions.
    def compileExpressionList(self):
        self.xmlOpenTag("expressionList")

        if self.tokenizer.currentToken != ")":
            self.compileExpression(False)
        while self.tokenizer.currentToken != ")":
            self.checkToken(",")
            self.compileExpression(False)

        self.xmlCloseTag("expressionList")
