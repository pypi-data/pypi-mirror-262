Activecode Exercises
--------------------

Answer the following **Activecode** questions to assess what you have learned in this chapter.


.. tabbed:: vectors_a1

   .. tab:: Question

      .. activecode:: vectors_a1q
         :language: cpp
         :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

         Fix the code below so that it creates a vector with 5 elements initialized to 1, and changes
         the third element of that vector to a 2.
         ~~~~
         #include <iostream>


         using namespace std;

         int main () {
             vector<int> nums (5) = 1;
             nums[3] = 2;
         }

   .. tab:: Answer

      .. activecode:: vectors_a1a
         :language: cpp
         :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

         Below is one way to fix the program.  You must always include the ``<vector>`` header when
         dealing with vectors.  Furthermore, to initialize a vector's elements to a certain value, you
         must include that value as a second argument to the size.  Finally, vectors are zero-indexed.
         ~~~~
         #include <iostream>
         #include <vector>
         using namespace std;

         int main () {
             vector<int> nums (5, 1);
             nums[2] = 2;
         }


.. selectquestion:: vectors_a2_sq
    :fromid: vectors_a2, vectors_a2_pp
    :toggle: lock


.. tabbed:: vectors_a3

   .. tab:: Question

      .. activecode:: vectors_a3q
         :language: cpp
         :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

         Fix the function below so that it creates a vector of all of the words in ``words`` that end with
         the passed character.
         ~~~~
         #include <iostream>
         #include <string>
         #include <vector>
         using namespace std;

         int endsWith (const vector<string>& vec, char c) {
             int count;
             for (size_t i = 0; i < vec.size(); i++) {
                 last = vec.size() - 1;
                 if (vec[last] == c) {
                     count++;
                 }
             }
             return count;
         }

   .. tab:: Answer

      .. activecode:: vectors_a3a
         :language: cpp
         :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

         Below is one way to fix the function.  You must initialize ``count`` to zero.
         You also must initialize ``last`` as an integer.  To access a string *inside* 
         of ``vec``,  we use ``vec[i]``.  To get the last character, we must index the
         string to the last index, which is one less than the length of the string.
         ~~~~
         #include <iostream>
         #include <string>
         #include <vector>
         using namespace std;

         int endsWith (const vector<string>& vec, char c) {
             int count = 0;
             for (size_t i = 0; i < vec.size(); i++) {
                 int last = vec[i].size() - 1;
                 if (vec[i][last] == c) {
                     count++;
                 }
             }
             return count;
         }


.. selectquestion:: vectors_a4_sq
    :fromid: vectors_a4, vectors_a4_pp
    :toggle: lock


.. tabbed:: vectors_a5

   .. tab:: Question

      .. activecode:: vectors_a5q
         :language: cpp
         :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

         Finish the code below so that it creates removes elements from the end of the vector until
         it ends with ``"stop"``.
         ~~~~
         #include <iostream>


         using namespace std;

         int main () {
             vector<string> words = {"roses", "are", "red", "violets", "stop", "are", "blue"}
         
             while(          ) {

             }

         }

   .. tab:: Answer

      .. activecode:: vectors_a5a
         :language: cpp
         :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

         Below is one way to finish the program.  We just use the ``pop_back`` function until the 
         last element of the vector is ``"stop"``.
         ~~~~
         #include <iostream>
         #include <vector>

         using namespace std;

         int main () {
             vector<string> words = {"roses", "are", "red", "violets", "stop", "are", "blue"};
         
             while (words[words.size() - 1] != "stop"){
                 words.pop_back();
             }
         }


.. selectquestion:: vectors_a6_sq
    :fromid: vectors_a6, vectors_a6_pp
    :toggle: lock


.. tabbed:: vectors_a7

   .. tab:: Question

      .. activecode:: vectors_a7q
         :language: cpp
         :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

         Write a function called ``has_char`` that returns a boolean of whether every string in the
         vector ``vec`` contains the character ``let``.  It should return true if all strings contain the ``let``.
         ~~~~
         #include <iostream>
         #include <vector>
         using namespace std;


   .. tab:: Answer

      .. activecode:: vectors_a7a
         :language: cpp
         :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

         Below is one way to finish the program.  We loop through the vector, and we loop through each string
         inside it.  If the string has the character, it is added to ``count``.  We then check whether ``count``
         is equal to the number of elements in ``vec`` and return a boolean.
         ~~~~
         #include <iostream>
         #include <vector>
         using namespace std;


         int has_char (const vector<string>& vec, char let) {
             int count = 0;
             for (size_t i = 0; i < vec.size(); i++) {
                 for (size_t c = 0; c < vec[i].size(); c++) {
                     if (vec[i][c] == let) {
                         count++;
                     }
                 }
             }
             if (count == vec.size()) {
                 return true;
             }
             return false;
         }
         

.. selectquestion:: vectors_a8_sq
    :fromid: vectors_a8, vectors_a8_pp
    :toggle: lock


.. tabbed:: vectors_a9

   .. tab:: Question

      .. activecode:: vectors_a9q
         :language: cpp
         :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

         Write the function ``mean`` which returns the average of a vector of numbers.
         ~~~~
         #include <iostream>
         #include <vector>
         using namespace std;


   .. tab:: Answer

      .. activecode:: vectors_a9a
         :language: cpp
         :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

         Below is one way to finish the program.  First we take the sum, then divide the sum by the number
         of elements in ``nums``.
         ~~~~
         #include <iostream>
         #include <vector>
         using namespace std;

         double mean (const vector<double> nums) {
             double sum = 0;
             for (size_t i = 0; i < nums.size(); ++i) {
                 sum = sum + nums[i];
             }
             return sum/nums.size();
         }


.. selectquestion:: vectors_a10_sq
    :fromid: vectors_a10, vectors_a10_pp
    :toggle: lock


.. tabbed:: vectors_a11

   .. tab:: Question

      .. activecode:: vectors_a11q
         :language: cpp
         :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

         Write the function ``make_odd`` which subtracts 1 from every even number in a vector of integers.
         We don't want any negative values so don't subtract 1 from 0.
         ( remember to take in the vector by reference to make changes to the actual vector! )
         ~~~~
         #include <iostream>
         #include <vector>
         using namespace std;


   .. tab:: Answer

      .. activecode:: vectors_a11a
         :language: cpp
         :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

         Below is one way to finish the program.  We us the modulus operator to check for even numbers and decrement them.
         we keep an extra check for 0 to make sure wew are not decrementing 0.
         ~~~~
         #include <iostream>
         #include <vector>
         using namespace std;

         void make_odd ( vector<int> &nums) {
             for (size_t i = 0; i < nums.size(); ++i) {

                 if((nums[i] % 2 == 0) && (nums[i] != 0)){
                     nums[i]--;
                 } 

             }
         }


.. selectquestion:: vectors_a12_sq
    :fromid: vectors_a12, vectors_a12_pp
    :toggle: lock