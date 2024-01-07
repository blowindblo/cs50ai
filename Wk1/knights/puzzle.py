from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    # A is knight/knave, cannot be both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # If A is a Knight, his statement is True
    Implication(AKnight, And(AKnight, AKnave)),

    # If A is a Knave, his statement is False
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    # A is knight/knave, cannot be both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # B is knight/knave, cannot be both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # If A is a Knight, his statement is True
    Implication(AKnight, And(AKnave, BKnave)),
    # If A is a Knave, his statement is False
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    # A is knight/knave, cannot be both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # B is knight/knave, cannot be both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # If A is a Knight, his statement is True
    Implication(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),
    # If A is a Knave, his statement is False
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),

    # If B is a Knight, his statement is True
    Implication(BKnight, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # If B is a Knave, his statement is False
    Implication(BKnave, Or(And(AKnave, BKnave), And(AKnight, BKnight))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
    # A is knight/knave, cannot be both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # B is knight/knave, cannot be both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # C is knight/knave, cannot be both
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),


    # B says "A said 'I am a knave'."
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    
    # Biconditional(BKnight, And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))),
    # if B is a Knave, all we know is that A did not say "I am a knave". A could have said something else or nothing at all
    # Biconditional(BKnave, Not(AKnave)),

    # B's statement
    # If B is a knight, his statement "C is a knave" has to be true and if C is a knave, then B told the truth and is thus a knight
    Biconditional(BKnight, CKnave),
    # Biconditional(BKnave, CKnight),
    # If C is a knight, his statement "A is a knight" has to be true and if A is a knight, then C told the truth and is thus a knight
    Biconditional(CKnight, AKnight),
    # Biconditional(CKnave, AKnave)

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
