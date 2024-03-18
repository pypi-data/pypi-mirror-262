Coding Practice
---------------

.. tabbed:: cp_13_AC_2_q

    .. tab:: Activecode

        .. activecode:: cp_13_AC_2q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            How long is a year on other planets? Let's write a program that prints out the number of days
            in a year on each planet using a switch statement. These values are, in planetary order,
            88 days, 225 days, 365 days, 687 days, 4333 days, 10759 days, 30687 days, and 60190 days.
            Print out this information in the following format: Planet ``planet`` has ``numDays`` number of days in
            a year! Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            enum Planet { MERCURY = 1, VENUS, EARTH, MARS, JUPITER, SATURN, URANUS, NEPTUNE };

            int main() {
                Planet p = JUPITER;
                // Write your code here.
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_13_AC_2_pp
            :numbered: left
            :adaptive:

            How long is a year on other planets? Let's write a program that prints out the number of days
            in a year on each planet using a switch statement. These values are, in planetary order,
            88 days, 225 days, 365 days, 687 days, 4333 days, 10759 days, 30687 days, and 60190 days.
            Print out this information in the following format: Planet ``planet`` has ``numDays`` number of days in
            a year! Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            enum Planet { MERCURY = 1, VENUS, EARTH, MARS, JUPITER, SATURN, URANUS, NEPTUNE };
            =====
            int main() {
            =====
                Planet p = VENUS;
            =====
                switch (p) {
            =====
                    case 1:
                        cout << "Planet Mercury has 88 number of days in a year!" << endl;
                        break;
            =====
                    case 2:
                        cout << "Planet Venus has 225 number of days in a year!" << endl;
                        break;
            =====
                    case 3:
                        cout << "Planet Earth has 365 number of days in a year!" << endl;
                        break;
            =====
                    case 4:
                        cout << "Planet Mars has 687 number of days in a year!" << endl;
                        break;
            =====
                    case 5:
                        cout << "Planet Jupiter has 4333 number of days in a year!" << endl;
                        break;
            =====
                    case 6:
                        cout << "Planet Saturn has 10759 number of days in a year!" << endl;
                        break;
            =====
                    case 7:
                        cout << "Planet Uranus has 30687 number of days in a year!" << endl;
                        break;
            =====
                    case 8:
                        cout << "Planet Neptune has 60190 number of days in a year!" << endl;
                        break;
            =====
                }
            =====
            }

.. tabbed:: cp_13_AC_4_q

    .. tab:: Activecode

        .. activecode:: cp_13_AC_4q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Now let's generate a ``BingoBoard``! We want to fill the 25 ``Space``\s on the ``BingoBoard`` with
            random values from 1 to 75 without repititon. To do this, we'll make a ``vector``
            of numbers from 1 to 75 and shuffle it using the same method as shown in this chapter. Then
            we will select the first 25 values for the 25 spaces on the ``BingoBoard``. We will
            do this entire process in multiple steps. First, write the function ``randomInt``, which
            generates a random value between low and high, inclusive. Be sure to include the relevant libraries!
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            // Add any relevant libraries here.
            using namespace std;

            // Write your code for the randomInt function here.

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_13_AC_4_pp
            :numbered: left
            :adaptive:

            Now let's generate a ``BingoBoard``! We want to fill the 25 ``Space``\s on the ``BingoBoard`` with
            random values from 1 to 75 without repititon. To do this, we'll make a ``vector``
            of numbers from 1 to 75 and shuffle it using the same method as shown in this chapter. Then
            we will select the first 25 values for the 25 spaces on the ``BingoBoard``. We will
            do this entire process in multiple steps. First, write the function ``randomInt``, which
            generates a random value between low and high, inclusive. Be sure to include the relevant libraries!
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            int randomInt(int low, int high) {
            =====
               srand(time(NULL));
            =====
               int x = random();
            =====
               int y = x % (high - low + 1) + low;
            =====
               return y;
            =====
            }

.. tabbed:: cp_13_AC_6_q

    .. tab:: Activecode

        .. activecode:: cp_13_AC_6q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Now that we have the functions ``randomInt`` and ``swapValues``, we can write the function
            ``generateRandVec``. ``generateRandVec`` creates a ``vector`` with values from 1 to 75,
            shuffles it using ``randomInt`` and ``swapValues``, and returns the shuffled ``vector``.
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            #include <vector>
            #include <cstdlib>
            #include <numeric>
            using namespace std;

            // Write your code for the generateRandVec function here.

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_13_AC_6_pp
            :numbered: left
            :adaptive:

            Now that we have the functions ``randomInt`` and ``swapValues``, we can write the function
            ``generateRandVec``. ``generateRandVec`` creates a ``vector`` with values from 1 to 75,
            shuffles it using ``randomInt`` and ``swapValues``, and returns the shuffled ``vector``.
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            vector<int> generateRandVec() {
            =====
               vector<int> vec(75);
            =====
               iota(vec.begin(), vec.end(), 1);
            =====
               for (size_t i = 0; i < vec.size(); ++i) {
            =====
                   int x = randomInt(i, vec.size() - 1);
            =====
                   swapValues(vec, i, x);
            =====
               }
            =====
               return vec;
            =====
            }

.. tabbed:: cp_13_AC_8_q

    .. tab:: Activecode

        .. activecode:: cp_13_AC_8q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's print out our ``BingoBoard``! Write the ``BingoBoard`` member function
            ``printBoard``. Insert tabs between each value in each row to make the board
            print out neater. Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            #include <vector>
            #include <cstdlib>
            #include <numeric>
            using namespace std;

            struct Space {
                int value;
                bool is_filled;
            };

            struct BingoBoard {
                vector<vector<Space> > board;
                void makeBoard ();
                void printBoard ();
            };

            int randomInt (int low, int high);
            void swapValues (vector<int> &vec, int index1, int index2);
            vector<int> generateRandVec ();

            // Write your code for the printBoard function here.

            int main() {
                BingoBoard bingo;
                bingo.makeBoard ();
                bingo.printBoard ();
            }
            ====
            int randomInt(int low, int high) {
                srand(time(NULL));
                int x = random();
                int y = x % (high - low + 1) + low;
                return y;
            }

            void swapValues(vector<int> &vec, int index1, int index2) {
                int temp = vec[index1];
                vec[index1] = vec[index2];
                vec[index2] = temp;
            }

            vector<int> generateRandVec() {
                vector<int> vec(75);
                iota(vec.begin(), vec.end(), 1);
                for (size_t i = 0; i < vec.size(); ++i) {
                    int x = randomInt(i, vec.size() - 1);
                    swapValues(vec, i, x);
                }
                return vec;
            }

            void BingoBoard::makeBoard() {
                // Initialize board
                Space s = {0, false};
                vector<Space> cols(5, s);
                for (size_t i = 0; i < 5; ++i) {
                    board.push_back(cols);
                }

                // Fill board with random values
                vector<int> vec = generateRandVec();
                int count = 0;
                for (size_t row = 0; row < board.size(); ++row) {
                    for (size_t col = 0; col < board[row].size(); ++col) {
                    board[row][col].value = vec[count];
                    ++count;
                    }
                }

                // Create free space
                board[2][2].value = 0;
                board[2][2].is_filled = true;
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_13_AC_8_pp
            :numbered: left
            :adaptive:

            Let's print out our ``BingoBoard``! Write the ``BingoBoard`` member function
            ``printBoard``. Insert tabs between each value in each row to make the board
            print out neater. Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            void BingoBoard::printBoard () {
            =====
                for (size_t j = 0; j < board.size(); j++) {
            =====
                    for (size_t i = 0; i < board[j].size(); i++) {
            =====
                        cout << board[j][i].value << "\t";
            =====
                    }
            =====
                    cout << endl;
            =====
                }
            =====
            }

.. tabbed:: cp_13_AC_10_q

    .. tab:: Activecode

        .. activecode:: cp_13_AC_10q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            You may have noticed that in some cases, our version of ``bubbleSort`` does
            an unnecessary amount of work. For example, if our ``vector`` was {1, 2, 3, 5, 4},
            ``bubbleSort`` would swap 4 and 5, but then keep going even though our ``vector``
            is already in order! We can save some work by including a ``bool`` called ``is_changed``.
            If we swap values during a pass, we set ``is_changed`` to true. If nothing has been swapped,
            then ``is_changed`` stays false, and we know to break out of the loop since our ``vector``
            is already sorted. Write the function ``fastBubbleSort``, which is ``bubbleSort`` with this
            modification. Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            void swapValues(vector<int> &vec, int index1, int index2) {
                int temp = vec[index1];
                vec[index1] = vec[index2];
                vec[index2] = temp;
            }

            // Write your code for the fastBubbleSort function here.

            int main() {
                vector<int> vec = { 1, 3, 5, 4, 6, 8, 9 };
                fastBubbleSort (vec);
                for (size_t i = 0; i < vec.size(); ++i) {
                    cout << vec[i] << " ";
                }
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_13_AC_10_pp
            :numbered: left
            :adaptive: 

            You may have noticed that in some cases, our version of ``bubbleSort`` does
            an unnecessary amount of work. For example, if our ``vector`` was {1, 2, 3, 5, 4},
            ``bubbleSort`` would swap 4 and 5, but then keep going even though our ``vector``
            is already in order! We can save some work by including a ``bool`` called ``is_changed``.
            If we swap values during a pass, we set ``is_changed`` to true. If nothing has been swapped,
            then ``is_changed`` stays false, and we know to break out of the loop since our ``vector``
            is already sorted. Write the function ``fastBubbleSort``, which is ``bubbleSort`` with this
            modification. Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            void fastBubbleSort(vector<int> &vec) {
            =====
                bool is_changed = false;
            =====
                for (size_t i = 0; i < vec.size() - 1; ++i) {
            =====
                    for (size_t j = 0; j < vec.size() - 1 - i; ++j) {
            =====
                        if (vec[j] > vec[j + 1]) {
            =====
                            swapValues(vec, j, j + 1);
            =====
                            is_changed = true;
            =====
                        }
            =====
                        if (is_changed == false) {
            =====
                            break;
            =====
                        }
            =====
                    }
            =====
                }
            =====
            }