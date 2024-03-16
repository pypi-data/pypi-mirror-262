Coding Practice
---------------

.. tabbed:: cp_5_1

    .. tab:: Question

        Write a function called ``calculator`` which takes two ``doubles``, ``first`` and
        ``second`` and a ``char operation`` as parameters. ``calculator`` performs
        addition, subtraction, multiplication, or division with the two ``doubles``
        depending on what operation is passed in (+, -, \*, /). It then returns the result.
        Run and test your code!

        .. activecode:: cp_5_AC_r1q
           :language: cpp
           :practice: T

           #include <iostream>
           using namespace std;

           double calculator (double first, double second, char operation) {
               // Write your implementation here.
           }
           ====
           #define CATCH_CONFIG_MAIN
           #include <catch.hpp>

           TEST_CASE("calculator function: addition") {
               REQUIRE(calculator(3, 6, '+') == 9);
               REQUIRE(calculator(-2.6, 4, '+') == 1.4);
           }

           TEST_CASE("calculator function: subtraction") {
               REQUIRE(calculator(19, 2, '-') == 17);
               REQUIRE(calculator(-2.3, 2, '-') == -4.3);
           }

           TEST_CASE("calculator function: multiplication") {
               REQUIRE(calculator(5, 8, '*') == 40);
               REQUIRE(calculator(0.5, -6, '*') == -3.0);
           }

           TEST_CASE("calculator function: division") {
               REQUIRE(calculator(16, 4, '/') == 4);
               REQUIRE(calculator(3, 8, '/') == 0.375);
           }

    .. tab:: Answer

        Below is one way to implement the ``calculator`` function. Using conditionals,
        we return the correct result depending on which operation was given.

        .. activecode:: cp_5_AC_1a
           :language: cpp
           :optional:

           #include <iostream>
           using namespace std;

           double calculator (double first, double second, char operation) {
               if (operation == '+') {
                   return first + second;
               }
               else if (operation == '-') {
                   return first - second;
               }
               else if (operation == '*') {
                   return first * second;
               }
               else {
                   return first / second;
               }
           }
           ====
           #define CATCH_CONFIG_MAIN
           #include <catch.hpp>

           TEST_CASE("calculator function: addition") {
               REQUIRE(calculator(3, 6, '+') == 9);
               REQUIRE(calculator(-2.6, 4, '+') == 1.4);
           }

           TEST_CASE("calculator function: subtraction") {
               REQUIRE(calculator(19, 2, '-') == 17);
               REQUIRE(calculator(-2.3, 2, '-') == -4.3);
           }

           TEST_CASE("calculator function: multiplication") {
               REQUIRE(calculator(5, 8, '*') == 40);
               REQUIRE(calculator(0.5, -6, '*') == -3.0);
           }

           TEST_CASE("calculator function: division") {
               REQUIRE(calculator(16, 4, '/') == 4);
               REQUIRE(calculator(3, 8, '/') == 0.375);
           }

.. selectquestion:: cp_5_AC_2q_sq
    :fromid: cp_5_AC_2q, cp_5_AC_2q_pp
    :toggle: lock

.. tabbed:: cp_5_3

    .. tab:: Question

        An interior angle of a polygon is the angle between two adjacent
        sides of the polygon. Each interior angle in an equilateral triangle
        measures 60 degree, each interior angle in a square measures 90 degrees,
        and in a regular pentagon, each interior angle measures 108 degrees.
        Write the function ``calculateIntAngle``, which takes a ``numSides``
        as a parameter and returns a ``double``. ``calculateIntAngle`` finds the
        interior angle of a regular polygon with ``numSides`` sides. The formula
        to find the interior angle of a regular ngon is (n - 2) x 180 / n.
        Run and test your code!

        .. activecode:: cp_5_AC_3q
           :language: cpp
           :practice: T

           #include <iostream>
           using namespace std;

           double calculateIntAngle (int numSides) {
               // Write your implementation here.
           }
           ====
           #define CATCH_CONFIG_MAIN
           #include <catch.hpp>

           TEST_CASE("calculateIntAngle function") {
               REQUIRE(calculateIntAngle (3) == 60);
               REQUIRE(calculateIntAngle (4) == 90);
               REQUIRE(calculateIntAngle (5) == 108);
               REQUIRE(calculateIntAngle (8) == 135);
           }


    .. tab:: Answer

        Below is one way to implement the program. Using the formula given,
        we can find the interior angle and return it. Notice how we use 180.0
        instead of 180 to avoid integer division.

        .. activecode:: cp_5_AC_3a
           :language: cpp
           :optional:

           #include <iostream>
           using namespace std;

           double calculateIntAngle (int numSides) {
               return (numSides - 2) * 180.0 / numSides;
           }
           ====
           #define CATCH_CONFIG_MAIN
           #include <catch.hpp>

           TEST_CASE("calculateIntAngle function") {
               REQUIRE(calculateIntAngle (3) == 60);
               REQUIRE(calculateIntAngle (4) == 90);
               REQUIRE(calculateIntAngle (5) == 108);
               REQUIRE(calculateIntAngle (8) == 135);
           }

.. selectquestion:: cp_5_AC_4q_sq
    :fromid: cp_5_AC_4q, cp_5_AC_4q_pp
    :toggle: lock

.. tabbed:: cp_5_5

    .. tab:: Question

        Dog owners will know that figuring out a dog's age is more complicated
        than just counting age directly. Dogs mature faster than humans do,
        so to get a more accurate calculation of a dog's age, write the
        ``dogToHumanYears`` function, which takes an ``dogAge`` as a parameter.
        ``dogToHumanYears`` converts and returns the dog's age to human years.
        A one year old dog is 15 years old in human years; a two year old dog is 24 years old in human years.
        Each year after the second year counts as 4 additional human years. For example, a dog that is
        3 years old is actually 28 years old in human years. Run and test your code!

        .. activecode:: cp_5_AC_5q
           :language: cpp
           :practice: T

           #include <iostream>
           using namespace std;

           int dogToHumanYears (int dogAge) {
               // Write your implementation here.
           }
           ====
           #define CATCH_CONFIG_MAIN
           #include <catch.hpp>

           TEST_CASE("dogToHumanYears function for 1 and under") {
               REQUIRE(dogToHumanYears (1) == 15);
           }

           TEST_CASE("dogToHumanYears function for >1") {
               REQUIRE(dogToHumanYears (2) == 24);
               REQUIRE(dogToHumanYears (3) == 28);
               REQUIRE(dogToHumanYears (5) == 36);
           }


    .. tab:: Answer

        Below is one way to implement the program. We can use a conditional to
        check to see if the dog is one year old. If it is older than one, then
        we can use the formula to return the correct age in human years.

        .. activecode:: cp_5_AC_5a
           :language: cpp
           :optional:

           #include <iostream>
           using namespace std;

           int dogToHumanYears (int dogAge) {
               if (dogAge == 1) {
                   return 15;
               }
               return 24 + (dogAge - 2) * 4;
           }
           ====
           #define CATCH_CONFIG_MAIN
           #include <catch.hpp>

           TEST_CASE("dogToHumanYears function for 1 and under") {
               REQUIRE(dogToHumanYears (1) == 15);
           }

           TEST_CASE("dogToHumanYears function for >1") {
               REQUIRE(dogToHumanYears (2) == 24);
               REQUIRE(dogToHumanYears (3) == 28);
               REQUIRE(dogToHumanYears (5) == 36);
           }

.. selectquestion:: cp_5_AC_6q_sq
    :fromid: cp_5_AC_6q, cp_5_AC_6q_pp
    :toggle: lock

.. tabbed:: cp_5_7

    .. tab:: Question

        If a year is divisible by 4, then it is a leap year. However, if it is also divisible by 100,
        then it is not a leap year. However, if it is also divisible by 400, then it is a leap year.
        Thus, 2001 is not a leap year, 2004 is a leap year, 2100 is not a leap year, and 2000 is a leap year.
        Write the boolean function ``isLeapYear``, which takes a ``year`` as a parameter and returns ``true``
        if the year is a leap year and ``false`` otherwise. Run and test your code!

        .. activecode:: cp_5_AC_7q
           :language: cpp
           :practice: T

           #include <iostream>
           using namespace std;

           bool isLeapYear (int year) {
               // Write your implementation here.
           }
           ====
           #define CATCH_CONFIG_MAIN
           #include <catch.hpp>

           TEST_CASE("isLeapYear not divisible by 4") {
               REQUIRE(isLeapYear (2001) == 0);
               REQUIRE(isLeapYear (2005) == 0);
           }

           TEST_CASE("isLeapYear divisible by 4") {
               REQUIRE(isLeapYear (2004) == 1);
               REQUIRE(isLeapYear (2008) == 1);
           }

           TEST_CASE("isLeapYear divisible by 100") {
               REQUIRE(isLeapYear (2100) == 0);
               REQUIRE(isLeapYear (1900) == 0);
           }

           TEST_CASE("isLeapYear divisible by 400") {
               REQUIRE(isLeapYear (2000) == 1);
               REQUIRE(isLeapYear (2400) == 1);
           }


    .. tab:: Answer

        Below is one way to implement the program. We can use conditionals in this
        order to efficiently determine whether or not a given year is a leap year.

        .. activecode:: cp_5_AC_7a
           :language: cpp
           :optional:

           #include <iostream>
           using namespace std;

           bool isLeapYear (int year) {
               if (year % 400 == 0) {
                   return true;
               }
               else if (year % 100 == 0) {
                   return false;
               }
               else if (year % 4 == 0) {
                   return true;
               }
               else {
                   return false;
               }
           }
           ====
           #define CATCH_CONFIG_MAIN
           #include <catch.hpp>

           TEST_CASE("isLeapYear not divisible by 4") {
               REQUIRE(isLeapYear (2001) == 0);
               REQUIRE(isLeapYear (2005) == 0);
           }

           TEST_CASE("isLeapYear divisible by 4") {
               REQUIRE(isLeapYear (2004) == 1);
               REQUIRE(isLeapYear (2008) == 1);
           }

           TEST_CASE("isLeapYear divisible by 100") {
               REQUIRE(isLeapYear (2100) == 0);
               REQUIRE(isLeapYear (1900) == 0);
           }

           TEST_CASE("isLeapYear divisible by 400") {
               REQUIRE(isLeapYear (2000) == 1);
               REQUIRE(isLeapYear (2400) == 1);
           }

.. selectquestion:: cp_5_AC_8q_sq
    :fromid: cp_5_AC_8q, cp_5_AC_8q_pp
    :toggle: lock

.. tabbed:: cp_5_9

    .. tab:: Question

        We know that a factorial is the product of an integer and all the integers below it.
        For example, four factorial (4!) is 24. A triangular number is the same as a factorial,
        except you add all the numbers instead of multiplying. For example, the 1st triangular
        number is 1, the 2nd is 3, the 3rd is 6, the 4th is 10, the 5th is 15, etc. You can imagine
        rows of dots, where each successive row has one more dot, thus forming a triangular shape.
        Write the ``triangularNum`` function, which takes an ``int n`` as a parameter and returns
        the ``n``\th triangular number. Use recursion. Run and test your code!

        .. activecode:: cp_5_AC_9q
           :language: cpp
           :practice: T

           #include <iostream>
           using namespace std;

           int triangularNum (int n) {
               // Write your implementation here.
           }
           ====
           #define CATCH_CONFIG_MAIN
           #include <catch.hpp>

           TEST_CASE("triangularNum function") {
               REQUIRE(triangularNum (1) == 1);
               REQUIRE(triangularNum (3) == 6);
               REQUIRE(triangularNum (6) == 21);
               REQUIRE(triangularNum (17) == 153);
           }


    .. tab:: Answer

        Below is one way to implement the program. We can use conditionals to
        separate the base case and recursive cases. Our base case is when ``n``
        is 1, and in that case we return 1. Otherwise, we recursively
        call ``triangularNum`` on ``n-1``.

        .. activecode:: cp_5_AC_9a
           :language: cpp
           :optional:

           #include <iostream>
           using namespace std;

           int triangularNum (int n) {
               if (n == 1) {
                   return 1;
               }
               else {
                   return n + triangularNum(n - 1);
               }
           }
           ====
           #define CATCH_CONFIG_MAIN
           #include <catch.hpp>

           TEST_CASE("triangularNum function") {
               REQUIRE(triangularNum (1) == 1);
               REQUIRE(triangularNum (3) == 6);
               REQUIRE(triangularNum (6) == 21);
               REQUIRE(triangularNum (17) == 153);
           }

.. selectquestion:: cp_5_AC_10q_sq
    :fromid: cp_5_AC_10q, cp_5_AC_10q_pp
    :toggle: lock
