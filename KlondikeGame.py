########################################################### 
#  Computer Project #10
# 
#  Algorithm 
#    import the cards classes  
#    use the classes to design Thump and Punch soltire game 
#    prompt the user to enter new command 
#    follow the game guidline to make sure that directions are followed 
############################################################ 
import cards        # this is required
# importing copy to use deepcopy method 
import copy

YAY_BANNER = """
__   __             __        ___                       _ _ _ 
\ \ / /_ _ _   _    \ \      / (_)_ __  _ __   ___ _ __| | | |
 \ V / _` | | | |    \ \ /\ / /| | '_ \| '_ \ / _ \ '__| | | |
  | | (_| | |_| |_    \ V  V / | | | | | | | |  __/ |  |_|_|_|
  |_|\__,_|\__, ( )    \_/\_/  |_|_| |_|_| |_|\___|_|  (_|_|_)
           |___/|/                                            

"""

RULES = """
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
"""

MENU = """
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
"""

def valid_fnd_move(src_card, dest_card):
    """
        This function decides whether a card is allowed to be placed in
        a foundation pile from either tableau or waste piles. it returns True or False
    """
    # if rank of destination card is 1 less than source card
    # and it's of the same suit, True; and False otherwise
    if dest_card.rank() + 1 == src_card.rank()  \
    and dest_card.suit() == src_card.suit():
        return True
    else:
        return False
        
def valid_tab_move(src_card, dest_card):
    """
        Check whether a move to tableau is valid and trurn True or False
    """    
    # if rank of destination is 1 more than source card and from different suite
    # then return True; return False otherwise
    if dest_card.rank() == src_card.rank() + 1 \
    and dest_card.suit() != src_card.suit():
        return True
    else:
        return False
            
def tableau_to_foundation(tab, fnd):
    """
        This function moves a card from a tableau pile to a foundation pile
        it appends the card -if valid- to fnd, and remove it from tab pile
    """ 
    # if both tab and fnd are not empty
    if tab and fnd:
        # check if the move is valid in tableau using another function
        # The last card has to be face up and satisfy the transfer requirements
        if tab[-1].is_face_up() and valid_fnd_move(tab[-1], fnd[-1]):
            fnd.append(tab.pop())
        else:
            raise RuntimeError('Error: invalid move due to mismatched cards')
    # if waste is not empty
    elif tab:
        if not fnd: #if foundation pile is empty
            # if top card of waste is an ace, add it to the empty fnd pile
            if tab[-1].rank() == 1 and tab[-1].is_face_up():
                fnd.append(tab.pop())
            else:
                raise RuntimeError('Error: tableau top card should be an ace')
    # error when the tableau pile is empty
    elif not tab:
        raise RuntimeError('Error: empty tableau pile')
            

def tableau_to_tableau(tab1, tab2, n):
    """
        This function take a card or set of cards from a tableau pile and transer
        it/them to another pile; it makes sure requirements are met thru another function
    """    
    # check if tab1 is not empty
    if tab1 and len(tab1)>= n :
        # if tab2 is not empty, check if cards are matched
        if tab2:
            # if last card from selected cards is face up the transfer is valid
            if tab1[-n].is_face_up() and valid_tab_move(tab1[-n], tab2[-1]):
                # extend the card(s) to the other pile
                tab2.extend(tab1[-n:])
                # delete the card(s) from the original pile
                del tab1[-n:]
            # if the last card is face down, then you cannot transfer
            elif not tab1[-n].is_face_up():
                raise RuntimeError('Error: insufficient number of cards to move')
            else: 
                raise RuntimeError('Error: invalid move due to mismatched cards')
        # if tab2 is empty, any cards can be moved, no match is required
        else:
            if tab1[-n].is_face_up():
                tab2.extend(tab1[-n:])
                del tab1[-n:]
            # if the last one is not face up, cannot move
            else:
                raise RuntimeError('Error: insufficient number of cards to move')
    # if the first pile is empty or small (less than n), you cannot move card(s)
    else: 
        raise RuntimeError('Error: You cannot move from empty or small pile')
            
    
def waste_to_foundation(waste, fnd, stock):
    """
        Takes a card from waste pile and transfer it to a foundation pile
    """    
    # fnd is one pile from foundation
    # if waste and fnd pile are not empty
    if fnd and waste:
        # check if the move is valid in foundation
        if valid_fnd_move(waste[-1], fnd[-1]):
            fnd.append(waste.pop())
        else:
            raise RuntimeError('Error: invalid move due to mismatched cards')
    # if fnd is empty and waste is not empty
    elif not fnd and waste:
        # if top card of waste is an ace, add it to the empty fnd pile
        if waste[-1].rank() == 1 :
            fnd.append(waste.pop())
        else:
            raise RuntimeError('Error: the waste card should be an ace')
    elif not waste:
        raise RuntimeError('Error: empty waste pile')

def waste_to_tableau(waste, tab, stock):
    """
        Takes a card from waste and transfer it to a tableau pile
    """    
    # tab is one column only ! 
    # if tab and waste piles are not empty:
    if tab and waste:
        # check if the move is valid in tableau, if so, append the last card
        if valid_tab_move(waste[-1], tab[-1]):
            tab.append(waste.pop())
        else:
            raise RuntimeError('Error: invalid move due to mismatched cards')
    # if tableau is empty and waste not empty, you can add any card from waste
    elif not tab and waste:
        tab.append(waste.pop())
    # if waste pile is empty, raise an error
    elif not waste:
        raise RuntimeError('Error: empty waste or tableau pile')
                    
def stock_to_waste(stock, waste):
    """
        Takes a card from stock and place it int the waste pile using deal method
    """
    waste.append(stock.deal())

                            
def is_winner(foundation):
    """
        This function makes sure that the winning criteria are met
        reutns True or False
    """
    # loop over foundation piles
    for i in foundation:
        # if 13 cards and the top one is the king, return True after checking all of them
        if len(i) == 13 and i[-1].rank() == 13:
            continue
        # if one of the criteria is not met, return False
        else:
            return False
    return True
        

def setup_game():
    """
        The game setup function, it has 4 foundation piles, 7 tableau piles, 
        1 stock and 1 waste pile. All of them are currently empty. This 
        function populates the tableau and the stock pile from a standard 
        card deck. 

        7 Tableau: There will be one card in the first pile, two cards in the 
        second, three in the third, and so on. The top card in each pile is 
        dealt face up, all others are face down. Total 28 cards.

        Stock: All the cards left on the deck (52 - 28 = 24 cards) will go 
        into the stock pile. 

        Waste: Initially, the top card from the stock will be moved into the 
        waste for play. Therefore, the waste will have 1 card and the stock 
        will be left with 23 cards at the initial set-up.

        This function will return a tuple: (foundation, tableau, stock, waste)
    """
    # you must use this deck for the entire game.
    # the stock works best as a 'deck' so initialize it as a 'deck'
    stock = cards.Deck()
    stock.shuffle()
    # the game piles are here, you must use these.
    foundation = [[], [], [], []]           # list of 4 lists
    tableau = [[], [], [], [], [], [], []]  # list of 7 lists
    waste = []                              # one list


    while True:
        # get an index for pile and access the pile list
        for count, a_tab in enumerate(tableau):
            # if the index is equal to the length of card
            # add a face up card to the first card from the left
            if len(a_tab) == count:
                a_tab.append(stock.deal())
            # if len of pile is one greater than index, don't add cards
            elif len(a_tab) == count + 1:
                continue
            else:
                a_tab_temp = stock.deal()
                a_tab_temp.flip_card()
                a_tab.append(a_tab_temp)
        # if we reach the last tableau pile and there're seven cards, stop
        if len(tableau[-1]) == 7:
            break
        # Deal one card to the waste pile
    waste.append(stock.deal())

    """
    #This was the old (wrong according to project description) way of ordering cards

        # deal cards into tableau, all are face up.
    for i in range(len(tableau)):
        tableau[i].append(stock.deal())
        # while the length of tableau pile not 1 more than the pile number,
        # append cards to the pile
        while len(tableau[i]) != i+1:
            tableau[i].append(stock.deal())
    # flip cards in tableau except the last one (the top one)
    for tab in tableau:
        for card in tab:
            # don't flip it if it's the top (last) card
            if card != tab[-1]:
                card.flip_card()
    # Deal one card to the waste pile
    waste.append(stock.deal())
    """

    return foundation, tableau, stock, waste

def display_game(foundation, tableau, stock, waste):
    """
    This function display the current foundation, tableau, and waste piles
    in a convenient way.
    """
    print('='*19,'FOUNDATIONS','='*19)
    # create an empty list and append to it the last card of each foundation pile
    f_list = []
    for fnd_pile in foundation: 
        if fnd_pile:
            f_list.append([fnd_pile[-1]])
        # if foundation pile is empty, append pile as is (empty)
        else:
            f_list.append(fnd_pile)
    # assign each foundation pile to a different variable
    f1, f2, f3, f4 = f_list
    print('{:10}{:10}{:10}{:10}'.format('f1','f2','f3','f4'))
    # convert to str using !s (found this way from the internet)
    print('{!s:10s}{!s:10s}{!s:10s}{!s:10s}'.format(f1,f2,f3,f4))
    
    print('='*21,'TABLEAU','='*21)
    print('{:8}{:8}{:8}{:8}{:8}{:8}{:8}'.format('t1','t2','t3','t4','t5','t6','t7'))
    # deep copy the tableau piles in order to add empty strings 
    main_list = copy.deepcopy(tableau)
    # find the longest tableau pile and make all other piles of the same length
    len_find = []
    for tab_pile in main_list:
        len_find.append(len(tab_pile))
    max_len = max(len_find)
    # fill in empty strings in the shorter piles
    for tab_pile in main_list:
        while len(tab_pile) < max_len:
            tab_pile.append('')
    # Assign different variables to the main list
    t1, t2, t3, t4, t5, t6, t7 = main_list
    for i in range(max_len):
        print('{!s:8s}{!s:8s}{!s:8s}{!s:8s}{!s:8s}{!s:8s}{!s:8s}'.format(t1[i], \
        t2[i], t3[i], t4[i], t5[i], t6[i], t7[i]))
    
    print('='*19,'STOCK/WASTE','='*19)
    print('Stock #({}) --> {}'.format(len(stock), waste))

def main():
    """
    A main function is used to organized the code and eliminate global variable usage
    """
    # print rules, minue and display current piles; then ask for a command
    print(RULES)
    fnd, tab, stock, waste = setup_game()
    display_game(fnd, tab, stock, waste)
    print(MENU)
    # lowercase the input
    command = input("prompt :> ").strip().lower()
    # keep looping until user input q
    while command.strip().lower() != 'q':
        try:
            # command_status is used to asses whether the user inputted a valid command or not
            command_status = True
            # Menue 
            if command == 'h':
                print(MENU)
            # Reset and re-shuffle
            elif command == 'r':
                # shuffle is done inside set_game() function
                fnd, tab, stock, waste = setup_game()
            # stock to waste
            elif command == 'sw':
                # check if stock is not empty
                if stock:
                    # call a function to do the required command
                    stock_to_waste(stock, waste)
                else: 
                    raise RuntimeError('Error: No more cards in stock')
            # waste to tableau
            elif 'wt' in command:
                # command list is used to seperate the different commands needed
                command_list = command.split()
                # make sure only the required commands are inputted
                if len(command_list) == 2:
                    # convert to integer to subtract later on
                    col_num = int(command_list[1])
                    # if numbers are out of range, raise an error
                    if not 1 <= col_num <= 7:
                        raise RuntimeError('Error: arguments must be numbers in range')
                    # substracted 1 because first index in lists is zero
                    waste_to_tableau(waste, tab[col_num - 1], stock)
                else:
                    raise RuntimeError('Error: wrong number of arguments')
            # waste to foundation
            elif 'wf' in command:
                # same comments as before
                command_list = command.split()
                if len(command_list) == 2:
                    fnd_num = int(command_list[1])
                    if not 1 <= fnd_num <= 4:
                        raise RuntimeError('Error: arguments must be numbers in range')
                    # substracted 1 because first index in lists is zero
                    waste_to_foundation(waste, fnd[fnd_num - 1], stock)
                else:
                    raise RuntimeError('Error: wrong number of arguments')
            # tableau to foundation
            elif 'tf' in command:
                # same comments as before
                command_list = command.split()
                if len(command_list) == 3:
                    col_num = int(command_list[1])
                    fnd_num = int(command_list[2])
                    if not 1 <= col_num <= 7 or not 1 <= fnd_num <= 4:
                        raise RuntimeError('Error: arguments must be numbers in range')
                    tableau_to_foundation(tab[col_num - 1], fnd[fnd_num - 1])
                    # if tableaue column is not empty after moving, flip the last card
                    if tab[col_num - 1] and not tab[col_num - 1][-1].is_face_up():
                        tab[col_num - 1][-1].flip_card()
                else:
                    raise RuntimeError('Error: wrong number of arguments')
            # tableau to tableau
            elif 'tt' in command: 
                # same comments as before
                command_list = command.split()
                if len(command_list) == 4:
                    tab1_num = int(command_list[1])
                    tab2_num = int(command_list[2])
                    if not 1 <= tab1_num <= 7 or not 1 <= tab2_num <= 7:
                        raise RuntimeError('Error: arguments must be numbers in range')
                    # number of cards to be moved in the specified pile
                    num_of_cards = int(command_list[3])
                    tableau_to_tableau(tab[tab1_num - 1], tab[tab2_num - 1], num_of_cards )
                    # if tableaue column is not empty after moving, flip the last card
                    if tab[tab1_num - 1]:
                        # flip if it's not already flipped
                        if not tab[tab1_num - 1][-1].is_face_up():
                            tab[tab1_num - 1][-1].flip_card()
                else:
                    raise RuntimeError('Error: wrong number of arguments')
            # if empty string is entered
            elif command == '':
                raise RuntimeError('Error: no command entered')
            # if input is not in one of the valid formats
            else:
                command_status = False
                raise RuntimeError('{} is an invalid Command'.format(command))
            # if the game is over, display the banner, and break the loop
            if is_winner(fnd):
                display_game(fnd, tab, stock, waste) 
                print(YAY_BANNER)
                break
            # don't display function is error is detected somehwere
            if command != 'h' and command_status:
                display_game(fnd, tab, stock, waste)                
            command = input("prompt :> ")
            
        except RuntimeError as error_message:  # any RuntimeError you raise lands here
            print("{:s}\nTry again.".format(str(error_message))) 
            command = input("prompt :> ")
            # continue the loop again
            continue
        except ValueError:
            print("{:s}\nTry again.".format('Invalid Input'))
            command = input("prompt :> ")
            continue


main()

############################################################ 
# Survey questions:  
# Q1: 7
# Q2: 4
# Q3: 3
# Q4: 7