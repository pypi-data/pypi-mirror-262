Vectors of cards
----------------

The reason I chose ``Cards`` as the objects for this chapter is that
there is an obvious use for a vector of cards—a deck. Here is some code
that creates a new deck of 52 cards:

::

     vector<Card> deck (52);

Here is the state diagram for this object:

.. figure:: Images/12.6deck_state_diagram.png
   :scale: 60%
   :align: center
   :alt: image

The three dots represent the 48 cards I didn’t feel like drawing. Keep
in mind that we haven’t initialized the instance variables of the cards
yet. In some environments, they will get initialized to zero, as shown
in the figure, but in others they could contain any possible value.

One way to initialize them would be to pass a ``Card`` as a second
argument to the constructor:

::

     Card aceOfSpades (3, 1);
     vector<Card> deck (52, aceOfSpades);

This code builds a deck with 52 identical cards, like a special deck for
a magic trick. Of course, it makes more sense to build a deck with 52
different cards in it. To do that we use a nested loop.

The outer loop enumerates the suits, from 0 to 3. For each suit, the
inner loop enumerates the ranks, from 1 to 13. Since the outer loop
iterates 4 times, and the inner loop iterates 13 times, the total number
of times the body is executed is 52 (13 times 4).

::

     int i = 0;
     for (int suit = 0; suit <= 3; suit++) {
       for (int rank = 1; rank <= 13; rank++) {
         deck[i].suit = suit;
         deck[i].rank = rank;
         i++;
       }
     }

I used the variable ``i`` to keep track of where in the deck the next
card should go.

Notice that we can compose the syntax for selecting an element from an
array (the ``[]`` operator) with the syntax for selecting an instance
variable from an object (the dot operator). The expression
``deck[i].suit`` means “the suit of the ith card in the deck”.

This deck-building code is encapsulated in a function called
``buildDeck`` that takes no parameters and that returns a
fully-populated vector of ``Card``\ s. 

.. activecode:: 12_6
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   Take a look at the active code below, which includes the implementation of
   the ``buildDeck`` function. 
   ~~~~
   #include <iostream>
   #include <string>
   #include <vector>
   using namespace std;

   struct Card {
       int suit, rank;

       Card ();
       Card (int s, int r);
       void print () const;
   };

   vector<Card> buildDeck() {
       vector<Card> deck (52);
       int i = 0;
       for (int suit = 0; suit <= 3; suit++) {
           for (int rank = 1; rank <= 13; rank++) {
               deck[i].suit = suit;
               deck[i].rank = rank;
               i++;
           }
       }
       return deck;
   }

   int main() {
       vector<Card> deck = buildDeck();
       cout << "We just created our deck of 52 cards. We can access an individual card by indexing." << endl;
       cout << "For example, the first card in the deck is: "; 
       deck[0].print();
   }

   ====

   Card::Card () {
      suit = 0;  rank = 0;
   }

   Card::Card (int s, int r) {
      suit = s;  rank = r;
   }

   void Card::print () const {
      vector<string> suits (4);
      suits[0] = "Clubs";
      suits[1] = "Diamonds";
      suits[2] = "Hearts";
      suits[3] = "Spades";

      vector<string> ranks (14);
      ranks[1] = "Ace";
      ranks[2] = "2";
      ranks[3] = "3";
      ranks[4] = "4";
      ranks[5] = "5";
      ranks[6] = "6";
      ranks[7] = "7";
      ranks[8] = "8";
      ranks[9] = "9";
      ranks[10] = "10";
      ranks[11] = "Jack";
      ranks[12] = "Queen";
      ranks[13] = "King";

      cout << ranks[rank] << " of " << suits[suit] << endl;
   }

.. mchoice:: vector_of_cards_1
   :multiple_answers:
   :answer_a: There are 16 cards in the deck.
   :answer_b: The deck is single-suited.
   :answer_c: There are no face cards in the deck.
   :answer_d: The deck does not contain any Hearts.
   :answer_e: There are two Jacks in the deck.
   :correct: a,d,e
   :feedback_a: Correct! You can verify this by checking how many times the for loops execute.
   :feedback_b: Incorrect! Look at the conditions of the outer for loop, you'll find that there are two suits in this deck.
   :feedback_c: Incorrect! Look at the conditions of the inner for loop, you'll find that this deck contains face cards.
   :feedback_d: Correct! The two suits in this deck are Clubs and Diamonds.
   :feedback_e: Correct! The deck contains the Jack of Clubs and the Jack of Diamonds.

   Take a look at the code below. What can we say about the deck that is created?
   ::

     vector<Card> createDeck() {
        vector<Card> deck (16);
        int i = 0;
        for (int suit = 0; suit <= 1; suit++) {
           for (int rank = 4; rank <= 11; rank++) {
              deck[i].suit = suit;
              deck[i].rank = rank;
              i++;
           }
        }
        return deck;
     }

.. fillintheblank:: vector_of_cards_2

    If we actually created the deck in the previous question, what is printed after the following code runs?
    
    ::

     deck[11].print();
   
    Type your answer exactly as it would appear in the terminal!

    - :(7 of Diamonds): Correct!
      :.*: Incorrect, try modifying the activecode and writing a print statement!

