import random
from math import ceil, floor
import simpy #for simulating battle

#version 2.0 (8/24/2017)
#removed all but 4 If-Statements from class Item
#removed all If-Statements from class Player
#only remaining If-Statements are for simulation logic, random rolls or menus.

#Program written by Charlie Staich
# staichcs@mail.uc.edu
# in fulfillment of Katas excercise for Roto
# To use, simply run in a console. You will be prompted with an easy menu.

#Purpose: an RPG item generator and battle simulator
# Battle Process:
    #give each player random head, chest, feet armor and random weapon
    #begin battle
        #repeat below until a player's health < 0
            #player with higher Agility attacks first
                #check for attack hit
                #   - miss: pass
                #   - hit: check for counterattacks
                    #   - no counter: hit lands (damage stat and chance)
                    #   - counter: deflect up to 1/3 damage back
                #wait to swing again until after (atkspeed) seconds
            #player with lower agility attacks
                #same as above

class Item:
    #usage: newItem = Item()
    #usage for specific itemtype: newItem = Item(5)
    #itemtypes listed below [0,5]
    itemtypes = ["Head Armor", "Chest Armor", "Feet Armor", "Melee Weapon", "Ranged Weapon", "Magic Weapon"]
    nameDict = {}
    nameDict['Head Armor'] = ["Helm", "Headpiece", "Mask", "Helmet", "Hood", "Cowl"]
    nameDict['Chest Armor'] = ["Armor", "Chestplate", "Cuirass"]
    nameDict['Feet Armor'] = ["Greaves", "Boots", "Leggings", "Legs", "Shin Guards"]
    nameDict['Melee Weapon'] = ["Sword", "Scimitar", "Lance", "Greatsword", "Axe", "War Axe", "Dagger", "Mace", "Warhammer"]
    nameDict['Ranged Weapon'] = ["Sling", "Bow", "Longbow", "Handcannon"]
    nameDict['Magic Weapon'] = ["Flame Staff", "Water Staff", "Earth Staff", "Air Staff"]
    prefixes = {
        'Armor': ['Broken', 'Tattered', 'Rugged', 'Reinforced', 'Epic', 'Legendary'],
        'Weapon': ['Broken', 'Dull', 'Worn', 'Tempered', 'Brutal', 'Legendary'],
        'Staff': ['Broken', 'Battered', 'Cracked', 'Wicked', 'Brutal', 'Legendary']
    }
    allAttributes = [
    #Armor: dmgabsorb,
        [0.30], #Head
        [0.45], #Chest
        [0.25], #Feet
    #Weapons: atkspeed, atkdamage, atkchance
        [1.00, 1.00, 1.00], #Melee
        [0.70, 0.80, 0.80], #Ranged
        [1.55, 1.45, 1.20]  #Magic
    ]

    def __init__ (self, decltypeid=None):
        #initialize item variables
        if decltypeid is not None: #type parameter is included:
            self.typeid = decltypeid
        else:
            self.typeid = random.randint(0,5)
        #Roll level, set type text for displa
        self.level = random.randint(0,10)
        self.type = Item.itemtypes[self.typeid]

        #STATS
        self.stats = {
            'Strength': 0,
            'Agility': 0,
            'Health': 0
        }
        #Boost random stats
        for key in self.stats.keys():
            if random.uniform(0.0,1.0) <= self.level * 0.08:
                self.stats[key] = self.level/2.0 * random.uniform(1.0, 4.0)

        #ATTRIBUTES
        attributes = Item.allAttributes[self.typeid]
        if self.typeid <= 2: #Armor
            self.dmgabsorb = attributes[0] * self.level / 10.0 * random.uniform(0.5, 1.0)
            self.buyprice = (((self.dmgabsorb * 100) * self.level) + (self.level * sum(self.stats.values()))) * 100
        else:           #Weapons
            self.atkspeed = attributes[0] * random.uniform(1.5, 2.5)
            self.atkdamage = attributes[1] * random.randint(5,9) * self.level
            self.atkchance = 0.8 + attributes[2] * (self.level * 0.1)
            self.dps = (self.atkspeed * self.atkdamage) * self.atkchance
            self.buyprice = ((self.dps * self.level) + (self.level * sum(self.stats.values()))) * 100

        self.sellprice = self.buyprice * random.uniform(2.0,5.0) / 10.0
        self.name = Item.namegen(self)

    def namegen(self):
        #Generates a name for an item based on type and level

        #Refactored name
        root = random.choice(self.nameDict[self.itemtypes[self.typeid]])

        #Refactored Prefix
        prefixIdx = int(floor(self.level/2.0)) #scale of 0 to 5 how spicy
        #             head    chest   feet    Melee    Ranged   Staff
        keyList = ['Armor','Armor','Armor','Weapon','Weapon','Staff']
        thisKey = keyList[self.typeid]
        prefix = self.prefixes[thisKey][prefixIdx]

        #Suffix Refactored
        if sum(self.stats.values()) == 0:
            suffix = ""
        else:
            suffix = " of " + max(self.stats, key=self.stats.get)

        return(prefix + " " + root + suffix)

class Player:
    #generate player with random stats, armor, and weapon.

    def __init__(self, name):
        self.name = name
        self.helmet = Item(0)
        self.chest = Item(1)
        self.feet = Item(2)
        self.weapontype = random.randint(3,5)
        self.weapon = Item(self.weapontype)
        self.armorlevel = self.helmet.dmgabsorb + self.chest.dmgabsorb + self.feet.dmgabsorb
        self.dps = self.weapon.dps
        self.stats = {
            'Strength': random.uniform(10,20),
            'Agility': random.uniform(10,20),
            'Health': random.uniform(10,20)
        }
        for key in self.stats.keys():
            self.stats[key] += self.helmet.stats[key] + self.chest.stats[key] + self.feet.stats[key] + self.weapon.stats[key]
        self.health = self.stats['Health'] + 100
        #adjusted atkspeed with agility multiplier
        self.atkspeed = self.weapon.atkspeed * (1 + (self.stats['Agility']/100))
        #ajusted atkdamage with strength multiplier
        self.atkdamage = self.weapon.atkdamage  + self.stats['Strength']
        self.atkchance = self.weapon.atkchance
    def describe(self):
        print "Player: %s    Class: %s" % (self.name, self.weapon.type)
        print "    STR: %.1f    AGI: %.1f    HLT: %.1f" % (self.stats['Strength'], self.stats['Agility'], self.stats['Health'])
        print "    DMG: %.1f    RATE: %.2f " % (self.atkdamage, self.atkspeed)
        print "    ARMOR: %.1f   COUNTER: %.1f " % (self.armorlevel, self.stats['Agility']/100)
        print "Equipped (TOTAL LVL %d): " % (self.weapon.level + self.helmet.level + self.chest.level + self.feet.level)
        print "    %s: LVL %d" % (self.weapon.name, self.weapon.level)
        print "    %s: LVL %d" % (self.helmet.name, self.helmet.level)
        print "    %s: LVL %d" % (self.chest.name, self.chest.level)
        print "    %s: LVL %d" % (self.feet.name, self.feet.level)

def attack(env, thisplayer, opponent):
    #SimPy simulation for an attacking player

    #player with higher agility swings first
    if thisplayer.stats['Agility'] < opponent.stats['Agility']:
        yield env.timeout(thisplayer.atkspeed)

    while True:
        #check if both players are alive
        if opponent.health <= 0:
            winner = thisplayer.name
            loser = opponent.name
            print("[%.2f]: %s has slain %s! The battle is over." % (env.now, winner, loser))
            env.exit(value=thisplayer.name)
        elif thisplayer.health <= 0:
            winner = opponent.name
            loser = thisplayer.name
            env.exit(value=opponent.name)
        #swing attempt
        if random.random() <= thisplayer.atkchance:
            if random.random() <= opponent.stats['Agility']/200:
                #opponent counterattacks up to 1/3 damage
                armordeflect = random.uniform(thisplayer.armorlevel/2.0, thisplayer.armorlevel)
                counterdamage = thisplayer.atkdamage * armordeflect * random.uniform(0.0,0.33)
                print("[%.2f]: %s attacks, but %s counters with %s for %d damage" % (env.now, thisplayer.name, opponent.name, opponent.weapon.name, counterdamage))
                thisplayer.health = thisplayer.health - counterdamage
            else:
                #hit
                armordeflect = random.uniform(opponent.armorlevel/2.0, opponent.armorlevel)
                hitdamage = thisplayer.atkdamage * armordeflect
                print("[%.2f]: %s attacks %s with %s for %d damage" % (env.now, thisplayer.name, opponent.name, thisplayer.weapon.name, hitdamage))
                opponent.health = opponent.health - hitdamage
        else:
            #miss
            print("[%.2f]: %s misses %s" % (env.now, thisplayer.name, opponent.name))
        yield env.timeout(thisplayer.atkspeed)

def runbattle():
    print("= = = = =")
    player1 = Player("Cain")
    player2 = Player("Abel")
    player1.describe()
    print("= = = = =")
    player2.describe()
    env = simpy.rt.RealtimeEnvironment(initial_time=0, factor=1.0, strict=True)
    env.process(attack(env, player1, player2))
    env.process(attack(env, player2, player1))
    print("= = = = =")
    print("Running Simulation")
    print("[time]: event")
    env.run()
    print("Simulation Complete")
    print("= = = = =")

def main():
    menu = {}
    menu['1']="Generate random loot"
    menu['2']="Generate specific type of loot"
    menu['3']="Generate player with random loot"
    menu['4']="Simulate battle between random players"
    menu['5']="Exit"
    typemenu = {}
    typemenu['1']="Headpiece"
    typemenu['2']="Chestpiece"
    typemenu['3']="Footpiece"
    typemenu['4']="Melee Weapon"
    typemenu['5']="Ranged Weapon"
    typemenu['6']="Magic Weapon"
    while True:
        print("= = = = = = = = = =")
        options = menu.keys()
        options.sort()
        for entry in options:
            print entry, menu[entry]
        sel = raw_input("Enter # of sel: ")
        if sel == '1':
            newItem = Item()
            print("= = = = =")
            print newItem.name + " with attributes:"
            print(vars(newItem))
        elif sel == '2':
            typeoptions = typemenu.keys()
            typeoptions.sort()
            for entry in typeoptions:
                print "    ", entry, typemenu[entry]
            typesel = raw_input("    Enter # of sel: ")
            newItem = Item(int(typesel) - 1)
            print("= = = = =")
            print newItem.name + " with attributes:"
            print(vars(newItem))
        elif sel == '3':
            newName = raw_input(    "Enter name for player: ")
            newPlayer = Player(newName + " the Destroyer")
            print("= = = = =")
            newPlayer.describe()
        elif sel == '4':
            print("= = = = =")
            runbattle()
        elif sel == '5':
            break
        else:
            print "Unknown Selection, try again."

if __name__ == "__main__":
    main()
