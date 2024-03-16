Activecode Exercises
-----------------------

Answer the following **Activecode** questions to assess what you have learned in this chapter.

.. tabbed:: vectors_p1_ac

    .. tab:: Question

        .. activecode:: vectors_p1_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Construct a block of code that changes the first element of ``vec`` to a 6,
            multiplies the third element of ``vec`` by 2, and increments the last element 
            of ``vec`` by 1 (in that order).  This should work no matter what ``vec`` is.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: vectors_p1_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to construct the code.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            int main() {
                vector<int> vec;
                vec.assign(1,10);
                vec[0] = 6;
                vec[2] = vec[2] * 2;
                int last = vec.size() - 1;
                vec[last]++;
            }


.. tabbed:: vectors_p2_ac

    .. tab:: Question

        .. activecode:: vectors_p2_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Construct a block of code that creates a vector called ``digs`` whose elements are
            7, 8, 7, 8.  Then access elements to change the ``digs`` to contain the elements
            7, 4, 7, 4. ``Important``: Change the ``8``'s to ``4``'s in order of 
            increasing index.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: vectors_p2_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to construct the code. 
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            int main() {
                vector<int> digs = {7, 8, 7, 8};
                digs[1] = 4;
                digs.pop_back();
                digs.push_back(4);
            }


.. tabbed:: vectors_p3_ac

    .. tab:: Question

        .. activecode:: vectors_p3_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Construct a block of code that creates a vector called ``nums`` whose elements are five ``1``'s.
            Then make a copy of this vector called ``digits``, and use vector operations to change
            digits to ``{1, 2, 3}``.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: vectors_p3_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to construct the code.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            int main() {
                vector<int> nums (5, 1);
                vector<int> digits = nums;  
                digits.pop_back();
                digits.pop_back();
                digits[1]++;
                digits[2] = digits[2] * 3;
            }


.. tabbed:: vectors_p4_ac

    .. tab:: Question

        .. activecode:: vectors_p4_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Construct a block of code that loops over a vector called ``numbers``
            and transforms the vector so each element is doubled.
            ~~~~
            #include <iostream>
            #include <vectors>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: vectors_p4_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to construct the code.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            int main() {
                vector<int> numbers = {1, 2, 3, 4, 5};
                for (size_t i = 0; i < numbers.size(); i++) {
                    numbers[i] = numbers[i] * 2;
                }
            }


.. tabbed:: vectors_p5_ac

    .. tab:: Question

        .. activecode:: vectors_p5_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Suppose you have the vector ``words``. 
            Construct a block of code that transforms the vector to: ``vector<string> words = {"cAr", "cAt", "switch", "mArio"}``.
            Write the necessary code. 
            ~~~~
            #include <iostream>  
            #include <vector>
            using namespace std;

            int main() {
                vector<string> words = {"car", "cat", "switch", "princess"};
                // YOUR CODE HERE
            

            }

    .. tab:: Answer

        .. activecode:: vectors_p5_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to construct the code.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            int main() {
                vector<string> words = {"car", "cat", "switch", "princess"};
                words.pop_back();
                words.push_back("mario");
                for (size_t i = 0; i < words.size(); ++i) {
                    for (size_t c = 0; c < words[i].size(); ++c) { 
                        if (words[i][c] == 'a') {
                            words[i][c] = 'A';
                        }
                    }
                }
            }


.. tabbed:: vectors_p6_ac

    .. tab:: Question

        .. activecode:: vectors_p6_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Suppose you run Club Keno, and you are in charge of picking the 20
            random numbered balls between 1 and 80.  Construct a block of code that
            chooses these random numbers, then saves them to a vector called ``keno``.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: vectors_p6_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to construct the code
            ~~~~
            #include <iostream> 
            #include <vector>
            using namespace std;

            int main() {
                vector<int> keno = {};
                for (size_t i = 0; i < 20; i++) {
                    int x = random ();
                    int y = x % 80;
                    keno.push_back(y + 1);
                }
            }


.. tabbed:: vectors_p7_ac

    .. tab:: Question

        .. activecode:: vectors_p7_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Suppose you have the defined vector ``album``. Construct a block of code that counts how many songs in ``album`` start with b. Write the necessary code. 
            ~~~~
            #include <iostream> 
            #include <vector>
            using namespace std;

            int main() {
                vector<string> album = {"imagine", "needy", "NASA", "bloodline", "fake smile", "bad idea", "make up", "ghostin", "in my head", "7 rings", "thank u, next", "break up with your girlfriend, i'm bored"};
                // YOUR CODE HERE


            }

    .. tab:: Answer

        .. activecode:: vectors_p7_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to construct the code
            ~~~~
            #include <iostream> 
            #include <vector>
            using namespace std;

            int main() {
                vector<string> album = {"imagine", "needy", "NASA", "bloodline", "fake smile", "bad idea", "make up", "ghostin", "in my head", "7 rings", "thank u, next", "break up with your girlfriend, i'm bored"};
                int count = 0;
                for (size_t i = 0; i < album.size(); i++) {
                    if (album[i][0] == 'b') {
                        ++count;
                    }
                }
            }


.. tabbed:: vectors_p8_ac

    .. tab:: Question

        .. activecode:: vectors_p8_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Suppose you have the defined vectors, ``temps`` and ``precip``. Your family will go to the beach if the temperature at least 75 degrees and the chance
            of precipitation is less than 50%.  Construct a block of code that counts how many days
            your family can hit the beach on your vacation.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            int main(){
                vector<double> temps = {82.0, 76.8, 74.3, 58.8, 79.2, 73.4, 80.1};
                vector<double> precip = {0.00, 0.30, 0.60, 0.90, 0.10, 0.20, 0.80};
                // YOUR CODE HERE

            
            }

    .. tab:: Answer

        .. activecode:: vectors_p8_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to construct the code
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            int main() {
                vector<double> temps = {82.0, 76.8, 74.3, 58.8, 79.2, 73.4, 80.1};
                vector<double> precip = {0.00, 0.30, 0.60, 0.90, 0.10, 0.20, 0.80};
                int count = 0;
                for (int i = 0; i < 7; ++i) {
                    if (temps[i] >= 75.0 && precip[i] < 0.50) {
                        ++count;
                    }
                }
            }


.. tabbed:: vectors_p9_ac

    .. tab:: Question

        .. activecode:: vectors_p9_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Suppose you have the defined vector ``nouns``. Construct a block of code that creates a vector of the **proper** nouns in ``nouns``.
            Use the ``isupper`` function to check if a letter is uppercase.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            int main() {
                vector<string> nouns = {"cereal", "Cocoa Puffs", "Mario", "luigi", "Aerosmith"};
                // YOUR CODE HERE

                
            }

    .. tab:: Answer

        .. activecode:: vectors_p9_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to construct the code. For this question, the ``isupper`` function is not defined but it returns a bool determined by an input of a string.
            ~~~~
            #include <iostream>
            #include <vector> 
            using namespace std;

            int main() {
                vector<string> nouns = {"cereal", "Cocoa Puffs", "Mario", "luigi", "Aerosmith"};
                vector<string> proper = {};
                for (size_t i = 0; i < nouns.size(); ++i) {
                    if (isupper(nouns[i][0])) {
                        proper.push_back(nouns[i]);
                    }
                }
            }


.. tabbed:: vectors_p10_ac

    .. tab:: Question           

        .. activecode:: vectors_p10_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Suppose you have the already defined ``howMany`` function and ``excl`` vector. Construct a block of code that counts how many times ".", "!", and "?" occur in ``excl``.
            Save the counts to a vector with "." count as the first element, "!" count as the second, and "?" count as the third.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            int howMany (const vector<string>& vec, char let) {
                int count = 0;
                for (size_t i = 0; i < vec.size(); i++) {
                    for (size_t c = 0; c < vec[i].size(); c++) {
                        if (vec[i][c] == let) {
                            count++;                                      
                        }
                    }
                }
                return count;
            }

            int main() {
                vector<string> excl = {"what?!", "how???", "fine!", "STOP.", "yay!!!!!", "ugh...!"};
                // YOUR CODE HERE
                

            }

    .. tab:: Answer

        .. activecode:: vector_p10_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to construct the code
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            int howMany (const vector<string>& vec, char let) {
                int count = 0;
                for (size_t i = 0; i < vec.size(); i++) {
                    for (size_t c = 0; c < vec[i].size(); c++) {
                        if (vec[i][c] == let) {
                            count++;                                      
                            }
                    }
                }
                return count;
            }

            int main() {
                vector<string> excl = {"what?!", "how???", "fine!", "STOP.", "yay!!!!!", "ugh...!"};
                vector<char> punc = {'.', '!', '?'};
                vector<int> counts = {};
                for (int i = 0; (unsigned)i < punc.size(); ++i) {
                    counts.push_back(howMany(excl, punc[i]));
                }
            }
