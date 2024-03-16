``string``\ s are mutable
-------------------------

You can change the letters in an ``string`` one at a time using the
``[]`` operator on the left side of an assignment.

.. activecode:: strings_are_mutable_AC_1
  :language: cpp
  :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
  :caption: String are mutable

  The active code below changes the first letter in ``greeting`` to be
  ``'J'``.
  ~~~~
  #include <iostream>
  using namespace std;

  int main() {
      string greeting = "Hello, world!";
      greeting[0] = 'J';
      cout << greeting << endl;
  }

This produces the output ``Jello, world!``.

.. mchoice:: string_mutable_1
   :practice: T
   :answer_a: icd cream
   :answer_b: icedcream
   :answer_c: ice cream
   :answer_d: iced
   :correct: b
   :feedback_a: Remember that indexing begins at 0, not 1.
   :feedback_b: Index 3 was a space and now it is "d".
   :feedback_c: The character at index 3 should be changed to "d".
   :feedback_d: The character at index 3 should be changed to "d", and the rest stays the same.


   What is printed by the following statements?

   .. code-block:: cpp

      string fav_food = "ice cream";
      fav_food[3] = "d";
      cout << fav_food << endl;

.. mchoice:: string_mutable_2
   :practice: T
   :answer_a: message[9] = "w";
   :answer_b: message[10] = "w";
   :answer_c: "w" = message[9];
   :answer_d: message[8] = "w";
   :correct: a
   :feedback_a: Since "l" is at index 9, replacing it with "w" fixes the message.
   :feedback_b: Remember indexing starts at 0.
   :feedback_c: In order to change a letter in a string, the ``[]`` operator must be on the left of the assignment.
   :feedback_d: Remember indexing starts at 0.

   How can we fix the message to be "You're a wizard Harry"?

   .. code-block:: cpp

      string message = "You're a lizard Harry";

.. parsonsprob:: string_mutable_3
   :numbered: left
   :adaptive:
   :noindent:

   Put together the code below to create a function ``mixer`` that takes in two strings and replaces every even index
   of the first string by the corresponding index of the second. It returns the modified first string.
   Example:
   ``string_a = "food"``  and ``string_b = "summer"`` .
   ``mixer(string_a ,string_b )`` makes ``string_a`` become "somd".

   Assume second string is greater than first.

   -----
   string greeter(string s1,string s2) {
   =====
   void mixer(string s1,string s2) { #paired
   =====
      int size = s1.length();
   =====
      int size = s2.length(); #paired
   =====
      index i = 0;
      while (i &lt size) {
   =====
      index i = size - 1; #distractor
      while (i &lt size) {
   =====
        if( (i % 2) == 0){
          s1[i] = s2[i];
        }
   =====
        if( (i % 2) == 1){ #paired
          s1[i] = s2[i];
        }
   =====
        i++;
   =====
      }
   =====
      return s1;
   =====
      return s2; #paired
   =====
   }
