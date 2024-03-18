Programs with Multiple Functions
--------------------------------

.. index::
   single: order of execution
   single: flow of execution

When you look at a class definition that contains several functions, it
is tempting to read it from top to bottom, but that is likely to be
confusing, because that is not the **order of execution** of the
program.

.. note::
   The order of execution is not necessarily the order in which functions
   are defined!  For example, the last function that you write might be the 
   first one that you call in the ``main`` function.

Execution always begins at the first statement of ``main``, regardless of
where it is in the program** (often it is at the bottom). Statements are
executed one at a time, in order, until you reach a function call.
Function calls are like a detour in the flow of execution. Instead of
going to the next statement, you go to the first line of the called
function, execute all the statements there, and then come back and pick
up again where you left off.

That sounds simple enough, except that you have to remember that one
function can call another. Thus, while we are in the middle of ``main``, we
might have to go off and execute the statements in ``threeLine``. But while
we are executing ``threeLine``, we get interrupted three times to go off and
execute ``newLine``.

Fortunately, C++ is adept at keeping track of where it is, so each time
``newLine`` completes, the program picks up where it left off in ``threeLine``,
and eventually gets back to ``main`` so the program can terminate.


.. activecode:: multiple_functions_AC_1
   :language: cpp
   :caption: Multiply / Add Two

   This program calls the multiplyTwo and addTwo functions in the
   main.  See if you can follow the order of execution.
   ~~~~
   #include <iostream>
   using namespace std;

   void printTotal (int x) {
       cout << x << endl;
   }

   int multiplyTwo (int x) {
       int total = x * 2;
       printTotal(total);
       return total;
   }

   int addTwo (int x) {
       int total = x + 2;
       return total;
   }

   int main () {
       int num = 3;
       int newNum = multiplyTwo(num);
       int newerNum = addTwo(newNum);
       printTotal(newerNum);
       return 0;
   }


What’s the moral of this sordid tale? When you read a program, don’t
read from top to bottom. Instead, **follow the flow of execution**.


.. dragndrop:: multiple_fun_1
    :feedback: Try again!
    :match_1: multiplyTwo ||| executes second
    :match_2: printTotal ||| executes third
    :match_3: main ||| executes first
    :match_4: addTwo ||| executes last

    Match the function to the order it is executed in the program above.


.. mchoice:: multiple_fun_2

    Consider the following C++ code. Note that line numbers are included 
    on the left.

    .. code-block:: cpp
       :linenos:

       #include <iostream>
       using namespace std;

       void newLine () {
         cout << endl;
       }

       void threeLine () {
         newLine ();  newLine ();  newLine ();
       }

       int main () {
         cout << "First Line." << endl;
         threeLine ();
         cout << "Second Line." << endl;
         return 0;
       }

    Which of the following reflects the order in which these functions 
    are executed in C++?

    -   ``newLine, threeLine, main``

        -   Remember to follow the order of execution, which is not necessarily the order the program is written.

    -   ``newLine, threeLine, newLine, newLine, newLine, main``

        -   Remember to follow the order of execution, which is not necessarily the order the program is written.

    -   ``main, threeLine, newLine, newLine, newLine``

        +   Execution begins in the main, then functions are executed as they are called.
    
    -   ``main, threeLine``

        -   Note that ``newLine`` is called inside of ``threeLine``.

.. mchoice:: multiple_fun_3

    Consider the following C++ code.

    .. code-block:: cpp
       :linenos:

       #include <iostream>
       using namespace std;
       
       void yo () {
         cout << "yo, ";
       }
       
       void hello () {
         cout << "hello, ";
         yo(); yo();
       }

       void goodbye () {
         yo(); hello();
         cout << "goodbye,";
       }

       int main () {
         cout << "welcome, ";
         goodbye();
         return 0;
       }

    What is printed when the code is executed?

    -   "welcome, yo, hello, goodbye,"

        -   take into account ``hello`` also calls ``yo`` .

    -   "welcome, goodbye,"

        -   ``goodbye`` calls other functions that print output as well.

    -   "welcome, yo, hello, yo, yo, goodbye,"

        +   The order of calls and composition of ``yo`` in ``hello`` and both of those in ``goodbye`` produce this output.
    
    -   "yo, hello, yo, yo, goodbye,"

        -   Note that the ``main`` also prints something directly.
