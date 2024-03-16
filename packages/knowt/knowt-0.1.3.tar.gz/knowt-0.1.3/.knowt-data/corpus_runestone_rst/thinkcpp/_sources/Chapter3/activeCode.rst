Activecode Exercises
--------------------

Answer the following **Activecode** questions to
assess what you have learned in this chapter.


.. tabbed:: functions_a1

   .. tab:: Question

      .. activecode:: functions_a1q
         :language: cpp

         Fix the errors in the code below so that it prints the area of a circle with radius 5.  Use cmath functions to get an accurate value for pi.
         ~~~~
         #include <iostream>
         #include <cmath>
         using namespace std;

         void printArea(int r) {
             double pi = acos(1.0);
             double area = pi * r ^ 2;
             cout << area;
         }

         int main () {
             // DO NOT MODIFY ANYTHING BELOW THIS LINE
             cout << "Testing with radius = 5..." << endl; cout << "    Your function had area = "; printArea(5); cout << endl; cout << "    The correct solution has area = 78.5398" << endl; cout << "Testing with radius = 7.5..." << endl; cout << "    Your function had area = "; printArea(7.5); cout << endl; cout << "    The correct solution has area = 176.715";
         }

   .. tab:: Answer

      .. activecode:: functions_a1a
         :language: cpp

         Below is one way to fix the program.  C++ doesn't use the ``^`` operator for exponents.  We can get the square of ``r`` by multiplying it by itself.  We call the function with an argument of ``5``.
         ~~~~
         #include <iostream>
         #include <cmath>
         using namespace std;

         void printArea(double r) {
             double pi = acos(-1.0);
             double area = pi * r * r;
             cout << area;
         }


.. selectquestion:: functions_a2_sq
    :fromid: functions_a2, functions_a2_pp
    :toggle: lock


.. tabbed:: functions_a3

   .. tab:: Question

      .. activecode:: functions_a3q
         :language: cpp

         Fix the code below so that it prints ``12 / 8 = 1.5.``
         ~~~~
         #include <iostream>
         using namespace std;

         void divide (int a, int b) {
             cout << a / b;
         }

         int main () {
             int a = 8;
             int b = 12;

             // DO NOT MODIFY ANYTHING BELOW THIS LINE
             cout << b << " / " << a << " = "; divide (b, a);
         }

   .. tab:: Answer

      .. activecode:: functions_a3a
         :language: cpp

         Below is one way to fix the program.  It's crucial that you input your arguments in the correct order so as to avoid a semantic error.  Also, it's important that you understand that when you divide two integers... you will get an integer as a result.
         ~~~~
         #include <iostream>
         using namespace std;

         void divide (double a, double b) {
             cout << a / b;
         }

         int main () {
             int a = 8;
             int b = 12;
             cout << b << " / " << a << " = "; divide (b, a);
         }


.. selectquestion:: functions_a4_sq
    :fromid: functions_a4, functions_a4_pp
    :toggle: lock


.. tabbed:: functions_a5

   .. tab:: Question

      .. activecode:: functions_a5q
         :language: cpp

         Finish the code below so that it prints "First Line", a border, and "Second Line." on three separate lines.
         ~~~~
         #include <iostream>
         using namespace std;

         void border () {
             cout << "------------" << endl;
         }

         int main () {
             // Write some code below to call the function appropriately

         }

   .. tab:: Answer

      .. activecode:: functions_a5a
         :language: cpp

         Below is one way to complete the program.
         ~~~~
         #include <iostream>
         using namespace std;

         void border () {
             cout << "------------" << endl;
         }

         int main () {
             cout << "First Line." << endl;
             border();
             cout << "Second Line." << endl;
         }


.. selectquestion:: functions_a6_sq
    :fromid: functions_a6, functions_a6_pp
    :toggle: lock


.. tabbed:: functions_a7

   .. tab:: Question

      .. activecode:: functions_a7q
         :language: cpp

         Write a function called gpaBoost that prints your GPA rounded up to the nearest point.  If your GPA is already at the nearest point, there is no rounding.  Be sure to include any necessary headers.
         ~~~~
         #include <iostream>
         #include <cmath>
         using namespace std;
         void gpaBoost () {

         }

         int main () {
             // DO NOT MODIFY ANYTHING BELOW THIS LINE
             cout << "Testing with GPA = 2.513..." << endl; cout << "    Your solution rounded the GPA to "; gpaBoost(2.513); cout << endl; cout << "    The correct solution rounds the GPA to 3.000" << endl; cout << "Testing with GPA = 4.000..." << endl; cout << "    Your solution rounded the GPA to "; gpaBoost(4.000); cout << endl; cout << "    The correct solution rounds the GPA to 4.000";
         }

   .. tab:: Answer

      .. activecode:: functions_a7a
         :language: cpp

         Below is one way to complete the program.  I used the ``ceil`` function from the ``cmath`` library, but you could have solved this problem without using any functions from ``cmath``.
         ~~~~
         #include <iostream>
         #include <cmath>
         using namespace std;

         void gpaBoost (double GPA) {
             int betterGPA = ceil(GPA);
             cout << betterGPA << ".000";
         }


.. selectquestion:: functions_a8_sq
    :fromid: functions_a8, functions_a8_pp
    :toggle: lock


.. tabbed:: functions_a9

   .. tab:: Question

      .. activecode:: functions_a9q
         :language: cpp

         Write a function called ``tanD`` that prints the tangent of an angle given as a ``double`` in degrees. Use 3.14 for pi.  Be sure to include any necessary headers.
         ~~~~
         #include <iostream>
         #include <cmath>
         using namespace std;
         void tanDegrees () {

         }

         int main () {
             // DO NOT MODIFY ANYTHING BELOW THIS LINE
             cout << "Testing with degrees = 45..." << endl; cout << "    Your solution calculated a tangent of "; tanDegrees(45); cout << endl; cout << "    The correct solution calculates a tangent of 0.999204" << endl; cout << "Testing with degrees = 112.1..." << endl; cout << "    Your solution calculated a tangent of "; tanDegrees(112.1); cout << endl; cout << "    The correct solution calculates a tangent of -2.46973";
         }


   .. tab:: Answer

      .. activecode:: functions_a9a
         :language: cpp

         Below is one way to complete the program.  You need to make sure to convert your angle to radians before doing any calculations with sinusoidal functions.
         ~~~~
         #include <iostream>
         #include <cmath>
         using namespace std;

         void tanDegrees (double degrees) {
             double radians = degrees * (2 * 3.14) / 360.0;
             double tangent = tan(radians);
             cout << tangent;
         }


.. selectquestion:: functions_a10_sq
    :fromid: functions_a10, functions_a10_pp
    :toggle: lock
