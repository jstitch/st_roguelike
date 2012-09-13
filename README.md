RogueWarts, the Harry Potter Roguelike Game
===========================================

A roguelike game themed on the Harry Potter world.

The idea behind the game is to create an adventure game in the
roguelike genre, with its world based on the one created by
J.K.Rowling in its Harry Potter series.

Its intention IS NOT to use any Harry Potter's characters (perhaps
just places). The idea is to follow the background information at
websites such as the Harry Potter Lexicon (hp-lexicon.org) to give the
game a 'real' Harry Potter look, not to replay any scenes from the
books/movies in it.

You need the doryen library (libtcod v1.5.0) to run this
game. Download at http://doryen.eptalys.net/libtcod/download/

To play, just type:

  python roguewarts.py

(please mind that Python 2 is required)

Feedback
--------
Please send feedback to jstitch @ gmail . com

If you are reporting any errors, don't forget to include logs and any
information the game displayed, and what were you doing when it
crashed.

Files Info
----------
- roguewarts.py is the entrance to the game, where the main loop lives.
- data/ holds data files for the game
- libtcod/ holds the python module for libtcod
- game/ holds the game engine logic
- world/ holds the game's world logic
- ui/ holds the UI logic
- objects/ holds the objects-monsters-players logic
- log/ stores the game logs
- libtcod is needed for roguewarts to work. Please download it and add
  it to the game root directory

(The reason that libtcod is not included as part of the game files is
because it's in fact an external library, not part of
roguewarts. Also, you may need a different specific compilation of the
doryen library, depending on your system)

DEV Info
--------

This game is developed using:

- Python (2.7, but earliear 2.x versions are supported as long as
  libtcod is supported by them)
- libtcod v1.5.0

Currently it may be played using the following graphical UI libraries:

- Curses *
- Libtcod **

(*) For running through a remote server, libtcod library must be
    recompiled. See the ui.uiwrappers package documentation for more
    info on this. libtcod directory includes a patch for libtcod
    v1.5.0 to achieve this. If you are not planning to run the game
    through a remote server, this patch and this note are irrelevant.

(**) Please download or compile your libtcod installation according to
     your system. Downloads at
     http://doryen.eptalys.net/libtcod/download/

But more graphical UI libraries may be added. Please consult the pydoc
documentation in the UI modules for more information.


Project Status
--------------

The current status of the game is a VERY BASIC development version
which is just capable of:

-Generating one tipe of level

-Creating a player that can move through the level

Why so basic yet?
-----------------

Because I spent most of the time until now to program a kind-of
framework for easy development (at least for myself).

The framework still has a lot of pending work to do, but at least it
now can support some game logic development without messing around too
much with details about UI or game engine.

The documentation at game/game.py may be a good starting point to
document yourself about the framework and internal architecture.

I got a lot of ideas from this sources:

- Roguebasin's Complete Roguelike Tutorial, using python+libtcod
  (http://roguebasin.roguelikedevelopment.org/index.php/Complete_Roguelike_Tutorial,_using_python%2Blibtcod)
- Its corresponding forum thread at Roguecentral (home of the Doryen
  site, which hosts libtcod development)
  (http://doryen.eptalys.net/forum/index.php?topic=328.0)
- A roguelike tutorial which began to appear at Kooneiform blog, but
  was then interrupted when Roguebasin published its own. However, I
  found a lot of interesting ideas in the source code I tried to use
  here too. (http://kooneiform.wordpress.com/)
- Some ideas were inspired in the source code for the Pyro roguelike
  game (http://sourceforge.net/projects/pyrogue/)

Known Bugs
----------

Dungeon type 2 generation may generate stairs in room's walls
coordinates, instead of just inside room (not counting walls).

Curses ui has problems with diagonal movement keys.

TODO
----

Here is a list of some TODO's I've detected that should be
addressed. They're kind of commented on the code too, in TODO sections
on the pydoc.

- Refactor the engine to add actions coming from a
  objects.player.Player class. Actions should come frome the current
  update class (for example the game.Game.Gameplay class) but also
  from the specific type of player. For example, movement actions
  should go in certain type of Player, while 'quit' command is part of
  the update class.

- That last ones means refactoring the objects.player.Player class
  too. But also, I think that the Player class should be some other
  component to be added on a objects.Objeto class so instead of
  representing a played character in the game by itself, the Player
  gives this attribute to some specific Objeto instance (this could
  add the possibility to control some given monster at certain part of
  the game?). So a given Player class should have its own commands to
  'play' the player in the Gameplay engine update instance...

- In the world, levels should be initilized in a non-hard-coded way,
  maybe reading the definition from some file.

- Implement room geometrics other than the Rect one.

- Intersection between rooms is done just for rectangular ones. Should
  be generalized for other geometrics too.

- Implement map generation for other types than the Dungeon2 one.

- Implement __str__ method for the world.level.Level class. This
  should draw the complete map of the level. It should be supported by
  some method which returns an array of world.tile.Tile instances,
  which may be used to draw the level in the UI.

- Right now the rules for deciding the type of map to associate the
  level on a given branch are HARD-CODED, must do this in another
  way... (some kind of config file?  some kind of class or structure
  holding this rules?).  Also, this rules defines, in a way, the
  complete structure of the world (where each branch begins and
  ends). This info should be delivered by the World itself, in
  not-hard-coded rules too.

- UI should manage the internals of messages queue and map render in
  it, instead of in the wrapper. Should only give the wrapper the
  contents of the messages/main/any area to be drawn, perhaps to some
  generic render method in there.

- UI Wrappers should draw level objects. It just draws the map (and
  the player but just in a testing manner). The UI should call some
  method in the level class to get Tiles or something to represent
  what is it to be drawn. Then it should give it to some generic
  render method in the wrapper.

- Also, as you may have guessed, the fact that this is all done over a
  kind-of-framework, the 'framework' logic may be separated in some
  way, so that the 'framework' does something in a specific place, and
  the game-logic living elsewhere, opening a lot of possibilities of
  future development for any other themed roguelike games, with
  different game rules for example.
