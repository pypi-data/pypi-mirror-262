The ``isGreater`` function
--------------------------

For basic types like ``int`` and ``double``, there are comparison
operators that compare values and determine when one is greater or less
than another. These operators (``<`` and ``>`` and the others) don’t
work for user-defined types. Just as we did for the ``==`` operator, we
will write a comparison function that plays the role of the ``>``
operator. Later, we will use this function to sort a deck of cards.

Some sets are totally ordered, which means that you can compare any two
elements and tell which is bigger. For example, the integers and the
floating-point numbers are totally ordered. Some sets are unordered,
which means that there is no meaningful way to say that one element is
bigger than another. For example, the fruits are unordered, which is why
we cannot compare apples and oranges. As another example, the ``bool``
type is unordered; we cannot say that ``true`` is greater than
``false``.

The set of playing cards is partially ordered, which means that
sometimes we can compare cards and sometimes not. For example, I know
that the 3 of Clubs is higher than the 2 of Clubs because it has higher
rank, and the 3 of Diamonds is higher than the 3 of Clubs because it has
higher suit. But which is better, the 3 of Clubs or the 2 of Diamonds?
One has a higher rank, but the other has a higher suit.

In order to make cards comparable, we have to decide which is more
important, rank or suit. To be honest, the choice is completely
arbitrary. For the sake of choosing, I will say that suit is more
important, because when you buy a new deck of cards, it comes sorted
with all the Clubs together, followed by all the Diamonds, and so on.

With that decided, we can write ``isGreater``. Again, the arguments (two
``Card``\ s) and the return type (boolean) are obvious, and again we
have to choose between a member function and a nonmember function. This
time, the arguments are not symmetric. It matters whether we want to
know “Is A greater than B?” or “Is B greater than A?” Therefore I think
it makes more sense to write ``isGreater`` as a member function:

::

   bool Card::isGreater (const Card& c2) const {
     // first check the suits
     if (suit > c2.suit) return true;
     if (suit < c2.suit) return false;

     // if the suits are equal, check the ranks
     if (rank > c2.rank) return true;
     if (rank < c2.rank) return false;

     // if the ranks are also equal, return false
     return false;
   }

Then when we invoke it, it is obvious from the syntax which of the two
possible questions we are asking:

::

     Card card1 (2, 10);
     Card card2 (2, 4);

     if (card1.isGreater (card2)) {
       card1.print ();
       cout << "is greater than" << endl;
       card2.print ();
     }

You can almost read it like English: “If card1 isGreater card2 ...” The
output of this program is

::

   10 of Hearts
   is greater than
   4 of Hearts

According to ``isGreater``, aces are less than deuces (2s). As an
exercise, fix it so that aces are ranked higher than Kings, as they are
in most card games.

.. activecode:: 12_5
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   Take a look at the active code below, which uses the ``isGreater`` function.
   Feel free to change the values of the cards.
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
       bool isGreater (const Card& c2) const;
   };

   int main() {
       Card card1 (2,10);
       Card card2 (2,4);
       if (card1.isGreater (card2)) {
           card1.print ();
           cout << "is greater than" << endl;
           card2.print ();
       }
       else {
           card2.print ();
           cout << "is greater than" << endl;
           card1.print ();
       }  
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

   bool Card::isGreater (const Card& c2) const {
     if (suit > c2.suit) return true;
     if (suit < c2.suit) return false;

     if (rank > c2.rank) return true;
     if (rank < c2.rank) return false;

     return false;
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

.. mchoice:: isGreater_function_1
   :multiple_answers:
   :answer_a: bool
   :answer_b: string
   :answer_c: int
   :answer_d: Animal
   :answer_e: Card
   :correct: b,c
   :feedback_a: Incorrect! We cannot say true is greater than false, or vice versa.
   :feedback_b: Correct! Strings are ordered lexiographically.
   :feedback_c: Correct! It is quite obvious how integers are ordered.
   :feedback_d: Incorrect! We cannot say that one animal is greater than another.
   :feedback_e: Incorrect! Cards are partially ordered.

   Select all **totally ordered** sets.

.. fillintheblank:: isGreater_function_2

    ::

     Card card1 (2,12);
     Card card2 (1,12);
     if (card1.isGreater (card2)) {
        card1.print ();
        cout << "is greater than" << endl;
        card2.print ();
     }
     else {
        card2.print ();
        cout << "is greater than" << endl;
        card1.print ();
     }

    If the above code is run, the terminal will print:
    "Queen of Hearts"
    |blank|
    "Queen of Diamonds"
    Type your answer exactly as it would appear in the terminal.

    - :(is greater than): Correct!
      :.*: Incorrect!  Try this input on the code above!