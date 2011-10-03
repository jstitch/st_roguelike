RogueWarts, the Harry Potter Roguelike Game
===========================================

A roguelike game themed on the Harry Potter world.

The idea behind the game is to create an adventures games in the
roguelike genre, with its world based on the one created by
J.K.Rowling in its Harry Potter series.

Its intention IS NOT to use any Harry Potter's characters (perhaps
just places). The idea is to follow the background information at
websites such as the Harry Potter Lexicon (hp-lexicon.org) to give the
game a 'real' Harry Potter look, not to replay any scenes from the
books/movies in it.

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
- libtcod.so is the library which supports a lot of the game's internals.
- data/ holds data files for the game
- libtcod/ holds the python module for libtcod
- game/ holds the game engine logic
- world/ holds the game's world logic
- ui/ holds the UI logic
- objects/ holds the objects-monsters-players logic
- log/ stores the game logs

DEV Info
--------

This game is developed using:

- Python (2.7, but earliear 2.x versions are supported as long as
  libtcod is supported by them)
- libtcod

Currently it may be played using the following graphical UI libraries:

- Curses*
- Libtcod**

* For running through a remote server, libtcod library must be
  recompiled. See the ui.uiwrappers package documentation for more
  info on this. libtcod directory includes a patch for libtcod v1.5.0
  to achieve this. If you are not planning to run the game through a
  remote server, this patch and this note are irrelevant.

** Default version of the game includes libtcod library compiled for a
   Linux-64 architecture (with the aforementioned patch
   applied). Please change your libtcod compilation according to your
   system. Downloads at http://doryen.eptalys.net/libtcod/download/

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

The frameworkd still has a lot of pending work to do, but at least it
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
