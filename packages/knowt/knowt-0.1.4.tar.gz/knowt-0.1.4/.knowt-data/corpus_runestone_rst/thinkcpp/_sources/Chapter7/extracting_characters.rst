Extracting characters from a string
-----------------------------------
.. index::
   pair: string; string extraction

Strings are called “strings” because they are made up of a sequence, or
string, of characters. The first operation we are going to perform on a
string is to extract one of the characters. C++ uses square brackets
(``[`` and ``]``) for this operation.

.. activecode:: extracting_characters_AC_1
  :language: cpp
  :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
  :caption: Accessing a string character

  Take a look at the active code below. We extract the character
  at index 1 from string ``fruit`` using ``[`` and ``]``.
  ~~~~
  #include <iostream>
  using namespace std;

  int main() {
      string fruit = "banana";
      char letter = fruit[1];
      cout << letter << endl;
  }

The expression ``fruit[1]`` indicates that I want character number 1
from the string named ``fruit``. The result is stored in a ``char``
named ``letter``. When I output the value of ``letter``, I get a
surprise:

::

   a

``a`` is not the first letter of ``"banana"``. Unless you are a computer
scientist. For perverse reasons, computer scientists always start
counting from zero. The 0th letter (“zeroeth”) of ``"banana"`` is ``b``.
The 1th letter (“oneth”) is ``a`` and the 2th (“twoeth”) letter is
``n``.

.. note::
   In C++, indexing begins at 0!

If you want the the zereoth letter of a string, you have to put zero in
the square brackets.

.. activecode:: extracting_characters_AC_2
  :language: cpp
  :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
  :caption: Accessing a string character

  The active code below accesses the first character in string ``fruit``.
  ~~~~
  #include <iostream>
  using namespace std;

  int main() {
      string fruit = "banana";
      char letter = fruit[0];
      cout << letter << endl;
  }

.. mchoice:: extracting_characters_1
   :practice: T
   :answer_a: 1
   :answer_b: 0
   :answer_c: 2
   :correct: b
   :feedback_a: Don't forget that computer scientists do not start counting at 1!
   :feedback_b: Yes, this would access the letter "b".
   :feedback_c: This would access the letter "k".


   What would replace the "?" in order to access the letter "b" in the string below?

   .. code-block:: cpp
      :linenos:

      #include <iostream>
      using namespace std;

      int main () {
        string bake = "bake a cake!";
        char letter = bake[?];
      }

.. mchoice:: extracting_characters_2
   :practice: T
   :answer_a: lunch
   :answer_b: jello
   :answer_c: lello
   :answer_d: heljo
   :correct: c
   :feedback_a: When we <code>cout</code> a <code>string</code> we print its content not its name.
   :feedback_b: Carefully check which string(s) we are indexing into.
   :feedback_c: Correct! We copy the 'l' from position 3 of "hello" to position 0. 
   :feedback_d: Consider which string(s) we are indexing into. 


   What is printed when the code below is run?

   .. code-block:: cpp
      :linenos:

      #include <iostream>
      using namespace std;

      int main () {
        string lunch = "hello";
        string person = "deejay";
        lunch[0] = lunch[3];
        cout << lunch;
      }

.. clickablearea:: extracting_characters_3
    :question: Click on each spot where a character in a string is accessed.
    :iscode:
    :feedback: Remember, square brackets [] are used to access a character in a string.

    :click-incorrect:def main() {:endclick:
        :click-incorrect:string fruit = "apple";:endclick:
        char letter = :click-correct:fruit[2];:endclick:
        :click-incorrect:cout << fruit << endl;:endclick:
        cout <<  :click-correct:fruit[4]:endclick:  << endl;
    }


.. parsonsprob:: extracting_characters_4
   :numbered: left
   :adaptive:

   Construct a block of code that correctly prints the letter "a".
   -----
   string x;

   x = "It is warm outside!";

   x = "It is warm outside" #paired

   cout << x[7] << endl;

   cout << x[8] << endl; #distractor
