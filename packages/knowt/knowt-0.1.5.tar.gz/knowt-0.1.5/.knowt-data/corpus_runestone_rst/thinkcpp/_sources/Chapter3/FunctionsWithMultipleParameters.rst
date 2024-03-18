Functions with Multiple Parameters
----------------------------------

The syntax for declaring and invoking functions with multiple parameters
is a common source of errors. First, remember that you have to declare
the type of every parameter. For example

::

    void printTime (int hour, int minute) {
      cout << hour;
      cout << ":";
      cout << minute;
    }

It might be tempting to write ``(int hour, minute)``, but that format is
only legal for variable declarations, not for parameters.

Another common source of confusion is that you do not have to declare
the types of arguments. The following is wrong!

::

    int hour = 11;
    int minute = 59;
    printTime (int hour, int minute);   // WRONG!

In this case, the compiler can tell the type of hour and minute by
looking at their declarations. 

.. warning::
   It is unnecessary and illegal to include the type when you pass 
   variables as arguments! The type is only needed for declaration.
   
The correct syntax is printTime (hour, minute).


.. activecode:: multiple_params_AC_1
   :language: cpp
   :caption: Understanding Multiple Parameters

   This program shows how the dollar_amount and cent_amount arguments
   are passed into the printPrice function.
   ~~~~
   #include <iostream>
   using namespace std;

   void printPrice (int dollars, int cents) {
       cout << "Price is " << dollars << " dollars and " << cents << " cents." << endl;
   }

   int main () {
       int dollar_amount = 2;
       int cent_amount = 92;
       printPrice (dollar_amount, cent_amount);
       return 0;
   }


.. mchoice::  multiple_params_1

    Which of the following is a correct function header (first line of 
    a function definition)?

    -   ``totalcost (double cost, tax, discount)``

        -   ``totalcost`` needs a return type, and each parameter needs a data type.

    -   ``totalCost (double cost, double tax) {``

        -   ``totalcost`` needs a return type.

    -   ``void totalCost (double cost, double tax, double discount) {``

        +   Correct!


.. mchoice::  multiple_params_2

    Which of the following is a legal function call of the function below?

    ::

        void multiplyTwo (int num, string name) {
          int total = num * 2;
          cout << "Hi " << name << ", your total is " << total << "!" << endl;
        }

        int main() {
          int x = 2;
          string phil = "Phil";
        }

    -   ``multiplyTwo (int x, string phil);``

        -   Data types are not needed when calling a function.

    -   ``multiplyTwo (x, phil);``

        +   Correct!

    -   ``void multiplyTwo (int num, string name) {``

        -   This is the function definition.

    -   ``void multiplyTwo (int x, string phil);``

        -   Data types are not needed when calling a function.
