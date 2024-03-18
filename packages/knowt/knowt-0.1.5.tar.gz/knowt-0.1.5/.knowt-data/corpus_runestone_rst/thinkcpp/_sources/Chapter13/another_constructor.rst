Another constructor
-------------------

Now that we have a ``Deck`` object, it would be useful to initialize the
cards in it. From the previous chapter we have a function called
``buildDeck`` that we could use (with a few adaptations), but it might
be more natural to write a second ``Deck`` constructor.

::

   Deck::Deck () {
     vector<Card> temp (52);
     cards = temp;

     int i = 0;
     for (Suit suit = CLUBS; suit <= SPADES; suit = Suit(suit+1)) {
       for (Rank rank = ACE; rank <= KING; rank = Rank(rank+1)) {
         cards[i].suit = suit;
         cards[i].rank = rank;
         i++;
       }
     }
   }

Notice how similar this function is to ``buildDeck``, except that we had
to change the syntax to make it a constructor. Now we can create a
standard 52-card deck with the simple declaration ``Deck deck;``

.. activecode:: deck_constructor_AC_1
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   The active code below prints out the cards in a deck using the loop from the previous section.
   ~~~~
   #include <iostream>
   #include <string>
   #include <vector>
   using namespace std;

   enum Suit { CLUBS, DIAMONDS, HEARTS, SPADES };

   enum Rank { ACE=1, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE,
   TEN, JACK, QUEEN, KING };

   struct Card {
       Rank rank;
       Suit suit;
       Card ();
       Card (Suit s, Rank r);
       void print () const;
   };

   struct Deck {
       vector<Card> cards;
       Deck ();
   };

   int main() {
       Deck deck;
       for (int i = 0; i < 52; i++) {
           deck.cards[i].print();
       }
   }

   ====
   Card::Card () {
       suit = SPADES;  rank = ACE;
   }

   Card::Card (Suit s, Rank r) {
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

   Deck::Deck () {
       vector<Card> temp (52);
       cards = temp;

       int i = 0;
       for (Suit suit = CLUBS; suit <= SPADES; suit = Suit(suit+1)) {
           for (Rank rank = ACE; rank <= KING; rank = Rank(rank+1)) {
               cards[i].suit = suit;
               cards[i].rank = rank;
               i++;
           }
       }
   }

.. mchoice:: deck_constructor_1
   :answer_a: True - we used the buildDeck function with a few modifications to do this.
   :answer_b: True - we wrote a Deck constructor to do this.
   :answer_c: False - we used the buildDeck function with a few modifications to do this.
   :answer_d: False - we wrote a Deck constructor to do this.
   :correct: b
   :feedback_a: How do we create the deck?
   :feedback_b: The for loops in the Deck constructor initialize each card to its proper value.
   :feedback_c: Look at the active code.  How do we create the deck?
   :feedback_d: Look at the active code.

   Based on your observations from the active code above, the cards in ``deck`` are initialized 
   to the correct suits and ranks of a standard deck of 52 cards.

.. parsonsprob:: deck_constructor_2
      :numbered: left
      :adaptive:

      Let's write a constructor for a deck of cards that uses 40 cards.
      This deck uses all 4 suits and ranks Ace through 10, omitting all
      face cards.
      -----
      Deck::Deck () {
      =====
         vector<Card> temp (40);
      =====
         vector<Card> temp (52);                         #paired
      =====
         cards = temp;
         int i = 0;
      =====
         for (Suit suit = CLUBS; suit <= SPADES; suit = Suit(suit+1)) {
      =====
         for (Suit suit = CLUBS; suit < SPADES; suit = Suit(suit+1)) {                         #paired
      =====
            for (Rank rank = ACE; rank <= TEN; rank = Rank(rank+1)) {
      =====
            for (Rank rank = ACE; rank <= KING; rank = Rank(rank+1)) {                         #paired
      =====
              cards[i].suit = suit;
              cards[i].rank = rank;
      =====
              cards[i].suit = rank;
              cards[i].rank = suit;                         #paired
      =====
              i++;
            }
         }
      }