import random
from math import ceil
import simpy #for simulating battle

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
    def __init__ (self, decltypeid=None):
        #initialize item variables
        if decltypeid is not None: #option to specify armor type
            self.typeid = decltypeid
        else:
            self.typeid = random.randint(0,5)
        self.level = random.randint(0,10)
        self.type = Item.itemtypes[self.typeid]
        self.itemclass = int(ceil((self.typeid+1)/3.0)) #1 = armor, 2 = weapon
        #Weapons: all
        if self.itemclass == 2:
            self.atkspeed = random.uniform(1.5, 2.5)
            self.atkchance = 0.9 + (self.level * 0.05)
            self.atkdamage = random.randint(5,9) * self.level
            self.dps = (self.atkspeed * self.atkdamage) * self.atkchance
        #Weapon modifiers: Ranged
        if self.typeid == 4:
            self.atkspeed = self.atkspeed * 0.75
            self.atkdamage = self.atkdamage * 0.5
            self.atkchance = self.atkchance * 0.75
        #Weapon modifiers: Magic
        if self.typeid == 5:
            self.atkspeed = self.atkspeed * 1.5
            self.atkdamage = self.atkdamage * 2.0
            self.atkchance = self.atkchance * 0.9
        #Armor: percent dmg reduction (30%/45%/25% head/chest/feet)
        elif self.typeid == 0: #head armor
            self.dmgabsorb = 0.30 * self.level / 10.0 * random.uniform(0.8,1.0)
        elif self.typeid == 1: #chest armor
            self.dmgabsorb = 0.45 * self.level / 10.0 * random.uniform(0.8,1.0)
        elif self.typeid ==2: #foot armor
            self.dmgabsorb = 0.25 * self.level / 10.0 * random.uniform(0.8,1.0)

        #stat boosts
        self.stats = [0,0,0] #Strength, Agility, Health
        self.allstats = 0
        for i in range(2):
            statchance = self.level * 0.08
            if random.uniform(0.0,1.0) <= statchance:
                statboost = self.level/2 * random.uniform(1.0, 4.0)
                self.stats[i] = self.stats[i] + statboost
                self.allstats = self.allstats + statboost
        #store
        if self.itemclass == 1: #armor pricing (no dps)
            self.buyprice = (((self.dmgabsorb * 100) * self.level) + (self.level * self.allstats)) * 100
        elif self.itemclass == 2: #weapon pricing
            self.buyprice = ((self.dps * self.level) + (self.level * self.allstats)) * 100
        self.sellprice = self.buyprice * random.uniform(2.0,5.0) / 10.0
        self.name = self.namegen()
    def namegen(self):
        #Generates a name for an item based on type and level
        if self.typeid == 0: #Helm
            root = random.choice(["Helm", "Headpiece", "Mask", "Helmet", "Hood", "Cowl"])
        elif self.typeid == 1: #Chest
            root = random.choice(["Armor", "Chestplate", "Cuirass"])
        elif self.typeid == 2: #Feet
            root = random.choice(["Greaves", "Boots", "Leggings", "Legs", "Shin Guards"])
        elif self.typeid == 3: #Melee Weapon
            root = random.choice(["Sword", "Scimitar", "Lance", "Greatsword", "Axe", "War Axe", "Dagger", "Mace", "Warhammer"])
        elif self.typeid == 4: #Ranged Weapon
            root = random.choice(["Sling", "Bow", "Longbow", "Handcannon"])
        elif self.typeid == 5: #Magic Weapon
            root = random.choice(["Flame Staff", "Water Staff", "Earth Staff", "Air Staff"])

        #Prefix
        if self.level == 10:
            prefix = "Legendary"
        elif self.level > 8:
            if self.itemclass == 1: #Armor
                prefix = "Epic"
            else:                   #Weapon
                prefix = "Brutal"
        elif self.level > 6:
            if self.itemclass == 1:
                prefix = "Reinforced"
            elif self.typeid == 5:
                prefix = "Wicked" #staff
            else:
                prefix = "Tempered" #other weapons
        elif self.level > 4:
            if self.itemclass == 1:
                prefix = "Rugged"
            elif self.typeid == 5: #staff
                prefix = "Twisted"
            else:
                prefix = "Worn"
        elif self.level > 2:
            if self.itemclass == 1:
                prefix = "Tattered"
            elif self.typeid == 5:
                prefix = "Battered"
            else:
                prefix = "Dull"
        else:
            prefix = "Broken"

        #Suffix
        if self.allstats == 0:
            suffix = ""
        elif (self.stats[0] >= self.stats[1]) and (self.stats[0] >= self.stats[2]):
            #Strength Dominant
            suffix = " of Strength"
        elif self.stats[1] >= self.stats[2]:
            #Agility Dominant
            suffix = " of Agility"
        else:
            #Health Dominant
            suffix = " of Health"


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
        self.basestats = [random.randint(10,20),random.randint(10,20),random.randint(0,25)]
        self.statups = [sum(x) for x in zip(self.helmet.stats, self.chest.stats, self.feet.stats, self.weapon.stats)]
        self.stats = [sum(x) for x in zip(self.basestats, self.statups)]
        self.health = self.stats[2] + 100
        #adjusted atkspeed with agility multiplier
        self.atkspeed = self.weapon.atkspeed * (1 + (self.stats[1]/100))
        #ajusted atkdamage with strength multiplier
        self.atkdamage = self.weapon.atkdamage  + self.stats[0]
        self.atkchance = self.weapon.atkchance
    def describe(self):
        print "Player: %s    Class: %s" % (self.name, self.weapon.type)
        print "    STR: %.1f    AGI: %.1f    HLT: %.1f" % (self.stats[0], self.stats[1], self.stats[2])
        print "    DMG: %.1f    RATE: %.2f " % (self.atkdamage, self.atkspeed)
        print "    ARMOR: %.1f   COUNTER: %.1f " % (self.armorlevel, self.stats[1]/100)
        print "Equipped (TOTAL LVL %d): " % (self.weapon.level + self.helmet.level + self.chest.level + self.feet.level)
        print "    %s: LVL %d" % (self.weapon.name, self.weapon.level)
        print "    %s: LVL %d" % (self.helmet.name, self.helmet.level)
        print "    %s: LVL %d" % (self.chest.name, self.chest.level)
        print "    %s: LVL %d" % (self.feet.name, self.feet.level)

def attack(env, thisplayer, opponent):
    #SimPy simulation for an attacking player

    #player with lower agility swings first
    if thisplayer.stats[1] < opponent.stats[1]:
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
            if random.random() <= opponent.stats[1]/200:
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
            newPlayer = Player(newName)
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
