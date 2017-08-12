from __future__ import division #for correct integer division
import pickle #for saving, loading files
import subprocess as sp #for screen clearing
import pprint #Pretty Printing
import msvcrt as m #for wait() function
import time
from functools import partial #for dictionary functions w/ specific parameters

#This program is for recording games over time, using the Elo rating system developed for chess tournaments to rank players.
#It is able to generate likelihood of winning, it keeps records of all operations in the menus, it allows individual scores
#management in case a score needs fixing or handicap, and it is able to reset, add, or remove players at any time.
#Code written by Charlie Staich

#DONE
    #track ratings
    #calculate new ratings
    #record games
    #player manager
    #ability to check scores
    #ability to view past games
    #better menus
#TO-DO
    #confirmation prompt for high-risk menu options
    #ability to edit most recent game
    #ratings-over-time display

#MENU FUNCTIONS
def main_menu():
    clearscreen()
    entry = menu(['Record a Game', 'Roster', 'Records', 'Tools'], 'main')
    choices = {
        0: partial(return_to,'main'),
        1: play_game,
        2: roster_menu,
        3: records_menu,
        4: tools_menu,
    }
    choices[entry]()
    return_to('main')
    return
def roster_menu():
    display_roster()
    entry = menu(['Add a player', 'Remove a player', 'Modify a rating', 'Reset all ratings', 'Delete Roster'], 'roster')
    choices = {
        0: partial(return_to,'main'),
        1: add_player,
        2: delete_player,
        3: modify_rating,
        4: reset_ratings,
        5: delete_roster,
    }
    choices[entry]()
    return_to('roster')
    return
def records_menu():
    entry = menu(['Display Records', 'Delete All'], 'records')
    choices = {
        0: partial(return_to,'main'),
        1: display_records,
        2: delete_records,
    }
    choices[entry]()
    return_to('records')
    return
def tools_menu():
    entry = menu(['Calculate Odds', 'Track Ratings'], 'tools')
    choices = {
        0: partial(return_to,'main'),
        1: calculate_odds,
        #2: track_ratings, #not added
    }
    choices[entry]()
    return_to('tools')
    return
def menu(options, return_menu = 'main'):
    opt_dict = {0: 'Return'}
    count = 1
    for item in options:
        opt_dict[count] = item
        count = count + 1
    key_list = opt_dict.keys()
    key_list.sort()
    for item in key_list:
        print "{}: {}".format(item, opt_dict[item])
    entry = prompt_number("Enter Selection: ", key_list)
    clearscreen()
    return entry
def return_to(return_menu, type = 0):
    if type == 1: #incorrect input
        print "Invalid Entry, returning to {} menu".format(return_menu)
        wait()
    clearscreen()
    menu_list[return_menu]()
    return
def play_game():
    roster = load_obj('roster')
    #Initialize player dictionaries
    p1 = {}
    p2 = {}

    display_roster()

    p1['name'] = prompt_name('Name of Player 1: ', 2)
    p2['name'] = prompt_name('Name of Player 2: ', 2)

    p1['rating'] = roster[p1['name']]
    p2['rating'] = roster[p2['name']]

    #Calculate adjusted logarithmic ratings
    p1['log'] = 10 ** (p1['rating']/ 400.00)
    p2['log'] = 10 ** (p2['rating'] / 400.00)

    #Calculate relative EVs
    p1['EV'] = p1['log'] / (p1['log'] + p2['log'])
    p2['EV'] = p2['log'] / (p1['log'] + p2['log'])

    #Display ratings and relative EVs
    print "{}: {:.2f} ({:.2f}% to win)".format(p1['name'], p1['rating'], p1['EV']*100)
    print "{}: {:.2f} ({:.2f}% to win)".format(p2['name'], p2['rating'], p2['EV']*100)

    p1['score'] = prompt_number("Enter {}'s score: ".format(p1['name']))
    p2['score'] = prompt_number("Enter {}'s score: ".format(p2['name']))

    #Outcome logic (used to generate new rankings)
    if p1['score'] > p2['score']:
        p1['outcome'] = 1
        p2['outcome'] = 0
    elif p1['score'] < p2['score']:
        p1['outcome'] = 0
        p2['outcome'] = 1
    elif p1['score'] == p2['score']:
        p1['outcome'] = 0.5
        p2['outcome'] = 0.5

    #Calculate new ratings
    multiplier = 32
    p1['new_rating'] = p1['rating'] + multiplier * (p1['outcome'] - p1['EV'])
    p2['new_rating'] = p2['rating'] + multiplier * (p2['outcome'] - p2['EV'])
    p1['difference'] = p1['new_rating'] - p1['rating']
    p2['difference'] = p2['new_rating'] - p2['rating']

    #Display new ratings
    print "{}: {:.2f} ---> {:.2f}  [{:.2f}]".format(p1['name'], p1['rating'], p1['new_rating'], p1['difference'])
    print "{}: {:.2f} ---> {:.2f}  [{:.2f}]".format(p2['name'], p2['rating'], p2['new_rating'], p2['difference'])

    #Record new ratings on the roster
    roster[p1['name']] = p1['new_rating']
    roster[p2['name']] = p2['new_rating']
    save_obj(roster, 'roster')

    #Record game for records
    metadata = {}
    metadata['time'] = time.time()
    records.append({
        'type': 'game',
        'metadata': metadata,
        'p1': p1,
        'p2': p2,
        })
    save_obj(records, 'records')
    wait()
    return_to('main')
    return
#ROSTER MENU FUNCTIONS
def display_roster():
    roster = load_obj('roster')
    print "=== Current Roster ==="
    pp.pprint(roster)
    print "\n"
    return
def add_player():
    roster = load_obj('roster')
    player = raw_input("Enter player: ").lower()
    if player in roster.keys():
        print "{} is already on the roster.".format(player)
        wait()
        return_to('roster')
    roster[player] = 400
    save_obj(roster, 'roster')
    metadata = {}
    metadata['time'] = time.time()
    metadata['description'] = "Added {} to roster with score of {}".format(player, roster[player])
    records.append({
        'type': 'records',
        'metadata': metadata
        })
    save_obj(records, 'records')
    return
def delete_player():
    roster = load_obj('roster')
    player = prompt_name()
    old_rating = roster[player]
    roster.pop(player, None)
    save_obj(roster, 'roster')
    metadata = {}
    metadata['time'] = time.time()
    metadata['description'] = "Deleted {} from roster with score of {}".format(player, old_rating)
    records.append({
        'type': 'records',
        'metadata': metadata
        })
    save_obj(records, 'records')
    return
def modify_rating():
    roster = load_obj('roster')
    player = prompt_name()
    old_rating = roster[player]
    new_rating = prompt_number("Enter new rating: ")
    roster[player] = new_rating
    save_obj(roster, 'roster')
    metadata = {}
    metadata['time'] = time.time()
    metadata['description'] = "Changed {}'s rating from {} to {}".format(player, old_rating, new_rating)
    records.append({
        'type': 'records',
        'metadata': metadata
        })
    save_obj(records, 'records')
    return
def reset_ratings():
    roster = load_obj('roster')
    for player in roster:
        roster[player] = 400
    save_obj(roster, 'roster')
    return
def delete_roster():
    roster = {}
    save_obj(roster, 'roster')
    roster = load_obj('roster')
    return
#RECORDS MENU FUNCTIONS
def display_records(max_records = -1):
    clearscreen()
    records = load_obj('records')
    count = 1
    for entry in records:
        metadata = entry['metadata']
        if count == max_records:
            break
        if entry['type'] == 'game':
            p1 = entry['p1']
            p2 = entry['p2']
            data = []
            data.append([" ", p1['name'], p2['name']])
            data.append(["Score", p1['score'], p2['score']])
            data.append(['EV', p1['EV'], p2['EV']])
            data.append(['Rating Change', p1['difference'], p2['difference']])
            data.append(['New Rating', p1['new_rating'], p2['new_rating']])
            #printing
            print "\n=== Game at {} ===\n".format(metadata['time'])
            col_width = max(len(str(item)) for line in data for item in line) + 2
            for line in data:
                print "\t" + "".join(str(item).ljust(col_width) for item in line)
        else:
            print "\n=== {} change at {} ===\n".format(entry['type'], metadata['time'])
            print "\t" + metadata['description']
        count = count + 1
        print "\n"
    wait()
    return
def delete_records():
    metadata = {}
    metadata['time'] = time.time()
    metadata['description'] = "Wiped All Records".format()
    records = [{
        'type': 'records',
        'metadata': metadata
        }]
    save_obj(records, 'records')
#TOOLS MENU FUNCTIONS
def calculate_odds():
    #Initialize player dictionaries
    p1 = {}
    p2 = {}

    #Poll user for participants
    p1['name'] = raw_input('Name of Player 1: ').lower()
    p2['name'] = raw_input('Name of Player 2: ').lower()

    #Get records for participants
    roster = load_obj('roster')
    p1['rating'] = roster[p1['name']]
    p2['rating'] = roster[p2['name']]

    #Calculate adjusted logarithmic ratings
    p1['log'] = 10 ** (p1['rating']/ 400.00)
    p2['log'] = 10 ** (p2['rating'] / 400.00)

    #Calculate relative EVs
    p1['EV'] = p1['log'] / (p1['log'] + p2['log'])
    p2['EV'] = p2['log'] / (p1['log'] + p2['log'])

    #Display ratings and relative EVs
    print "{}: {:.2f} ({:.2f}% to win)".format(p1['name'], p1['rating'], p1['EV']*100)
    print "{}: {:.2f} ({:.2f}% to win)".format(p2['name'], p2['rating'], p2['EV']*100)

    wait()
    return


#COMMON FUNCTIONS
def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
def wait(): #waits for keystrike before continuing
    m.getch()
    return
def prompt_name(message = "Enter player: ", min_length = 1):
    roster = load_obj('roster')
    if len(roster) < min_length:
        print "The roster is not long enough!"
        wait()
        return_to('main')2
    player = raw_input(message).lower()
    try:
        roster[player]
    except:
        print "That name is not on the roster. "
        return prompt_name(message, min_length)
    return player
def prompt_number(message = "Enter number: ", values = -1):
    number = raw_input(message)
    try:
        number = int(number)
    except ValueError:
        print "Invalid entry."
        return prompt_number(message, values)
    if values != -1:
        for value in values:
            value = int(value)
        if number not in values:
            print "Out of range."
            return prompt_number(message, values)
    return number

def clearscreen():
    sp.call('cls',shell=True) #clears the screen
    return

#COMMON VARIABLES
roster = load_obj('roster')
records = load_obj('records')
pp = pprint.PrettyPrinter()
menu_list = {
    'main': main_menu,
    'roster': roster_menu,
    'records': records_menu,
    'tools': tools_menu,
    }
#BODY
main_menu()
