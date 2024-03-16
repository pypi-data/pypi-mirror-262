Subdecks
--------

How should we represent a hand or some other subset of a full deck? One
easy choice is to make a ``Deck`` object that has fewer than 52 cards.

We might want a function, ``subdeck``, that takes a vector of cards and
a range of indices, and that returns a new vector of cards that contains
the specified subset of the deck:

::

   Deck Deck::subdeck (int low, int high) const {
     Deck sub (high - low + 1);

     for (size_t i = 0; i < sub.cards.size(); i++) {
       sub.cards[i] = cards[low + i];
     }
     return sub;
   }

To create the local variable named ``subdeck`` we are using the ``Deck``
constructor that takes the size of the deck as an argument and that does
not initialize the cards. The cards get initialized when they are copied
from the original deck.

The length of the subdeck is ``high - low + 1`` because both the low card
and high card are included. 

.. warning::
   This sort of computation can be confusing and can lead to “off-by-one” 
   errors. Drawing a picture is usually the best way to avoid them.

As an exercise, write a version of ``findBisect`` that takes a subdeck
as an argument, rather than a deck and an index range. Which version is
more error-prone? Which version do you think is more efficient?

.. activecode:: subdeck_cards_1
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   Try writing the ``findBisect`` function in the commented section
   of the active code below. If done correctly, the program should output that
   the Seven of Clubs is at index 6 and the King of Diamonds is at index -1. 
   If you get stuck, you can reveal the extra problem at the end for help. 
   ~~~~
   #include <iostream>
   #include <string>
   #include <vector>
   #include <cstdlib>
   using namespace std;

   enum Suit { CLUBS, DIAMONDS, HEARTS, SPADES };

   enum Rank { ACE=1, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE,
   TEN, JACK, QUEEN, KING };

   int randomInt (int low, int high);

   struct Card {
       Rank rank;
       Suit suit;
       Card ();
       Card (Suit s, Rank r);
       void print () const;
       bool isGreater (const Card& c2) const;
       bool equals (const Card& c2) const;
   };

   struct Deck {
       vector<Card> cards;
       Deck ();
       Deck (int n);
       void print () const;
       void swapCards (int index1, int index2);
       int findLowestCard (int index);
       void shuffleDeck ();
       void sortDeck ();
       Deck subdeck (int low, int high) const;
   };

   int findBisect (Deck subdeck, Card card) {
       // ``findBisect`` should search through the subdeck and 
       // return the location of card. If card is not found in 
       // subdeck, it should return -1.
       // Delete the return 0 and write your implementation here.
       return 0;
   }

   int main() {
       Deck deck;
       Deck clubs = deck.subdeck(0, 12);
       clubs.print();
       Card card1 (CLUBS, SEVEN);
       Card card2 (DIAMONDS, KING);
       cout << endl;
       cout << "The Seven of Clubs is at index " << findBisect (clubs, card1) << endl;
       cout << "The King of Diamonds is at index " << findBisect (clubs, card2) << endl;
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

   bool Card::isGreater (const Card& c2) const {
       if (suit > c2.suit) return true;
       if (suit < c2.suit) return false;
       if (rank > c2.rank) return true;
       if (rank < c2.rank) return false;
       return false;
   }

   bool Card::equals (const Card& c2) const {
       return (rank == c2.rank && suit == c2.suit);
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

   Deck::Deck (int size) {
        vector<Card> temp (size);
        cards = temp;
   }

   void Deck::print () const {
       for (size_t i = 0; i < cards.size(); i++) {
           cards[i].print ();
       }
   }

   int randomInt (int low, int high) {
       srand (time(NULL));
       int x = random ();
       int y = x % (high - low + 1) + low; 
       return y;
   }

   void Deck::swapCards (int index1, int index2) {
       Card temp = cards[index1];
       cards[index1] = cards[index2]; 
       cards[index2] = temp;
   }

   int Deck::findLowestCard (int index) {
       int min = index;
       for (size_t i = index; i < cards.size(); ++i) { 
           if (cards[min].isGreater(cards[i])) { 
               min = i;
           }
      }
      return min;
   }

   void Deck::shuffleDeck () {
       for (size_t i = 0; i < cards.size(); i++) {
           int x = randomInt (i, cards.size() - 1);
           swapCards (i, x);
       }
   }

   void Deck::sortDeck () {
       for (size_t i = 0; i < cards.size(); i++) {
           int x = findLowestCard (i);
           swapCards (i, x);
       }
   }

   Deck Deck::subdeck (int low, int high) const {
       Deck sub (high-low+1);

       for (size_t i = 0; i<sub.cards.size(); i++) {
           sub.cards[i] = cards[low+i];
       }
       return sub;
   }

.. reveal:: subdecks_reveal_1
   :showtitle: findBisect Help
   :hidetitle: Hide Problem

   .. parsonsprob:: subdecks_help_1
      :numbered: left
      :adaptive:

      Let's write the code for this version of the findBisect function. 
      findBisect should take a subdeck and a card as parameters and
      return the index of the card in the subdeck or -1 if it's not found.
      -----
      int findBisect (Deck subdeck, Card card) {
      =====
      int findBisect (Subdeck subdeck, Card card) {                         #paired
      =====
       if (subdeck.size() == 1 && !subdeck[0].equals(card)) return -1;
      =====
        int mid = subdeck.size() / 2;
      =====
        int mid = (high + low) / 2;                         #paired
      =====
       if (subdeck[mid].equals(card)) return mid;
      =====
       else if (subdeck[mid].isGreater(card)) {
        return findBisect (subdeck.subdeck(0, mid - 1), card);
       }  
      =====
       else if (subdeck[mid].isGreater(card)) {                         #paired
        return findBisect (subdeck.subdeck(mid + 1, subdeck.size()), card);
       } 
      =====
       else {
        return findBisect (subdeck.subdeck(mid + 1, subdeck.size()), card);
       }
      }