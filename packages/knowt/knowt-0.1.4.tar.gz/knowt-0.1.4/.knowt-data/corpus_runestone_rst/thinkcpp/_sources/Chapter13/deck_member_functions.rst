``Deck`` member functions
-------------------------

Now that we have a ``Deck`` object, it makes sense to put all the
functions that pertain to ``Deck``\ s in the ``Deck`` structure
definition. Looking at the functions we have written so far, one obvious
candidate is ``printDeck`` (:numref:`printdeck`).
Here’s how it looks, rewritten as a ``Deck`` member function:

::

   void Deck::print () const {
     for (size_t i = 0; i < cards.size(); i++) {
       cards[i].print ();
     }
   }

As usual, we can refer to the instance variables of the current object
without using dot notation.

.. activecode:: deck_members_AC_1
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   The active code below prints out the deck of cards like in the previous section. Notice we can just use ``deck.print ()``
   to print out the deck instead of writing a for loop in main.
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
      void print () const;
   };

   int main() {
       Deck deck;
       deck.print ();
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

   void Deck::print () const {
       for (size_t i = 0; i < cards.size(); i++) {
           cards[i].print ();
       }
   }

For some of the other functions, it is not obvious whether they should
be member functions of ``Card``, member functions of ``Deck``, or
nonmember functions that take ``Card``\ s and ``Deck``\ s as parameters.
For example, the version of ``find`` in the previous chapter takes a
``Card`` and a ``Deck`` as arguments, but you could reasonably make it a
member function of either type. As an exercise, rewrite ``find`` as a
``Deck`` member function that takes a ``Card`` as a parameter.

Writing ``find`` as a ``Card`` member function is a little tricky.
Here’s my version:

::

   int Card::find (const Deck& deck) const {
     for (size_t i = 0; i < deck.cards.size(); i++) {
       if (equals (deck.cards[i], *this)) return i;
     }
     return -1;
   }

The first trick is that we have to use the keyword ``this`` to refer to
the ``Card`` the function is invoked on.

The second trick is that C++ does not make it easy to write structure
definitions that refer to each other. The problem is that when the
compiler is reading the first structure definition, it doesn’t know
about the second one yet.

One solution is to declare ``Deck`` before ``Card`` and then define
``Deck`` afterwards:

::

   // declare that Deck is a structure, without defining it
   struct Deck;

   // that way we can refer to it in the definition of Card
   struct Card {
     int suit, rank;

     Card ();
     Card (int s, int r);

     void print () const;
     bool isGreater (const Card& c2) const;
     int find (const Deck& deck) const;
   };

   // and then later we provide the definition of Deck
   struct Deck {
     vector<Card> cards;

     Deck ();
     Deck (int n);
     void print () const;
     int find (const Card& card) const;
   };

.. _shuffle:

.. mchoice:: deck_members_1
   :multiple_answers:
   :answer_a: Use the keyword this.
   :answer_b: Define Deck before Card.
   :answer_c: Pass a Card parameter in the Card member function find.
   :answer_d: Declare Deck before Card and then define Deck afterwards.
   :correct: a,d
   :feedback_a: We use this to refer to the Card that the function is invoked on.
   :feedback_b: We don't have to define Deck before Card.
   :feedback_c: What do we pass as a parameter in find?
   :feedback_d: This is how we implemented our code!

   Multiple Response: What are some tricks we can use to write ``find`` as a ``Card`` member function?

.. parsonsprob:: deck_members_2
   :numbered: left
   :adaptive:

   Write find as a Deck member function that takes a Card as a parameter.
   -----
   int Deck::find (Card card) const {
   =====
   int find (Card) {                         #paired
   =====
      for (size_t i = 0; i &#60; cards.size(); i++) {
   =====
      for (size_t i = 0; i &#60; deck.cards.size(); i++) {                       #paired
   =====
         if (cards[i].equals(card)) {
            return i; 
         }
   =====
         if (equals (deck.cards[i], *this)) {                         #paired
            return i; 
         }
   =====
      }
      return -1;
   }

.. activecode:: deck_members_AC_2
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   The active code below uses the ``find`` function that we just wrote.
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
       bool equals (const Card& c2) const;
   };

   struct Deck {
       vector<Card> cards;
       Deck ();
       void print () const;
       int find (Card card) const;
   };

   int main() {
       Deck deck;
       Card card (CLUBS, ACE);
       Card card2 (DIAMONDS, ACE);
       // Should output 0 and 13
       cout << deck.find(card) << endl;
       cout << deck.find(card2) << endl;
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

   void Deck::print () const {
       for (size_t i = 0; i < cards.size(); i++) {
           cards[i].print ();
       }
   }

   int Deck::find (Card card) const {
       for (size_t i = 0; i &#60; cards.size(); i++) {
           if (cards[i].equals(card)) {
               return i; 
           }
       }
       return -1;
   }

   bool Card::equals (const Card& c2) const {
       return (rank == c2.rank && suit == c2.suit);
   }
