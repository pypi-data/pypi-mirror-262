Activecode Exercises
----------------------

Answer the following **Activecode** questions to assess what you have learned in this chapter.

.. tabbed:: mucp_13_1_ac

    .. tab:: Question

        .. activecode:: mucp_13_1_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write the enumerated type ``Days`` which maps days of the week to integers
            starting at 1. Use a switch statement to determine whether or not day
            is a weekend or not. Check for cases in numerical order.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_13_1_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to use a switch statement to classify a day of the week.
            ~~~~
            #include <iostream>
            using namespace std;

            enum Day { MON = 1, TUE, WED, THU, FRI, SAT, SUN };

            int main () {
                Day day = SUN;
                switch (day > 5) {
                    case 0:
                        cout << "It is not the weekend :(" << endl;
                        break;
                    case 1:
                        cout << "It is the weekend :)" << endl;
                        break;
                    default:
                        cout << "Invalid input." << endl;
                        break;
                }
            }

.. tabbed:: mucp_13_2_ac

    .. tab:: Question

        .. activecode:: mucp_13_2_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Use a switch statement to check and print out whether a number is divisible by two.
            Prompt and get input from the user. If input isn't valid,
            print out the default statement "Invalid input." Check for cases in numerical order.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_13_2_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to use a switch statement to check and print out whether a number is divisible by 
            two.
            ~~~~
            #include <iostream>
            using namespace std;

            int main () {
                int input;
                cout << "Please enter an integer: ";
                cin >> input;
                switch (input % 2) {
                    case 0:
                        cout << input << " is even!" << endl;
                        break;
                    case 1:
                        cout << input << " is odd!" << endl;
                        break;
                    default:
                        cout << "Invalid input." << endl;
                        break;
                }
            }

.. tabbed:: mucp_13_3_ac

    .. tab:: Question

        .. activecode:: mucp_13_3_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Use a switch statement to check and print out the maximum between two numbers.
            Prompt and get input from the user for two integers. If input isn't valid,
            print out the default statement "Invalid input." Check for cases in numerical order.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_13_3_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to use a switch statement to check and print out the maximum between two numbers.
            ~~~~
            #include <iostream>
            using namespace std;

            int main () {
                int input1;
                int input2;
                cout << "Please enter first integer: ";
                cin >> input1;
                cout << "Please enter second integer: ";
                cin >> input2;
                switch (input1 > input2) {
                    case 0:
                        cout << "The maximum is " << input2 << endl;
                        break;
                    case 1:
                        cout << "The maximum is " << input1 << endl;
                    default:
                        cout << "Invalid input." << endl;
                        break;
                }
            }

.. tabbed:: mucp_13_4_ac

    .. tab:: Question

        .. activecode:: mucp_13_4_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write the pseudocode for the implementation of ``mergeSort``. 
            ~~~~
            // YOUR PSEUDOCODE HERE


    .. tab:: Answer

        .. activecode:: mucp_13_4_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the pseudocode of ``mergeSort``.
            ~~~~
            Deck Deck::mergeSort () const {
                find the midpoint of the deck
                divide the deck into two subdecks
                sort the subdecks using sort
                merge the two halves and return the result
                divide each subdeck into two more subdecks
            }

.. tabbed:: mucp_13_5_ac

    .. tab:: Question

        .. activecode:: mucp_13_5_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's revisit the Dictionary data structure defined in the previous section.
            Write the struct definitions for ``Entry``, which has member variables word and page,
            and for ``Dictionary``, which has a vector of Entries. 
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_13_5_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the struct definition for ``Entry`` and for ``Dictionary``. 
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            struct Entry {
                string word;
                int page;
            };

            struct Dictionary {
                vector<Entry> entries;
            };

.. tabbed:: mucp_13_6_ac

    .. tab:: Question

        .. activecode:: mucp_13_6_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Assume our dictionary is currently unsorted. Let's write a Dictionary member function ``find``
            that takes a string word as a parameter and returns the index of its corresponding
            entry. If the word isn't in the dictionary, return -1. 
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE

    .. tab:: Answer
        
        .. activecode:: mucp_13_6_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the Dictionary member function.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            struct Entry {
                string word;
                int page;
            };

            struct Dictionary {
                vector<Entry> entries;
            };

            int Dictionary::find (string word) {
                for (size_t i = 0; i < entries.size(); ++i) {
                    if (entries[i].word == word) {
                        return i;
                    }
                }
                return -1;
            }

.. tabbed:: mucp_13_7_ac

    .. tab:: Question

        .. activecode:: mucp_13_7_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Of course, all dictionaries are in some sort of order. In order to do this, we
            must first write the Dictionary member function ``findFirstWord``, which takes a starting
            index as a parameter returns the index of the Entry with the highest priority alphabetically
            (i.e. the Entry with a word that would come first in the alphabet). 
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_13_7_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the ``findFirstWord`` member function.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            struct Entry {
                string word;
                int page;
            };

            struct Dictionary {
                vector<Entry> entries;
            };

            int Dictionary::findFirstWord (int start) {
                int min = start;
                for (size_t i = start; i < entries.size(); ++i) {
                    if (entries[i].word < entries[min].word) {
                        min = i;
                    }
                }
                return min;
            }

.. tabbed:: mucp_13_8_ac

    .. tab:: Question

        .. activecode:: mucp_13_8_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            We also need a swap function. Write the Dictionary member function
            ``swap`` which takes two indices as parameters and swaps the Entries
            at those indices. 
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_13_8_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the ``swap`` member function
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            struct Entry {
                string word;
                int page;
            };

            struct Dictionary {
                vector<Entry> entries;
            };

            void Dictionary::swap (int a, int b) {
                Entry temp = entries[a];
                entries[a] = entries[b];
                entries[b] = temp;
            }

.. tabbed:: mucp_13_9_ac

    .. tab:: Question

        .. activecode:: mucp_13_9_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
            
            Now let's write the Dictionary member function ``alphabetize``, which
            sorts the Entries in the Dictionary in alphabetical order. Use
            the ``findFirstWord`` and ``swap`` functions we defined earlier! 
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_13_9_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the Dictionary member function ``alphabetize``.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            void Dictionary::alphabetize () {
                for (size_t i = 0; i < entries.size(); ++i) {
                    int min = findFirstWord (i);
                    swap (i, min);
                }
            }

.. tabbed:: mucp_13_10_ac

    .. tab:: Question

        .. activecode:: mucp_13_10_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's check to see if our sorting worked! Write the Dictionary
            member function ``printDictionary``, which prints out the word in each 
            Entry.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_13_10_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the Dictionary member function ``printDictionary``.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            struct Entry {
                string word;
                int page;
            };

            struct Dictionary {
                vector<Entry> entries;
            };

            void Dictionary::printDictionary () {
                for (size_t i = 0; i < entries.size(); ++i) {
                    cout << entries[i].word << endl;
                }
            }