Coding Practice
---------------

.. tabbed:: cp_5_AC_2q_q

    .. tab:: Activecode

        .. activecode:: cp_5_AC_2q
            :language: cpp
            :practice: T

            A binary number is one that is expressed in the base-2 numeral system.
            Write a function ``convertToBinary`` which takes a ``decimal`` as
            a parameter. ``convertToBinary`` takes the number in decimal, converts
            it into a binary number, and returns the binary number. Test your function
            in ``main``. Run and test your code! Select the Parsonsprob tab for hints
            for the construction of the code.
            ~~~~
            #include <iostream>
            #include <bits/stdc++.h>
            using namespace std;

            int convertToBinary (int decimal) {
                // Write your implementation here.
            }
            ====
            #define CATCH_CONFIG_MAIN
            #include <catch.hpp>

            TEST_CASE("convertToBinary function") {
                REQUIRE(convertToBinary (1) == 1);
                REQUIRE(convertToBinary (5) == 101);
                REQUIRE(convertToBinary (16) == 10000);
                REQUIRE(convertToBinary (31) == 11111);
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_5_AC_2q_pp
            :numbered: left
            :adaptive:

            A binary number is one that is expressed in the base-2 numeral system.
            Write a function ``convertToBinary`` which takes a ``decimal`` as
            a parameter. ``convertToBinary`` takes the number in decimal, converts
            it into a binary number, and returns the binary number. Test your function
            in ``main``. Use the lines to construct the code, then go back to complete 
            the Activecode tab.

            -----
            int convertToBinary (int decimal) {
            =====
                if (decimal == 0) {
                    return 0;
                }
            =====
                if (decimal >= 0) { #paired
                    return 0;
                }
            =====
                else {
                    return (decimal % 2 + 10 * convertToBinary(decimal / 2));
                }
            =====
            }

.. tabbed:: cp_5_AC_4q_q

    .. tab:: Activecode

        .. activecode:: cp_5_AC_4q
            :language: cpp
            :practice: T

            The astronomical start and end dates of the four seasons are based on the position of
            the Earth relative to the Sun. As a result, it changes every year and can be difficult to
            remember. However, the meteorological start and end dates are based on the Gregorian calendar
            and is easier to remember. Spring starts on March 1, summer starts on June 1, fall starts on
            September 1, and winter starts on December 1. Write a function called ``birthSeason``, which takes
            two parameters, ``month`` and ``day``. ``birthSeason`` calculates which season
            the birthday falls in according to the meteorological start and returns a ``string`` with the correct season.
            For example, ``birthSeason (7, 5)`` returns "summer" since July 5 is in the summer. Select the Parsonsprob tab 
            for hints for the construction of the code. Run and test your code!
            ~~~~
            #include <iostream>
            using namespace std;

            string birthSeason (int month, int day) {
                // Write your implementation here.
            }
            ====
            #define CATCH_CONFIG_MAIN
            #include <catch.hpp>

            TEST_CASE("birthSeason function: spring") {
                REQUIRE(birthSeason (5, 3) == "spring");
                REQUIRE(birthSeason (3, 1) == "spring");
                REQUIRE(birthSeason (5, 31) == "spring");
            }

            TEST_CASE("birthSeason function: summer") {
                REQUIRE(birthSeason (7, 5) == "summer");
                REQUIRE(birthSeason (6, 1) == "summer");
                REQUIRE(birthSeason (8, 31) == "summer");
            }

            TEST_CASE("birthSeason function: fall") {
                REQUIRE(birthSeason (11, 24) == "fall");
                REQUIRE(birthSeason (9, 1) == "fall");
                REQUIRE(birthSeason (11, 30) == "fall");
            }

            TEST_CASE("birthSeason function: winter") {
                REQUIRE(birthSeason (2, 20) == "winter");
                REQUIRE(birthSeason (12, 1) == "winter");
                REQUIRE(birthSeason (2, 28) == "winter");
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_5_AC_4q_pp
            :numbered: left
            :adaptive:

            The astronomical start and end dates of the four seasons are based on the position of
            the Earth relative to the Sun. As a result, it changes every year and can be difficult to
            remember. However, the meteorological start and end dates are based on the Gregorian calendar
            and is easier to remember. Spring starts on March 1, summer starts on June 1, fall starts on
            September 1, and winter starts on December 1. Write a function called ``birthSeason``, which takes
            two parameters, ``month`` and ``day``. ``birthSeason`` calculates which season
            the birthday falls in according to the meteorological start and returns a ``string`` with the correct season.
            For example, ``birthSeason (7, 5)`` returns "summer" since July 5 is in the summer. Use the lines to construct
            the code, then go back to complete the Activecode tab.

            -----
            string birthSeason (int month, int day) {
            =====
                if (month >= 3 && month < 6){
                    return "spring";
                }
            =====
                if (month >= 6 && month < 9){
                    return "summer";
                }
            =====
                if (month >= 9 && month < 12){
                    return "fall";
                }
            =====
                if (month == 12 || month < 3){
                    return "winter";
                }
            =====
            }

.. tabbed:: cp_5_AC_6q_q

    .. tab:: Activecode
            
        .. activecode:: cp_5_AC_6q
            :language: cpp
            :practice: T

            A number is a common factor of two other numbers if it divides evenly into both of the
            other numbers. For example, 2 is a common factor of 4 and 18, because 2 goes evenly into
            4 and 18. Write the function ``isCommonFactor``, which takes three parameters,
            ``num1``, ``num2``, and ``factor``. ``isCommonFactor`` returns ``true`` if ``factor`` is a
            factor of both ``num1`` and ``num2``, and returns ``false`` otherwise. Run and test your code!
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            bool isCommonFactor (int num1, int num2, int factor) {
                // Write your implementation here.
            }
            ====
            #define CATCH_CONFIG_MAIN
            #include <catch.hpp>

            TEST_CASE("isCommonFactor function: true cases") {
                REQUIRE(isCommonFactor (24, 8, 4) == 1);
                REQUIRE(isCommonFactor (75, 20, 5) == 1);
            }

            TEST_CASE("isCommonFactor function: false cases") {
                REQUIRE(isCommonFactor (132, 42, 11) == 0);
                REQUIRE(isCommonFactor (74, 23, 3) == 0);
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_5_AC_6q_pp
            :numbered: left
            :adaptive:

            A number is a common factor of two other numbers if it divides evenly into both of the
            other numbers. For example, 2 is a common factor of 4 and 18, because 2 goes evenly into
            4 and 18. Write the function ``isCommonFactor``, which takes three parameters,
            ``num1``, ``num2``, and ``factor``. ``isCommonFactor`` returns ``true`` if ``factor`` is a
            factor of both ``num1`` and ``num2``, and returns ``false`` otherwise. Run and test your code!
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            bool isCommonFactor (int num1, int num2, int factor) {
            =====
                if (num1 % factor == 0 && num2 % factor == 0) {
            =====
                if (num1 % factor == 0 || num2 % factor == 0) { #paired
            =====
                    return true;
            =====
                else {
                    return false;
                }
            =====
                }
            =====
            }

.. tabbed:: cp_5_AC_8q_q

    .. tab:: Activecode

        .. activecode:: cp_5_AC_8q
            :language: cpp
            :practice: T

            In the enchanted Mushroom Forest, there are many different types of
            mushrooms as far as the eye can see. Most of these mushrooms
            can make delicious stews and dishes, but some of them are poisonous.
            Write the function ``isPoisonous``, which takes an ``char size``,
            ``int numSpots``, and ``bool isRed`` as parameters. If a mushroom is large
            ('L') and has fewer than 3 spots, it is poisonous. If a mushroom is small ('S')
            and is red, it is poisonous. If a mushroom has fewer than 3 spots or is not red,
            it is poisonous. Otherwise, it is not. ``isPoisonous`` should return ``true`` if
            the mushroom is poisonous and ``false`` otherwise. Run and test your code!
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            bool isPoisonous (char size, int numSpots, bool isRed) {
                // Write your implementation here.
            }
            ====
            #define CATCH_CONFIG_MAIN
            #include <catch.hpp>

            TEST_CASE("isPoisonous function: true cases") {
                REQUIRE(isPoisonous ('S', 10, 0) == 1);
                REQUIRE(isPoisonous ('S', 10, 0) == 1);
                REQUIRE(isPoisonous ('L', 1, 1) == 1);
            }

            TEST_CASE("isPoisonous function: false cases") {
                REQUIRE(isPoisonous ('L', 4, 1) == 0);
                REQUIRE(isPoisonous ('L', 9, 1) == 0);
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_5_AC_8q_pp
            :numbered: left
            :adaptive:

            In the enchanted Mushroom Forest, there are many different types of
            mushrooms as far as the eye can see. Most of these mushrooms
            can make delicious stews and dishes, but some of them are poisonous.
            Write the function ``isPoisonous``, which takes an ``char size``,
            ``int numSpots``, and ``bool isRed`` as parameters. If a mushroom is large
            ('L') and has fewer than 3 spots, it is poisonous. If a mushroom is small ('S')
            and is red, it is poisonous. If a mushroom has fewer than 3 spots or is not red,
            it is poisonous. Otherwise, it is not. ``isPoisonous`` should return ``true`` if
            the mushroom is poisonous and ``false`` otherwise. Use the lines to construct the 
            code, then go back to complete the Activecode tab.

            -----
            bool isPoisonous (char size, int numSpots, bool isRed) {
            =====
                if (size == 'L' && numSpots < 3) {
                    return true;
                }
            =====
                if (size == 'L' || numSpots < 3) { #paired
                    return true;
                }
            =====
                if (size == 'S' && isRed == true) {
                    return true;
                }
            =====
                if (size == 'S' || isRed == false) { #distractor
                    return true;
                }
            =====
                if (numSpots < 3 || isRed == false) {
                    return true;
                }
            =====
                else {
                    return false;
                }
            =====
            }

.. tabbed:: cp_5_AC_10q_q

    .. tab:: Activecode

        .. activecode:: cp_5_AC_10q
            :language: cpp
            :practice: T

            Write the function ``digitSum`` which takes an ``int num`` as a parameter
            and returns the sum of all its digits. For example, ``digitSum (1423)``
            would return 10. Use recursion. Run and test your code! Select the Parsonsprob
            tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            int digitSum (int num) {
                // Write your implementation here.
            }
            ====
            #define CATCH_CONFIG_MAIN
            #include <catch.hpp>

            TEST_CASE("digitSum function") {
                REQUIRE(digitSum (123) == 6);
                REQUIRE(digitSum (8739) == 27);
                REQUIRE(digitSum (440) == 8);
                REQUIRE(digitSum (2) == 2);
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_5_AC_10q_pp
            :numbered: left
            :adaptive:

            Write the function ``digitSum`` which takes an ``int num`` as a parameter
            and returns the sum of all its digits. For example, ``digitSum (1423)``
            would return 10. Use recursion. Use the lines to construct the code, then
            go back to complete the Activecode tab.      

            -----
            int digitSum (int num) {
            =====
                if (num == 0) {
                    return 0;
                }
            =====
                if (num == 0) { #paired
                    return num;
                }
            =====
                return (num % 10 + digitSum(num / 10));
            =====
                return (num % 10 + digitSum(num)); #paired
            =====
                return (digitsum(num) % 10); #distractor
            =====
            }
