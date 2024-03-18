.. _printdeck:

The ``printDeck`` function
--------------------------

Whenever you are working with vectors, it is convenient to have a
function that prints the contents of the vector. We have seen the
pattern for traversing a vector several times, so the following function
should be familiar:

::

   void printDeck (const vector<Card>& deck) {
     for (size_t i = 0; i < deck.size(); i++) {
       deck[i].print ();
     }
   }

By now it should come as no surprise that we can compose the syntax for
vector access with the syntax for invoking a function.

Since ``deck`` has type ``vector<Card>``, an element of ``deck`` has
type ``Card``. Therefore, it is legal to invoke ``print`` on
``deck[i]``.

.. activecode:: 12_7
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   A Euchre Deck contains 9's, 10's, Jacks, Queens, Kings, and Aces of all four suits.  
   Modify the ``buildDeck`` function below to create a Euchre deck. The ``printDeck``
   function will allow you to verify that you have done this correctly.
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

   void printDeck(const vector<Card>& deck);

   int main() {
       vector<Card> deck = buildDeck();
       printDeck(deck);
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

    void printDeck (const vector<Card>& deck) {
      for (size_t i = 0; i < deck.size(); i++) {
        deck[i].print ();
      }
    }

Hopefully you took some time to try and figure out the code yourself.  The solution
below is just one of several correct solutions for creating the Euchre deck:

::

  vector<Card> buildEuchreDeck() {
    vector<Card> deck (24);
    int i = 0;
    for (int suit = 0; suit <= 3; suit++) {
        for (int rank = 1; rank <= 13; rank++) {
          if (rank == 1 || rank >= 9){
            deck[i].suit = suit;
            deck[i].rank = rank;
            i++;
          }
        }
    }
    return deck;
  }
