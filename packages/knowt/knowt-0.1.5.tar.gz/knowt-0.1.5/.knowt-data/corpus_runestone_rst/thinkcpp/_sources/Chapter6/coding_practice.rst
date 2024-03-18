Coding Practice
---------------

.. tabbed:: cp_6_1

    .. tab:: Question

        Write a program that prints out a 5x5 triangle using asterisks.
        An example is shown below. Your code should use while loops.

        ::
   
           *
           **
           ***
           ****
           *****

        .. activecode:: cp_6_AC_1q
           :language: cpp
           :practice: T

           #include <iostream>
           using namespace std;

           int main() {
               // Write your implementation here.
           }


    .. tab:: Answer

        Below is one way to implement the program. We use nested loops
        similar to the last version of the ``printMultTable`` function
        to print out the triangular shape.

        .. activecode:: cp_6_AC_1a
           :language: cpp
           :optional:

           #include <iostream>
           using namespace std;

           int main() {
               int row = 0;
               while (row < 5) {
                   int col = 0;
                   while (col <= row) {
                       cout << "*";
                       col++;
                   }
                   cout << endl;
                   row++;
               }
           }

.. selectquestion:: cp_6_AC_2q_sq
    :fromid: cp_6_AC_2q, cp_6_AC_2q_pp
    :toggle: lock

.. tabbed:: cp_6_3

    .. tab:: Question

        Write a function called ``printPyramid`` that prints out an ``n``\x``n`` pyramid using asterisks.
        An example is shown below with ``n`` equal to 5. Your code should use while loops.

        ::
   
               *
              ***
             *****
            *******
           *********

        .. activecode:: cp_6_AC_3q
           :language: cpp
           :practice: T

           #include <iostream>
           using namespace std;

           void printPyramid (int n) {
               // Write your implementation here.
           }

           int main() {
               printPyramid (5);
           }


    .. tab:: Answer

        Below is one way to implement the program. We use multiple ``while``
        loops to print out spaces and asterisks. The outer loop creates the
        number of rows, and within the outer loop, the two inner loops
        print out the correct number of spaces and asterisks.

        .. activecode:: cp_6_AC_3a
           :language: cpp
           :optional:

           #include <iostream>
           using namespace std;

           void printPyramid(int n) {
               int space, numAsterisks;
               int count = 1;
               while (count <= n) {
                   space = n - count;
                   while (space > 0) {
                       cout << " ";
                       space--;
                   }
                   numAsterisks = 2 * count - 1;
                   while (numAsterisks > 0) {
                       cout << "*";
                       numAsterisks--;
                   }
                   cout << endl;
                   count++;
               }
           }

           int main() {
               printPyramid (5);
           }

.. selectquestion:: cp_6_AC_4q_sq
    :fromid: cp_6_AC_4q, cp_6_AC_4q_pp
    :toggle: lock

.. tabbed:: cp_6_5

    .. tab:: Question

        A common coding interview question that's also a popular children's game used to teach division is
        FizzBuzz. Write a program that uses a while loop and prints the numbers 1 through 100, but every
        multiple of 3 is replaced with the word "Fizz," every multiple of 5 is replaced with the word "Buzz,"
        and every multiple of both 3 and 5 is replaced with "FizzBuzz." Your output should be the following:

        ::
   
           1
           2
           Fizz
           4
           Buzz
           ...
           14
           FizzBuzz
           16
           ...
           98
           Fizz
           Buzz

        .. activecode:: cp_6_AC_5q
           :language: cpp
           :practice: T

           #include <iostream>
           using namespace std;

           int main() {
               // Write your implementation here.
           }


    .. tab:: Answer

        Below is one way to implement the "FizzBuzz" program. We use conditionals
        with modulus operators in a while loop to categorize every number and print
        the correct output. Feel free to search up on the FizzBuzz coding interview
        problem if you are interested in other ways to code this program!

        .. activecode:: cp_6_AC_5a
           :language: cpp
           :optional:

           #include <iostream>
           using namespace std;

           int main() {
               int n = 1;
               while (n <= 100) {
                   if (n % 3 == 0 && n % 5 == 0) {
                       cout << "FizzBuzz" << endl;
                   }
                   else if (n % 3 == 0) {
                       cout << "Fizz" << endl;
                   }
                   else if (n % 5 == 0) {
                       cout << "Buzz" << endl;
                   }
                   else {
                       cout << n << endl;
                   }
                   n++;
               }
           }

.. selectquestion:: cp_6_AC_6q_sq
    :fromid: cp_6_AC_6q, cp_6_AC_6q_pp
    :toggle: lock

.. tabbed:: cp_6_7

    .. tab:: Question

        A number is a prime number if its only factors are 1 and itself.
        Write the function ``isPrime``, which takes an ``int num`` as a parameters.
        ``isPrime`` is a boolean function that returns ``true`` if ``num`` is a prime
        number and returns ``false`` otherwise. Run and test your code!

        .. activecode:: cp_6_AC_7q
           :language: cpp
           :practice: T

           #include <iostream>
           using namespace std;

           bool isPrime (int num) {
               // Write your implementation here.
           }
           ====
           #define CATCH_CONFIG_MAIN
           #include <catch.hpp>

           TEST_CASE("isPrime function") {
               REQUIRE(isPrime (1) == 0);
               REQUIRE(isPrime (13) == 1);
               REQUIRE(isPrime (24) == 0);
           }

           TEST_CASE("isPrime for 0") {
               REQUIRE(isPrime (0) == 0);
           }


    .. tab:: Answer

        Below is one way to implement the ``isPrime`` function. First,
        we check to see if ``num`` is less than or equal to 1, and return
        ``false`` if that is the case. Next, we use a ``while`` loop
        to continuously check if a factor ``n`` divides ``num`` evenly.
        If it does, we return ``false``. If no value of ``n`` divides ``num``
        evenly, then we return ``true``. Notice the ``while`` loop only goes up to
        ``num / 2`` because if 2 doesn't divide evenly, then there isn't a smaller factor.

        .. activecode:: cp_6_AC_7a
           :language: cpp
           :optional:

           #include <iostream>
           using namespace std;

           bool isPrime (int num) {
               if (num <= 1) {
                   return false;
               }
               int n = 2;
               while (n < num / 2) {
                   if (num % n == 0) {
                       return false;
                   }
                   n++;
               }
               return true;
           }
           ====
           #define CATCH_CONFIG_MAIN
           #include <catch.hpp>

           TEST_CASE("isPrime function") {
               REQUIRE(isPrime (1) == 0);
               REQUIRE(isPrime (13) == 1);
               REQUIRE(isPrime (24) == 0);
           }

           TEST_CASE("isPrime for 0") {
               REQUIRE(isPrime (0) == 0);
           }

.. selectquestion:: cp_6_AC_8q_sq
    :fromid: cp_6_AC_8q, cp_6_AC_8q_pp
    :toggle: lock

.. tabbed:: cp_6_9

    .. tab:: Question

        The Fibonacci sequence is a sequence of numbers such that each
        successive number is the sum of the two previous numbers.
        This sequence is as follows: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34,
        and so on. Write a program that prints the first 20 Fibonacci
        numbers.

        .. activecode:: cp_6_AC_9q
           :language: cpp
           :practice: T

           #include <iostream>
           using namespace std;

           int main() {
               // Write your implementation here.
           }


    .. tab:: Answer

        Below is one way to implement the program. First,
        we check to see if ``num`` is less than or equal to 1, and return
        ``false`` if that is the case. Next, we use a ``while`` loop
        to continuously check if a factor ``n`` divides ``num`` evenly.
        If it does, we return ``false``. If no value of ``n`` divides ``num``
        evenly, then we return ``true``. Notice the ``while`` loop only goes up to
        ``num / 2`` because if 2 doesn't divide evenly, then there isn't a smaller factor.

        .. activecode:: cp_6_AC_9a
           :language: cpp
           :optional:

           #include <iostream>
           using namespace std;

           int main() {
               int first = 0;
               int second = 1;
               int third;
               int n = 2;
               cout << first << " " << second << " ";
               while (n < 20) {
                   third = first + second;
                   cout << third << " ";
                   first = second;
                   second = third;
                   n++;
               }
           }

.. selectquestion:: cp_6_AC_10q_sq
    :fromid: cp_6_AC_10q, cp_6_AC_10q_pp
    :toggle: lock