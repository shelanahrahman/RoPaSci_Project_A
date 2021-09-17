"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

Created by : Shelanah Rahman [student id: 995900], and Ayda Zhao [student id: 1081566]

"""

###BONJOUR THIS FILE IS main.py

import sys
import json
import itertools
import copy

# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:
from search.util import print_board, print_slide, print_swing, InputDictConversion, MakeBigDict, updateBigBoardDict


def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file) ### this is our data to convert to dictionary
            
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # TODO:
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information).
    
    ### first turn the json file into a dictionary
    
#    for tokeninfo in data['upper']:
#      print(tokeninfo)
#    for tokeninfo in data['lower']:
#      print(tokeninfo)
#    for tokeninfo in data['block']:
#      print(tokeninfo)
    

    ### PREPROCESSING STAGE
  
  ## TURNING EVERY SECTION OF THE DICTIONARY, INTO ITs OWN MINI DICTIONARY
    UpperTokensInputDict = InputDictConversion(data, "upper")
   # print("printing uppertokens")
    #print(UpperTokensInputDict)
    
    LowerTokensInputDict = InputDictConversion(data, "lower")
   # print("printing lowertokems")
   # print(LowerTokensInputDict)
    
    BlockInputDict = InputDictConversion(data, "block")
    #print("printing blocks")
    #print(BlockInputDict)
    
    ### so now that we can confirm all the info has been read in and stuffed into dictionary, we put every key into
    ### the board state dictionary
    
   # BigBoardDict = {}
 
   # MakeBigDict(BigBoardDict, UpperTokensInputDict)
   # print("printing uppertokens")
   # print(BigBoardDict)
    
   # MakeBigDict(BigBoardDict, LowerTokensInputDict)
    #print("printing uppertokens and lower tokens")
    #print(BigBoardDict)
    
   # MakeBigDict(BigBoardDict, BlockInputDict)
   # print("printing uppertokens and lower tokens and blocks")
   # print(BigBoardDict)
    
    
   # print_board(BigBoardDict, "Initial board")
    
   
    playGame(UpperTokensInputDict, LowerTokensInputDict, BlockInputDict)

    
    return

    
      
def playGame(UpperInitial, LowerInitial, BlockInitial):
    ## put 3 initial dictionariesm, making up the board state,
    #into the play game function, and it should play the game until the end

    ### first form the first board state

    InitialBoard = updateBigBoardDict(UpperInitial, LowerInitial, BlockInitial)
    
    #print_board(InitialBoard, "Initial board in playgame function test")
    
    newLowerDict = LowerInitial
    
    
    #queue for storing all possible [paths,upperdict,lowerdict,blockdict]
    all_turnsequences_and_boards = []
    # int indicating the highest number of lowertoken beaten out all the paths generated
    highestEatenNum = 0
    
    while len(newLowerDict) != 0:
    
      ##if the queue is empty then the path is nothing, and the boardstate is initial
        if len(all_turnsequences_and_boards) == 0:
            dequeued_turnsequence = []
            dequeued_UpperDict = UpperInitial
            dequeued_LowerDict = LowerInitial
            dequeued_BlockDict = BlockInitial
            dequeued_eaten_Num = 0
        
            #print("starting queue from fresh")
        
        else:
        
            ## sort the queue based from how many tokens are eaten, based from
            ## https://stackoverflow.com/questions/17555218/python-how-to-sort-a-list-of-lists-by-the-fourth-element-in-each-list/
            ## 
            
            all_turnsequences_and_boards.sort(key=lambda x: x[4])
            ##take off the first element of the queue, and its boardstates
            ##/ dequeue an element and turn sequence + resulting board-state that lead to it to consider
            
            
            
            
            queue_element = all_turnsequences_and_boards.pop()
            
            dequeued_turnsequence = queue_element[0]
            dequeued_UpperDict = queue_element[1]
            dequeued_LowerDict = queue_element[2]
            dequeued_BlockDict = queue_element[3]
            ##eaten num is how many lower tokens have been eaten by now
            dequeued_eaten_Num = queue_element[4]
            
            
            #FOLLOWING PRINTS INFO
            #print("Popped queue element", queue_element)
            #print("What the board looks like from this point")
            #showBoardDict = updateBigBoardDict(dequeued_UpperDict, dequeued_LowerDict, dequeued_BlockDict)
            #print_board(showBoardDict, "What the board looks like from this dequeued")
            #print("HOW MANY TURNS THIS TIME", len(dequeued_turnsequence))

    
    ##by the end of this blocks of code
    # we are either starting fresh with a new path
    # or we are considering the board state for one of the previous
    # paths in the queue
    
      ### this is the part where we generate a possible movelist for every upper token
        moveslist_for_every_upper_token = []
        token_number = -1  
        for cell in dequeued_UpperDict:
        # cell is a token's coordinates
        
            for tokentype in dequeued_UpperDict[cell]:
                token_number = token_number + 1
        ##so right now, token is the type of token e.g. rock/paper/scissors
        
     
                # FILL MOVELIST WITH ALL THE POSSIBLE MOVES
                moveslist = []
                ## a move is formatted
                # [     (previous coordinate a, previous coordinate b),
                #  (potential coordinate a, potential coordinate b)
                # token type,
                #   is_swing boolen     ]

                ## these below contain moves
                slidesTemporary = []
                swingsTemporary = []

                ######### might have to adapt some functions since for this version, the boardstate
                ### is a combination of the three dictionaries

                ##gets possible slides for current token
                slidesTemporary = getSlides(cell, tokentype, dequeued_UpperDict, dequeued_LowerDict, dequeued_BlockDict)
                ## generates possible swings based on adjacent uppertokens
                swingsTemporary = getSwings(cell, tokentype, dequeued_UpperDict, dequeued_LowerDict, dequeued_BlockDict)

                ## Note, removing slides from swings list/ making slides and swings
                ### mutually exclusive, since a token cannot SWING to a spot it can already SLIDE to
                for a_swing in swingsTemporary:
                    for a_slide in slidesTemporary:
                        if a_swing[1] == a_slide[1]:
                            swingsTemporary.remove(a_swing)

                moveslist = slidesTemporary + swingsTemporary
                
                

				#REMOVE MOVES WHERE A SPECIFIC TOKEN MOVES BACK TO A PREVIOUS LOCATION IN THE LAST TURN
                for a_turn in dequeued_turnsequence:
                    for potential_move in moveslist: 
                        token_prev_move = a_turn[token_number]
                        #token_prev_move and potential_move are structured as the following
                        #[(previous/current_coordinate_a, current_coordinate_b), (new_coordinate_a, new_coordinate_b), tokentype, is_swing_bool
                    #if the turn history notes that the token has prevously occupied where the potential move is going
                        if token_prev_move[0] == potential_move[1] or token_prev_move[1] == potential_move[1]:
                            if token_prev_move[2]== potential_move[2]:
                                if potential_move in moveslist:
                                    moveslist.remove(potential_move)
                                    #print("removed!")

                ## individual token's potential moves now added to the movelist_for_all_upper_tokens
                moveslist_for_every_upper_token.append(moveslist)
            #end of loop
            
            
        ## So now you have a valid movelist for every upper token in movelist_for_every_upper_token
        ## With this list, find the possible combinations of different upper tokens moving in Combination Turns
        
        CombinationTurns = itertools.product(*moveslist_for_every_upper_token)
        CombinationTurnsList = []
        ##Convert to type list since you can only iterate over an itertools object once
        for turn in CombinationTurns:
            CombinationTurnsList.append(list(turn))
          
        
        
        ## LASTLY EXECUTE ALL MOVES FROM COMBINATIONTURNSLIST AND ADD THE NEW PATH TO THE QUEUE
        ##considering every combination of turns for all tokens
        for turn in CombinationTurnsList:
            
            #created new turnsequence
            new_generated_turnsequence = copy.deepcopy(dequeued_turnsequence)
            new_generated_turnsequence.append(turn)
          
          
            ThreeNewDictsandEaten = []
          #three new dicts is a list of three dictionaries that make up the new boarddstate
            ThreeNewDictsandEaten = addturn(turn, dequeued_UpperDict, dequeued_LowerDict, dequeued_BlockDict, dequeued_eaten_Num)
            
          # create new dictionaries
            newUpperDict = ThreeNewDictsandEaten[0]
            newLowerDict = ThreeNewDictsandEaten[1]
            newBlockDict = ThreeNewDictsandEaten[2]
            neweatenNum = ThreeNewDictsandEaten[3]
            
            # The following skips adding new path to the queue if an upper token kills an uppertoken
            if (check_token_kill(newUpperDict)):
                continue;
                
            #if the move reduced the number of lowertokens consumed compared to other paths,
            # don't add it to the queue and discard path
       #     if neweatenNum > highestEatenNum:
       #             highestEatenNum= neweatenNum
       #     elif neweatenNum < highestEatenNum:
       #         continue
                
                
                
            # prints the turn sequence if the program wins. Then, loop ends and playGame() returns
            if (len(newLowerDict) == 0):
                #showBoardDict = updateBigBoardDict(newUpperDict, newLowerDict, newBlockDict)
                #print_board(showBoardDict, "Final board")
                printTurnSequence(new_generated_turnsequence)
                return
            
            #if not, append the new turn sequence + boardstate to the queue_element
            else:
                toBeQueued = [new_generated_turnsequence , newUpperDict, newLowerDict, newBlockDict, neweatenNum]
                if neweatenNum == True:
                    all_turnsequences_and_boards =  [toBeQueued] + all_turnsequences_and_boards
                else:
                    all_turnsequences_and_boards.append(toBeQueued)   
        ##end of whileloop

    return

def check_token_kill(dequeued_UpperDict):
    #check if opposing types are on the same coordinate which will kills own uppertoken
    # returns 1 if it defeats own uppertoken and 0 if it doesn't
    for coordinate in dequeued_UpperDict:
        if len(coordinate)>1:
            first_tokenType= dequeued_UpperDict[coordinate][0]
            for tokenType in dequeued_UpperDict[coordinate]:
                if tokenType!= first_tokenType:
                    return 1
    return 0

def getSlides(cell, tokentype, dequeued_UpperDict, dequeued_LowerDict, dequeued_BlockDict, is_swing=0, og_coordinate=False):
    # returns a list of all possible slides
    # og_coordinate is only True when is_swing is True. It is the coordinate where the coordinate is swinging from. In the case,
    # of a swing, the cell argument is the adjacent token to the original token.
    move_lst=[]
    sorted_move_dict= {1: [], 0: []}
    r= cell[0]
    q= cell[1]
    token_type= tokentype### get token_type
    r_lst= [r+1, r+1, r, r, r-1, r-1]
    q_lst= [q-1, q, q-1, q+1, q, q+1]
    r_directions= copy.deepcopy(r_lst)
    q_directions= copy.deepcopy(q_lst)
    #when it's not a slide as part of getSwings(), the original coordinate is the same as the cell coordinate
    if og_coordinate:
        for i in range(len(r_lst)):
            if (r_lst[i],q_lst[i]) == og_coordinate:
                r_directions.remove(r_lst[i])
                q_directions.remove(q_lst[i])
                break
                
    else:
        og_coordinate = cell
    for i,j in zip(r_directions, q_directions):
        unsorted_move_dict= validMove(sorted_move_dict, dequeued_UpperDict, dequeued_LowerDict, dequeued_BlockDict, token_type, og_coordinate,(i,j), is_swing)
        
    #convert unsorted_move_dict to a sorted move list
    for key in sorted_move_dict:
        for i in sorted_move_dict[key]:
            move_lst.append(i)
    return move_lst
  

def getSwings(cell, tokentype, dequeued_UpperDict, dequeued_LowerDict, dequeued_BlockDict):
  #addSwings returns a list of possible swing moves
  move_lst= []
  ##gets a list of adjacent tokens of the same team and find the slide moves possible from the adjacent tokens
  adjToklst= findAdjacentTok(dequeued_UpperDict, cell) 
  for adjTok in adjToklst:
    temp_move_lst= getSlides(adjTok, tokentype, dequeued_UpperDict, dequeued_LowerDict, dequeued_BlockDict, 1, cell)
    move_lst= move_lst + temp_move_lst
  return move_lst
  
  
  
  
def findAdjacentTok(dequeued_UpperDict, cell):
  #This function returns a list of coordinates for adjacent tokens  
  AdjacentToklst = []
  r= cell[0]
  q= cell[1]
  r_directions= [r+1, r+1, r, r, r-1, r-1]
  q_directions= [q-1, q, q-1, q+1, q, q+1]
  for i,j in zip(r_directions, q_directions):
    if dequeued_UpperDict.get((i, j)):
      AdjacentToklst.append((i,j))
  return AdjacentToklst
  
def coordinatesInBoundary(coordinatetuple):
  ##given coordinates, if it's in the boundaries of board
  ## return true, otherwise, return false
  #if row/x is larger than 0
  if coordinatetuple[0] in range(5):
    #y should be more than -4, and be less than 4-x
    if coordinatetuple[1] >= -4 and coordinatetuple[1] <= (4-coordinatetuple[0]):
      return True
  #if row/x is less than 0
  elif coordinatetuple[0] in range(-4,0):
    #y should be less than 4, and be less than -4-x
    if coordinatetuple[1] <= 4 and coordinatetuple[1] >= (-4-coordinatetuple[0]):
      return True
  else:
    return False
  

def validMove(unsorted_move_dict, dequeued_UpperDict, dequeued_LowerDict, dequeued_BlockDict, tok_type, coordinate_a, coordinate_b, is_swing):
    # This function adds a direction token to the move_lst
    upper_tok= dequeued_UpperDict.get(coordinate_b)
    lower_tok= dequeued_LowerDict.get(coordinate_b)
    #ensures the lower_tok is of type list
    if lower_tok!= None:
        if type(lower_tok)!= list:
            lower_tok= list(lower_tok) 
    #when faced with token of the opposing team, ties and winning are the only valid move
        for lower_tok_type in lower_tok:
            fight_res= rps_fight(tok_type, lower_tok_type)
            if fight_res!=-1:
                movenode= [coordinate_a, coordinate_b, tok_type, is_swing]
                unsorted_move_dict[fight_res].append(movenode)
# if it is within or the boundaries and there is no other token or blocks, add to directions
    if  dequeued_BlockDict.get(coordinate_b)==None and lower_tok==None and  coordinatesInBoundary(coordinate_b):
        movenode= [coordinate_a, coordinate_b, tok_type, is_swing]
        unsorted_move_dict[0].append(movenode)
    return unsorted_move_dict

    

 
def rps_fight(firsttokentype, secondtokentype):
  ## given two types, determine who is winner based on who is first.
   ### returns: 1= 1st token beat 2nd token, 0= tie, -1= 1st token lost to 2nd token
  if firsttokentype == secondtokentype:
    return 0
  elif firsttokentype == "r" and secondtokentype == "p":
    return -1
  elif firsttokentype == "r" and secondtokentype == "s":
    return 1
  elif firsttokentype == "s" and secondtokentype == "r":
    return -1
  elif firsttokentype == "s" and secondtokentype == "p":
    return 1
  elif firsttokentype == "p" and secondtokentype == "s":
    return -1
  elif firsttokentype == "p" and secondtokentype == "r":
    return 1
  
#turn sequence is a list. of lists, of lists
# printing these suckers out
def printTurnSequence(turnsequence):
  for turncount in range(0,len(turnsequence)):
    for move in turnsequence[turncount]:
      # move is formatted 
      #[(previous/current_coordinate_a, current_coordinate_b), (new_coordinate_a, new_coordinate_b), token_type, is_swing_bool]
      
      # move[3] corresponds to swing bool
      #if it's a swing, print the swing
      if move[3] == True:
        
        current_coordinate_a = move[0][0]
        current_coordinate_b = move[0][1]
        
        new_coordinate_a = move[1][0]
        new_coordinate_b = move[1][1]
        
        print_swing(turncount+1, current_coordinate_a, current_coordinate_b, 
                    new_coordinate_a, new_coordinate_b)
      else:
        ## print a slide
        current_coordinate_a = move[0][0]
        current_coordinate_b = move[0][1]
        
        new_coordinate_a = move[1][0]
        new_coordinate_b = move[1][1]
        
        print_slide(turncount+1, current_coordinate_a, current_coordinate_b, 
                    new_coordinate_a, new_coordinate_b)
        
  return
  
  
def addturn(turn, UpperDict, LowerDict, BlockDict, eatenNum):

  ## turn example formatting for reference. The below example is for three tokens.
  # a turn is a set of moves
  
 # [

#	[(previous/current_coordinate_a, current_coordinate_b), (new_coordinate_a, new_coordinate_b), tokentype, is_swing_bool], 

#	[(previous/current_coordinate_a, current_coordinate_b), (new_coordinate_a, new_coordinate_b), tokentype, is_swing_bool], 

#	[(previous/current_coordinate_a, current_coordinate_b), (new_coordinate_a, new_coordinate_b), tokentype, is_swing_bool]

# ]
	### changes upperdict, lowerdict, and blockdict, based on what happens in the turn
  
  ## note, by this stage, every move listed in a turn, should be valid,
  # so no validity checks are done.
  
    
  changedUpperDict = copy.deepcopy(UpperDict)
  changedLowerDict = copy.deepcopy(LowerDict)
  changedBlockDict = BlockDict
  changedEatenNum = eatenNum
  
  
  for token_move in turn:
    currentcoordinate = token_move[0]
    newcoordinate = token_move[1]
    tokenType = token_move[2]
    
    #slide off token=type from its current cell's list
    #token_move[0] is coordinate for current cell
    changedUpperDict[currentcoordinate].remove(tokenType)
    
    
    #if entry is empty, remove from dictionary
    if changedUpperDict[currentcoordinate] == []:
      del changedUpperDict[currentcoordinate]
      
    #slide token=type onto new cell's list. token_move_1 corresponds to the new coordinate
    #if entry exsists, append onto it
    if newcoordinate in changedUpperDict:
      changedUpperDict[newcoordinate].append(tokenType)
    else:
      changedUpperDict[newcoordinate] = [tokenType]
    
    ## check to see if any tokens from upper are sitting on the same spot 
    # with a lower token
    # and if any lower tokens need to be removed
    if newcoordinate in changedLowerDict:
      # fight between uppertoken's type, and lowerdict's 
      fightresult = rps_fight(tokenType, changedLowerDict[newcoordinate][0])
      #if upper token wins
      if fightresult == 1:
        # remove a piece from lowerdict
        changedLowerDict[newcoordinate].pop()
       # print("UPPER HAS EATEN LOWER")
        changedEatenNum = changedEatenNum + 1
        #if the hex for the lower dict is empty,
        if changedLowerDict[newcoordinate] == []:
            del changedLowerDict[newcoordinate]
        

  threeDictListandEaten = [changedUpperDict, changedLowerDict, changedBlockDict, changedEatenNum]
  
  return threeDictListandEaten 
    
    ### 
    
 