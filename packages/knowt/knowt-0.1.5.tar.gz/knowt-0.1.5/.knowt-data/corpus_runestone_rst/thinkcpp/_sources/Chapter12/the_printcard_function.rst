The ``printCard`` function
--------------------------

When you create a new type, the first step is usually to declare the
instance variables and write constructors. The second step is often to
write a function that prints the object in human-readable form.

In the case of ``Card`` objects, “human-readable” means that we have to
map the internal representation of the rank and suit onto words. A
natural way to do that is with a vector of ``string``\ s. You can
create a vector of ``string``\ s the same way you create an vector of
other types:

::

     vector<string> suits (4);

Of course, in order to use ``vector``\ s and ``string``\ s, you will
have to include the header files for both.

To initialize the elements of the vector, we can use a series of
assignment statements.

::

     suits[0] = "Clubs";
     suits[1] = "Diamonds";
     suits[2] = "Hearts";
     suits[3] = "Spades";

A state diagram for this vector looks like this:

We can build a similar vector to decode the ranks. Then we can select
the appropriate elements using the ``suit`` and ``rank`` as indices.
Finally, we can write a function called ``print`` that outputs the card
on which it is invoked:

::

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

The expression ``suits[suit]`` means “use the instance variable ``suit``
from the current object as an index into the vector named ``suits``, and
select the appropriate string.”

Because ``print`` is a ``Card`` member function, it can refer to the
instance variables of the current object implicitly (without having to
use dot notation to specify the object). The output of this code

::

     Card card (1, 11);
     card.print ();

is ``Jack of Diamonds``.

.. activecode:: 12_3
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   The active code below uses the ``Card::print()`` function.  Feel free to modify 
   the values that ``card`` is being initialized to in the constructor:  this will 
   change the output from the ``Card::print()`` function.
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

   int main() {
       Card card (1,11);
       card.print ();
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

You might notice that we are not using the zeroeth element of the
``ranks`` vector. That’s because the only valid ranks are 1–13. By
leaving an unused element at the beginning of the vector, we get an
encoding where 2 maps to “2”, 3 maps to “3”, etc. From the point of view
of the user, it doesn’t matter what the encoding is, since all input and
output uses human-readable formats. On the other hand, it is often
helpful for the programmer if the mappings are easy to remember.

.. mchoice:: printCard_function_1
   :answer_a: rank.ranks
   :answer_b: ranks.rank
   :answer_c: ranks[rank]
   :answer_d: rank[ranks]
   :correct: c
   :feedback_a: Incorrect! Remember, ranks is a vector!
   :feedback_b: Incorrect! Remember, ranks is a vector!
   :feedback_c: Correct! This is an example of how we use mapping!
   :feedback_d: Incorrect! This is using the vector "ranks" as an index to a single "rank".

   How would we select the appropriate string for the instance variable ``rank``?

.. fillintheblank:: printCard_function_2

    ::

     Card card (3, 1);
     card.print ();

    What is printed by card.print()? Type your answer exactly as it would appear in the terminal.

    - :(Ace of Spades): Correct!
      :.*: Incorrect!  Try this input on the code above!

.. mchoice:: printCard_function_3
   :multiple_answers:
   :answer_a: Yes, because the mappings should be easy for the programmer to remember.
   :answer_b: Yes, because the mappings should be easy for the user to remember.
   :answer_c: No! All input and output uses human-readable formats, so the programmer doesn't need to understand what is going on behind the scenes.
   :answer_d: No! All input and output uses human-readable formats, so the user doesn't need to understand what is going on behind the scenes.
   :correct: a,d
   :feedback_a: Correct! The programmer should uses mappings that are easy to remember (even if this means we don't use the zeroeth element of the ranks vector).
   :feedback_b: Incorrect! The user doesn't need to know how things are mapped.
   :feedback_c: Incorrect! The programmer should always know what is going on with their code.
   :feedback_d: Correct! The user doesn't need to know how the programmer coded things.

   Does it matter how we encode a mapping?