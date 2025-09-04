from enum import Enum


class Ttypes(Enum):
    # Haupt-Typen
    TNULL = 0
    TNUM = 1

    # Operatoren
    TADD = 2
    TSUB = 3
    TMULT = 4
    TDIV = 5
    TEXP = 6

    # Tokens
    T_LPAREN = 7
    T_RPAREN = 8

    # Other
    T_IDENT = 9


class Tokens:
    def __init__(self, TokenValue, TokenType, line=1, linepos=1):
        self.ttype = TokenType
        self.tvalue = TokenValue
        self.tline = line
        self.tlinepos = linepos

    def __repr__(self):
        return f"Tokens({self.tvalue}, {self.ttype})"


class TokenContainer:
    def __init__(self):
        self.TokenList = []

    def AddToken(self, TokenType, Value, line=1, linepos=1):
        self.TokenList.append(Tokens(Value, TokenType, line, linepos))

    def __len__(self):
        return len(self.TokenList)

    def __getitem__(self, idx):
        return self.TokenList[idx]


# --------------------------
# Lexer implementation
# --------------------------

def GetNumber(code, pos):
    tempNum = ""
    while pos < len(code) and (code[pos].isdigit() or code[pos] == "."):
        # prevent multiple dots
        if code[pos] == "." and "." in tempNum:
            raise ValueError("Error: Invalid floating point number")
        tempNum += code[pos]
        pos += 1
    return tempNum, pos

def GetIdent(code, pos):
    tempIdent = ""
    while pos < len(code) and (code[pos].isalpha() or code[pos] == "_"):
        tempIdent += code[pos]
        pos += 1
    return tempIdent, pos


def tokenize(code: str) -> TokenContainer:
    tokens = TokenContainer()
    pos = 0
    line = 1
    linepos = 1

    while pos < len(code):
        ch = code[pos]

        # Skip whitespace
        if ch.isspace():
            if ch == "\n":
                line += 1
                linepos = 1
            else:
                linepos += 1
            pos += 1
            continue

        # Number
        if ch.isdigit():
            number, pos = GetNumber(code, pos)
            tokens.AddToken(Ttypes.TNUM, number, line, linepos)
            linepos += len(number)
            continue
        elif ch.isalpha() or ch == "_":
            ident, pos = GetIdent(code, pos)
            tokens.AddToken(Ttypes.T_IDENT, ident, line, linepos)
            linepos += len(ident)
            continue

        # Operators & parentheses
        mType = None
        if ch == "+": mType = Ttypes.TADD
        elif ch == "-": mType = Ttypes.TSUB
        elif ch == "*": mType = Ttypes.TMULT
        elif ch == "/": mType = Ttypes.TDIV
        elif ch == "^": mType = Ttypes.TEXP
        elif ch == "(": mType = Ttypes.T_LPAREN
        elif ch == ")": mType = Ttypes.T_RPAREN

        if mType is not None:
            tokens.AddToken(mType, ch, line, linepos)
            pos += 1
            linepos += 1
        else:
            raise ValueError(f"Invalid token '{ch}' at line {line}, pos {linepos}")

    return tokens


