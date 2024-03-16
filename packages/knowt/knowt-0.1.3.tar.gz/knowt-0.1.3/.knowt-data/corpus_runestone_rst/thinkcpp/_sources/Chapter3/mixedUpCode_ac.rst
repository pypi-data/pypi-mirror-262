Activecode Exercises
-----------------------

Answer the following **Activecode** questions to
assess what you have learned in this chapter.


.. tabbed:: functions_p9_ac

    .. tab:: Question

        .. activecode:: functions_p9_ac_q
            :language: cpp

            Construct a function ``printInteger`` that correctly prints the integer conversion of the passed double. 
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


            // DO NOT MODIFY BELOW THIS LINE
            int main() {
                double x = 3.14159265;
                printInteger(x);
            }

    .. tab:: Answer

        .. activecode:: functions_p9_ac_a
            :language: cpp

            Below is one way to write the ``printInteger`` function.
            ~~~~
            #include <iostream>
            using namespace std;

            void printInteger (double d) {
                d = int(d);
                cout << d;
            }

            int main() {
                double x = 3.14159265;
                printInteger(x);
            }


.. tabbed:: functions_p0_ac

    .. tab:: Question

        .. activecode:: functions_p0_ac_q
            :language: cpp

            Construct a function called ``newLine`` that takes no arguments and prints a blank line.  Then construct another function called ``divider`` that prints two blank lines separated by a line of ". . . . . . . . . . . ."
            ~~~~
            #include <iostream> 
            using namespace std;
            // YOUR CODE HERE


            // DO NOT MODIFY BELOW THIS LINE
            int main() { // Implement the two functions
                newLine();
                divider();
            }

    .. tab:: Answer

        .. activecode:: functions_p0_ac_a
            :language: cpp

            Below is one way to write the two functions, ``newLine`` and ``divider``. 
            ~~~~
            #include <iostream>
            using namespace std;

            void newLine () {
                cout << endl;
            }  //newLine

            void divider () {
                newLine ();  //first call
                cout << ". . . . . . . . . . . . " << endl;
                newLine ();  //second call
            }  //divider

            int main() { // Use the two functions
                newLine();
                divider();
            }


.. tabbed:: functions_p1_ac

    .. tab:: Question

        .. activecode:: functions_p1_ac_q
            :language: cpp

            Construct a function, ``volumeCone``, that takes as inputs the radius then the height and correctly calculates the volume of a cone with as much precision as possible and prints the value to the terminal.  Use 3.14 for pi.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


            // DO NOT MODIFY BELOW THIS LINE
            int main() {
                double r = 2.5;
                double h = 5.5;
                volumeCone(r,h);
            } 

    .. tab:: Answer

        .. activecode:: functions_p1_ac_a
            :language: cpp

            Below is one way to write the ``volumeCone`` function. 
            ~~~~
            #include <iostream>
            using namespace std;

            void volumeCone (double r, double h) {
                double vol = 1/3.0 * 3.14 * r * r * h;
                cout << vol;
            }


.. tabbed:: functions_p3_ac

    .. tab:: Question

        .. activecode:: functions_p3_ac_q
            :language: cpp

            Construct a function, ``sineDegrees``, that prints the sin of an angle given in degrees. Use 3.14 for pi.
            ~~~~
            #include <iostream>
            #include <cmath>
            using namespace std;
            // YOUR CODE HERE


            // DO NOT MODIFY BELOW THIS LINE
            int main() {
                double degrees = 25.00;
                sineDegrees(degrees);
            }

    .. tab:: Answer

        .. activecode:: functions_p3_ac_a
            :language: cpp

            Below is one way to write the ``sineDegrees`` function.
            ~~~~
            #include <iostream>
            #include <cmath>
            using namespace std;

            void sineDegrees (double d) {
                double r = d * (2 * 3.14) / 360.0;
                double sine = sin(r);
                cout << sine;
            }

            int main() {
                double degrees = 25.00;
                sineDegrees(degrees);
            }


.. tabbed:: functions_p4_ac

    .. tab:: Question

        .. activecode:: functions_p4_ac_q
            :language: cpp

            Construct a function, ``finalPrice``, that prints the price (with 8% sales tax) of an item with after using a 30% off coupon.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


            // DO NOT MODIFY BELOW THIS LINE
            int main() {
                double item = 200.50;
                finalPrice(item);
            }

    .. tab:: Answer

        .. activecode:: functions_p4_ac_a
            :language: cpp

            Below is one way to write the ``finalPrice`` function.
            ~~~~
            #include <iostream>
            using namespace std;

            void finalPrice (double item) {
                double discount = item * 0.30;
                double final = (item - discount) * 1.08;
                cout << final;
            }


.. tabbed:: functions_p5_ac

    .. tab:: Question

        .. activecode:: functions_p5_ac_q
            :language: cpp

            Suppose you have already defined a function called ``sumOfSquares`` which returns the sum of the squares of two numbers and ``root`` which returns the square root of a number.  Construct a function that calculates the hypotenuse of the right triangle and prints the three sidelengths.
            ~~~~
            #include <iostream>
            #include <math.h>
            using namespace std;
            // DO NOT MODIFY THIS CODE

            double sumOfSquares ( double s2, double s1) {
                return (s2 * s2) + (s1 * s1);
            }

            double root ( double num ) {
                return sqrt(num);
            }

            // YOUR CODE HERE


    .. tab:: Question

        .. activecode:: functions_p5_ac_a
            :language: cpp

            Below is one way to write the ``sumOfSquares`` and ``root`` functions. 
            ~~~~
            #include <iostream> 
            #include <math.h>
            using namespace std;

            double sumOfSquares ( double s2, double s1) {
                return (s2 * s2) + (s1 * s1);
            }

            double root ( double num ) {
                return sqrt(num);
            }

            int main () {
                double s1 = 4.8;
                double s2 = 3.8;
                double sqSum = sumOfSquares(s2, s1);
                double hyp = root(sqSum);
                cout << "The sides of the triangle are: " << s1 << ", " << s2 << ", " << hyp;
            }


.. tabbed:: functions_p6_ac

    .. tab:: Question

        .. activecode:: functions_p6_ac_q
            :language: cpp

            The chickens from the previous chapter are infuriated.  Construct a function, ``eatMore``, that prints "Eat" on the first line, "More" on the second line, and the name of the passed animal on the fourth line, followed by an exclamation point.  
            ~~~~
            #include <iostream> 
            using namespace std;
            // YOUR CODE HERE


            // DO NOT MODIFY BELOW THIS LINE
            int main() {
                string animal = "Chicken";
                eatMore(animal);
            }

    .. tab:: Answer

        .. activecode:: functions_p6_ac_a
            :language: cpp

            Below is one way to write the ``eatMore`` function.
            ~~~~
            #include <iostream> 
            using namespace std;

            void eatMore (string animal) {
                cout << "Eat";
                cout << endl; cout << "More" << endl;
                cout << endl;
                cout << animal << "!" << endl;
            }

            int main() {
                string animal = "Chicken";
                eatMore(animal);
            }


.. tabbed:: functions_p7_ac

    .. tab:: Question

        .. activecode:: functions_p7_ac_q
            :language: cpp

            Construct a function, ``printAmount``, that takes a dollar amount and cent amount and prints the total amount of money that you have. Hint: the mod operator '%' returns the remainder of a division.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


            // DO NOT MODIFY BELOW THIS LINE
            int main() {
                int dollars = 45;
                int cents = 56;
                printAmount(dollars, cents);
            }

    .. tab:: Answer

        .. activecode:: functions_p7_ac_a
            :language: cpp

            Below is onw way to write the ``printAmount`` function.
            ~~~~
            #include <iostream>
            using namespace std;

            void printAmount (int dollars, int cents) {
                int dollarTotal = dollars + cents / 100;
                double centTotal = cents % 100;
                cout << "$" << dollarTotal << "." << centTotal;
            }

            int main() {
                int dollars = 45;
                int cents = 56;
                printAmount(dollars, cents);
            }


.. tabbed:: functions_p8_ac

    .. tab:: Question

        .. activecode:: functions_p8_ac_q
            :language: cpp

            In Michigan, the probability that it snows on any given day in the winter is about 14%.  The probability of having a snow day on any given day in the winter is about 4%.  The probability that is snows and you have a snow day is 8%.  
            Construct and call a function, ``conditionalProb``, that calculates the probability of a having a snow day, given the fact that it will snow tonight.  
            For reference, the formula for conditional probability is: P(A|B) = P(B and A) / P(B).
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: functions_p8_ac_a
            :language: cpp

            Below is one way to write and call the ``conditionalProb`` function.
            ~~~~
            #include <iostream>
            using namespace std;

            void conditionalProb (double B, double both) {
                double prob = both / B;
                cout << prob;
            } //conditionalProb
            
            int main () {
                double pSnow = 0.14;
                double pBoth = 0.08;
                conditionalProb(pSnow, pBoth);
            } //main


.. tabbed:: functions_p2_ac

    .. tab:: Question

        .. activecode:: functions_p2_ac_q
            :language: cpp

            Your final grade is determined by a midterm component (each midterm is worth 20% of the grade) and a final component that is worth 60% of the grade. In order to avoid any discrepancies with students who's grades are on the fence, your teacher follows this strict grading scale: 
            [0%,60%) = F, [60%, 70%) = D, [70%, 80%) = C, [80%, 90%) = B and [90%, 100%] = A. He does not round until the very end.  
            Construct a function, ``finalGrade``, that determines a student's final grade percentage according to this grading scheme and prints the result.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: functions_p2_ac_a
            :language: cpp

            Below is one way to construct the ``finalGrade`` function. 
            ~~~~
            #include <iostream>
            using namespace std;

            void finalGrade (double m1, double m2, double f) {
                double m_comp = m1 * 0.2 + m2 * 0.2;
                double f_comp = f * 0.6;
                double final_grade = m_comp + f_comp;
                cout << int(final_grade);
            }

            int main() {
                finalGrade(80,70,80);
            }