Decks
-----

In the previous chapter, we worked with a vector of objects, but I also
mentioned that it is possible to have an object that contains a vector
as an instance variable. In this chapter I am going to create a new
object, called a ``Deck``, that contains a vector of ``Card``\ s.

The structure definition looks like this

::

   struct Deck {
     vector<Card> cards;

     Deck (int n);
   };

   Deck::Deck (int size) {
     vector<Card> temp (size);
     cards = temp;
   }

The name of the instance variable is ``cards`` to help distinguish the
``Deck`` object from the vector of ``Card``\ s that it contains.

For now there is only one constructor. It creates a local variable named
``temp``, which it initializes by invoking the constructor for the
``vector`` class, passing the size as a parameter. Then it copies the
vector from ``temp`` into the instance variable ``cards``.

Now we can create a deck of cards like this:

::

     Deck deck (52);

Here is a state diagram showing what a ``Deck`` object looks like:

.. figure:: Images/13.3stackdiagram.png
   :scale: 35%
   :align: center
   :alt: image

The object named ``deck`` has a single instance variable named
``cards``, which is a vector of ``Card`` objects. To access the cards in
a deck we have to compose the syntax for accessing an instance variable
and the syntax for selecting an element from an array. For example, the
expression ``deck.cards[i]`` is the ith card in the deck, and
``deck.cards[i].suit`` is its suit. The following loop

::

     for (int i = 0; i<52; i++) {
       deck.cards[i].print();
     }

demonstrates how to traverse the deck and output each card.

.. fillintheblank:: decks_1

    A euchre deck consists of 9's, 10's, Jacks, Queens, Kings, and Aces.
    If we wanted to create a deck that is the size of the euchre deck, we 
    would type: ``Deck euchre_deck`` |blank| ``;``

    - :\(24\): Correct!
      :.*: Try again!

.. mchoice:: decks_2
   :answer_a: The ranks and suits of the cards are initialized to the proper ranks and suits in a standard deck of cards.
   :answer_b: There will be 52 cards.
   :answer_c: The ranks and suits will be initialized to their default values.
   :answer_d: The only instance variable in the deck is cards.
   :answer_e: You can't access individual cards in the deck.
   :correct: b,c,d
   :feedback_a: Unless you the programmer tell it to, the computer won't do it.
   :feedback_b: We initialized cards with a value of 52.
   :feedback_c: In our case is, the default values are zero.
   :feedback_d: cards is a vector of Cards!
   :feedback_e: You can access any card by indexing, for example: deck.cards[n].

   Take a look at the state diagram above. When we create a deck of cards using ``Deck deck (52)``, 
   what is true about our new deck?

.. mchoice:: decks_3
   :answer_a: True - because this is the default mapping of enumerated types.
   :answer_b: True - because our definition of rank overrides the default mapping.
   :answer_c: False - because this is the default mapping of enumerated types.
   :answer_d: False - because our definition of rank overrides the default mapping.
   :correct: d
   :feedback_a: The default mapping begins with 0.
   :feedback_b: Our definition doesn't use the default mapping, which begins with 0.
   :feedback_c: The default mapping begins with 0.
   :feedback_d: If we wanted to, we could have set the rank of ace to 7, and the rest of the cards would still be ranked in order.

   ``ACE`` corresponds to a rank of value ``0``. 
