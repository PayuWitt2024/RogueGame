# RogueGame
A rogue-like RPG made with ASCII Art, 2021
Modules used: os, random, math time (standard Python library)
The game is set in a dungeon where a player must navigate through different floors, collect items, defeat enemies, and defeat the final boss
The difficulty of the game is dependent on random luck (gold, items)
However, all games are possible to win
The main mechanisms of the game:
  Player will have the option to select the size of the starting dungeon
  Player will move and enemies will move in a turn-based style
  Player's interactions with items do not count towards the turn counter
  Enemies will move depending on their 'detection radius'
    Once Player is within this radius, enemies will move towards the hero, with a random chance between decreasing the x-separation or the y-separation
    The higher the level of the Enemy, the larger the radius
    Player should strategize according to this algorithm
  Player will experience Hits regeneration and hunger
