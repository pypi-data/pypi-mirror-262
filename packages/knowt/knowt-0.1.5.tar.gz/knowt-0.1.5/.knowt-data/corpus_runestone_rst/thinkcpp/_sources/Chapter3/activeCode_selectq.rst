Activecode Exercises
--------------------

Answer the following **Activecode** questions to
assess what you have learned in this chapter.


.. tabbed:: functions_a2_q

    .. tab:: Activecode

        .. activecode:: functions_a2
            :language: cpp

            Fix the code below so that it prints "2 elephants". Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            void printAnimals(string a, int b) {
                cout << b << a;
            }

            int main () {
                // DO NOT MODIFY ANYTHING BELOW THIS LINE
                printAnimals(2, "elephants");
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: functions_a2_pp
            :numbered: left
            :adaptive:

            Fix the code below so that it prints "2 elephants". Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            void printAnimals(int a, string b) {
            =====
            void printAnimals(string a, int b) { #paired
            =====
                cout << a << " " << b;
            =====
                cout << b << " " << a; #paired
            =====
                cout << b << a; #paired
            =====
            }
            =====
            int main() {
            =====
                printAnimals(2, "elephants");
            =====
            }


.. tabbed:: functions_a4_q

    .. tab:: Activecode

        .. activecode:: functions_a4
            :language: cpp

            Finish the code below so that it calculates the common log of ``a`` minus the *natural* log of ``a`` and prints the difference. You will need to use cmath functions. 
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            #include <cmath>
            using namespace std;

            void logSubtraction (double a) {
                // Create the variable difference and assign it to the difference mentioned in the instructions
                
                cout << difference;
            }

            int main () {
                // DO NOT MODIFY ANYTHING BELOW THIS LINE
                cout << "Testing with a = 8..." << endl; cout << "    Your solution has difference = "; logSubtraction(8); cout << endl; cout << "    The correct solution has difference = -1.17635" << endl; cout << "Testing with a = -2..." << endl; cout << "    Your solution has difference = "; logSubtraction(-2); cout << endl; cout << "    The correct solution has difference = nan";
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: functions_a4_pp
            :numbered: left
            :adaptive:

            Finish the code below so that it calculates the common log of ``a`` minus the *natural* log of ``a`` and prints the difference. You will need to use cmath functions. Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            void logSubtraction (double a) {
            =====
                double difference;
            =====
                int difference; #paired
            =====
                difference = log10(a) - log(a);
            =====
                difference = log(a) - log10(a); #paired
            =====
                cout << difference;
            =====
            }


.. tabbed:: functions_a6_q

    .. tab:: Activecode
        
        .. activecode:: functions_a6
            :language: cpp

            Write a function called ``intDivision`` that takes two doubles as parameters and prints the quotient of the **integer division** of the first number divided by the second.  Be sure to include any necessary headers.
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            void intDivision () {

            }

            int main () {
                // DO NOT MODIFY ANYTHING BELOW THIS LINE
                cout << "Testing with a = 2.4, b = 6.8..." << endl; cout << "    Your solution has a quotient of "; intDivision(2.4, 6.8); cout << endl; cout << "    The correct solution has a quotient of 0" << endl; cout << "Testing with a = -8.6, b = 4.2..." << endl; cout << "    Your solution has a quotient of "; intDivision(-8.6, 4.2); cout << endl; cout << "    The correct solution has a quotient of -2";
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: functions_a6_pp
            :numbered: left
            :adaptive:

            Write a function called ``intDivision`` that takes two doubles as parameters and prints the quotient of the **integer division** of the first number divided by the second.
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            void intDivision( double a, double b ) {
            =====
            void intDivision( int a, int b ) { #paired
            =====
                int difference;
            =====
                double difference; #paired
            =====
                difference = a / b;
            =====
                difference = b / a; #distractor
            =====
                cout << difference << endl;
            =====
            }


.. tabbed:: functions_a8_q

    .. tab:: Activecode
            
        .. activecode:: functions_a8
            :language: cpp
        
            Write a function called ``volumePrism`` that takes three ``double`` sidelengths as parameters, and calculates and prints the volume of a the rectangular prism.  Be sure to include any necessary headers.
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            void volumePrism () {
                
            }

            int main () {
                // DO NOT MODIFY ANYTHING BELOW THIS LINE
                cout << "Testing with a = 3, b = 4, c = 5..." << endl; cout << "    Your solution calculated a volume of "; volumePrism(3,4,5); cout << endl; cout << "    The correct solution calculates a volume of 60" << endl; cout << "Testing with a = 5.7, b = 3.9, c = 1.3..." << endl; cout << "    Your solution calculated a volume of "; volumePrism(5.7,3.9,1.3); cout << endl; cout << "    The correct solution calculates a volume of 28.899";
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: functions_a8_pp
            :numbered: left
            :adaptive:

            Write a function called ``volumePrism`` that takes three ``double`` sidelengths as parameters, and calculates and prints the volume of a the rectangular prism.
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            void volumePrism (double s1, double s2, double s3) {
            =====
            void volumePrism (int s1, int s2, int s3) { #paired
            =====
                double volume;
            =====
                int volume; #distractor
            =====
                volume = s1 * s2 * s3;
            =====
                cout << volume << endl;
            =====
            }


.. tabbed:: functions_a10_q

    .. tab:: Activecode

        .. activecode:: functions_a10
           :language: cpp

           Write a function called ``volumeSphere`` that takes a ``double`` radius as a parameter, and calculates and prints the volume of a sphere with that radius.  Use 3.14 for ``pi``.  Be sure to include any necessary headers.
           Select the Parsonsprob tab for hints for the construction of the code.
           ~~~~
           #include <iostream>
           using namespace std;

           void volumeSphere () {
            
           }
            
           int main() {
               // DO NOT MODIFY ANYTHING BELOW THIS LINE
               cout << "Testing with radius = 3..." << endl; cout << "    Your solution calculated a volume of "; volumeSphere(3); cout << endl; cout << "    The correct solution calculates a volume of 113.04" << endl; cout << "Testing with radius = 3.24..." << endl; cout << "    Your solution calculated a volume of "; volumeSphere(3.24); cout << endl; cout << "    The correct solution calculates a volume of 142.398";
           }

    .. tab:: Parsonsprob

        .. parsonsprob:: functions_a10_pp
            :numbered: left
            :adaptive:

            Write a function called ``volumeSphere`` that takes a ``double`` radius as a parameter, and calculates and prints the volume of a sphere with that radius.  Use 3.14 for ``pi``.
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            void volumeSphere(double radius) {
            =====
                double pi = 3.14;
            =====
                double volume;
            =====
                int volume; #paired
            =====
                volume = 4 * pi * radius * radius * radius / 3;
            =====
                volume = 4 / 3 * pi * radius ^ 3; #distractor
            =====
                cout << volume << endl;
            =====
            }
