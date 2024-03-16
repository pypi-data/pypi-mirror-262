.. _find:

Searching
---------

The next function I want to write is ``find``, which searches through a
vector of ``Card``\ s to see whether it contains a certain card. It may
not be obvious why this function would be useful, but it gives me a
chance to demonstrate two ways to go searching for things, a ``linear``
search and a ``bisection`` search.

Linear search is the more obvious of the two; it involves traversing the
deck and comparing each card to the one we are looking for. If we find
it we return the index where the card appears. If it is not in the deck,
we return -1.

::

   int find (const Card& card, const vector<Card>& deck) {
     for (size_t i = 0; i < deck.size(); i++) {
       if (equals (deck[i], card)) return i;
     }
     return -1;
   }

The loop here is exactly the same as the loop in ``printDeck``. In fact,
when I wrote the program, I copied it, which saved me from having to
write and debug it twice.

Inside the loop, we compare each element of the deck to ``card``. The
function returns as soon as it discovers the card, which means that we
do not have to traverse the entire deck if we find the card we are
looking for. If the loop terminates without finding the card, we know
the card is not in the deck and return ``-1``.

To test this function, I wrote the following:

::

     vector<Card> deck = buildDeck ();

     int index = card.find (deck[17]);
     cout << "I found the card at index = " << index << endl;

The output of this code is

::

   I found the card at index = 17

.. activecode:: 12_8
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   The code below searches for a particular card in a standard deck of 52 cards.
   It returns the index that the card was located at.
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

   vector<Card> buildDeck();
   
   bool equals (const Card& c1, const Card& c2){
       return (c1.rank == c2.rank && c1.suit == c2.suit);
   }

   void printDeck(const vector<Card>& deck);

   int find (const Card& card, const vector<Card>& deck);

   int main() {
       vector<Card> deck = buildDeck();
       Card card (3, 6);
       cout << find(card, deck);
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

   int find (const Card& card, const vector<Card>& deck) {
      for (size_t i = 0; i < deck.size(); i++) {
       if (equals (deck[i], card)) return i;
      }
      return -1;
   }

.. fillintheblank:: searching_1

   Say we have standard deck of cards. According to our ``find()`` function, the 
   for loop will execute a minimum of |blank| times, and a maximum of |blank|
   times while searching for a particular card.

   - :1: Correct!
     :x: Incorrect! What if the card we were searching for was the first one in the deck?
   - :52: Correct!
     :.*: Incorrect! What if the card we were searching for wasn't in the deck? In this case, we'd have looped through all of the cards!

.. fillintheblank:: searching_2

   ``buildEuchreDeck()`` returns the deck of Euchre cards defined on the previous page.
   If we run the following code, what is returned?

   ::
     
     int main() {
        EuchreDeck = buildEuchreDeck();
        Card card (3, 6);
        find(card, EuchreDeck);
      }
    
   |blank|.

   - :-1: Correct! The find method should return -1 if the card is not part of the deck.
     :x: Incorrect! Hint: take a look at the suit and rank of card.