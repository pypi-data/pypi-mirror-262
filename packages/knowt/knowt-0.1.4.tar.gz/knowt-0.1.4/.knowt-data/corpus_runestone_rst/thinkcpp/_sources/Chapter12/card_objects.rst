``Card`` objects
----------------

If you are not familiar with common playing cards, now would be a good
time to get a deck, or else this chapter might not make much sense.
There are 52 cards in a deck, each of which belongs to one of four suits
and one of 13 ranks. The suits are Spades, Hearts, Diamonds and Clubs
(in descending order in Bridge). The ranks are Ace, 2, 3, 4, 5, 6, 7, 8,
9, 10, Jack, Queen and King. Depending on what game you are playing, the
rank of the Ace may be higher than King or lower than 2.

If we want to define a new object to represent a playing card, it is
pretty obvious what the instance variables should be: ``rank`` and
``suit``. It is not as obvious what type the instance variables should
be. One possibility is ``string``\ s, containing things like
``"Spade"`` for suits and ``"Queen"`` for ranks. One problem with this
implementation is that it would not be easy to compare cards to see
which had higher rank or suit.

.. index::
   single: encode

An alternative is to use integers to **encode** the ranks and suits. By
“encode,” I do not mean what some people think, which is to encrypt, or
translate into a secret code. What a computer scientist means by
“encode” is something like “define a mapping between a sequence of
numbers and the things I want to represent.” For example,

======== =============== =
Spades   :math:`\mapsto` 3
Hearts   :math:`\mapsto` 2
Diamonds :math:`\mapsto` 1
Clubs    :math:`\mapsto` 0
======== =============== =

The symbol :math:`\mapsto` is mathematical notation for “maps to.” The
obvious feature of this mapping is that the suits map to integers in
order, so we can compare suits by comparing integers. The mapping for
ranks is fairly obvious; each of the numerical ranks maps to the
corresponding integer, and for face cards:

===== =============== ==
Jack  :math:`\mapsto` 11
Queen :math:`\mapsto` 12
King  :math:`\mapsto` 13
===== =============== ==

The reason I am using mathematical notation for these mappings is that
they are not part of the C++ program. They are part of the program
design, but they never appear explicitly in the code. The class
definition for the ``Card`` type looks like this:

::

   struct Card {
     int suit, rank;

     Card ();
     Card (int s, int r);
   };

   Card::Card () {
     suit = 0;  rank = 0;
   }

   Card::Card (int s, int r) {
     suit = s;  rank = r;
   }

There are two constructors for ``Card``\ s. You can tell that they are
constructors because they have no return type and their name is the same
as the name of the structure. The first constructor takes no arguments
and initializes the instance variables to a useless value (the zero of
clubs).

The second constructor is more useful. It takes two parameters, the suit
and rank of the card.

The following code creates an object named ``threeOfClubs`` that
represents the 3 of Clubs:

::

      Card threeOfClubs (0, 3);

The first argument, ``0`` represents the suit Clubs, the second,
naturally, represents the rank 3.

.. fillintheblank:: card_objects_1

    The instance variables for a playing card are |blank| and |blank|.

    - :([Ss][Uu][Ii][Tt])|([Rr][Aa][Nn][Kk]): Correct!
      :x: Incorrect!  Try again!
    - :([Ss][Uu][Ii][Tt])|([Rr][Aa][Nn][Kk]): Correct!
      :.*: Incorrect!  Try again!

.. mchoice:: card_objects_2
   :answer_a: To translate each rank / suit into a secret code.
   :answer_b: To create strings to represent each rank / suit.
   :answer_c: To define a mapping between each rank / suit and a sequence of numbers.
   :answer_d: To write code describing real objects, like cards, with their respective ranks / suits.
   :correct: c
   :feedback_a: Incorrect! This is called encryption.
   :feedback_b: Incorrect! We create strings before we encode.
   :feedback_c: Correct! This makes it easier to compare cards.
   :feedback_d: Incorrect! This is how we describe object-oriented programming.

   What does it mean to **encode** the ranks and suits?

.. fillintheblank:: card_objects_3

    The symbol :math:`\mapsto` means __________.

    - :([Mm][Aa][Pp][Ss] [Tt][Oo]): Correct!
      :.*: Incorrect!  Try again!

.. mchoice:: card_objects_4
   :answer_a: To have better organization in your code.
   :answer_b: To make it possible to compare objects that have non-numerical values.
   :answer_c: To represent complex objects visually.
   :answer_d: To add complexity to your code.
   :correct: b
   :feedback_a: Incorrect! Mapping helps more with order than with organization.
   :feedback_b: Correct! By mapping non-numerical values to integers, we can compare them!
   :feedback_c: Incorrect! There is nothing visual about mapping.
   :feedback_d: Incorrect! Mapping actually simplifies your code.

   What is the purpose of mapping?
