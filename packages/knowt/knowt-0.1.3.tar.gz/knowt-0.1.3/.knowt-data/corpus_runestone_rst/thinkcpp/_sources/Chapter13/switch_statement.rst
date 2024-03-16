``switch`` statement
--------------------

.. index::
   single: switch

It’s hard to mention enumerated types without mentioning ``switch``
statements, because they often go hand in hand. A ``switch`` statement
is an alternative to a chained conditional that is syntactically
prettier and often more efficient. It looks like this:

::

     switch (symbol) {
     case '+':
       perform_addition ();
       break;
     case '*':
       perform_multiplication ();
       break;
     default:
       cout << "I only know how to perform addition and multiplication" << endl;
       break;
     }

This ``switch`` statement is equivalent to the following chained
conditional:

::

     if (symbol == '+') {
       perform_addition ();
     } 
     else if (symbol == '*') {
       perform_multiplication ();
     } 
     else {
       cout << "I only know how to perform addition and multiplication" << endl;
     }

The ``break`` statements are necessary in each branch in a ``switch``
statement because otherwise the flow of execution “falls through” to the
next case. 

.. note::
   Be sure to incorporate a ``break`` statment into each branch so
   that the flow of execution stops after that branch.

Without the ``break`` statements, the symbol ``+`` would make the program 
perform addition, and then perform multiplication, and then print the 
error message. Occasionally this feature is useful, but most of the time 
it is a source of errors when people forget the ``break`` statements.

.. activecode:: switch_AC_1
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   Take a look at the active code below that allows you to choose your starter Pokemon.
   If you change the value of ``type``, it will change the Pokemon you choose. Notice how 
   if you don't assign ``type`` to a valid type, it outputs the default message. Try taking out
   the ``break`` statements in each case. What happens if you run the code with ``type`` as 'g' afterwards?
   ~~~~
   #include <iostream>
   #include <string>
   using namespace std;

   int main() {
       char type = 'w';

       switch (type) {
       case 'g':
           cout << "You've chosen Bulbasaur!" << endl;
           break;
       case 'f':
           cout << "You've chosen Charmander!" << endl;
           break;
       case 'w':
           cout << "You've chosen Squirtle!" << endl;
          break;
       default:
           cout << "Invalid type! Please try again." << endl;
           break;
       }
   }

``switch`` statements work with integers, characters, and enumerated
types. For example, to convert a ``Suit`` to the corresponding string,
we could use something like:

::

     switch (suit) {
     case CLUBS:     return "Clubs";
     case DIAMONDS:  return "Diamonds";
     case HEARTS:    return "Hearts";
     case SPADES:    return "Spades";
     default:        return "Not a valid suit";
     }

In this case we don’t need ``break`` statements because the ``return``
statements cause the flow of execution to return to the caller instead
of falling through to the next case.

In general it is good style to include a ``default`` case in every
``switch`` statement, to handle errors or unexpected values.

.. _deck:

.. fillintheblank:: switch_1

    A(n) |blank| statement is necessary for each branch in a ``switch`` statement.

    - :[Bb][Rr][Ee][Aa][Kk]: A return would also suffice.
      :.*: Try again! How do we prevent the flow of execution from "falling through?"

.. mchoice:: switch_2
   :answer_a: ints
   :answer_b: chars
   :answer_c: strings
   :answer_d: enumerated types
   :correct: c
   :feedback_a: We can use ints with switch statements.
   :feedback_b: We can use chars with switch statements.
   :feedback_c: Switch statements only work on integral values, so we cannot use strings with switch statements!
   :feedback_d: We can use enumerated types with switch statements.

   Which one of the following types do NOT work with ``switch`` statement?

.. mchoice:: switch_3
   :answer_a: 4
   :answer_b: 49
   :answer_c: 49Invalid num! Please try again.
   :answer_d: Invalid num! Please try again.
   :answer_e: Code will not run.
   :correct: b
   :feedback_a: Incorrect! Try running it with the active code.
   :feedback_b: Case 2 doesn't end with a break statement, so case 3 also runs!
   :feedback_c: Where do we encounter a break statement?
   :feedback_d: Is 2 one of the invalid numbers?
   :feedback_e: There is no reason why the code wouldn't run.

   What is the correct output of the code below?

   .. code-block:: cpp

      int main() {
        int num = 2;

        switch (num) {
        case 1:
          cout << 1;
          break;
        case 2:
          cout << 4;
        case 3:
          cout << 9;
          break;
        default:
          cout << "Invalid num! Please try again.";
          break;
        }
      }


.. mchoice:: switch_4
   :answer_a: 1
   :answer_b: 149
   :answer_c: 149Invalid num! Please try again.
   :answer_d: Invalid num! Please try again.
   :answer_e: Code will not run.
   :correct: a
   :feedback_a: The first statement ends with a break, so only 1 will print!
   :feedback_b: Where do we encounter a break statement?
   :feedback_c: Is 1 one of the valid numbers?  Where do we encounter a break statement?
   :feedback_d: Is 1 one of the invalid numbers?
   :feedback_e: There is no reason why the code wouldn't run.

   What is the correct output **this time**?

   .. code-block:: cpp

      int main() {
        int num = 1;

        switch (num) {
        case 1:
          cout << 1;
          break;
        case 2:
          cout << 4;
        case 3:
          cout << 9;
        default:
          cout << "Invalid num! Please try again.";
        }
      }


.. mchoice:: switch_5
   :answer_a: 4
   :answer_b: 49
   :answer_c: 49Invalid num! Please try again.
   :answer_d: Invalid num! Please try again.
   :answer_e: Code will not run.
   :correct: c
   :feedback_a: Where do we / don't we encounter a break statement?
   :feedback_b: Where do we / don't we encounter a break statement?
   :feedback_c: Notice that 2 is not an invalid number, but since we are missing break statements, multiple branches execute.
   :feedback_d: Is 2 one of the invalid numbers?
   :feedback_e: There is no reason why the code wouldn't run.

   And finally, what about **this time**?

   .. code-block:: cpp

      int main() {
        int num = 2;

        switch (num) {
        case 1:
          cout << 1;
          break;
        case 2:
          cout << 4;
        case 3:
          cout << 9;
        default:
          cout << "Invalid num! Please try again.";
        }
      }
