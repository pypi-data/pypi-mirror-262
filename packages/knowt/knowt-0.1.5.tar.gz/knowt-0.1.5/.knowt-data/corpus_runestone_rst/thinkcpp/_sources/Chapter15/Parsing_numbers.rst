Parsing numbers
---------------

The next task is to convert the numbers in the file from strings to
integers. When people write large numbers, they often use commas to
group the digits, as in 1,750. Most of the time when computers write
large numbers, they don’t include commas, and the built-in functions for
reading numbers usually can’t handle them. That makes the conversion a
little more difficult, but it also provides an opportunity to write a
comma-stripping function, so that’s ok. Once we get rid of the commas,
we can use the library function ``atoi`` to convert to integer. ``atoi``
is defined in the header file ``cstdlib``.

To get rid of the commas, one option is to traverse the string and check
whether each character is a digit. If so, we add it to the result
string. At the end of the loop, the result string contains all the
digits from the original string, in order.

::

    #include <iostream>
    using namespace std;

   int convertToInt (const string& s)
   {
     string digitString = "";

     for (size_t i = 0; i < s.length(); i++) {
       if (isdigit (s[i])) {
         digitString += s[i];
       }
     }
     return atoi (digitString.c_str());
   }

.. index::
   single: accumulator

The variable ``digitString`` is an example of an **accumulator**. It is
similar to the counter we saw in :numref:`loopcount`,
except that instead of getting incremented, it gets accumulates one new
character at a time, using string concatentation.

The expression

::

         digitString += s[i];

is equivalent to

::

         digitString = digitString + s[i];

Both statements add a single character onto the end of the existing
string.

Since ``atoi`` takes a C string as a parameter, we have to convert
``digitString`` to a C string before passing it as an argument.

Try the function out for yourself! As you can see, this function can also be used
to parse phone numbers!

.. activecode:: 15_6
   :language: cpp

   #include <iostream>
   #include <string>
   #include <vector>
   using namespace std;

   int convertToInt (const string& s) {
      string digitString = "";

      for (size_t i = 0; i < s.length(); i++) {
         if (isdigit (s[i])) {
            digitString += s[i];
         }
      }
      return atoi (digitString.c_str());
   }

   int main() {
      int num = convertToInt("867-5309");
      cout << num << endl;
   }

.. mchoice:: question15_6_1
   :answer_a: takes the absolute value of a number
   :answer_b: converts a double to an int
   :answer_c: converts a string to an int
   :answer_d: converts an int to a string
   :correct: c
   :feedback_a: Incorrect! Go back and read for the answer.
   :feedback_b: Incorrect! Go back and read for the answer.
   :feedback_c: Correct! This is very helpful when we read numbers from a file (where they are strings).
   :feedback_d: Incorrect! Go back and read for the answer.

   What does the ``atoi()`` function do?

.. mchoice:: question15_6_2
   :multiple_answers:
   :answer_a: 2020
   :answer_b: ab,jkl2!!moo0?huh2mth0haha.
   :answer_c: 2,00!!!!!!!!2
   :answer_d: 2OOO020OOOOO
   :answer_e: we2love0parsing2numbersO!
   :correct: a,b,d
   :feedback_a: Correct! This one is quite simple.
   :feedback_b: Correct! This long, confusing string will clean up nicely!
   :feedback_c: Incorrect!
   :feedback_d: Correct! You have to look closely to see that some of these are 0's!
   :feedback_e: Incorrect! Although we do love parsing numbers, this is incorrect.

   Which of the following strings will return "2020" when passed into ``convertToInt()``?

.. parsonsprob:: question15_6_3
   :adaptive:
   :numbered: left

   Create the replace_with() function that takes a string "str", a character to get rid of "olc_char", 
   and a character to replace it with "new_char".  It should return a new string that has replaces any 
   occurances of old_char with new_char.
   -----
   string replace_with (string str, char old_char, char new_char) {
   =====
   string replace_with () {                              #paired
   =====
    for (size_t i = 0; i < str.length(); i++) {
   =====
    for (int i = 0; i < str.length(); i++) {                              #paired
   =====
    for (size_t i = 0; i < str.size(); i++) {                              #paired
   =====
     if (str[i] == old_char) {
   =====
     if (i == old_char) {                              #paired
   =====
      str[i] = new_char;
     }
   =====
      new_char = str[i];                              #paired
     }
   =====
      i = new_char;                              #paired
     }
   =====
    }
    return str;
   }
   =====
    }                              #paired
    return new_char;
   }
