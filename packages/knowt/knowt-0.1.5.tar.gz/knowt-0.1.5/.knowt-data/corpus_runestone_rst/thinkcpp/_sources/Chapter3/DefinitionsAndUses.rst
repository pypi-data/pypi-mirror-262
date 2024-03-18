Definitions and Uses
--------------------

Pulling together all the code fragments from the previous section, the
whole program looks like this:

::

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

This program contains three function definitions: ``newLine``, ``threeLine``,
and ``main``.

Inside the definition of ``main``, there is a statement that uses or calls
``threeLine``. Similarly, ``threeLine`` calls ``newLine`` three times. Notice that
the definition of each function appears above the place where it is
used.

This is necessary in C++; the definition of a function must appear
before (above) the first use of the function. You should try compiling
this program with the functions in a different order and see what error
messages you get.


.. fillintheblank:: defns_uses_1

   The function definition must be written |blank| the first use of the function.
    
   - :([Bb][Ee][Ff][Oo][Rr][Ee])|([Aa][Bb][Oo][Vv][Ee]): Correct!
     :.*: Try again!


.. mchoice::  defns_uses_2

    Which of the following is a correct function header (first line of 
    a function definition)?

    -   ``void printName()``

        -   This function header is missing a ``{``, which is needed to begin defining the function.

    -   ``totalCostAfterTax () {``

        -   This function header is missing a return type.

    -   ``void todaysWeather () {``

        +   Correct!

    -   ``void finalGrade {``

        -   This function header is missing parentheses. Even if a function does not take in any parameters, empty parentheses should be used.


.. parsonsprob:: defns_uses_3
   :adaptive:

   Construct a block of code that correctly defines a the addTwo function.
   -----
   void addTwo(int x) {

   void addTwo(int x); #distractor

   void addTwo(int x) #distractor

    int plustwo = x + 2;

    cout << plustwo;

   }
