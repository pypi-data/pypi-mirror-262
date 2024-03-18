Coding Practice
---------------

.. tabbed:: cp_6_AC_2q_q

    .. tab:: Activecode
            
        .. activecode:: cp_6_AC_2q
            :language: cpp

            Encapsulate the triangle printing program into a function called
            ``printTriangle``. Generalize it so that it takes a parameter
            ``int n`` to generate a nxn triangle. Select the Parsonsprob tab 
            for hints for the construction of the code. Call your function in main
            with an input of 4, which should result in the following output:

            ::

                *
                **
                ***
                ****
            ~~~~
            #include <iostream>
            using namespace std;

            void printTriangle (int n) {
                // Write your implementation here.
            }

            int main() {
                // Write your implementation here.
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_6_AC_2q_pp
            :numbered: left
            :adaptive:

            Encapsulate the triangle printing program into a function called
            ``printTriangle``. Generalize it so that it takes a parameter
            ``int n`` to generate a nxn triangle. Use the lines to construct the
            code, then go back to complete the Activecode tab. Call your function in main
            with an input of 4, which should result in the following output:

            ::

                *
                **
                ***
                ****

            -----
            // Create function
            void printTriangle (int n) {
            =====
                int row = 0;
            =====
                int row = 4; #distractor
            =====
                while (row < n) {
            =====
                    int col = 0;
            =====
                    int col = 4; #paired
            =====
                    while (col <= row) {
            =====
                    while (col <= n) {
            =====
                        cout << "*";
            =====
                        col++;
            =====
                    }
            =====
                    cout << endl;
            =====
                    row++;
            =====
                    }
            =====
                }
            =====
            }
            =====
            // Write main implementation
            int main() {
            =====
                printTriangle(4);
            =====
            }

.. tabbed:: cp_6_AC_4q_q

    .. tab:: Activecode
            
        .. activecode:: cp_6_AC_4q
            :language: cpp
            :practice: T

            Write a function called ``printNumPyramid`` that prints out an ``n`` x ``n`` number pyramid.
            An example is shown below with ``n`` equal to 5. Your code should use while loops. Select the 
            Parsonsprob tab for hints for the construction of the code. (Hint: similar to the previous 
            question, if you want the output to look nice, using conditionals that print different amounts of spaces.)

            ::
        
                    1
                   222
                  33333
                 4444444
                555555555
            ~~~~
            #include <iostream>
            using namespace std;

            void printNumPyramid (int n) {
                // Write your implementation here.
            }

            int main() {
                printNumPyramid (5);
            }
    
    .. tab:: Parsonsprob

        .. parsonsprob:: cp_6_AC_4q_pp
            :numbered: left
            :adaptive:

            Write a function called ``printNumPyramid`` that prints out an ``n`` x ``n`` number pyramid.
            An example is shown below with ``n`` equal to 5. Your code should use while loops. Use the lines to 
            construct the code, then go back to complete the Activecode tab. (Hint: similar to the previous 
            question, if you want the output to look nice, using conditionals that print different amounts of spaces.)

            ::
        
                    1
                   222
                  33333
                 4444444
                555555555

            -----
            void printNumPyramid (int n) {
            =====
                int space;
                int numPrinted;
                int count = 1;
                int sub = 4;
            =====
                int space; #paired
                int numPrinted = 5;
                int count = 1;
                int sub = 1;
            =====
                while (count <= n) {
                    space = n - count;
            =====
                    while (space > 0) {
                        cout << " ";
                        space --
                    }
            =====
                    numprinted = 2 * count - 1;
            =====
                    while (numPrinted > 0) {
                        cout << n - sub;
                        numPrinted--;
                    }
            =====
                    cout << endl;
                    count ++;
                    sub--;
            =====
                    cout << endl; #paired;
                    count++;
                    sub++;
            =====
                }
            }

.. tabbed:: cp_6_AC_6q_q

    .. tab:: Activecode

        .. activecode:: cp_6_AC_6q
            :language: cpp
            :practice: T

            Write the function ``printAddTable`` which takes an ``int n`` as a parameter
            and prints out a nxn addition table. Call your function in ``main`` with
            "10" as the argument. Select the Parsonsprob tab for hints for the construction of the code.
            Your output should look like this:

            ::

                0       1       2       3       4       5       6       7       8       9       10
                1       2       3       4       5       6       7       8       9       10      11
                2       3       4       5       6       7       8       9       10      11      12
                3       4       5       6       7       8       9       10      11      12      13
                4       5       6       7       8       9       10      11      12      13      14
                5       6       7       8       9       10      11      12      13      14      15
                6       7       8       9       10      11      12      13      14      15      16
                7       8       9       10      11      12      13      14      15      16      17
                8       9       10      11      12      13      14      15      16      17      18
                9       10      11      12      13      14      15      16      17      18      19
                10      11      12      13      14      15      16      17      18      19      20
            ~~~~
            #include <iostream>
            using namespace std;

            void printAddTable (int n) {
                // Write your implementation here.
            }

            int main() {
                // Call your function here.
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_6_AC_6q_pp
            :numbered: left
            :adaptive:

            Write the function ``printAddTable`` which takes an ``int n`` as a parameter
            and prints out a nxn addition table. Call your function in ``main`` with
            "10" as the argument. Use the lines to construct the code, then go back to complete
            the Activecode tab. Your output should look like this:

            ::

                0       1       2       3       4       5       6       7       8       9       10
                1       2       3       4       5       6       7       8       9       10      11
                2       3       4       5       6       7       8       9       10      11      12
                3       4       5       6       7       8       9       10      11      12      13
                4       5       6       7       8       9       10      11      12      13      14
                5       6       7       8       9       10      11      12      13      14      15
                6       7       8       9       10      11      12      13      14      15      16
                7       8       9       10      11      12      13      14      15      16      17
                8       9       10      11      12      13      14      15      16      17      18
                9       10      11      12      13      14      15      16      17      18      19
                10      11      12      13      14      15      16      17      18      19      20

            -----
            void printAddTable (int n) {
            =====
                for (int i = 0; i <= n; i++) {
            =====
                for (int i = 0; i < n; i++) { #paired
            =====
                    for (int j = 0; j <= n; j++) {
            =====
                    for (int j = 0; j < n; j++) { #distractor
            =====
                        cout << i + j << '\t';
            =====
                    }
            =====
                    cout << '\n';
            =====
                }
            =====
            }

.. tabbed:: cp_6_AC_8q_q

    .. tab:: Activecode

        .. activecode:: cp_6_AC_8q
            :language: cpp
            :practice: T

            Write a program that uses a ``while`` loop to print out the alphabet from 'a' to 'z'.
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            int main() {
                // Write your implementation here.
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_6_AC_8q_pp
            :numbered: left
            :adaptive:

            Write a program that uses a ``while`` loop to print out the alphabet from 'a' to 'z'.
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            int main() {
            =====
                char letter = 'a';
            =====
                while (letter <= 'z') {
            =====
                while (letter != 'z') { #paired
            =====
                    cout << letter << endl;
            =====
                    letter++;
            =====
                }
            =====
            }    

.. tabbed:: cp_6_AC_10q_q

    .. tab:: Activecode
            
        .. activecode:: cp_6_AC_10q
            :language: cpp
            :practice: T

            Write a function called ``factorial`` which takes an ``int n`` as a parameter
            and returns ``n`` factorial. Remembers that a factorial (denoted by !) is the product of all
            positive integers less than or equal to ``n``, so 4! is 24. Use a ``while`` loop.
            Run and test your code! Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            int factorial (int n) {
                // Write your implementation here.
            }
            ====
            #define CATCH_CONFIG_MAIN
            #include <catch.hpp>

            TEST_CASE("factorial function") {
                REQUIRE(factorial (4) == 24);
                REQUIRE(factorial (6) == 720);
                REQUIRE(factorial (9) == 362880);
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_6_AC_10q_pp
            :numbered: left
            :adaptive:

            Write a function called ``factorial`` which takes an ``int n`` as a parameter
            and returns ``n`` factorial. Remembers that a factorial (denoted by !) is the product of all
            positive integers less than or equal to ``n``, so 4! is 24. Use a ``while`` loop.
            Run and test your code! Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            int factorial (int n) {
            =====
                int i = n;
            =====
                int fact = 1;
            =====
                int fact = 0; #distractor;
            =====
                while (n / i != n) {
            =====
                    fact *= i;
            =====
                    fact = n * (n - 1); #paired
            =====
                    i--;
            =====
                }
            =====
                return fact; 
            =====
            }
