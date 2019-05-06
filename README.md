# KlondikeGame
A simple python version of Klondike Game

    *------------------------------------------------------*
    *-------------* Thumb and Pouch Solitaire *------------*
    *------------------------------------------------------*
    Foundation: Columns are numbered 1, 2, ..., 4; built
                up by rank and by suit from Ace to King.
                You can't move any card from foundation,
                you can just put in.

    Tableau:    Columns are numbered 1, 2, 3, ..., 7; built
                down by rank only, but cards can't be laid on
                one another if they are from the same suit.
                You can move one or more faced-up cards from
                one tableau to another. An empty spot can be
                filled with any card(s) from any tableau or
                the top card from the waste.


     To win, all cards must be in the Foundation.


=================== FOUNDATIONS ===================

f1        f2        f3        f4
[]        []        []        []

===================== TABLEAU =====================

t1      t2      t3      t4      t5      t6      t7
5♠      XX      XX      XX      XX      XX      XX
        6♠      XX      XX      XX      XX      XX
                9♣      XX      XX      XX      XX
                        10♦     XX      XX      XX
                                2♣      XX      XX
                                        5♣      XX
                                                8♥
                                                
=================== STOCK/WASTE ===================

Stock #(23) --> [4♦]

Game commands:

    TF x y     Move card from Tableau column x to Foundation y.
    TT x y n   Move pile of length n >= 1 from Tableau column x
                to Tableau column y.
    WF x       Move the top card from the waste to Foundation x
    WT x       Move the top card from the waste to Tableau column x
    SW         Draw one card from Stock to Waste
    R          Restart the game with a re-shuffle.
    H          Display this menu of choices
    Q          Quit the game
