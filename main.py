import Tokenizer
import Interpreter


def main():
    TList = Tokenizer.tokenize("(((3^2 + 5*4) - (7 - 2)^3) / (8 + 6*(2^3 - 3)) + 9)")
    for TK in TList:
        print(str(TK.ttype) + " >> " + TK.tvalue)

    print(Interpreter.compute(TList))

if __name__ == "__main__":
    main()
