Activecode Exercises
--------------------

Answer the following **Activecode** questions to assess what you have learned in this chapter.


.. tabbed:: VARS_a1_ps

   .. tab:: Question

      .. activecode:: VARS_a1q_ps
         :language: cpp

         Fix the code below so that it runs without errors.  Hint: you might need to change the names of some variables.
         ~~~~
         #include <iostream>
         using namespace std;

         int main () {
             char true = 'T';
             char false = 'F';

             cout << true << " is short for true. ";
             cout << false << " is short for false." << endl;
         }

   .. tab:: Answer

      .. activecode:: VARS_a1a_ps
         :language: cpp

         Below is one way to fix the program.  ``true`` and ``false`` are keywords, so they cannot be used as variable names.
         ~~~~
         #include <iostream>
         using namespace std;

         int main () {
             char t = 'T';
             char f = 'F';
             cout << t << " is short for true. ";
             cout << f << " is short for false." << endl;
         }    


.. tabbed:: VARS_a2_q_ps

   .. tab:: Activecode

      .. activecode:: VARS_a2_ps
         :language: cpp

         Finish the code below so that it prints "I drive a 2014 Buick Regal". Select the Pseudocode tab for hints for the construction of the code.
         ~~~~
         #include <iostream>
         using namespace std;

         int main () {
            string make;
            make = "Buick"

            // Finish the rest of the assignment statements by assigning
            // 2014 and Regal to their respective variables.

            // DO NOT MODIFY ANYTHING BELOW THIS LINE.
            cout << "I drive a " << year << " " << make << " ";
            cout << model << endl;
         }

   .. tab:: Pseudocode

      .. parsonsprob:: VARS_a2_p_ps
         :numbered: left
         :adaptive:
         :noindent:

         Finish the code below so that it prints "I drive a 2014 Buick Regal". Use the lines to construct the pseudocode, then go back to complete the Activecode tab.

         -----
         Open main()
         =====
         Initialize variable make as string
         =====
         Assign Buick to make;
         =====
         Initialize year as int;
         =====
         Initialize year as double; #paired
         =====
         Assign a number to year;
         =====
         Initialize model as string;
         =====
         Initialize model as char; #paired
         =====
         Assign model name to model;
         =====
         Output year and make;
         =====
         Output model name;
         =====
         Close main()


.. tabbed:: VARS_a3_ps

   .. tab:: Question

      .. activecode:: VARS_a3q_ps
         :language: cpp

         Fix the code below so that it prints "Cady scored 90% on the exam." 
         ~~~~
         #include <iostream>
         using namespace std;

         int main() {
             // Modify the next line so that Cady = 0.9.
             int Cady = 3 * 5 * (6 / 100);

             // DO NOT MODIFY ANYTHING BELOW THIS LINE.
             cout << "Cady scored " << Cady * 100 << "% on the exam.";
         }

   .. tab:: Answer

      .. activecode:: VARS_a3a_ps
         :language: cpp

         Below is one way to fix the program.  We want to use doubles so that our result isn't rounded down to 0 through integer division.
         ~~~~
         #include <iostream>
         using namespace std;

         int main() {
             double Cady = (3 * 5) * 6 / 100.0;
             cout << "Cady scored " << Cady * 100 << "% on the exam.";
         }    


.. tabbed:: VARS_a4_q_ps

   .. tab:: Activecode

      .. activecode:: VARS_a4_ps
         :language: cpp

         Finish the code below so that it returns the correct volume of a sphere. Select the Pseudocode tab for hints for the construction of the code.
         Hint: think about what happens when you use integer division. The volume of a sphere is given by V = (4/3)(pi)(r^3).
         ~~~~
         #include <iostream>
         using namespace std;

         int main () {
            int radius = 5;
            double pi = 3.14;

            // Use these variables and the formula for volume to complete the next line.
            volume = 

            // DO NOT MODIFY ANYTHING BELOW THIS LINE.
            cout << "Your solution had volume = " << volume << endl;  cout << "The correct solution has volume = 104.667";
         }

   .. tab:: Pseudocode

      .. parsonsprob:: VARS_a4_p_ps
         :numbered: left
         :adaptive:
         :noindent:

         Finish the code below so that it returns the correct volume of a sphere. Select the Parsonsprob tab for hints for the construction of the code. Hint: think about what happens when you use integer division. The volume of a sphere is given by V = (4/3)(pi)(r^3). 
         Use the lines on to construct the pseudocode, then go back to complete the Activecode tab.

         -----
         Open main() 
         =====
         Initialize and assign radius;
         =====
         Initialize and assign pi;
         =====
         Initialize volume as double;
         =====
         Initialize volume as int; #paired
         =====
         Calculate volume with spherical volume formula;
         =====
         Output calculated volume;
         =====
         Close main()


.. tabbed:: VARS_a5_ps

   .. tab:: Question

      .. activecode:: VARS_a5q_ps
         :language: cpp

         Fix the code below so that assigns ``a`` its correct value of ``'a'``.  Hint: use character operations!
         ~~~~
         #include <iostream>
         using namespace std;

         int main () {
            char a = 's';

            // Fix the line below.  Do NOT change the numbers!  Instead, 
            // change the location of the parentheses.
            a = a - 3 * 4 + (1 + 3);

            // DO NOT MODIFY ANYTHING BELOW THIS LINE.
            cout << a;
         }

   .. tab:: Answer

      .. activecode:: VARS_a5a_ps
         :language: cpp

         Below is one way to complete the program.  There are many creative ways that you could use the order of operations to come up with a complex expression that will bring you to ``'a'``, here is one way.
         ~~~~
         #include <iostream>
         using namespace std;
      
         int main () {
            char a = 's';
            a = a - (3 * (4 + 1) + 3);
            cout << a;
         }


.. tabbed:: VARS_a6_q_ps

   .. tab:: Activecode

      .. activecode:: VARS_a6_ps
         :language: cpp

         Write code that assigns "apples" to the variable oranges, and "oranges" to the variable apples, then swaps their values.  Be sure to inclue any necessary headers.  YOU MAY NOT HARDCODE YOUR SOLUTION. Select the Pseudocode tab for hints for the construction of the code.
         ~~~~
         int main () {
            
            // DO NOT MODIFY ANYTHING BELOW THIS LINE.
            cout << "Your solution had apples = " << apples << "and oranges = " << oranges << "." << endl; cout << "The correct solution has apples = apples, and oranges = oranges.";
         }

   .. tab:: Pseudocode

      .. parsonsprob:: VARS_a6_p_ps
         :numbered: left
         :adaptive:
         :noindent:

         Write code that assigns "apples" to the variable oranges, and "oranges" to the variable apples, then swaps their values.  Be sure to inclue any necessary headers. Use the lines to construct the pseudocode, then go back to complete the Activecode tab.

         -----
         Open main()
         =====
         Initialize oranges as string;
         =====
         Assign "apples" to oranges;
         =====
         Initialize apples as string;
         =====
         Assign "oranges" to apples;
         =====
         Assign apples to a temporary variable;
         =====
         Assign oranges to apples;
         =====
         Assign the temporary variable to oranges;
         =====
         Output apples and oranges;
         =====
         Close main()


.. tabbed:: VARS_a7_ps

   .. tab:: Question

      .. activecode:: VARS_a7q_ps
         :language: cpp

         Write code that prints "Eat", "More", and "Chicken" on 3 consecutive lines. Be sure to inclue any necessary headers.
         ~~~~
         int main () {

         }

   .. tab:: Answer

      .. activecode:: VARS_a7a_ps
         :language: cpp

         Below is one way to implement the solution.
         ~~~~
         #include <iostream>
         using namespace std;

         int main () {
             cout << "Eat" << endl;
             cout << "More" << endl;
             cout << "Chicken" << endl;
         } 


.. tabbed:: VARS_a8_q_ps

   .. tab:: Activecode

         .. activecode:: VARS_a8_ps
            :language: cpp

            Write code that calculates how much you you will spend after tipping 20% on your $36.25 dinner.  Save the result of this calculation in ``plusTip``.  Be sure to include any necessary headers. Select the Pseudocode tab for hints for the construction of the code.
            ~~~~
            int main () {

               // DO NOT MODIFY ANYTHING BELOW THIS LINE.
               cout << "Your solution had plusTip = " << plusTip << endl; cout << "The correct solution has plusTip = 43.5";
            }

   .. tab:: Pseudocode

      .. parsonsprob:: VARS_a8_p_ps
         :numbered: left
         :adaptive:
         :noindent:

         Write code that calculates how much you you will spend after tipping 20% on your $36.25 dinner.  Save the result of this calculation in ``plusTip``. 
         Use the lines to construct the pseudocode, then go back to complete the Activecode tab.

         -----
         Open main()
         =====
         Initialize and assign $36.25 to price;
         =====
         Initialize and assign 1.20 to tip;
         =====
         Initialize and assign .20 to tip; #paired
         =====
         Calculate plusTip using tip and price;
         =====
         Output plusTip;
         =====
         Close main()


.. tabbed:: VARS_a9_ps

   .. tab:: Question

      .. activecode:: VARS_a9q_ps
         :language: cpp

         You have about three hours and fifteen minutes of homework to do today.  Rather than starting it right away, you choose to procrastinate by calculating how many seconds you'll be spending on your work.  Convert the time to seconds and store the result in ``seconds``.  Be sure to inclue any necessary headers.
         ~~~~
         int main () {

             // DO NOT MODIFY ANYTHING BELOW THIS LINE.
             cout << "Your solution had seconds = " << seconds << endl;  cout << "The correct solution has seconds = 11700";
         }

   .. tab:: Answer

      .. activecode:: VARS_a9a_ps
         :language: cpp

         Below is one way to implement the solution.
         ~~~~
         #include <iostream>
         using namespace std;

         int main () {
             int hours = 3;
             int minutes = 15;
             int totalMinutes = minutes + 60 * hours;
             int seconds = totalMinutes * 60;
         }


.. tabbed:: VARS_a10_q_ps

   .. tab:: Activecode
   
      .. activecode:: VARS_a10_ps
         :language: cpp

         Write code that calculates and prints the average of a and b if a = 3.14, and b = 1.59.  You may only use one line of code.  Be sure to inclue any necessary headers. Select the Pseudocode tab for hints for the construction of the code.
         ~~~~
         int main () {

            // DO NOT MODIFY ANYTHING BELOW THIS LINE.
            cout << endl;  cout << "Your program should have printed 2.365";
         }

   .. tab:: Pseudocode

      .. parsonsprob:: VARS_a10_p_ps
         :numbered: left
         :adaptive:
         :noindent:

         Write code that calculates and prints the average of a and b if a = 3.14, and b = 1.59.  You may only use one line of code. Use the lines on the to construct the pseudocode, then go back to complete the Activecode tab.

         -----
         Open main() 
         =====
         Output the expression for average of 2 numbers;
         =====
         Close main()
