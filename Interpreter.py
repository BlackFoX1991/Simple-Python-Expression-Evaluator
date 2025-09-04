from Tokenizer import TokenContainer, Ttypes


class Position:
    __TPos = 0

    @classmethod
    def Reset(cls):
        cls.__TPos = 0

    @classmethod
    def Move(cls):
        cls.__TPos += 1

    @classmethod
    def Undo(cls):
        cls.__TPos -= 1

    @classmethod
    def Get(cls):
        return cls.__TPos


class TokenCollection:
    __Tokens: TokenContainer = None

    @classmethod
    def Init(cls, ListT: TokenContainer):
        cls.__Tokens = ListT
        Position.Reset()

    @classmethod
    def Current(cls):
        return cls.__Tokens.TokenList[Position.Get()]

    @classmethod
    def Length(cls):
        return len(cls.__Tokens.TokenList)


def ThrowInterError(Text):
    pos = Position.Get()
    print(f"{Text} at token index {pos}")
    exit(1)


def compute(TokenList: TokenContainer):
    TokenCollection.Init(TokenList)
    result = Term()
    return result


def Expr():
    token = TokenCollection.Current()

    # Number literal
    if token.ttype == Ttypes.TNUM:
        Position.Move()
        return float(token.tvalue)

    # Parentheses
    elif token.ttype == Ttypes.T_LPAREN:
        Position.Move()
        lvalue = Term()
        if Position.Get() < TokenCollection.Length() and \
           TokenCollection.Current().ttype == Ttypes.T_RPAREN:
            Position.Move()
        else:
            ThrowInterError("Error: Expected parenthesis close")
        return lvalue

    ThrowInterError("Error: Unexpected token")
    return 0


def Expo():
    lvalue = Expr()
    while Position.Get() < TokenCollection.Length() and TokenCollection.Current().ttype == Ttypes.TEXP:
        Position.Move()
        rvalue = Expr()
        lvalue = lvalue ** rvalue
    return lvalue


def Factor():
    lvalue = Expo()
    while Position.Get() < TokenCollection.Length() and \
          TokenCollection.Current().ttype in (Ttypes.TMULT, Ttypes.TDIV):
        op = TokenCollection.Current().ttype
        Position.Move()
        rvalue = Expo()
        if op == Ttypes.TMULT:
            lvalue *= rvalue
        else:
            lvalue /= rvalue
    return lvalue


def Term():
    lvalue = Factor()
    while Position.Get() < TokenCollection.Length() and \
          TokenCollection.Current().ttype in (Ttypes.TADD, Ttypes.TSUB):
        op = TokenCollection.Current().ttype
        Position.Move()
        rvalue = Factor()
        if op == Ttypes.TADD:
            lvalue += rvalue
        else:
            lvalue -= rvalue
    return lvalue
