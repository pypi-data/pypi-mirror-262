``string`` variables
--------------------
.. index::
   pair: variables; string variables
   pair: string; string variables

You can create a variable with type ``string`` in the usual ways.

.. activecode:: string_variables_AC_1
  :language: cpp
  :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
  :caption: Creating a string variable

  In the active code below, the first line creates a ``string`` without 
  giving it a value. The second line assigns it the string value ``"Hello,"``. 
  The third line is a combined declaration and assignment, also called an initialization.
  ~~~~
  #include <iostream>
  using namespace std;

  int main() {
      string first;
      first = "Hello, ";
      string second = "world.";
  }

Normally when string values like ``"Hello, "`` or ``"world."`` appear,
they are treated as C strings. In this case, when we assign them to an
``string`` variable, they are converted automatically to ``string``
values.

We can output strings in the usual way:

::

     cout << first << second << endl;

In order to compile this code, you will have to include the header file
for the ``string`` class, and you will have to add the file ``string``
to the list of files you want to compile. The details of how to do this
depend on your programming environment.

.. activecode:: string_variables_AC_2
  :language: cpp
  :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
  :caption: Outputting a string variable

  Run the active code below!
  ~~~~
  #include <iostream>
  using namespace std;

  int main() {
      string first;
      first = "Hello, ";
      string second = "world.";
      cout << first << second << endl;
  }

.. parsonsprob:: string_variables_1
   :numbered: left
   :adaptive:

   Construct a block of code that correctly prints out a string variable.
   -----
   string x;

   x = "It is cold outside!";

   x = "It is cold outside" #paired

   cout << x << endl;


.. mchoice:: string_variables_2
   :practice: T
   :answer_a: string x = "Hello";
   :answer_b: x = "Hello";
   :answer_c: string x;
   :correct: a
   :feedback_a: This is the correct way to initialize a string.
   :feedback_b: This is an assignment.
   :feedback_c: This is a declaration.


   How would you initialize a string?


.. clickablearea:: string_variables_3
    :question: Click on each spot where a string assignment occurs.
    :iscode:
    :feedback: Remember, square brackets [] are used to access a character in a string.

    :click-incorrect:def main() {:endclick:
        :click-incorrect:string fruit;:endclick:
        :click-correct:fruit = "apple";:endclick:
        :click-correct:fruit = "pear";:endclick:
        :click-incorrect:string flavor;:endclick:
        :click-correct:flavor = "vanilla";:endclick:
    }
