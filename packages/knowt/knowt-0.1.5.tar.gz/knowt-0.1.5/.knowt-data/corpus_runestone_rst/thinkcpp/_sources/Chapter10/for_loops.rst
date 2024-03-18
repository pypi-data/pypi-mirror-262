``for`` loops
-------------

The loops we have written so far have a number of elements in common.
All of them start by initializing a variable; they have a test, or
condition, that depends on that variable; and inside the loop they do
something to that variable, like increment it.

.. index::
   single: for loop

This type of loop is so common that there is an alternate loop
statement, called ``for``, that expresses it more concisely. The general
syntax looks like this:

::

     for (INITIALIZER; CONDITION; INCREMENTOR) {
       BODY
     }

This statement is exactly equivalent to

::

     INITIALIZER;
     while (CONDITION) {
       BODY
       INCREMENTOR
     }

except that it is more concise and, since it puts all the loop-related
statements in one place, it is easier to read. For example:

::

     int i;
     for (i = 0; i < 4; i++) {
       cout << count[i] << endl;
     }

is equivalent to

::

     int i = 0;
     while (i < 4) {
       cout << count[i] << endl;
       i++;
     }

.. activecode:: for_loops_AC_1
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   Run the active code below, which uses a ``for`` loop.
   ~~~~
   #include <iostream>
   #include <vector>
   using namespace std;

   int main() {
       vector<int> count = {1,2,3,4};
       int i;
       for (i = 0; i < 4; i++) {
           cout << count[i] << endl;
       }
   }

.. activecode:: for_loops_AC_2
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   Run the active code below, which uses a ``while`` loop.
   ~~~~
   #include <iostream>
   #include <vector>
   using namespace std;

   int main() {
       vector<int> count = {1,2,3,4};
       int i = 0;
       while (i < 4) {
           cout << count[i] << endl;
           i++;
       }
   }

.. fillintheblank:: for_loops_1

    How many times would the following loop execute?  ``for (int i = 1; i < 4; i++)``

    - :3: Correct!
      :4: Incorrect! The loop does not execute when i = 4.
      :.*: Incorrect!

.. mchoice:: for_loops_2
   :answer_a: in the BODIES of both loops
   :answer_b: in the BODY of a for loop, and in the statement of a while loop
   :answer_c: in the statement of a for loop, and in the BODY of a while loop
   :answer_d: in the statements of both loops
   :correct: c
   :feedback_a: Incorrect!
   :feedback_b: Incorrect!
   :feedback_c: Correct!
   :feedback_d: Incorrect!

   Where are the incrementors in ``for`` loops and ``while``?

.. parsonsprob:: question10_4_3
   :numbered: left
   :adaptive:

   Construct the ``half_life()`` function that prints the first num half lives
   of the initial amount.
   -----
   void half_life(int initial_amount, int num) {
   =====
   int half_life(int initial_amount, int num) {                         #paired
   =====
      int new_amount = initial_amount;
   =====
      for (int i = 0; i &#60; num; i++) {
   =====
      for (int i = 0; i &#60;= num; i++) {                         #paired
   =====
         new_amount = new_amount / 2;
   =====
         new_amount / 2;                         #paired
   =====
         cout << new_amount << endl;
   =====
      return new_amount;                         #distractor
   =====
      }
   }

.. activecode:: for_loops_AC_3
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   Run the active code below, which uses a ``for`` loop with a negative change in the "INCREMENTOR".
   ~~~~
   #include <iostream>
   #include <vector>
   using namespace std;

   int main() {
       vector<int> count = {1,2,3,4};
       int i;
       for (i = 3; i > -1; i--){
          cout << count[i] << endl;
       }
   }
