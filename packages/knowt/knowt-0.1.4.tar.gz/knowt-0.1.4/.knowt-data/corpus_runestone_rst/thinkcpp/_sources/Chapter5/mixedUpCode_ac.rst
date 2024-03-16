Activecode Exercises
----------------------

Answer the following **Activecode** questions to
assess what you have learned in this chapter.

.. tabbed:: mucp_5_1_ac

    .. tab:: Question

        .. activecode:: mucp_5_1_ac_q
           :language: cpp

           Vacation time! But before you go, you need to convert your currency.
           Let's write the code for the ``dollarToYen`` function. dollarToYen
           takes dollar as a parameter and returns the equivalent amount of Japanese yen.
           The conversion rate is 1 USD equals 105.42 Japanese yen.
           Write the code that performs this conversion.
           ~~~~
           #include <iostream>
           using namespace std;
           // YOUR CODE HERE


           ====
           #define CATCH_CONFIG_MAIN
           #include <catch.hpp>

           TEST_CASE("dollarToYen function") {
              REQUIRE(dollarToYen(1) == 105.42);
              REQUIRE(dollarToYen(2) == 210.84);
           }

    .. tab:: Answer

        .. activecode:: mucp_5_1_ac_a
           :language: cpp

           Below is one way to write the function. You need to make sure your function's output accounts for decimal values.
           ~~~~
           #include <iostream>
           using namespace std;

           double dollarToYen (double dollar) {
               return 105.42 * dollar;
           }

           ====
           #define CATCH_CONFIG_MAIN
           #include <catch.hpp>

           TEST_CASE("dollarToYen function") {
              REQUIRE(dollarToYen(1) == 105.42);
              REQUIRE(dollarToYen(2) == 210.84);
           }


.. tabbed:: mucp_5_2_ac

    .. tab:: Question

        .. activecode:: mucp_5_2_ac_q
           :language: cpp

           When you buy something, you also need to pay sales tax. For example,
           a nice shirt could be labeled with a price of exactly $20, but when 
           you pay, you actually need to pay $21.20 in a state with 6% sales tax.
           However, different states have different tax rates. Write the function
           ``priceWithTax``, which takes price and percentTax as parameters.
           priceWithTax calculates the price after tax and returns it.
           For example, priceWithTax(20,6) returns 21.2.
           ~~~~
           #include <iostream>
           using namespace std;
           // YOUR CODE HERE


           ====
           #define CATCH_CONFIG_MAIN
           #include <catch.hpp>

           TEST_CASE("priceWithTax function") {
              REQUIRE(priceWithTax(20,6) == 21.2);
              REQUIRE(priceWithTax(100,0) == 100);
           }

    .. tab:: Answer

        .. activecode:: mucp_5_2_ac_a
           :language: cpp

           Below is one way to write the function. You need to make sure your function returns cent values
           ~~~~
           #include <iostream>
           using namespace std;
           
           double priceWithTax (double price, double percentTax) {
               return (1 + percentTax / 100) * price;
           }

           ====
           #define CATCH_CONFIG_MAIN
           #include <catch.hpp>

           TEST_CASE("priceWithTax function") {
              REQUIRE(priceWithTax(20,6) == 21.2);
              REQUIRE(priceWithTax(100,0) == 100);
           }



.. tabbed:: mucp_5_3_ac

    .. tab:: Question

        .. activecode:: mucp_5_3_ac_q
            :language: cpp

            Most assignments and tests are graded as a percentage, but final
            grades are letters. Let's write the code for the ``percentToLetter`` function. 
            percentToLetter takes a percentage and returns the corresponding
            letter grade. A 90 and above is an 'A', an 80 and above is a 'B', a 70 and above
            is a 'C', and anything under a 70 is an 'F'. Write the necessary code to 
            convert a grade percentage to a letter grade.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


            ====
            #define CATCH_CONFIG_MAIN
            #include <catch.hpp>

            TEST_CASE("percentToLetter function") {
               REQUIRE(percentToLetter(0) == 'F');
               REQUIRE(percentToLetter(90) == 'A');
            }           

    .. tab:: Answer

        .. activecode:: mucp_5_3_ac_a
            :language: cpp

            Below is one way to write the function. Your syntax for the letter returns much match the return variable type of the function
            ~~~~
            #include <iostream>
            using namespace std;

            char percentToLetter (double percentage){
                if (percentage >= 90){
                    return 'A';
                }
                else if (percentage >= 80){
                    return 'B';
                }
                else if (percentage >= 70){
                    return 'C';
                }
                else {
                    return 'F';
                }
            }

            ====
            #define CATCH_CONFIG_MAIN
            #include <catch.hpp>

            TEST_CASE("percentToLetter function") {
               REQUIRE(percentToLetter(0) == 'F');
               REQUIRE(percentToLetter(90) == 'A');
            }     


.. tabbed:: mucp_5_4_ac

    .. tab:: Question

        .. activecode:: mucp_5_4_ac_q
            :language: cpp

            Let's write the code for the ``triangleArea`` function. triangleArea
            takes two parameters, base and height. It returns the 
            area of the triangle using the formula 1/2 * base * height.
            Write the necessary code to find the area of a triangle.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


            ====
            #define CATCH_CONFIG_MAIN
            #include <catch.hpp>

            TEST_CASE("triangleArea function") {
               REQUIRE(triangleArea(4.5,6.2) == 13.95);
               REQUIRE(triangleArea(4,5) == 10.0);
            }

    .. tab:: Answer

        .. activecode:: mucp_5_4_ac_a
            :language: cpp

            Below is one way to write the function. Your function must take in more than integer base and height values and return more than integer area values.
            ~~~~
            #include <iostream>
            using namespace std;

            double triangleArea (double base, double height){
                return 0.5 * base * height;
            }

            ====
            #define CATCH_CONFIG_MAIN
            #include <catch.hpp>

            TEST_CASE("triangleArea function") {
               REQUIRE(triangleArea(4.5,6.2) == 13.95);
               REQUIRE(triangleArea(4,5) == 10.0);
            }


.. tabbed:: mucp_5_5_ac

    .. tab:: Question

        .. activecode:: mucp_5_5_ac_q
            :language: cpp

            Let's write the code for the ``cylinderVolume`` function. cylinderVolume
            takes two parameters, radius and height. It returns the 
            volume of the cylinder using the formula pi * radius * radius * height.
            Write the necessary code to find the volume of a cylinder.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE
            

            ====
            #define CATCH_CONFIG_MAIN
            #include <catch.hpp>

            TEST_CASE("cylinderVolume function") {
               REQUIRE(cylinderVolume(2.5,3.0) == 58.875);
               REQUIRE(cylinderVolume(11.0,4.5) == 1709.73);
               REQUIRE(cylinderVolume(6.25,5.0) == 613.28125);
            }

    .. tab:: Answer

        .. activecode:: mucp_5_5_ac_a
            :language: cpp

            Below is one way to write the function. Your function should incorporate the value for pi.
            ~~~~
            #include <iostream>
            using namespace std;

            double cylinderVolume(double radius, double height){
                double pi = 3.14;
                return pi * radius * radius * height;
            }

            ====
            #define CATCH_CONFIG_MAIN
            #include <catch.hpp>

            TEST_CASE("cylinderVolume function") {
               REQUIRE(cylinderVolume(2.5,3.0) == 58.875);
               REQUIRE(cylinderVolume(11.0,4.5) == 1709.73);
               REQUIRE(cylinderVolume(6.25,5.0) == 613.28125);
            }


.. tabbed:: mucp_5_6_ac

   .. tab:: Question

      .. activecode:: mucp_5_6_ac_q
         :language: cpp

         On a distant planet, depending on the characteristics of an egg, a kenchic,
         an ooseg, or a guinpen might hatch from it. Let's write the function 
         ``birdType`` which returns an int corresponding to each type of bird
         (1 for kenchic, 2 for ooseg, and 3 for guinpen). If the egg is round, then it is a 
         guinpen. Otherwise, if the egg is round and it isn't gray, then it is a kenchic. If 
         it isn't a guinpen and it isn't a kenchic, then it's an ooseg. Write the necessary
         code to classify these eggs. 
         ~~~~
         #include <iostream>
         using namespace std;
         // YOUR CODE HERE


         ====
         #define CATCH_CONFIG_MAIN
         #include <catch.hpp>

         TEST_CASE("birdType function") {
            REQUIRE(birdType(1,1) == 3);
            REQUIRE(birdType(1,0) == 1);
            REQUIRE(birdType(0,0) == 2);
         }

   .. tab:: Answer

      .. activecode:: mucp_5_6_ac_a
         :language: cpp

         Below is one way to write the function. 
         ~~~~
         #include <iostream>
         using namespace std;

         int birdType(bool isRound, bool isGray){
            if (isRound && !isGray){
               return 1;
            }
            else if(!isRound && isGray){
               return 2;
            }
            else{
               return 3;
            }
         }

         ====
         #define CATCH_CONFIG_MAIN
         #include <catch.hpp>

         TEST_CASE("birdType function") {
            REQUIRE(birdType(1,1) == 3);
            REQUIRE(birdType(1,0) == 1);
            REQUIRE(birdType(0,0) == 2);
         }

.. tabbed:: mucp_5_7_ac

   .. tab:: Question

      .. activecode:: mucp_5_7_ac_q
         :language: cpp

         Let's write the code for the ``isDoubleDigit`` function. isDoubleDigit
         takes num as a parameter. isDoubleDigit returns true if 
         num is a double digit number and returns false otherwise.
         Write the necessary code to determine if a number is a double digit number.
         ~~~~
         #include <iostream>
         using namespace std;
         // YOUR CODE HERE


         ====
         #define CATCH_CONFIG_MAIN
         #include <catch.hpp>

         TEST_CASE("isDoubleDigit function") {
            REQUIRE(isDoubleDigit(10) == true);
            REQUIRE(isDoubleDigit(100) == false);
         }

   .. tab:: Answer

      .. activecode:: mucp_5_7_ac_a
         :language: cpp

         Below is one way to write the function. Your function must account for numbers that are greater than 100.
         ~~~~
         #include <iostream>
         using namespace std;

         bool isDoubleDigit (int num){
            if(num >= 10 && num < 100){
               return true;
            }
            else {
               return false;
            }
         }

         ====
         #define CATCH_CONFIG_MAIN
         #include <catch.hpp>

         TEST_CASE("isDoubleDigit function") {
            REQUIRE(isDoubleDigit(10) == true);
            REQUIRE(isDoubleDigit(100) == false);
         }
         

.. tabbed:: mucp_5_8_ac

   .. tab:: Question

      .. activecode:: mucp_5_8_ac_q
         :language: cpp

         Let's write the code for the ``Compare`` function. Compare
         takes two integers a, b. Compare returns 1 if 
         a is greater than b, -1 if a is less than b and 0 if they are equal.
         Write the necessary code to compare two integers.
         ~~~~
         #include <iostream>
         using namespace std;
         // YOUR CODE HERE


         ====
         #define CATCH_CONFIG_MAIN
         #include <catch.hpp>

         TEST_CASE("Compare function") {
            REQUIRE(Compare(10,49) == -1);
            REQUIRE(Compare(10,10) == 0);
            REQUIRE(Compare(10,5) == 1);
         }

   .. tab:: Answer

      .. activecode:: mucp_5_8_ac_a
         :language: cpp

         Below is one way to write the function. Your function must account for equal integers.
         ~~~~
         #include <iostream>
         using namespace std;

         int Compare(int a, int b){
            if (a > b){
               return 1;
            }
            else if(a < b){
               return -1;
            }
            else{
               return 0;
            }
         }

         ====
         #define CATCH_CONFIG_MAIN
         #include <catch.hpp>

         TEST_CASE("Compare function") {
            REQUIRE(Compare(10,49) == -1);
            REQUIRE(Compare(10,10) == 0);
            REQUIRE(Compare(10,5) == 1);
         }


.. tabbed:: mucp_5_9_ac

   .. tab:: Question

      .. activecode:: mucp_5_9_ac_q
         :language: cpp

         Let's write the code for the ``isFactor`` function. isFactor
         takes two parameters, num and factor.
         isFactor returns true if factor is a factor of num 
         and returns false otherwise. Write the necessary code to deternube is a number
         is a factor of another.
         ~~~~
         #include <iostream>
         using namespace std;
         // YOUR CODE HERE


         ====
         #define CATCH_CONFIG_MAIN
         #include <catch.hpp>

         TEST_CASE("isFactor function") {
            REQUIRE(isFactor(8,2) == true);
            REQUIRE(isFactor(7,4) == false);
            REQUIRE(isFactor(9,1) == true);
         }

   .. tab:: Answer

      .. activecode:: mucp_5_9_ac_a
         :language: cpp

         Below is one way to write the function. The modulo (%) operator performs the necessary calculation.
         ~~~~
         #include <iostream> 
         using namespace std;

         bool isFactor(int num, int factor){
            if (num % factor == 0){
               return true;
            }
            else {
               return false;
            }
         }

         ====
         #define CATCH_CONFIG_MAIN
         #include <catch.hpp>

         TEST_CASE("isFactor function") {
            REQUIRE(isFactor(8,2) == true);
            REQUIRE(isFactor(7,4) == false);
            REQUIRE(isFactor(9,1) == true);
         }


.. tabbed:: mucp_5_10_ac

   .. tab:: Question

      .. activecode:: mucp_5_10_ac_q
         :language: cpp

         Let's write the code for the ``isPerfectSquare`` function. isPerfectSquare
         takes input as a parameter and returns true if input is a 
         perfect square and returns false otherwise. Write the necessary code
         to determine if a number is a perfect square.
         ~~~~
         #include <iostream>
         #include <math.h>
         using namespace std;
         // YOUR CODE HERE


         ====
         #define CATCH_CONFIG_MAIN
         #include <catch.hpp>

         TEST_CASE("isPerfectSquare function") {
            REQUIRE(isPerfectSquare(4) == true);
            REQUIRE(isPerfectSquare(16) == true);
            REQUIRE(isPerfectSquare(10) == false);
         }

   .. tab:: Answer

      .. activecode:: mucp_5_10_ac_a
         :language: cpp

         Below is one way to write the function.
         ~~~~
         #include <iostream>
         #include <math.h>
         using namespace std;

         bool isPerfectSquare(int input){
            int root = sqrt(input);
            if(pow(root,2) == input){
               return true;
            }
            else{
               return false;
            }
         }

         ====
         #define CATCH_CONFIG_MAIN
         #include <catch.hpp>

         TEST_CASE("isPerfectSquare function") {
            REQUIRE(isPerfectSquare(4) == true);
            REQUIRE(isPerfectSquare(16) == true);
            REQUIRE(isPerfectSquare(10) == false);
         }


.. tabbed:: mucp_5_11_ac

   .. tab:: Question
      
      .. activecode:: mucp_5_11_ac_q
         :language: cpp

         Most bacteria cultures grow exponentially. For this problem,
         assume the number of cells in a bacterial culture doubles every hour.
         Let's write the code for the ``countBacteria`` function. countBacteria 
         takes hour as a parameter and returns the number of bacteria cells
         after hour hours. Assume when hour is 0, there is one cell. When 
         hour is one, the number of cells doubles to two. When hour is two, 
         the number of cells doubles to four. Use recursion. Write the 
         necesary code to count the bacteria.
         ~~~~
         #include <iostream>
         using namespace std;
         // YOUR CODE HERE


         ====
         #define CATCH_CONFIG_MAIN
         #include <catch.hpp>

         TEST_CASE("countBacteria function") {
            REQUIRE(countBacteria(0) == 1);
            REQUIRE(countBacteria(5) == 32);
         }

   .. tab:: Answer

      .. activecode:: mucp_5_11_ac_a
         :language: cpp

         Below is one way to write the function.
         ~~~~
         #include <iostream> 
         using namespace std;

         int countBacteria (int hour) {
            if (hour == 0) {
               return 1;
            }
            else {
               return 2 * countBacteria (hour -1);
            }
         }

         ====
         #define CATCH_CONFIG_MAIN
         #include <catch.hpp>

         TEST_CASE("countBacteria function") {
            REQUIRE(countBacteria(0) == 1);
            REQUIRE(countBacteria(5) == 32);
         }