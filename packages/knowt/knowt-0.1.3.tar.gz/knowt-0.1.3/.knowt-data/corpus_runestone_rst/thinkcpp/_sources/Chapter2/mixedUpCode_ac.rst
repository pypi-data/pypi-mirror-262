Activecode Exercises
-----------------------

Answer the following **Activecode** questions to assess what you have learned in this chapter.


.. tabbed:: VARS_p1_ac

    .. tab:: Question

        .. activecode:: VARS_p1_ac_q
            :language: cpp

            Construct a block of code that prints: "Lions &" one the first line, "Tigers & Bears!" on the second line, and "Oh my!" on the FOURTH line.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: VARS_p1_ac_a
            :language: cpp

            Below is one way to write the code to print one separate lines.
            ~~~~
            #include <iostream>
            using namespace std;

            int main() {
                cout << "Lions &" << endl;
                cout << "Tigers &";
                cout << " Bears!" << endl;
                cout << endl;
                cout << "Oh my!";
            }


.. tabbed:: VARS_p2_ac

    .. tab:: Question

        .. activecode:: VARS_p2_ac_q
            :language: cpp

            Construct a block of code that swaps the value of integers x and y, which have values 3 and 6, respectively.
            ~~~~
            #include <iostream> 
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: VARS_p2_ac_a
            :language: cpp

            Below is one way to write the code to declare and swap these variables. 
            ~~~~
            #include <iostream>
            using namespace std;

            int main() {
                int x;
                int y;
                x = 3;
                y = 6;
                int temp = x;
                x = y;
                y = temp;
            }


.. tabbed:: VARS_p3_ac

    .. tab:: Question

        .. activecode:: VARS_p3_ac_q
            :language: cpp

            Dan Humphrey is a 3.98 student at Constance High School. His crush's first initial is S. Construct a program that assigns the variables name, GPA, and crush, in that order. Output the variables to the terminal to check your code.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE

    
    .. tab:: Answer

        .. activecode:: VARS_p3_ac_a
            :language: cpp

            Below is one way to write the code to assign the variables. 
            ~~~~
            #include <iostream>
            using namespace std;

            int main() {
                string name = "Dan Humphrey";
                double GPA;
                GPA = 3.98;
                char crush = 'S';
            }


.. tabbed:: VARS_p4_ac

    .. tab:: Question

        .. activecode:: VARS_p4_ac_q
            :language: cpp

            You decide to make homemade Mac 'n' Cheese for you and your roomates.  Whoever wrote the recipe wanted to make things hard for you by stating that it calls for 1% of a gallon of milk.  Construct a block of code that converts this to tablespoons.
            Use the variable name 'tbsp' for the final tablespoons conversion.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: VARS_p4_ac_a
            :language: cpp

            Below is one way to write the code to convert units to tablespoons.
            ~~~~
            #include <iostream> 
            using namespace std;

            int main() {
                double gallons = 0.01;
                double cups = 16 * gallons;
                double tbsp;
                tbsp = 16 * cups;
            }


.. tabbed:: VARS_p5_ac

    .. tab:: Question

        .. activecode:: VARS_p5_ac_q
            :language: cpp

            Construct a block of code that takes the 'volume' of the rectangular prism defined by length, width, and height and prints the result to the terminal. The volume of a rectangular prism is given by ``Volume = length * width * height``.
            Use a length of 2, width of 3, and height of 4.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: VARS_p5_ac_a
            :language: cpp

            Below is one way to write the code to define variables, find volume and print results to the terminal. 
            ~~~~
            #include <iostream>
            using namespace std;

            int main() {
                int length = 2;
                int width = 3;
                int height = 4;
                int volume;
                volume = height * width * length;
                cout << volume;
            }


.. tabbed:: VARS_p6_ac

    .. tab:: Question

        .. activecode:: VARS_p6_ac_q
            :language: cpp

            Construct a block of code that changes the value of the variable a from the character 'a' to the character 'z'. Remember that number values can be used with characters and operations. 
            ~~~~
            #include <iostream> 
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: VARS_p6_ac_a
            :language: cpp

            Below is one way to write the code to change the value of the character variable. 
            ~~~~
            #include <iostream> 
            using namespace std;

            int main() {
                char a = 'a';
                a = a + 25;
            }


.. tabbed:: VARS_p7_ac

    .. tab:: Question

        .. activecode:: VARS_p7_ac_q
            :language: cpp

            Construct a block of code that outputs the ``volume`` of a cylinder with a radius of 3 and a height of 4. The formula for volume of a cylinder is V = (pi)(r^2)(h). Use 3.14 for pi.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: VARS_p7_ac_a
            :language: cpp

            Below is one way to write the code to output the volume of the cylinder. 
            ~~~~
            #include <iostream> 
            using namespace std;

            int main() {
                double radius = 3.00;
                double height = 4.00;
                double pi = 3.14;
                double volume = pi * radius * radius * height;
                cout << volume << endl;
            }


.. tabbed:: VARS_p8_ac

    .. tab:: Question

        .. activecode:: VARS_p8_ac_q
            :language: cpp

            Construct a block of code that assigns the string "MATH" to a variable and prints "My favorite class is MATH" on the same line.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: VARS_p8_ac_a
            :language: cpp

            Below is one way to write the code to output the string.
            ~~~~
            #include <iostream>
            using namespace std;

            int main() {
                string favClass = "MATH";
                cout << "My favorite class is ";
                cout << favClass;
            }


.. tabbed:: VARS_p9_ac

    .. tab:: Question

        .. activecode:: VARS_p9_ac_q
            :language: cpp

            It's Black Friday and the Nintendo Switch you'be been saving up for is marked down to 60% of its original price!  Construct a block of code that calculates and outputs the variable ``moneySaved``, which is how much money you'd be saving if the system originally costed $359.99?
            ~~~~
            #include <iostream>
            using namespace std;

            int main() {
            // YOUR CODE HERE


                cout << moneySaved << endl;
                cout << "moneySaved should be $143.99." << endl;
            }

    .. tab:: Answer

        .. activecode:: VARS_p9_ac_a
            :language: cpp

            Below is one way to write the code to calculate your savings.
            ~~~~
            #include <iostream>
            using namespace std;

            int main() {
                double game = 359.99;
                double discount = game * 0.60;
                double moneySaved = game - discount;
            }


.. tabbed:: VARS_p10_ac

    .. tab:: Question

        .. activecode:: VARS_p10_ac_q
            :language: cpp

            Your family just bought a dog and everyone has been fighting over what to name it.  It went from Champ to Copper to Higgins, and after a few days of being Higgins, everyone agreed on Buddy.  Construct a block of code that illustrates this concept.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


            
    .. tab:: Answer

        .. activecode:: VARS_p10_ac_a
            :language: cpp

            Below is one way to write the code to illustrate the dog's name change process. 
            ~~~~
            #include <iostream>
            using namespace std;

            int main() {
                string name = "Champ";
                name = "Copper";
                string newName = "Higgins";
                name = newName;
                name = "Buddy";
            }
