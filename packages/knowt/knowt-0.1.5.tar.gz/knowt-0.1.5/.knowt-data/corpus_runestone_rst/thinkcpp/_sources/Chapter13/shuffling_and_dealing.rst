Shuffling and dealing
---------------------

In :numref:`shuffling`, I wrote pseudocode for a shuffling
algorithm. Assuming that we have a function called ``shuffleDeck`` that
takes a deck as an argument and shuffles it, we can create and shuffle a
deck:

::

     Deck deck;               // create a standard 52-card deck
     deck.shuffleDeck ();     // shuffle it

Then, to deal out several hands, we can use ``subdeck``:

::

     Deck hand1 = deck.subdeck (0, 4);
     Deck hand2 = deck.subdeck (5, 9);
     Deck pack = deck.subdeck (10, 51);

This code puts the first 5 cards in one hand, the next 5 cards in the
other, and the rest into the pack.

When you thought about dealing, did you think we should give out one
card at a time to each player in the round-robin style that is common in
real card games? I thought about it, but then realized that it is
unnecessary for a computer program. The round-robin convention is
intended to mitigate imperfect shuffling and make it more difficult for
the dealer to cheat. Neither of these is an issue for a computer.

This example is a useful reminder of one of the dangers of engineering
metaphors: sometimes we impose restrictions on computers that are
unnecessary, or expect capabilities that are lacking, because we
unthinkingly extend a metaphor past its breaking point. Beware of
misleading analogies.

.. activecode:: shuffle_deal_AC_1
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   The active code below deals a deck of cards among three players for a game
   of Go Fish. Feel free to experiment with the code and deal decks for other 
   games like War, Poker, and Egyptian Ratscrew.
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

   int findBisect (Deck subdeck, Card card);

   int main() {
       Deck deck;
       deck.shuffleDeck();
       Deck hand1 = deck.subdeck(0, 6);
       Deck hand2 = deck.subdeck(7, 13);
       Deck hand3 = deck.subdeck(14, 20);
       Deck pack = deck.subdeck(21, 51);
       cout << "Player 1's hand:" << endl;
       hand1.print();
       cout << endl;
       cout << "Player 2's hand:" << endl;
       hand2.print();
       cout << endl;
       cout << "Player 3's hand:" << endl;
       hand3.print();
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

   Deck Deck::subdeck (int low, int high) const {
       Deck sub (high-low+1);

       for (size_t i = 0; i<sub.cards.size(); i++) {
           sub.cards[i] = cards[low+i];
       }
       return sub;
   }

   int findBisect (Deck subdeck, Card card) {
       if (subdeck.cards.size() == 1 && !subdeck.cards[0].equals(card)) return -1;
       int mid = subdeck.cards.size() / 2;
       if (subdeck.cards[mid].equals(card)) return mid;
       else if (subdeck.cards[mid].isGreater(card)) {
           return findBisect (subdeck.subdeck(0, mid - 1), card);
       }  
       else {
           return findBisect (subdeck.subdeck(mid + 1, subdeck.cards.size()), card);
       }
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
