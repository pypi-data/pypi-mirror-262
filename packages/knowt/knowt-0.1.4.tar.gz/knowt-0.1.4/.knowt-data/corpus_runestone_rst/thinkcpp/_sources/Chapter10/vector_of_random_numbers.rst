Vector of random numbers
------------------------

The first step is to generate a large number of random values and store
them in a vector. By “large number,” of course, I mean 20. It’s always a
good idea to start with a manageable number, to help with debugging, and
then increase it later.

The following function takes a single argument, the size of the vector.
It allocates a new vector of ``int``\ s, and fills it with random values
between 0 and ``upperBound-1``.

::

   vector<int> randomVector (int n, int upperBound) {
     vector<int> vec (n);
     for (size_t i = 0; i < vec.size(); i++) {
       vec[i] = random () % upperBound;
     }
     return vec;
   }

The return type is ``vector<int>``, which means that this function
returns a vector of integers. To test this function, it is convenient to
have a function that outputs the contents of a vector.

::

   void printVector (const vector<int>& vec) {
     for (size_t i = 0; i < vec.size(); i++) {
       cout << vec[i] << " ";
     }
   }

Notice that it is legal to pass ``vector``\ s by reference. In fact it
is quite common, since it makes it unnecessary to copy the vector. Since
``printVector`` does not modify the vector, we declare the parameter
``const``.

The following code generates a vector and outputs it:

::

     int numValues = 20;
     int upperBound = 10;
     vector<int> vector = randomVector (numValues, upperBound);
     printVector (vector);

On my machine the output is

::

   3 6 7 5 3 5 6 2 9 1 2 7 0 9 3 6 0 6 2 6

which is pretty random-looking. Your results might be different.

.. activecode:: vector_of_rand_nums_AC_1
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   Try running the active code below!
   ~~~~
   #include <iostream>
   #include <vector>
   using namespace std;

   vector<int> randomVector (int n, int upperBound);
   void printVector (const vector<int> & vec);

   int main() {
       int numValues = 20;
       int upperBound = 10;
       vector<int> vector = randomVector (numValues, upperBound);
       printVector (vector);
   }

   ====

   vector<int> randomVector (int n, int upperBound) {
      vector<int> vec (n);
      for (size_t i = 0; i<vec.size(); i++) {
         vec[i] = random () % upperBound;
      }
      return vec;
   }
   
   void printVector (const vector<int>& vec) {
      for (size_t i = 0; i<vec.size(); i++) {
         cout << vec[i] << " ";
      }
   }

If these numbers are really random, we expect each digit to appear the
same number of times—twice each. In fact, the number 6 appears five
times, and the numbers 4 and 8 never appear at all.

Do these results mean the values are not really uniform? It’s hard to
tell. With so few values, the chances are slim that we would get exactly
what we expect. But as the number of values increases, the outcome
should be more predictable.

To test this theory, we’ll write some programs that count the number of
times each value appears, and then see what happens when we increase
``numValues``.

.. fillintheblank:: vector_of_rand_nums_1

    How should we declare the parameter, **vector**, if we don't intend to make any changes to it?

    - :([Cc]onst|CONST): Correct!
      :.*: Incorrect, Try again!

.. mchoice:: vector_of_rand_nums_2
   :answer_a: more uniform
   :answer_b: less uniform
   :answer_c: more normal
   :answer_d: less normal
   :correct: a
   :feedback_a: Correct!
   :feedback_b: Incorrect! As we store more random numbers in a vector, we see that the frequencies of each number are approximately equal.
   :feedback_c: Incorrect! The distribution of random numbers is not related to the normal distribution.
   :feedback_d: Incorrect! The distribution of random numbers is not related to the normal distribution.

   As we store more and more random numbers in a vector, we expect its contents to be __________.

.. mchoice:: vector_of_rand_nums_3
   :practice: T
   :answer_a: yes we would get a compile error
   :answer_b: no we would not because values remain same.
   :correct: a
   :feedback_a: Correct! we can't make changes to a vector we take in by constant reference
   :feedback_b: Even if we keep the values same we are editing a constant which is not allowed.

   Would compiling the following code lead to a compiler error?

   .. code-block:: cpp
      :linenos:

      void dostuff (const vector<int> & vec) {
         for (size_t i = 0; i < vec.size(); i++) {
            vec[i] = vec[i] ;
         }
      }