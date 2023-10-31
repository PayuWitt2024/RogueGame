import os
import random
import math
import time

class Gate:
    def __init__(self):
        self.x = 0
        self.y = 0


class Stats:
    """Class Stats - will be instantiated to form record of Player's and Merchant's stats"""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.Level = 1
        self.Hits = 12
        self.MaxHits = 12
        self.Str = 8
        self.MaxStr = 8
        self.Gold = 0
        self.Armor = 5
        self.Exp = 0
        self.ExpCap = 1
        self.Inventory = []
        self.EquippedItems = []
        self.StatusEffect = ""
        self.Satiety = 100
        self.MoveCounter = 0

    def RenewStats(self):
        RenewPoint = 5
        if self.Hits <= int(0.5 * self.MaxHits):
            RenewPoint = 3
        if self.MoveCounter >= RenewPoint:
            if self.Hits < self.MaxHits:
                self.Hits += 1
            if self.Str < self.MaxStr:
                self.Str += 1
            if self.Satiety > 0:
                self.Satiety -= 1
            self.MoveCounter = 0
        if self.Satiety > 100:
            self.Satiety = 100
        elif 5 <= self.Satiety < 10:
            self.Hits -= 1
        elif 0 <= self.Satiety < 5:
            self.Hits -= 2

class Enemy:
    """(Starting off with) Stats of the lowest-level enemy NPC (Slime)""" 
    def __init__(self):
        self.x = 0
        self.y = 0
        self.type = "Slime"
        self.MaxHits = 4
        self.Hits = 4
        self.Str = 1
        self.Armor = 1
        self.Level = 1
        ## exp given to Player when killed will be formulated (linear equation? or expo?)
        

class Item:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.name = ""
        self.type = "" # melee atk wep: ")", shield: "[", ring: "=", food: ":", jewelry: "*"
        self.Description = ""
        self.Hits = 0
        self.Str = 0
        self.Armor = 0
        self.Satiety = 30

        
def MovePlayer(Player, Direction, Width, Height): # Parameter Direction would be the variable PlayerInput
    """Function that changes the Player's coordinate variables, increments MoveCounter and returns Player object"""
    OriginalPlayerX = Player.x
    OriginalPlayerY = Player.y
    if Direction == "LEFT":
        Player.x -= 1
    elif Direction == "RIGHT":
        Player.x += 1
    elif Direction == "DOWN":
        Player.y += 1
    elif Direction == "UP":
        Player.y -= 1

    if Player.x < 0 or Player.x > Width-1 or Player.y < 0 or Player.y > Height-1:
        print("You have hit a wall!")
        Player.x, Player.y = OriginalPlayerX, OriginalPlayerY
    else:
        print("Player is now at x: {}, y: {}".format(Player.x, Player.y))
    Player.MoveCounter += 1 # MoveCounter needed for purposes e.g. regen
    return Player

def MakeGrid(Width, Height): # Now accept parameter to make new dungeons
    Grid = []
    for i in range(Height):
        Row = []
        for z in range(Width):
            Row.append(".")
        Grid.append(Row)
    
    gold_x, gold_y = Width // 2, Height // 2
    while (gold_x == Width // 2 and gold_y == Height // 2) or [gold_x, gold_y] == [2, 0]:
        gold_x = random.randint(0, Width-1)
        gold_y = random.randint(0, Height-1)
    Grid[gold_y][gold_x] = "G"
    # Adding on the gates to new dungeons
    # NumberOfGates = random.randint(1, 3)
    # for gate in NumberOfGates:
    return Grid

def MakeDungeonGatesCoords(Grid):    
    Dungeon2Gate = Gate()  
    Dungeon2Gate.x, Dungeon2Gate.y = len(Grid[0]) // 2, len(Grid) // 2
    # Sets dungeon coordinate to Player coordinate
    # So condition below evaluates to True and the generation of a non-object-overlapping gate can occur
    
    while Grid[Dungeon2Gate.y][Dungeon2Gate.x] != "." or (Dungeon2Gate.y == len(Grid) // 2 and Dungeon2Gate.x == len(Grid[0]) // 2):
        Dungeon2Gate.x = random.randint(0, len(Grid[0])-1)
        if Dungeon2Gate.x == 0 or Dungeon2Gate.x == len(Grid[0])-1:
            Dungeon2Gate.y = random.randint(0, len(Grid)-1)
        else:
            Dungeon2Gate.y = random.choice([0, len(Grid)-1])                    
    # Confirmed and tested by output - gate coordinates DO EXIST as an int
    return [Dungeon2Gate.x, Dungeon2Gate.y] # Somehow updating cell in the nested loop then returning Grid outside did not work

def DisplayGrid(Grid, Player, Enemies):
    EnemyTypes = [Enemy.type[0] for Enemy in Enemies]
    EnemyCoordinates = [(Enemy.x, Enemy.y) for Enemy in Enemies]
    EnemyDict = dict(zip(EnemyCoordinates, EnemyTypes))
    # The dictionary created will actually hold a list of x and y as a key rather than a value
    # UPDATE: dictionaries cannot hold lists as keys, use tuple (x, y) instead
    # This is so that we can obtain the type of the enemy in this subsequent iteration of grid by referencing to (x, y)
    print("\n" + "-" * (len(Grid[0])*2 + 2))
    for y, row in enumerate(Grid):
        print("|", end="")
        for x, cell in enumerate(row):
            if cell == None:
                cell = "."
            if x == Player.x and y == Player.y and Player.Hits > 0:
                print("P", end=" ")
            elif (x, y) in EnemyCoordinates and Enemies != []:
                print(EnemyDict[(x, y)], end=" ")
            else:
                print(cell, end=" ")
        print("|")
    print("-" * (len(Grid[0])*2 + 2))

def DisplayStats(Player):
    print("Level: {}  ".format(Player.Level), end="")
    print("Hits: {}({})  ".format(Player.Hits, Player.MaxHits), end="")
    print("Str: {}({})  ".format(Player.Str, Player.MaxStr), end="")
    print("Gold: {}  ".format(Player.Gold), end="")
    print("Armor: {}  ".format(Player.Armor), end="")
    print("Satiety: {}%  ".format(Player.Satiety), end="")
    print("Exp: {}/{}  ".format(Player.ExpCap, Player.Exp))

def CheckAndRemoveObjectCollected(Object, Grid, Player):
    ObjectX, ObjectY = None, None
    for y, row in enumerate(Grid):
        for x, cell in enumerate(row):
            # Finding and identifying coordinates of the cell
            if cell == Object:
                ObjectX, ObjectY = x, y
    if Player.x == ObjectX and Player.y == ObjectY:
        Grid[ObjectY][ObjectX] = "."
        return True
    else:
        return False

def GenerateEnemy(Level):
    """Function that returns a list of enemies as [ClassObjects], the variety (number, types) of enemies determined by Level param"""
    LowLevelEnemies = ["S", "E", "Z", "B"]
    MediumLevelEnemies = ["I", "C", "R"] # Might change centaur to leprechaun
    HighLevelEnemies = ["D", "N"] # Might re-add minotaur
    GeneratedEnemies = []
    if Level == 1: # Level 1 - one low level
        GeneratedEnemies.append(CreateEnemies(1, LowLevelEnemies)[0])
    elif Level == 2: # Level 2 - two to three low levels
        EnemyCount = random.randint(2, 3)
        for GeneratedEnemy in CreateEnemies(EnemyCount, LowLevelEnemies):
            GeneratedEnemies.append(GeneratedEnemy)
    elif Level == 3: # Level 3 - two medium or [two to three low levels and one medium]
        if random.randint(0,1) == 0:
            for GeneratedEnemy in CreateEnemies(2, MediumLevelEnemies):
                GeneratedEnemies.append(GeneratedEnemy)
        else:
            for GeneratedLowLevelEnemy in CreateEnemies(random.randint(2, 3), LowLevelEnemies):
                GeneratedEnemies.append(GeneratedLowLevelEnemy)
            GeneratedEnemies.append(CreateEnemies(1, MediumLevelEnemies)[0])
    elif Level == 4:
        GeneratedEnemies.append(CreateEnemies(1, HighLevelEnemies)[0])
            
    return GeneratedEnemies

def CreateEnemies(EnemyCount, EnemyList):
    """Function that instantiates the Enemy class to actually form the Enemy list to be later used and generated on the grid"""
    CreatedEnemies = []
    for i in range(EnemyCount):
        EnemyType = random.choice(EnemyList)
        if EnemyType == "S":
            Slime = Enemy()
            CreatedEnemies.append(Slime)
        elif EnemyType == "E":
            Emu = Enemy()
            Emu.type = "Emu"
            Emu.MaxHits, Emu.Hits = 6, 6
            Emu.Str = 3
            Emu.Armor = 2
            CreatedEnemies.append(Emu)
        elif EnemyType == "Z":
            Zombie = Enemy()
            Zombie.type = "Zombie"
            Zombie.MaxHits, Zombie.Hits = random.randint(4, 7), random.randint(4, 7)
            Zombie.Str = 3
            Zombie.Level = 2
            CreatedEnemies.append(Zombie)
        elif EnemyType == "B":
            Bat = Enemy()
            Bat.type = "Bat"
            Bat.Str = 3
            CreatedEnemies.append(Bat)
        elif EnemyType == "I":
            IceMonster = Enemy()
            IceMonster.type = "Ice monster"
            IceMonster.Str = 5
            IceMonster.MaxHits, IceMonster.Hits = 12, 12
            IceMonster.Armor = 4
            IceMonster.Level = 4
            CreatedEnemies.append(IceMonster)
        elif EnemyType == "C":
            Centaur = Enemy()
            Centaur.type = "Centaur"
            Centaur.Str = random.randint(4, 6)
            Centaur.MaxHits, Centaur.Hits = 18, 18
            Centaur.Armor = 10
            Centaur.Level = 5
            CreatedEnemies.append(Centaur)
        elif EnemyType == "R": # inflict poison
            Rattlesnake = Enemy()
            Rattlesnake.type = "Rattlesnake"
            Rattlesnake.Str = 3
            Rattlesnake.MaxHits, Rattlesnake.Hits = random.randint(12, 16), random.randint(12, 16)
            Rattlesnake.Armor = 4
            Rattlesnake.Level = 4
            CreatedEnemies.append(Rattlesnake)
        elif EnemyType == "D":
            Dragon = Enemy()
            Dragon.type = "Dragon"
            Dragon.Str = random.randint(15, 25)
            Dragon.MaxHits, Dragon.Hits = random.randint(30, 40), random.randint(30, 40)
            Dragon.Armor = random.randint(10, 15)
            Dragon.Level = 10
            CreatedEnemies.append(Dragon)
        #elif EnemyType == "N":
        else:
            Necromancer = Enemy() # Necro should be able to summon zombies
            Necromancer.type = "Necromancer"
            Necromancer.Str = random.randint(5, 8)
            Necromancer.MaxHits, Necromancer.Hits = random.randint(15, 22), random.randint(15, 22)
            Necromancer.Armor = random.randint(20, 25)
            Necromancer.Level = 10
            CreatedEnemies.append(Necromancer)
            
    return CreatedEnemies
        
def RandomPlaceEnemy(Grid, Enemies, Player):
    """Procedure to randomly change coordinate values of each enemy in iterable list of Enemies so no overlap with items/player"""
    for Enemy in Enemies:
        Enemy.x, Enemy.y = Player.x, Player.y
        while (Enemy.x == Player.x and Enemy.y == Player.y) or Grid[Enemy.y][Enemy.x] != ".":
            Enemy.x, Enemy.y = random.randint(0, len(Grid[0])-1), random.randint(0, len(Grid)-1)
        
def MoveEnemy(Grid, Enemies, Player):
    """Function that moves each enemy in an iterable list Enemies, towards Player if within certain proxim., else randomly"""
    CoordinateChanges = {"LEFT": -1, "RIGHT": 1, "UP": -1, "DOWN": 1}
    Directions = []
    
    for Enemy in Enemies:

        # Linear equation so that level 1 enemy has sensitivity 3 cells, level 10 has sensitivity 8 cells
        EnemyRadius = int(5/9 * Enemy.Level + (22/9))
        
        if Enemy.x-EnemyRadius <= Player.x <= Enemy.x+EnemyRadius and Enemy.y-EnemyRadius <= Player.y <= Enemy.y+EnemyRadius:
            if Enemy.x < Player.x and Enemy.y == Player.y and Grid[Enemy.y][Enemy.x+1] == ".":
                EnemyDirection = "RIGHT"
            elif Enemy.x > Player.x and Enemy.y == Player.y and Grid[Enemy.y][Enemy.x-1] == ".":
                EnemyDirection = "LEFT"
            elif Enemy.x == Player.x and Enemy.y < Player.y and Grid[Enemy.y+1][Enemy.x] == ".":
                EnemyDirection = "DOWN"
            elif Enemy.x == Player.x and Enemy.y > Player.y and Grid[Enemy.y-1][Enemy.x] == ".":
                EnemyDirection = "UP"
                
            elif Enemy.x < Player.x and Enemy.y < Player.y:
                if Grid[Enemy.y][Enemy.x+1] == "." and Grid[Enemy.y+1][Enemy.x] == ".":
                    EnemyDirection = random.choice(["RIGHT", "DOWN"])
                elif Grid[Enemy.y][Enemy.x+1] != "." and Grid[Enemy.y+1][Enemy.x] == ".":
                    EnemyDirection = "DOWN"
                elif Grid[Enemy.y][Enemy.x+1] == "." and Grid[Enemy.y+1][Enemy.x] != ".":
                    # Not using else because don't want Enemy to move over cell of an item, same with next 3 branches
                    EnemyDirection = "RIGHT"
                    
            elif Enemy.x > Player.x and Enemy.y < Player.y:
                if Grid[Enemy.y][Enemy.x-1] == "." and Grid[Enemy.y+1][Enemy.x] == ".":
                    EnemyDirection = random.choice(["LEFT", "DOWN"])
                elif Grid[Enemy.y][Enemy.x-1] != "." and Grid[Enemy.y+1][Enemy.x] == ".":
                    EnemyDirection = "DOWN"
                elif Grid[Enemy.y][Enemy.x-1] == "." and Grid[Enemy.y+1][Enemy.x] != ".":
                    #
                    EnemyDirection = "LEFT"
                    
            elif Enemy.x < Player.x and Enemy.y > Player.y:
                if Grid[Enemy.y][Enemy.x+1] == "." and Grid[Enemy.y-1][Enemy.x] == ".":
                    EnemyDirection = random.choice(["RIGHT", "UP"])
                elif Grid[Enemy.y][Enemy.x+1] != "." and Grid[Enemy.y-1][Enemy.x] == ".":
                    EnemyDirection = "UP"
                elif Grid[Enemy.y][Enemy.x+1] == "." and Grid[Enemy.y-1][Enemy.x] != ".":
                    #
                    EnemyDirection = "RIGHT"
                    
            #elif Enemy.x > Player.x and Enemy.y > Player.y:
            else:
                if Grid[Enemy.y][Enemy.x-1] == "." and Grid[Enemy.y-1][Enemy.x] == ".":
                    EnemyDirection = random.choice(["LEFT", "UP"])
                elif Grid[Enemy.y][Enemy.x-1] != "." and Grid[Enemy.y-1][Enemy.x] == ".":
                    EnemyDirection = "UP"
                elif Grid[Enemy.y][Enemy.x-1] == "." and Grid[Enemy.y-1][Enemy.x] != ".":
                    #
                    EnemyDirection = "LEFT"
                else:
                    EnemyDirection = ""
                    
            if EnemyDirection in ["LEFT", "RIGHT"]:
                Enemy.x += CoordinateChanges[EnemyDirection]
            elif EnemyDirection in ["UP", "DOWN"]:
                Enemy.y += CoordinateChanges[EnemyDirection]
                
        else:
            EnemyDirection = random.choice(["UP", "RIGHT", "DOWN", "LEFT"])
            if EnemyDirection == "LEFT" and Enemy.x-1 >= 0 and Grid[Enemy.y][Enemy.x-1] == ".":
                Enemy.x -= 1
            elif EnemyDirection == "RIGHT" and Enemy.x+1 <= len(Grid[0])-1 and Grid[Enemy.y][Enemy.x+1] == ".":
                Enemy.x += 1
            elif EnemyDirection == "DOWN" and Enemy.y+1 <= len(Grid)-1 and Grid[Enemy.y+1][Enemy.x] == ".":
                Enemy.y += 1
            elif EnemyDirection == "UP" and Enemy.y-1 >= 0 and Grid[Enemy.y-1][Enemy.x] == ".":
                Enemy.y -= 1
        
        Directions.append(EnemyDirection) # Needed for collision checking
    return Directions
        
def CheckEnemyCollision(Grid, Player, Enemies, PlayerDirection, EnemiesDirections):
    """Function that checks whether [Player or enemy] has collided with [enemy or player] and therefore attacks the [enemy or player]"""
    # Unsure whether line 339 efficient - CheckEnemyCollision() needs to occur after Player's move and Enemy's move
    # However, EnemiesDirections is reset to [] every iteration, before Player's move so the elif EnemyDirection branch of this procedure doesn't happen
    # The procedure therefore won't occur because using zip - unless fill in with something (see line below)
    EnemiesDirections = ["" for Enemy in range(len(Enemies)) if EnemiesDirections == []] or EnemiesDirections or ""
    for Enemy, EnemyDirection in zip(Enemies, EnemiesDirections):
        if Player.x == Enemy.x and Player.y == Enemy.y:
            if PlayerDirection != "":
                print("\nPlayer attacked!\n")
                # Damage calculation
                PlayerDamage = math.ceil(Player.Str * random.randint(50, 100)/100)
                DamageToEnemy = math.ceil(PlayerDamage * (100/(100 + Enemy.Armor)))
                Enemy.Hits -= DamageToEnemy
                print("{} damage to {}!\n".format(DamageToEnemy, Enemy.type))
                # Move Player back to cell, before they moved
                if PlayerDirection == "LEFT":
                    Player.x += 1
                elif PlayerDirection == "RIGHT":
                    Player.x -= 1
                elif PlayerDirection == "UP":
                    Player.y += 1
                elif PlayerDirection == "DOWN":
                    Player.y -= 1
                print("Player moved back to x: {}, y: {}\n".format(Player.x, Player.y))
            elif EnemyDirection != "":
                print(Enemy.type,"attacked!\n")
                # Damage calculation
                EnemyDamage = math.ceil(Enemy.Str * random.randint(50, 100)/100)
                DamageToPlayer = math.ceil(EnemyDamage * (100/(100 + Player.Armor)))
                Player.Hits -= DamageToPlayer
                print(DamageToPlayer,"damage to Player!\n")
                # Move enemy back to cell, before they moved (will need to amend MoveEnemy() so they can 'move' over and collide w/ Player
                # Grid[Enemy.y][Enemy.x] = "."
                if EnemyDirection == "LEFT":
                    Enemy.x += 1
                elif EnemyDirection == "RIGHT":
                    Enemy.x -= 1
                elif EnemyDirection == "UP":
                    Enemy.y += 1
                elif EnemyDirection == "DOWN":
                    Enemy.y -= 1
                
def CheckCharacterAlive(Hits):
    return (Hits > 0)

def CheckEnemiesDead(Enemies):
    DeadEnemies = []
    for Enemy in Enemies:
        if not CheckCharacterAlive(Enemy.Hits):
            DeadEnemies.append(Enemy)
            Enemies.remove(Enemy)
    return DeadEnemies

def KillEnemyReward(Grid, Level, Player, DeadEnemies):
    """Procedure that displays message, rewards Player by giving exp every time, but has a random chance of dropping item, which calculated using Enemy.Level"""
    if DeadEnemies != []:
        for DeadEnemy in DeadEnemies:
            print("You have defeated",DeadEnemy.type + "!\n")
            Player.Exp += DeadEnemy.Level
            if DeadEnemy.type[0] not in ["N", "D"]:
                ItemDropChance = random.randint(0, 40 + 3*DeadEnemy.Level + Level)
                if random.randint(0, 100) <= ItemDropChance:
                    ItemType = random.choice([")", "[", "=", ":"])
                    if random.randint(0, 100) <= 15:
                        ItemType = "*"
                    return ItemType
            else:
                return "?"
            
def GenerateItem(DeadEnemyCoordinatePair, Player, Enemies, ItemType, Grid):
    if DeadEnemyCoordinatePair == [None, None]:
        x, y = Player.x, Player.y
        EnemyCoordinates = [[Enemy.x, Enemy.y] for Enemy in Enemies if Enemies not in [[], [None]]]
        while (x == Player.x and y == Player.y) or [x, y] in EnemyCoordinates or Grid[y][x] != ".":
            x, y = random.randint(0, len(Grid[0])-1), random.randint(0, len(Grid)-1)
    else:
        x, y = DeadEnemyCoordinatePair[0], DeadEnemyCoordinatePair[1]
    if ItemType == ")": # Sword
        Sword1 = Item()
        Sword1.x, Sword1.y = x, y
        Sword1.name = random.choice(["Dagger", "Mace", "Shortsword", "Axe"])
        Sword1.type = ItemType
        Sword1.Str = random.randint(2, 5)
        Grid[y][x] = Sword1.type
        return Sword1
    elif ItemType == "[":
        Shield1 = Item()
        Shield1.x, Shield1.y = x, y
        Shield1.name = random.choice(["Buckler shield", "Kite shield", "Light shield"])
        Shield1.type = ItemType
        Shield1.Armor = random.randint(5, 10)
        Grid[y][x] = Shield1.type
        return Shield1
    elif ItemType == "=":
        Ring1 = Item()
        Ring1.x, Ring1.y = x, y
        Ring1.name = random.choice(["Vitality ring", "Blood ring", "Ring of zen"])
        Ring1.type = ItemType
        if Ring1.name == "Vitality ring":
            Ring1.Hits = random.randint(4, 6)
        elif Ring1.name == "Blood ring":
            Ring1.Hits = random.randint(7, 10)
        elif Ring1.name == "Ring of zen":
            Ring1.Hits = 20
        Grid[y][x] = Ring1.type
        return Ring1
    elif ItemType == "*":
        Jewelry1 = Item()
        Jewelry1.x, Jewelry1.y = x, y
        Jewelry1.name = random.choice(["Frost gem", "Ruby gem", "Sky gem"])
        Jewelry1.type = ItemType
        if Jewelry1.name == "Frost gem":
            Jewelry1.Description = "A rare item worth many gold"
        elif Jewelry1.name == "Ruby gem":
            Jewelry1.Description = "Exceptionally scarce"
        elif Jewelry1.name == "Sky gem":
            Jewelry1.Description = "???"
        Grid[y][x] = Jewelry1.type
        return Jewelry1
    elif ItemType == ":": # so no cases of None are accepted
        Food1 = Item()
        Food1.x, Food1.y = x, y
        Food1.name = "Food"
        Food1.type = ":"
        Grid[y][x] = Food1.type
        return Food1
    elif ItemType == "?":
        Ratsauyap = Item()
        Ratsauyap.name = "Amulet of Ratsauyap"
        Ratsauyap.type = "?"
        Grid[y][x] = Ratsauyap.type
        return Ratsauyap
    
def CollectItem(Grid, Items, Player):
    if Items != []:
        for Item in Items:
        # Iterates through a list of class objects
            if Item != None:
                if CheckAndRemoveObjectCollected(Item.type, Grid, Player):
                    Player.Inventory.append(Item) # Append the class object
                    print("\nYou picked up {}!".format(Item.name))

def PlayerLevelUp(Player):
    if Player.Exp >= Player.ExpCap:
        while Player.Exp >= Player.ExpCap:
            Player.Exp -= Player.ExpCap
            Player.Level, Player.ExpCap = Player.Level + 1, Player.ExpCap + 1
            UpgradedStat, UpgradedStatValue = random.choice(["max hits", "max strength"]), random.randint(3, 5)
            if UpgradedStat == "max hits":
                Player.MaxHits += UpgradedStatValue
            else:
                Player.MaxStr += UpgradedStatValue
            print("You have leveled up! Player's {} increased by {}!\n".format(UpgradedStat, UpgradedStatValue))
        print("You are now level", Player.Level)

def OpenInventory(Player, Items, Grid):
    DisplayInventory(Player, "Your inventory", True)
    if Player.Inventory != [] or Player.EquippedItems != []:
        UseItem(Player, Items, Grid)
        os.system("clear")

def DisplayInventory(Player, YoursOrMerchants, EquippedInventoryAsWell):
    """Module that displays each item in Player's inventory and equipped items - ItemName left aligned and Stats right aligned within 50 char line"""
    # Also have to check which stats to display - validate by Item.name
    print("-" * 50)
    print("|{:<48}|".format(YoursOrMerchants+":", "Stats"))
    print("|{:<48}|".format(" "))
    for Item in Player.Inventory:
        if "SHIELD" in Item.name.upper():
            print("|{:<24}{:>25}".format(Item.name, "Armor +{}|".format(Item.Armor)))
        elif "RING" in Item.name.upper():
            print("|{:<24}{:>25}".format(Item.name, "Hits +{}|".format(Item.Hits)))
        elif "GEM" in Item.name.upper():
            print("|{:<24}{:>25}|".format(Item.name, Item.Description))
        elif Item.name == "Food":
            print("|{:<24}{:>25}".format(Item.name, "Satiety +{}%|".format(Item.Satiety)))
        else: # Item is a sword
            print("|{:<24}{:>25}".format(Item.name, "Str +{}|".format(Item.Str)))
    if EquippedInventoryAsWell:
        print("|{0:<48}|\n|{1:<48}|\n|{0:<48}|".format(" ", "Equipped:"))
        for EquippedItem in Player.EquippedItems:
            if "SHIELD" in EquippedItem.name.upper():
                print("|{:<24}{:>25}".format(EquippedItem.name, "Armor +{}|".format(EquippedItem.Armor)))
            elif "RING" in EquippedItem.name.upper():
                print("|{:<24}{:>25}".format(EquippedItem.name, "Hits +{}|".format(EquippedItem.Hits)))
            else: # Item is a sword
                print("|{:<24}{:>25}".format(EquippedItem.name, "Str +{}|".format(EquippedItem.Str)))
    print("|{:<48}|".format(" "))
    print("-" * 50)

def UseItem(Player, Items, Grid):
    # Param Items for appending to list of items to display if Player discards an item
    print("To equip/unequip or use an item, enter USE item's name/UNEQUIP item's name\n\nTo discard an item, enter DISCARD item's name\n\nTo exit the inventory screen, enter EXIT\n")
    ItemInput = ""
    AllItems = Player.Inventory.copy()
    AllItems.extend(Player.EquippedItems)
    while ItemInput.upper() != "EXIT" and AllItems != []:
        ItemInput = input("Enter USE item's name, UNEQUIP item's name, DISCARD item's name, or EXIT: ")
        if ItemInput[0:3].upper() == "USE":
            if Player.Inventory != []:
                if ItemInput[4:] in [Item.name for Item in Player.Inventory]:
                    for Item in Player.Inventory:
                        if Item.name == ItemInput[4:]:
                            if Item.type == ":":
                                print("\nYou ate Food\n")
                                Player.Satiety += Item.Satiety
                                Player.Inventory.remove(Item)
                                break
                            elif Item.type == "*":
                                print("\nYou equipped the '{}' but found that nothing happened...you put it back into your inventory\n".format(Item.name))
                                break
                            else:
                                if Item in Player.EquippedItems:
                                    print("\n'{}' is already equipped!\n".format(Item.name))
                                    break
                                elif Item.type == ")":
                                    print("\nYou equipped '{}'\n".format(Item.name))
                                    Player.MaxStr, Player.Str = Player.MaxStr + Item.Str, Player.Str + Item.Str
                                    Player.EquippedItems.append(Item)
                                    Player.Inventory.remove(Item)
                                    break
                                elif Item.type == "[":
                                    print("\nYou equipped {}\n".format(Item.name))
                                    Player.Armor += Item.Armor
                                    Player.EquippedItems.append(Item)
                                    Player.Inventory.remove(Item)
                                    break
                                #elif Item.type == "=":
                                else:
                                    print("\nYou equipped {}\n".format(Item.name))
                                    Player.MaxHits, Player.Hits = Player.MaxHits + Item.Hits, Player.Hits + Item.Hits
                                    Player.EquippedItems.append(Item)
                                    Player.Inventory.remove(Item)
                                    break
                                # break used in each branch otherwise may equip item with same name more than once
                else:
                    print("\nThere is no '{}' in your inventory!\n".format(ItemInput[4:]))
            else:
                print("\nYou have nothing to equip or use!\n")

        elif ItemInput[0:7].upper() == "UNEQUIP":
            if Player.EquippedItems != []:
                if ItemInput[8:] in [EquippedItem.name for EquippedItem in Player.EquippedItems]:
                    for EquippedItem in Player.EquippedItems:
                        if ItemInput[8:] == EquippedItem.name:
                            print("\nYou unequipped {}\n".format(EquippedItem.name))
                            Player.EquippedItems.remove(EquippedItem)
                            Player.Inventory.append(EquippedItem)
                            if EquippedItem.type == ")":
                                Player.MaxStr, Player.Str = Player.MaxStr - EquippedItem.Str, Player.Str - EquippedItem.Str
                            elif EquippedItem.type == "[":
                                Player.Armor -= EquippedItem.Armor
                            else:
                                Player.MaxHits, Player.Hits = Player.MaxHits - EquippedItem.Hits, Player.Hits - EquippedItem.Hits
                            break
            else:
                print("You have nothing to unequip!\n")

        elif ItemInput[0:7].upper() == "DISCARD":
            if ItemInput[8:] in [Item.name for Item in AllItems]:
                for Item in AllItems:
                    if ItemInput[8:] == Item.name:
                        print("\nYou discarded {}\n".format(Item.name))
                        AllItems.remove(Item)
                        if Item in Player.Inventory:
                            Player.Inventory.remove(Item)
                        else:
                            Player.EquippedItems.remove(Item)
                            if Item.type == ")":
                                Player.MaxStr, Player.Str = Player.MaxStr - Item.Str, Player.Str - Item.Str
                            elif Item.type == "[":
                                Player.Armor -= Item.Armor
                            else:
                                Player.MaxHits, Player.Hits = Player.MaxHits - Item.Hits, Player.Hits - Item.Hits
                        Item.x, Item.y = Player.x, Player.y
                        Grid[Item.y][Item.x] = Item.type
                        Items.append(Item)
                        break           
            else:
                print("\nThere is no '{}' in your inventory!\n".format(ItemInput[8:]))
        DisplayInventory(Player, "Your inventory",True)

def WinCondition(Player):
    return ("?" in [Item.type for Item in Player.Inventory])

def MerchantStore(Player, MerchantSword, MerchantShield, MerchantRing):
    os.system("clear")
    print("You find yourself in a peculiar floor, alone with an old and ragged man...")
    Merchant = Stats()
    MerchantSword.name, MerchantSword.type, MerchantSword.Str = "Nightingale blade", ")", random.randint(10, 18)
    MerchantShield.name, MerchantShield.type, MerchantShield.Armor = "Daedric shield", "[", random.randint(15, 22)
    MerchantRing.name, MerchantRing.type, MerchantRing.Hits = "Havel's ring", "=", random.randint(25, 30)
    Merchant.Inventory.extend([MerchantSword, MerchantShield, MerchantRing])
    DisplayInventory(Merchant, "Merchant's shop", False)
    print("Your gold:",Player.Gold)

    print("\n'Welcome to my floor, adventurer...'\n\n'Each item in here is worth 100 gold coins...'\n\n'Enter the name of the item you want...'\n\n(Enter EXIT to leave, at any point)\n")
    ItemName = ""
    while ItemName.upper() != "EXIT":
        ItemName = input("Enter the item's name: ")
        if ItemName in [MerchantItem.name for MerchantItem in Merchant.Inventory]:
            PayMethod = input("\n'Tell me 'GOLD' if you want to pay in gold coins, or tell me 'GEM' if you want to pay with a gem...'\n")
            if PayMethod.upper() == "EXIT":
                break
            elif PayMethod.upper() == "GOLD":
                if Player.Gold >= 100:
                    Player.Gold -= 100
                else:
                    print("\nHah! That is not enough gold...\n")
                    continue
            elif PayMethod.upper() == "GEM":
                if "GEM" not in "".join([Item.name for Item in Player.Inventory]).upper():
                    print("\nHmm...you do not have a gem...\n")
                    continue
                else:
                    for Item in Player.Inventory:
                        if "GEM" in Item.name.upper():
                            Player.Inventory.remove(Item)
                            break
            else:
                continue
            for MerchantItem in Merchant.Inventory:
                if ItemName == MerchantItem.name:
                    Player.Inventory.append(MerchantItem)
                    Merchant.Inventory.remove(MerchantItem)
                    print("\nA good deal for the {}...\n".format(ItemName))
                    break
            DisplayInventory(Merchant, "Merchant's shop", False)
            print("Your gold:",Player.Gold)
        else:
            print("\nI do not have '{}'...\n".format(ItemName))
    os.system("clear")
    
def DisplayCommands():
    for ValidDirection in ["LEFT", "RIGHT", "DOWN", "UP"]:
        print("\nTo move {} one space, enter {}".format(ValidDirection.lower(), ValidDirection))
    print("\nTo not move and simply pass a turn, enter NONE\n")
    print("To view your inventory of items, enter INVENTORY\n")
    print("To view the dictionary of this game's symbols, enter SYMBOLS\n")
    print("To view the set of valid commands, enter COMMANDS")

def Main():    
    # Level used for creation of new Dungeons, checking which set of coordinate should be used
    Level = 0

    # Welcome user, get Width, Height + Validation
    print("""
██████╗░░█████╗░░██████╗░██╗░░░██╗███████╗
██╔══██╗██╔══██╗██╔════╝░██║░░░██║██╔════╝
██████╔╝██║░░██║██║░░██╗░██║░░░██║█████╗░░
██╔══██╗██║░░██║██║░░╚██╗██║░░░██║██╔══╝░░
██║░░██║╚█████╔╝╚██████╔╝╚██████╔╝███████╗
╚═╝░░╚═╝░╚════╝░░╚═════╝░░╚═════╝░╚══════╝
    """)
    PlayerName = input("What is Rogue's name? ")
    Messages = ["\nHello {}, Welcome to the Dungeons of Doom\n".format(PlayerName),
                "To beat this game, you must collect the amulet of Ratsauyap\n",
                "To view all possible commands, input 'COMMANDS'\n",
                "Good luck, {}!\n".format(PlayerName)]
    for Message in Messages:
        print(Message)
        time.sleep(1.5)
    os.system("clear")
    print("The smallest starting grid possible is 2 x 2")
    global Width, Height
    Width, Height = "", ""
    while not Width.isdigit() or Width == "1":
        Width = input("\nEnter the width of the grid: ")
    while not Height.isdigit() or Height == "1":
        Height = input("\nEnter the height of the grid: ")
    Width, Height = int(Width), int(Height)
    print("\nGrid dimensions set to {} x {}\n".format(Width, Height))

    # List LevelSizes to access the Widths and Heights of each level/dungeon
    LevelsSizes = [[Width, Height]]

    # Record of player's x and y coordinates
    Player = Stats()
    Player.x, Player.y = Width // 2, Height // 2
    
    # The centre in any even-numbered grid will be the upper half (in this game)
    print("The player starts at x: {}, y: {}".format(Player.x, Player.y))
    DisplayCommands()

    Enemies = []
    Items = []
    
    Symbols = {"|": "Vertical wall", "_": "Horizontal wall", ".": "Floor", "P": "Player", "𖡄": "Floor gate, you will be transported and CANNOT COME BACK once you land on it", "G": "Gold coin", ")": "Sword", "[": "Shield", "=": "Ring", ":": "Food", "*": "Jewelry", "A-Z": "Enemies (excluding P (Player) and G (Gold coin))"}
    Grid = MakeGrid(Width, Height)
    GateX, GateY = MakeDungeonGatesCoords(Grid)
    Grid[GateY][GateX] = "𖡄"
    DisplayGrid(Grid, Player, Enemies)
    DisplayStats(Player)

    PlayerAlreadyMoved = False

    while CheckCharacterAlive(Player.Hits):
        PlayerInput = input("Enter a command: ").upper()
        EnemiesDirections = []
        if PlayerInput in ["LEFT", "RIGHT", "DOWN", "UP", "NONE", "INVENTORY", "COMMANDS", "SYMBOLS"]:
            if PlayerInput in ["LEFT", "RIGHT", "DOWN", "UP", "NONE"]:
                os.system("clear")
                time.sleep(0.2)
                print("\nDirection specified:", PlayerInput, "\n")

                # Amend the MovePlayer so that validation for CoordinateError uses input parameters Width, Height
                Player = MovePlayer(Player, PlayerInput, LevelsSizes[Level][0], LevelsSizes[Level][1])
                PlayerAlreadyMoved = True
                if Level != 0:
                    CheckEnemyCollision(Grid, Player, Enemies, PlayerInput, EnemiesDirections)
                if not CheckCharacterAlive(Player.Hits):
                    break
                DeadEnemies = CheckEnemiesDead(Enemies)
                for DeadEnemy in DeadEnemies:
                    DeadEnemyCoordinatePair = [DeadEnemy.x, DeadEnemy.y]
                    GeneratedItem = GenerateItem(DeadEnemyCoordinatePair,Player, Enemies, KillEnemyReward(Grid, Level, Player, DeadEnemies), Grid)
                    if GeneratedItem != None:
                        Items.append(GeneratedItem)
                CollectItem(Grid, Items, Player)
                Player.RenewStats()
                PlayerLevelUp(Player)

                if WinCondition(Player):
                    break
                
                # Direction is reset so that CheckEnemyCollision() can work after Enemy has moved but Player doesn't 'move back'
                PlayerInput = ""
                
                EnemiesDirections = MoveEnemy(Grid, Enemies, Player)
                if Level != 0:
                    CheckEnemyCollision(Grid, Player, Enemies, PlayerInput, EnemiesDirections)
                if not CheckCharacterAlive(Player.Hits):
                    break

                # Check if coin collected
                if CheckAndRemoveObjectCollected("G", Grid, Player):
                    gold_found = random.randint(10, 50)
                    Player.Gold += gold_found
                    print("\nYou found {} gold pieces".format(gold_found))

                # Check if Player is now on a gate, and teleport, and enemies: delete old, generate new
                elif GateX == Player.x and GateY == Player.y:
                    Level += 1
                
                    # Call some function to change to a new grid
                    Width2, Height2 = random.randint(8, 15), random.randint(8, 15)
                    LevelsSizes.append([Width2, Height2])
                    # Making sure the CoordinateError of initial gate boundaries don't carry on to 2nd one:
                    # Make a list of widths/heights? Use a 'Level' variable to represent which set of data should be used?
                    Grid = MakeGrid(LevelsSizes[Level][0], LevelsSizes[Level][1])

                    if Level == 3:
                        MerchantStore(Player, Item(), Item(), Item())

                    if Level < 4: # Final level, no more gates generated
                        GateX, GateY = MakeDungeonGatesCoords(Grid)
                        Grid[GateY][GateX] = "𖡄"
                    
                    Enemies = []
                    for GeneratedEnemy in GenerateEnemy(Level):
                        Enemies.append(GeneratedEnemy)
                    Player.x, Player.y = LevelsSizes[Level][0] // 2, LevelsSizes[Level][1] // 2
                    print("\nPlayer is transported to x: {}, y: {} of a new dungeon\n".format(Player.x, Player.y))
                    print("New dungeon dimensions are {} x {}".format(Width2, Height2))
                    RandomPlaceEnemy(Grid, Enemies, Player)
                    PlayerAlreadyMoved = False
                    if not PlayerAlreadyMoved:
                        if (Level == 1 and random.randint(0, 100) <= 100) or (Level == 2 and random.randint(0, 100) <= 35) or (Level in [3, 4] and random.randint(0, 100) <= 45):
                            Items.append(GenerateItem([None, None], Player, Enemies, random.choice([")", "[", "=", "*", ":"]), Grid))

            elif PlayerInput == "INVENTORY":
                os.system("clear")
                time.sleep(0.2)
                OpenInventory(Player, Items, Grid)
                Player.RenewStats()

            elif PlayerInput == "COMMANDS":
                os.system("clear")
                time.sleep(0.2)
                DisplayCommands()

            elif PlayerInput == "SYMBOLS":
                os.system("clear")
                time.sleep(0.2)
                for Symbol, Meaning in Symbols.items():
                    print("\n", Symbol, ":", Meaning)

            DisplayGrid(Grid, Player, Enemies)
            DisplayStats(Player)

    if not CheckCharacterAlive(Player.Hits):
        DisplayGrid(Grid, Player, Enemies)
        print("""
Player has died!

██████╗ ███████╗███████╗███████╗ █████╗ ████████╗
██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗╚══██╔══╝
██║  ██║█████╗  █████╗  █████╗  ███████║   ██║   
██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██╔══██║   ██║   
██████╔╝███████╗██║     ███████╗██║  ██║   ██║   
╚═════╝ ╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝
    """)

    else:
        DisplayGrid(Grid, Player, Enemies)
        print("""
You have found the amulet of Ratsauyap!

██╗   ██╗ ██████╗ ██╗   ██╗    ██╗    ██╗██╗███╗   ██╗
╚██╗ ██╔╝██╔═══██╗██║   ██║    ██║    ██║██║████╗  ██║
 ╚████╔╝ ██║   ██║██║   ██║    ██║ █╗ ██║██║██╔██╗ ██║
  ╚██╔╝  ██║   ██║██║   ██║    ██║███╗██║██║██║╚██╗██║
   ██║   ╚██████╔╝╚██████╔╝    ╚███╔███╔╝██║██║ ╚████║
   ╚═╝    ╚═════╝  ╚═════╝      ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝
    """)

if __name__ == "__main__":
    Main()
