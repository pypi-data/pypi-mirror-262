Mergesort
---------

In :numref:`sorting`, we saw a simple sorting algorithm that
turns out not to be very efficient. In order to sort :math:`n` items, it
has to traverse the vector :math:`n` times, and each traversal takes an
amount of time that is proportional to :math:`n`. The total time,
therefore, is proportional to :math:`n^2`.

.. index::
   single: mergesort

In this section I will sketch a more efficient algorithm called
**mergesort**. To sort :math:`n` items, mergesort takes time
proportional to :math:`n \log n`. That may not seem impressive, but as
:math:`n` gets big, the difference between :math:`n^2` and
:math:`n \log n` can be enormous. Try out a few values of :math:`n` and
see.

The basic idea behind mergesort is this: if you have two subdecks, each
of which has been sorted, it is easy (and fast) to merge them into a
single, sorted deck. Try this out with a deck of cards:

#. Form two subdecks with about 10 cards each and sort them so that when
   they are face up the lowest cards are on top. Place both decks face
   up in front of you.

#. Compare the top card from each deck and choose the lower one. Flip it
   over and add it to the merged deck.

#. Repeat step two until one of the decks is empty. Then take the
   remaining cards and add them to the merged deck.

The result should be a single sorted deck. Here’s what this looks like
in pseudocode:

::

     Deck merge (const Deck& d1, const Deck& d2) {
       // create a new deck big enough for all the cards
       Deck result (d1.cards.size() + d2.cards.size());

       // use the index i to keep track of where we are in
       // the first deck, and the index j for the second deck
       int i = 0;
       int j = 0;

       // the index k traverses the result deck
       for (size_t k = 0; k<result.cards.size(); k++) {

         // if d1 is empty, d2 wins; if d2 is empty, d1 wins;
         // otherwise, compare the two cards

         // add the winner to the new deck
       }
       return result;
     }

I chose to make ``merge`` a nonmember function because the two arguments
are symmetric.

The best way to test ``merge`` is to build and shuffle a deck, use
subdeck to form two (small) hands, and then use the sort routine from
the previous chapter to sort the two halves. Then you can pass the two
halves to ``merge`` to see if it works.

If you can get that working, try a simple implementation of
``mergeSort``:

::

   Deck Deck::mergeSort () const {
     // find the midpoint of the deck
     // divide the deck into two subdecks
     // sort the subdecks using sort
     // merge the two halves and return the result
   }

Notice that the current object is declared ``const`` because
``mergeSort`` does not modify it. Instead, it creates and returns a new
``Deck`` object.

If you get that version working, the real fun begins! The magical thing
about mergesort is that it is recursive. At the point where you sort the
subdecks, why should you invoke the old, slow version of ``sort``? Why
not invoke the spiffy new ``mergeSort`` you are in the process of
writing?

Not only is that a good idea, it is *necessary* in order to achieve the
performance advantage I promised. In order to make it work, though, you
have to add a base case so that it doesn’t recurse forever. A simple
base case is a subdeck with 0 or 1 cards. If ``mergesort`` receives such
a small subdeck, it can return it unmodified, since it is already
sorted.

The recursive version of ``mergesort`` should look something like this:

::

   Deck Deck::mergeSort (Deck deck) const {
     // if the deck is 0 or 1 cards, return it

     // find the midpoint of the deck
     // divide the deck into two subdecks
     // sort the subdecks using mergesort
     // merge the two halves and return the result
   }

As usual, there are two ways to think about recursive programs: you can
think through the entire flow of execution, or you can make the “leap of
faith.” I have deliberately constructed this example to encourage you to
make the leap of faith.

When you were using ``sort`` to sort the subdecks, you didn’t feel
compelled to follow the flow of execution, right? You just assumed that
the ``sort`` function would work because you already debugged it. Well,
all you did to make ``mergeSort`` recursive was replace one sort
algorithm with another. There is no reason to read the program
differently.

Well, actually you have to give some thought to getting the base case
right and making sure that you reach it eventually, but other than that,
writing the recursive version should be no problem. Good luck!


.. mchoice:: mergesort_1
   :answer_a: n, nlogn, more efficient
   :answer_b: n^2, nlogn, more efficient
   :answer_c: nlogn, n, less efficient
   :answer_d: nlogn, n^2, less efficient
   :answer_e: n^2, nlogn, less efficient
   :correct: b
   :feedback_a: Simple sort traverses the vector n times, and each traversal takes additional time.
   :feedback_b: Simple sort takes time proporitonal to n^2, mergesort takes time proportional to nlogn (which is more efficient).
   :feedback_c: You might be confused about which algorithm is which.  Also, what is the efficiency of simple sort?
   :feedback_d: You might be confused about which algorithm is which.
   :feedback_e: Which algorithm is more efficient? (Which function grows more slowly?)

   The efficiency of a simple sorting algorithm is __________.  The
   efficiency of mergesort is __________.  Mergesort is __________ than
   the simple sorting algorithm.


.. activecode:: mergesort_2
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   Write your implementation of ``merge`` in the commented area of the active 
   code below. Read the comments in ``main`` to see how we'll test if your
   ``merge`` function works. If you get stuck, you can reveal the extra problem
   at the end for help. 
   ~~~~
   #include <iostream>
   #include <string>
   #include <vector>
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

   Deck merge (const Deck& d1, const Deck& d2) {
       // ``merge`` should merge d1 with d2 and return
       // a merged deck. Follow the pseudocode above,
       // delete the existing code, and write your 
       // implementation here.
       Deck deck(0); return deck;
   }

   int main() {
       Deck deck;

       // Shuffle a deck of cards and split it in half
       deck.shuffleDeck();
       Deck d1 = deck.subdeck(0, 25);
       Deck d2 = deck.subdeck(26, 51);

       // Sort each half
       d1.sortDeck();
       d2.sortDeck();
       cout << "Sorted first half:" << endl;
       d1.print();
       cout << endl;
       cout << "Sorted second half:" << endl;
       d2.print();
       cout << endl;

       // Merge sorted decks together
       Deck finished = merge(d1, d2);
     
       // We should see a sorted standard deck of 52 cards
       cout << "Merged sorted full deck:" << endl;
       finished.print();
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

.. reveal:: mergesort_reveal_1
   :showtitle: merge Help
   :hidetitle: Hide Problem

   .. parsonsprob:: mergesort_help_1
      :numbered: left
      :adaptive:

      First, let's write the code for the merge function. merge should 
      take two decks as parameters and return a deck with the deck merged.
      -----
      Deck merge (const Deck& d1, const Deck& d2) {
      =====
      void merge (const Deck& d1, const Deck& d2) {                         #paired
      =====
       Deck result (d1.cards.size() + d2.cards.size());
      =====
       size_t i = 0;
       size_t j = 0;
      =====
       for (size_t k = 0; k < result.cards.size(); ++k) {
      =====
        if (d1.cards.empty()) {
         result.cards[k] = d2.cards[j];
         ++j;
        }
      =====
        if (d1.cards.empty()) {
         result.cards[k] = d1.cards[i];                         #paired
         ++i;
        }
      =====
        else if (d2.cards.empty()) {
         result.cards[k] = d1.cards[i];
         ++i;
        }
      =====
        else if (d1.cards.empty()) {
         result.cards[k] = d2.cards[j];                         #paired
         ++j;
        }
      =====
        else {
      =====
         if (j >= d2.cards.size()) {
          result.cards[k] = d1.cards[i];
          ++i;
         }
      =====
         else if (i >= d1.cards.size() || d1.cards[i].isGreater(d2.cards[j])) {
          result.cards[k] = d2.cards[j];
          ++j;
         }
      =====
         else {
          result.cards[k] = d1.cards[i];
          ++i;
         }
        }
      =====
       }
       return result;
      }

.. activecode:: mergesort_3 
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   Now that we've written ``merge``, it's time to write the ``mergeSort`` function. Try writing
   the non-recursive version of ``mergeSort`` first before writing the recursive version. Follow the
   comments in ``main`` to test your functions. If done correctly, the program should output a sorted
   deck of cards. If you get stuck, you can reveal the extra problems at the end for help.
   ~~~~
   #include <iostream>
   #include <string>
   #include <vector>
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
       Deck mergeSort () const;
       Deck mergeSort (Deck deck) const;
   };

   int findBisect (Deck subdeck, Card card);
   Deck merge (const Deck& d1, const Deck& d2);

   Deck Deck::mergeSort () const {
       // This version of ``mergeSort`` is the non-recursive version.
       // Follow the pseudocode above delete the existing code, 
       // and write your implementation here.
       Deck deck(0); return deck;
   }
   
   Deck Deck::mergeSort (Deck deck) const {
       // This version of ``mergeSort`` is the recursive version.
       // Follow the pseudocode above delete the existing code, 
       // and write your implementation here.
       Deck deck1(0); return deck;
   }

   int main() {
       Deck deck1;
       deck1.shuffleDeck();
       Deck sorted1 = deck1.mergeSort();
       sorted1.print();

       // Once you get the above code to work, comment it
       // out and uncomment the code below to test the 
       // recursive version of ``mergeSort``.

       /*
       Deck deck2;
       deck2.shuffleDeck();
       Deck sorted2 = deck2.mergeSort(deck2);
       sorted2.print();
       */
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

   Deck merge (const Deck& d1, const Deck& d2) {
       Deck result (d1.cards.size() + d2.cards.size());
       size_t i = 0;
       size_t j = 0;
       for (size_t k = 0; k < result.cards.size(); ++k) {
           if (d1.cards.empty()) {
               result.cards[k] = d2.cards[j];
               ++j;
           }
           else if (d2.cards.empty()) {
               result.cards[k] = d1.cards[i];
               ++i;
           }
           else {
               if (j >= d2.cards.size()) {
                   result.cards[k] = d1.cards[i];
                   ++i;
               }
               else if (i >= d1.cards.size() || d1.cards[i].isGreater(d2.cards[j])) {
                   result.cards[k] = d2.cards[j];
                   ++j;
               }
               else {
                   result.cards[k] = d1.cards[i];
                   ++i;
               }
           }
       }
       return result;
   }

.. reveal:: mergesort_reveal_2
   :showtitle: mergeSort Help
   :hidetitle: Hide Problem

   .. parsonsprob:: mergesort_help_2
      :numbered: left
      :adaptive:

      Let's write the code for the mergeSort function. mergeSort 
      should be a Deck member function that returns a sorted deck.
      -----
      Deck Deck::mergeSort () const {
      =====
      Deck mergeSort () {                         #paired
      =====
       int mid = cards.size() / 2;
      =====
       Deck d1 = subdeck(0, mid - 1);
       Deck d2 = subdeck(mid, cards.size() - 1); 
      =====
       d1.sortDeck();
       d2.sortDeck();
      =====
       return merge(d1, d2);
      }

.. reveal:: mergesort_reveal_3
   :showtitle: mergeSort Recursion Help
   :hidetitle: Hide Problem

   .. parsonsprob:: mergesort_help_3
      :numbered: left
      :adaptive:

      Let's take it one step further and rewrite ``mergeSort`` as a
      recursive function.
      -----
      Deck Deck::mergeSort (Deck deck) const {
      =====
       if (deck.cards.size() == 0 || deck.cards.size() == 1) {
        return deck;
       }
      =====
       int mid = deck.cards.size() / 2;
      =====
       Deck d1 = subdeck(0, mid - 1);
       Deck d2 = subdeck(mid, deck.cards.size() - 1); 
      =====
       Deck merged1 = d1.mergeSort(d1);
       Deck merged2 = d2.mergeSort(d2);
      =====
       return merge(merged1, merged2);
      }
