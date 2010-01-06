
Tale
====

Tale is intended to be an immersive, quirky, humerous, text-based, multi-player
adventure game set on the faces of a six-sided die and played in a web browser.

Thematically, Tale takes place in a fantasy world that combines magical
medi-aeval Fairae with certain Viking motifs and smashes them up against a
premature mechanical Victorian era inhabited by creatures that might have
evolved from the seminal cyan-haired creatures from Lemmings.  On an unrelated
note, I have never taken drugs; close friends tell me I do not need to.

In terms of Gameplay, Tale is intended to borrow from Zork/Adventure and MUDs
room exploration and melee; the original Zelda for top-down perspective
tactics, strategy, and world exploration; and Final Fantasy for magic and
combat.  Or something completely unlike those things since I have never
excelled at any of those games and have no idea what I am talking about.

The Tale world is called Dya, and is like a single six sided Die, or 1D6 in the
Nerd parlance.  Each face of the die corresponds with various factions and
alliances, political motivations, character alignment, key signatures, dominant
forms of life, biomes, and pedigrees.  Euia, Occia, Borea, Austra, Oria, and
Dysia are the names of each face from 6 down to 1 vaguely from nice down to
quite naughty.

In terms of Music, Chris Pasillas has scored and is responsible for rendering
theme music for each face of the world.  The Euian anthem with which the game
begins was originally scored for a church event DVD in San Luis Obispo when we
were in college called "Getting on the Bus".  It is our intent that it will get
stuck in your head, that you will occasionally wake up and sing it in the
shower to shake your spirit out and make you ready for just about any
adventure.  Bring it.

In terms of art, Tale is drawn in Inkscape.  I do my own stunts.  Honestly, you
can do them if you want.  In any case, Inkscape saves vector graphics to
Scalable Vector Graphics format, which in turn is a well-formed XML language.
Much of the Tale art is programmable; its layers can be permuted, sorted, and
transformed.  Particularly, the avatar, rider, and ride graphic contain
hundreds of layers for visualizing various combinations of equipment, character
gender, and breeds of mount from equine to piscene.  The vessel graphic has
layers ranging from boat to warship with three styles of sail plans and can be
refit for zeppelin and rocket plane modes.  I plan to do something similar for
castles.  There are plates of individual trees and giant mushrooms that include
boundary boxes and pathing squares to assist in programmatically composing them
into scenes.

Technologically, Tale is a Python-based game engine built on the Twisted
asynchronous event-driven IO system.  Presently, Tale is designed to run
through a LigHTTPd daemon that hosts static content and serves as an HTTP proxy
for the underlying Tale game engine daemon that both manages the world and
persistent session state for all connected users.  The Tale daemon communicates
with the web browser over either push or pull messaging (the design is flexible
in acommodating either strategy, whichever works best).  If NodeJS
matures and V8 implements ECMAScript 5, abandoning Python and its handy
generators in favor of a securely user-customizable engine built entirely in
JavaScript might be persuable for some components.  Components that do not need
events or persistent state, like the game Wiki and graphics generators will
probably be managed with FastCGI and possibly Django.  Give unto Dyo that
which belongs to Dyo.

If Tale is to scale to become massively multi-player, it is intended that the
game engine should grow to run on multiple hosts, permitting a single game
instance to be played by a large number of players.  This would be accomplished
by distributing the nodes of the world tree and balancing the scope that each
node is responsible for managing based on player activity.  Ryan Witt and I
have an inkling of using the Chord algorithm directly for running various
distributed hash tables across the nodes of the world server.

The Tale world tree is a single root with six children (one for each die-face),
where each face is divided into six tiles (one for each pip), and each pip
is divided recusrively into quadrants (a quad-tree) to the finest
granularily room (axiomatically having the length and width of exactly one
room).  Events and Objects move and propagate in and out of rooms
to larger and smaller rooms, but not directly across adjacent rooms of the
same size.  This permits certain optimizations, the authoring of simple
map/reduce style event propagation and physics simulations, and flushes well
with Zelda-like room to room movement.

Setup
-----

* Twisted Python (python-twisted)
* LigHTTPd (lighttpd)
* Python `simplejson`
* Chiron installed in `www/chiron`

