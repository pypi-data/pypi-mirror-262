Chained Conditionals
--------------------

.. index::
   single: chaining
   single: chained conditionals

Sometimes you want to check for a number of related conditions and
choose one of several actions. One way to do this is by **chaining** a
series of ifs and elses:

.. activecode:: chained_conditionals_AC_1
   :language: cpp
   :caption: Classifying a Number as +, -, or 0.

   The following program classifies a number (x) as positive,
   negative, or zero.  Feel free to change the value of x to 
   make sure it works.
   ~~~~
   #include <iostream>
   using namespace std;

   int main () {
       int x = -4;
       if (x > 0) {
           cout << "x is positive" << endl;
       }
       else if (x < 0) {
           cout << "x is negative" << endl;
       }
       else {
           cout << "x is zero" << endl;
       }
       return 0;
   }

Try changing the value of x above to see how the output is impacted.

.. note::
   If you have a chain of ``if`` statements, the program will go through 
   executing each conditional, regardless if the conditions are met.  
   However, as soon as you add an ``else`` or even an ``else if`` statement,
   the program will stop executing the chained conditionals as soon as a 
   condition is met.


These chains can be as long as you want, although they can be difficult
to read if they get out of hand. One way to make them easier to read is
to use standard indentation, as demonstrated in these examples. If you
keep all the statements and squiggly-braces lined up, you are less
likely to make syntax errors and you can find them more quickly if you
do.


.. mchoice:: chained_conditionals_1
   :answer_a: Three!
   :answer_b: One!
   :answer_c: One! Two!
   :answer_d: One! Two! Three!
   :correct: d
   :feedback_a: Make note of the use of "if" instead of "else if" or "else".
   :feedback_b: Make note of the use of "if" instead of "else if" or "else".
   :feedback_c: Make note of the use of "if" instead of "else if" or "else".
   :feedback_d: When we have "if" statments, but no "else if" or "else", every condition will be checked.

   What will print after the following code is executed?

   ::

       #include <iostream>
       using namespace std;

       int main () {
         int x = 10;
         if (x > 8) {
           cout << "One! ";
         }
         if (x > 6) {
           cout << "Two! ";
         }
         if (x > 3) {
           cout << "Three!" << endl;
         }
         return 0;
       }


.. mchoice:: chained_conditionals_2
   :answer_a: Three!
   :answer_b: One!
   :answer_c: One! Two!
   :answer_d: One! Two! Three!
   :correct: b
   :feedback_a: Remember that only one action will be completed in a chain of "ifs", "else ifs", and "ifs"
   :feedback_b: The chain of "ifs", "else ifs", and "elses" results in only one action being completed.
   :feedback_c: Remember that a chain of "ifs", "else ifs", and "elses" will result in only one action being completed.
   :feedback_d: Remember that a chain of "ifs", "else ifs", and "elses" will result in only one action being completed.
   
   What will print after the following code is executed?

   ::

       #include <iostream>
       using namespace std;

       int main () {
         int x = 10;
         if (x > 8) {
           cout << "One! " ;
         }
         else if (x > 6) {
           cout << "Two! ";
         }
         else {
           cout << "Three!" << endl;
         }
         return 0;
       }


.. mchoice:: chained_conditionals_3
   :answer_a: Two!
   :answer_b: Two! Three!
   :answer_c: One! Two!
   :answer_d: One! Two! Three!
   :correct: b
   :feedback_a: Make note of the use of "if" instead of "else if" or "else".
   :feedback_b: When we have "if" statments, but no "else if" or "else", every condition will be checked.
   :feedback_c: The first statement will not be executed because x > 8 is not true.  Also, make note of the use of "if" instead of "else if" or "else".
   :feedback_d: The first statement will not be executed because x > 8 is not true.

   What will print after the following code is executed?

   ::

       #include <iostream>
       using namespace std;

       int main () {
         int x = 7;
         if (x > 8) {
           cout << "One! " ;
         }
         if (x > 6) {
           cout << "Two! ";
         }
         if (x > 3) {
           cout << "Three!" << endl;
         }
         return 0;
       }


.. mchoice:: chained_conditionals_4
   :answer_a: Two!
   :answer_b: Two! Three!
   :answer_c: One! Two!
   :answer_d: One! Two! Three!
   :correct: a
   :feedback_a: Only one action will is completed in a chain of "ifs", "else ifs", and "ifs";
   :feedback_b: Remember that only one action will be completed in a chain of "ifs", "else ifs", and "ifs".
   :feedback_c: The first condition will not be satisfied.  Also, a chain of "ifs", "else ifs", and "elses" will result in only one action being completed.
   :feedback_d: hge first condition will not be satisfied.  Also, a chain of "ifs", "else ifs", and "elses" will result in only one action being completed.
   
   What will print after the following code is executed?

   ::

       #include <iostream>
       using namespace std;

       int main () {
         int x = 7;
         if (x > 8) {
           cout << "One! " ;
         }
         else if (x > 6) {
           cout << "Two! ";
         }
         else {
           cout << "Three!" << endl;
         }
         return 0;
       }