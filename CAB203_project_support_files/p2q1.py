def gamesOK(games):
    #Assumed1: no player plays against themselves
    #Assumed2: every player plays in at least one game
    for A,B in games:
        # A and B can't be the same person
        if A == B:
            return false
        #primary game is the planned A vs B match, secondary game is the other C vs A and C vs B 
        Primarygame = (A,B) in games
        secondarygame = any((A, C) in games and (C,B) in games for C in games)
        if not primarygame and not secondarygame:
            return false
    return true