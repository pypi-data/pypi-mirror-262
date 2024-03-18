Activecode Exercises
-----------------------

Answer the following **Activecode** questions to
assess what you have learned in this chapter.


.. tabbed:: cond_recc_p1_ac

    .. tab:: Question

        .. activecode:: cond_recc_p1_ac_q
            :language: cpp

            Construct a block of code that prints the remainder of 18 when
            divided by 13.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: cond_recc_p1_ac_a
            :language: cpp

            Below is one way to write the code to print the remainder of 18 when divided by 13.
            ~~~~
            #include <iostream>
            using namespace std;

            int main () {
                int x = 18;
                int y = 13; 
                cout << x % y;
            }


.. tabbed:: cond_recc_p2_ac

    .. tab:: Question

        .. activecode:: cond_recc_p2_ac_q
            :language: cpp
                        
            Construct a function, ``is_even``, that prints whether a number
            is even.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


            // DO NOT MODIFY BELOW THIS LINE
            int main() {
                is_even(4);
                is_even(3);
                is_even(0);
            }

    .. tab:: Answer

        .. activecode:: cond_recc_p2_ac_a
            :language: cpp

            Below is one way to construct the ``is_even`` function.
            ~~~~
            #include <iostream> 
            using namespace std;

            void is_even (int number) {
                if (number % 2 == 0) {
                cout << true;
                }
                else {
                cout << false;
                }
            }

            int main() {
                is_even(4);
                is_even(3);
                is_even(0);
            }


.. tabbed:: cond_recc_p3_ac

    .. tab:: Question

        .. activecode:: cond_recc_p3_ac_q
            :language: cpp

            Construct a function, ``difference``, that prints the difference of a and b if the result
            would result in a positive number.  Otherwise, prints -1.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


            // DO NOT MODIFY BELOW THIS LINE
            int main() {
                int a = 25;
                int b = 10;
                difference(a,b);
            }

    .. tab:: Answer

        .. activecode:: cond_recc_p3_ac_a
            :language: cpp

            Below is one way to write the ``difference`` function. 
            ~~~~
            #include <iostream>
            using namespace std;

            void difference (int a, int b) {
                if (a - b > 0) {
                cout << a - b;
                }
                else {
                cout << -1;
                }
            }

            int main() {
                int a = 25;
                int b = 10;
                difference(a,b);
            }


.. tabbed:: cond_recc_p4_ac

    .. tab:: Question

        .. activecode:: cond_recc_p4_ac_q
            :language: cpp

            Construct a function, ``matic``, that takes as inputs 2 integers, x and y, and prints "automatic" if x is
            an odd number, "systematic" if x is greater than y, AND
            "hydromatic" if y is not equal to x.  Check all 3 conditions.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: cond_recc_p4_ac_a
            :language: cpp

            Below is one way to construct the code.
            ~~~~
            #include <iostream>
            using namespace std;

            void matic(int x, int y) {
                if (x % 2 > 0) {
                    cout << "automatic"; }
                if (x > y) {
                    cout << "systematic"; }
                if (y != x) {
                    cout << "hydromatic"; }
            }

            int main() {
                matix(5,4);
            }
   

.. tabbed:: cond_recc_p5_ac

    .. tab:: Question

        .. activecode:: cond_recc_p5_ac_q
            :language: cpp

            Construct a block of code that prints "Pick me!" if x is
            equal to y, "Choose me!" if x is less than y, OR "Love me!" 
            if x + y is even.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: cond_recc_p5_ac_a
            :language: cpp

            Below is one way to construct the code.
            ~~~~
            #include <iostream>
            using namespace std;

            int main() {
                if (x == y) {
                    cout << "Pick me!"; }
                else if (y > x) {
                    cout << "Choose me!"; } 
                else if ((x + y) % 2 == 0) {
                    cout << "Love me!"; } 
            }


.. tabbed:: cond_recc_p6_ac

    .. tab:: Question

        .. activecode:: cond_recc_p6_ac_q
            :language: cpp

            Construct a function, ``printLetterGrade``, that prints your letter grade according to this scheme.
            [0, 70) = F, [70, 80) = C, [80, 90) = B, and [90, 100] = A.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


            // DO NOT MODIFY BELOW THIS LINE
            int main() {
                double grade = 90.0;
                printLetterGrade(grade);
            }

    .. tab:: Answer

        .. activecode:: cond_recc_p6_ac_a
            :language: cpp

            Below is one way to write the ``printLetterGrade`` function.
            ~~~~
            #include <iostream>
            using namespace std;

            void printLetterGrade (double grade) {
                if (grade < 70) {
                cout << "F"; }
                else if (grade < 80) {
                cout << "C"; }
                else if (grade < 90) {
                cout << "B"; }
                else {
                cout << "A"; }
            }

            int main() {
                double grade = 90.0;
                printLetterGrade(grade);
            }


.. tabbed:: cond_recc_p7_ac

    .. tab:: Question

        .. activecode:: cond_recc_p7_ac_q
            :language: cpp

            According to a logic game, a knight is someone who cannot tell a lie,
            and a knave is someone who cannot tell the truth.  Construct a function
            that takes two booleans: the truth value of the story, and the truth value
            told by the person.  The function should print whether the person was a
            knight or a knave.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: cond_recc_p7_ac_a
            :language: cpp

            Below is one way to construct the ``knightKnave`` function.
            ~~~~
            #include <iostream>
            using namespace std;

            void knightKnave (bool truth, bool told) {
                if (truth == true) {
                    if (told == true) {
                        cout << "Knight";
                    }
                    else {
                        cout << "Knave";
                    } }
                    else {
                        if (told == true) {
                            cout << "Knave";
                        }
                    else {
                        cout << "Knive";
                    }
                    }
            }
   

.. tabbed:: cond_recc_p8_ac

    .. tab:: Question

        .. activecode:: cond_recc_p8_ac_q
            :language: cpp

            If a cat is in a good mood, it purrs; when it's in a bad mood, it
            meows.  If a doog is in a good mood, it barks; when it's in a bad
            mood it woofs.  Construct a function that accomplishes this.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: cond_recc_p8_ac_a
            :language: cpp

            Below is one way to construct the ``makeVocals`` function.
            ~~~~
            #include <iostream>
            using namespace std;

            void makeVocals (string animal, string mood) {
                if (mood == "bad") {
                    if (animal == "dog") {
                        cout << "Woof!" << endl;
                    }
                    else {
                        cout << "Meow!" << endl;
                    }
                }
                else {
                    if (animal == "dog") {
                        cout << "Bark!" << endl;
                    }
                    else {
                        cout << "Purr!" << endl;
                    }
                }
            }

            int main() {
                makeVocals("dog","good");
                makeVocals("cat","bad");
            }


.. tabbed:: cond_recc_p9_ac

    .. tab:: Question

        .. activecode:: cond_recc_p9_ac_q
            :language: cpp

            Construct a recursive function that tells the user to enter a positive
            number.  It should then output that number to the terminal.  If the user
            enters a negative number or zero, prompt the user again.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: cond_recc_p9_ac_a
            :language: cpp

            Below is one way to write the ``takeSum`` recursive function.
            ~~~~
            #include <iostream>
            using namespace std;

            void takeSum () {
                cout << "Input a positive number!";
                int num;
                cin >> num;
                if (num < 0) {
                    takeSum ();
                } // END "if"
                cout << num;
            } // END function

            int main() {
                takeSum();
            }


.. tabbed:: cond_recc_p10_ac

    .. tab:: Question

        .. activecode:: cond_recc_p10_ac_q
            :language: cpp

            In the table of ASCII characters, the lowercase alphabet consists
            of characters 97-122.  The uppercase alphabet consists of characters
            65-90, which is a 32 character shift back from the lowercase.  Construct
            a recursive function that asks the user to input a LOWERCASE character,
            converts that character to UPPERCASE character and prints it.  If the user
            enters a character outside of the range of the LOWERCASE alphabet, prompt
            the user again.  Hint:  "||" means "or" when used between two conditional
            statements.
            ~~~~
            #include <iostream> 
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: cond_recc_p10_ac_a
            :language: cpp

            Below is one way to write the ``capitalize`` function. 
            ~~~~
            #include <iostream>
            using namespace std;

            void capitalize () {
                cout << "Input a lowercase character!";
                char let;
                cin >> let;
                if (int(let) < 97 || int(let) > 122) {
                capitalize (); }
                let = let - 32;
                cout << char(let);
            }

            int main() {
                capitalize();
            }
