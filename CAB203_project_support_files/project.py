import csv
import collections 
import digraphs 
import graphs

def gamesOK(games):
    V = {p for game in games for p in game}
    E = {game for game in games}

    # Make the graph undirected for the connectivity check
    undirectedE = E | {(v, u) for u, v in E}

    # Check if the graph is connected
    if not graphs.connected(V, undirectedE):
        return False

    for A in V:
        for B in V:
            if A != B:
                if (A, B) not in E and (B, A) not in E:
                    # Check if there exists a player C such that A plays against C and C plays against B
                    if not any((C != A and C != B and ((A, C) in E or (C, A) in E) and ((C, B) in E or (B, C) in E)) for C in V):
                        return False

    return True

def potentialReferees(refereecsvfilename, player1, player2):
   
    referees = set()
    with open(refereecsvfilename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            referee = row[0]
            conflicts = row[1:]

            # Add referee to the set only if they don't conflict with the players
            # and they are not one of the players
            if player1 not in conflicts and player2 not in conflicts and referee not in [player1, player2]:
                referees.add(referee)
    
    return referees

def gameReferees(gamePotentialReferees):
   
   # Create a list of games
   assignedReferees = {}

    # Sort the games by the number of potential referees in ascending order
   sortedGames = sorted(gamePotentialReferees.keys(), key=lambda game: len(gamePotentialReferees[game]))

   for game in sortedGames:
        potentialReferees = gamePotentialReferees[game]
        # Check if any potential referee is available to referee the game
        availableReferees = potentialReferees - set(assignedReferees.values())
        if len(availableReferees) > 0:
            assignedReferee = availableReferees.pop()
            assignedReferees[game] = assignedReferee
        else:
            # No available referees, assignment not possible
            return None

   return assignedReferees



def gameSchedule(assignedReferees=None):
    schedule = [] 
    if assignedReferees is None:
        assignedReferees = {}
            
    # Iterate over the assignedReferees dictionary and schedule the games
    for game, referee in assignedReferees.items():
        # Find an available timeslot to schedule the game
        scheduled = False
        for timeslot in schedule:
            # Check if the game conflicts with any game in the timeslot
            conflicting = False
            for scheduled_game in timeslot:
                # Check if any player or the referee is already involved in another game in the timeslot
                if game[0] in scheduled_game or game[1] in scheduled_game or referee in scheduled_game:
                    conflicting = True
                    break
            if not conflicting:
                # Add the game to the timeslot
                timeslot.add((*game, referee))
                scheduled = True
                break
        if not scheduled:
            # Create a new timeslot and schedule the game
            schedule.append({(*game, referee)})

    # Print the schedule for debugging
    for i, timeslot in enumerate(schedule):
        print(f"Timeslot {i + 1}:")
        for game in timeslot:
            print(game)
        print()

    return schedule

def ranking(games):
    players = set()
    edges = set()

    # Create the set of players and the set of edges based on the games
    for winner, loser in games:
        players.add(winner)
        players.add(loser)
        edges.add((winner, loser))

    # Find a topological ordering of the players
    ordering = digraphs.topOrdering(players, edges)

    # Check if a valid ranking is possible
    if ordering is None:
        return None  # No valid ranking is possible

    # Return the topological ordering as the ranking
    return ordering