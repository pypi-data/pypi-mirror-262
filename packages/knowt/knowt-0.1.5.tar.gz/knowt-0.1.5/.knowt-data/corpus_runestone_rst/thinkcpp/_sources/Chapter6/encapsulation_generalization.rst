Encapsulation and generalization
--------------------------------

Encapsulation usually means taking a piece of code and wrapping it up in
a function, allowing you to take advantage of all the things functions
are good for. We have seen two examples of encapsulation, when we wrote
``printParity`` in :numref:`alternative` and
``isSingleDigit`` in :numref:`bool`.

Generalization means taking something specific, like printing multiples
of 2, and making it more general, like printing the multiples of any
integer.

Here’s a function that encapsulates the loop from the previous section
and generalizes it to print multiples of ``n``.

::

   void printMultiples (int n) {
     int i = 1;
     while (i <= 6) {
       cout << n * i << "   ";
       i = i + 1;
     }
     cout << endl;
   }

To encapsulate, all I had to do was add the first line, which declares
the name, parameter, and return type. To generalize, all I had to do was
replace the value 2 with the parameter ``n``.

If we call this function with the argument 2, we get the same output as
before. With argument 3, the output is:

::

   3   6   9   12   15   18

and with argument 4, the output is

::

   4   8   12   16   20   24

By now you can probably guess how we are going to print a multiplication
table: we’ll call ``printMultiples`` repeatedly with different
arguments. In fact, we are going to use another loop to iterate through
the rows.

::

     int i = 1;
     while (i <= 6) {
       printMultiples (i);
       i = i + 1;
     }

First of all, notice how similar this loop is to the one inside
``printMultiples``. All I did was replace the print statement with a
function call.


.. activecode:: encapsulation_generalization_AC_1
  :language: cpp
  :caption: Two-dimensional tables

  Try running the active code below, which uses ``printMultiples``.
  ~~~~
  #include <iostream>
  using namespace std;

  void printMultiples (int n) {
      int i = 1;
      while (i <= 6) {
          cout << n * i << "   ";
          i = i + 1;
      }
      cout << endl;
  }

  int main() {
      int i = 1;
      while (i <= 6) {
          printMultiples (i);
          i = i + 1;
      }
  }

The output of this program is

::

   1   2   3   4   5   6
   2   4   6   8   10   12
   3   6   9   12   15   18
   4   8   12   16   20   24
   5   10   15   20   25   30
   6   12   18   24   30   36

which is a (slightly sloppy) multiplication table. If the sloppiness
bothers you, you can also use tab characters, like below.

.. activecode:: encapsulation_generalization_AC_2
  :language: cpp
  :caption: Two-dimensional tables

  The active code below uses tab characters to make the table neater.
  ~~~~
  #include <iostream>
  using namespace std;

  void printMultiples (int n) {
      int i = 1;
      while (i <= 6) {
          cout << n * i << '\t';
          i = i + 1;
      }
      cout << endl;
  }

  int main() {
      int i = 1;
      while (i <= 6) {
          printMultiples (i);
          i = i + 1;
      }
  }


.. mchoice:: encapsulation_generalization_1
   :answer_a: Replacing integers with parameters.
   :answer_b: Using a parameter that exists in several different functions.
   :answer_c: Taking a very specific task and making it more applicable to other situations.
   :answer_d: Creating two functions with the same purpose but different names.
   :correct: c
   :feedback_a: This may be a possible way to generalize, but not the purpose.
   :feedback_b: This is not the purpose of generalization.
   :feedback_c: This makes your code more versatile.
   :feedback_d: This is not the purpose of generalization.

   What is the purpose of generalization?

.. parsonsprob:: encapsulation_generalization_2
   :numbered: left
   :adaptive:

   Create a function called ``powersOfTwo`` which prints out a table with the powers of two up to :math:`2^{5}`.
   -----
   void powersOfTwo () {
   =====
     int x = 1;
   =====
     while (x <= 5) {
   =====
       cout << x << "\t" << pow(2, x) << endl;
   =====
       cout << x << "\t" << pow(x, 2) << endl;  #paired
   =====
       x++;
     }
   }

.. parsonsprob:: encapsulation_generalization_3
   :numbered: left
   :adaptive:

   Now let's generalize the function to print out the powers of a parameter n up to :math:`n^{5}`. Create a
   function called ``powersOfn`` which takes an int n as a parameter.
   -----
   void powersOfn (int n) {
   =====
   void powersOfn (string n) {  #paired
   =====
     int x = 1;
   =====
     while (x <= 5) {
   =====
       cout << x << "\t" << pow(n, x) << endl;
   =====
       cout << x << "\t" << pow(5, x) << endl;  #paired
   =====
       x++;
     }
   }

