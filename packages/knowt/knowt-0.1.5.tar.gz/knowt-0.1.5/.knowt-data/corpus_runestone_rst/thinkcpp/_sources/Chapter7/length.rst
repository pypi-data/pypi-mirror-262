Length
------

To find the length of a string (number of characters), we can use the
``length`` function. The syntax for calling this function is a little
different from what we’ve seen before.

.. activecode:: length_AC_1
  :language: cpp
  :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
  :caption: Finding the length of a string

  The active code below outputs the length of string ``fruit``.
  ~~~~
  #include <iostream>
  using namespace std;

  int main() {
      string fruit = "Watermelon";
      int length;
      length = fruit.length();
      cout << length << endl;
  }

.. index::
   single: invoking

To describe this function call, we would say that we are **invoking**
the length function on the string named ``fruit``. This vocabulary may
seem strange, but we will see many more examples where we invoke a
function on an object. The syntax for function invocation is called “dot
notation,” because the dot (period) separates the name of the object,
``fruit``, from the name of the function, ``length``.

``length`` takes no arguments, as indicated by the empty parentheses
``()``. The return value is an integer, in this case 6. Notice that it
is legal to have a variable with the same name as a function.

To find the last letter of a string, you might be tempted to try
something like

::

     int length = fruit.length();
     char last = fruit[length];       // WRONG!!

That won’t work. The reason is that there is no 6th letter in
``"banana"``. Since we started counting at 0, the 6 letters are numbered
from 0 to 5. To get the last character, you have to subtract 1 from
``length``.

.. warning::
   A common source of error involving strings and other arrays is indexing
   out of bounds. This is usually the result of forgetting to subtract 1 from
   ``length``.

.. activecode:: length_AC_2
  :language: cpp
  :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
  :caption: Finding the length of a string and outputting it

  The active code below outputs the last character in string ``fruit``
  using the ``length`` function.
  ~~~~
  #include <iostream>
  using namespace std;

  int main() {
      string fruit = "Watermelon";
      int length = fruit.length();
      char last = fruit[length-1];
      cout << last;
  }

.. mchoice:: length_1
   :practice: T
   :answer_a: 11
   :answer_b: 12
   :correct: b
   :feedback_a: The space counts as a character.
   :feedback_b: Yes, there are 12 characters in the string.


   What is printed by the following statements?

   .. code-block:: cpp

      string s = "coding rocks";
      cout << s.length() << endl;


.. mchoice:: length_2
   :practice: T
   :answer_a: o
   :answer_b: r
   :answer_c: s
   :answer_d: Error, s.length() is 12 and there is no index 12.
   :correct: b
   :feedback_a: Take a look at the index calculation again, s.length()-5.
   :feedback_b: Yes, s.length() is 12 and 12-5 is 7.  Use 7 as index and remember to start counting with 0.
   :feedback_c: s is at index 11.
   :feedback_d: You subtract 5 before using the index operator so it will work.


   What is printed by the following statements?

   .. code-block:: cpp

      string s = "coding rocks";
      cout << (s[s.length()-5]) << endl;


.. parsonsprob:: length_3
   :numbered: left
   :adaptive:

   Construct a block of code that correctly implements the accumulator pattern, with ``course`` being the first variable initialized.
   -----
   int main() {

      string course = "Programming";

      int num_chars;

      string num_chars; #distractor

      num_chars = course.length();

      num_chars = length(course); #distractor

      cout << num_chars << endl;

   }
