The ``equals`` function
-----------------------

In order for two cards to be equal, they have to have the same rank and
the same suit. Unfortunately, the ``==`` operator does not work for
user-defined types like ``Card``, so we have to write a function that
compares two cards. We’ll call it ``equals``. It is also possible to
write a new definition for the ``==`` operator, but we will not cover
that in this book.

It is clear that the return value from ``equals`` should be a boolean
that indicates whether the cards are the same. It is also clear that
there have to be two ``Card``\ s as parameters. But we have one more
choice: should ``equals`` be a member function or a free-standing
function?

As a member function, it looks like this:

::

   bool Card::equals (const Card& c2) const {
     return (rank == c2.rank && suit == c2.suit);
   }

To use this function, we have to invoke it on one of the cards and pass
the other as an argument:

::

     Card card1 (1, 11);
     Card card2 (1, 11);

     if (card1.equals(card2)) {
       cout << "Yup, that's the same card." << endl;
     }

This method of invocation always seems strange to me when the function
is something like ``equals``, in which the two arguments are symmetric.
What I mean by symmetric is that it does not matter whether I ask “Is A
equal to B?” or “Is B equal to A?” In this case, I think it looks better
to rewrite ``equals`` as a nonmember function:

::

   bool equals (const Card& c1, const Card& c2) {
     return (c1.rank == c2.rank && c1.suit == c2.suit);
   }

When we call this version of the function, the arguments appear
side-by-side in a way that makes more logical sense, to me at least.

::

     if (equals (card1, card2)) {
       cout << "Yup, that's the same card." << endl;
     }

Of course, this is a matter of taste. My point here is that you should
be comfortable writing both member and nonmember functions, so that you
can choose the interface that works best depending on the circumstance.

.. activecode:: 12_4
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   Run the active code below to see how the ``equals()`` function works.
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
       bool equals (const Card& c2) const;
   };

   int main() {
       Card card1 (1,11);
       Card card2 (1,11);
       Card card3 (3,11);
       card1.equals(card2);
       card1.equals(card3);
   }

   ====

   Card::Card () {
     suit = 0;  rank = 0;
   }

   Card::Card (int s, int r) {
     suit = s;  rank = r;
   }

   bool Card::equals (const Card& c2) const {
     bool boolean = (rank == c2.rank && suit == c2.suit);
     if (boolean == true) {
       cout << "Yup, that's the same card." << endl;
     }
     else {
       cout << "Nope, those cards are different." << endl;
     }
     return boolean;
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

.. mchoice:: equals_function_1
   :answer_a: Directly, using the build in == operator.
   :answer_b: Compare their ranks and suits separately using the == operator. If either comparison is true, then they are equal.
   :answer_c: Compare their ranks and suits separately using the == operator. If either comparison is false, then they are NOT equal.
   :answer_d: They cannot be compared because they are non-numerical objects.
   :correct: c
   :feedback_a: Incorrect! We have to create our own method to compare two Card objects, the == operator won't work.
   :feedback_b: Incorrect! This would return true if two cards have the same rank, but different suits OR the same suit, but different ranks.
   :feedback_c: Correct! Both ranks and suits must be the same for two cards to be equal.
   :feedback_d: Incorrect! Card objects can be compared, but we must create our own method.

   How can we compare two ``Card`` objects?

.. mchoice:: equals_function_2

   Should we write the ``equals()`` function as a free-standing function, or as a member function of ``Card``?

   - A free-standing function, because we shouldn't "invoke" the function on just one ``Card``.

     - Incorrect! We can invoke the function on a ``Card``!

   - A member function, because the ``equals()`` operation is part of the ``Card`` data structure.

     -  Incorrect! The ``equals()`` operation is not necessarily part of the ``Card`` data structure.

   - Both are viable.

     + Correct! This is a matter of preference!


.. parsonsprob:: equals_function_3
   :numbered: left
   :adaptive:

   In a card game called Euchre, the highest ranked suit is called the trump suit.  The trump suit contains
   all of the cards of that suit, and the Jack of the other suit of the same color.  For example, if Hearts
   was trump, the trump suit would contain all Hearts, and the Jack of Diamonds.  Implement the is_trump()
   function that returns true of a Card is part of the trump suit.  Assume we have a helper function same_color()
   that returns the other suit of the same color.
   -----
   bool Card::is_trump (string trump_suit) {
   =====
    if (suit == trump_suit) {
     return true;
    }
   =====
    if (suit != trump_suit) {                         #paired
     return false;
    }
   =====
    else if (rank == "Jack" && suit == same_color()) {
     return true;
    }
   =====
    else if (rank == "Jack") {                         #paired
     return true;
    }
   =====
    else {
     return false;
    }
   =====
   }
   =====
   };                         #paired

   
