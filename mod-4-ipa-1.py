'''Module 4: Individual Programming Assignment 1
Parsing Data
This assignment covers your ability to manipulate data in Python.
'''

def relationship_status(from_member, to_member, social_graph):
    '''Relationship Status.
    20 points.
    Let us pretend that you are building a new app.
    Your app supports social media functionality, which means that users can have
    relationships with other users.
    There are two guidelines for describing relationships on this social media app:
    1. Any user can follow any other user.
    2. If two users follow each other, they are considered friends.
    This function describes the relationship that two users have with each other.
    Please see "assignment-4-sample-data.py" for sample data. The social graph
    will adhere to the same pattern.
    Parameters
    ----------
    from_member: str
        the subject member
    to_member: str
        the object member
    social_graph: dict
        the relationship data    
    Returns
    -------
    str
        "follower" if fromMember follows toMember,
        "followed by" if fromMember is followed by toMember,
        "friends" if fromMember and toMember follow each other,
        "no relationship" if neither fromMember nor toMember follow each other.
    '''
    # Replace `pass` with your code. 
    # Stay within the function. Only use the parameters as input. The function should return your answer.

    from_member_ff = (social_graph[from_member]["following"])
    to_member_ff = (social_graph[to_member]["following"])
    
    if to_member in from_member_ff and from_member in to_member_ff:
        return("friends")
    elif to_member in from_member_ff:
        return("follower")
    elif from_member in to_member_ff:
        return("followed")
    else:
        return("no relationship")


def tic_tac_toe(board):
    '''Tic Tac Toe. 
    25 points.
    Tic Tac Toe is a common paper-and-pencil game. 
    Players must attempt to successfully draw a straight line of their symbol across a grid.
    The player that does this first is considered the winner.
    This function evaluates a tic tac toe board and returns the winner.
    Please see "assignment-4-sample-data.py" for sample data. The board will adhere
    to the same pattern. The board may by 3x3, 4x4, 5x5, or 6x6. The board will never
    have more than one winner. The board will only ever have 2 unique symbols at the same time.
    Parameters
    ----------
    board: list
        the representation of the tic-tac-toe board as a square list of lists
    Returns
    -------
    str
        the symbol of the winner or "NO WINNER" if there is no winner
    '''
    # Replace `pass` with your code. 
    # Stay within the function. Only use the parameters as input. The function should return your answer.

    horizontal = [x for x in board]
    vertical = [x for x in zip(*board)]
    d_down_up = [board[i][i] for i,v in enumerate(board)]
    d_up_down = [board[len(board)-1-i][i] for i,v in enumerate(board)]
    
    for i,a in enumerate(horizontal):
        if all([move=="X" for move in a]):
            return("X")
        elif all([move=="O" for move in a]):
            return("O")
        else:
            continue
    
    for j,b in enumerate(vertical):
        if all([move=="X" for move in b]):
            return("X")
        elif all([move=="O" for move in b]):
            return("O")
        else:
            continue
            
    if all([move=='X' for move in d_down_up]) or all([move=='X' for move in d_up_down]):
        return("X")
    elif all([move=='O' for move in d_down_up]) or all([move=='O' for move in d_up_down]):
        return("O")
    else:
        return("NO WINNER")

def eta(first_stop, second_stop, route_map):
    '''ETA. 
    25 points.
    A shuttle van service is tasked to travel along a predefined circlar route.
    This route is divided into several legs between stops.
    The route is one-way only, and it is fully connected to itself.
    This function returns how long it will take the shuttle to arrive at a stop
    after leaving another stop.
    Please see "mod-4-ipa-1-sample-data.py" for sample data. The route map will
    adhere to the same pattern. The route map may contain more legs and more stops,
    but it will always be one-way and fully enclosed.
    Parameters
    ----------
    first_stop: str
        the stop that the shuttle will leave
    second_stop: str
        the stop that the shuttle will arrive at
    route_map: dict
        the data describing the routes
    Returns
    -------
    int
        the time it will take the shuttle to travel from first_stop to second_stop
    '''
    # Replace `pass` with your code. 
    # Stay within the function. Only use the parameters as input. The function should return your answer.

    routes = legs.keys()
    
    a = [i for i,j in enumerate(routes)]
    b = [j for i,j in enumerate(routes)]
    c = [j for j,k in b]
    d = [k for j,k in b]
    
    time = 0
    
    for x in c:
        m = c.index(x)
        if x == first_stop:
            while(True):
                if d[m] != second_stop:
                    first_stop_time = int(legs[c[m],d[m]]['travel_time_mins'])
                    time += first_stop_time 
                    if m == len(c) - 1:
                        m = 0
                    elif m < len(c):
                        m += 1
                    continue
                elif d[m] == second_stop:
                    second_stop_time = int(legs[c[m],d[m]]['travel_time_mins'])
                    return time + second_stop_time