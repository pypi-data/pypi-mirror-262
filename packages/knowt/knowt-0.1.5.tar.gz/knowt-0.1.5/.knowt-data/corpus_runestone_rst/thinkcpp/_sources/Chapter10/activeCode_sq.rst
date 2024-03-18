Coding Practice
---------------

.. tabbed:: vectors_a2_q

    .. tab:: Activecode

        .. activecode::  vectors_a2
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Fix the function below so that it returns how many even numbers are in ``nums``.
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            int evenCount (const vector<int> &vec) {
                for (int i = 0; i < vec.size(); i++) {
                    if (i % 2 == 0) {
                        count++;
                    }
                }
                return count;
            }

            int main() {
                vector<int> vec{1,2,3,4};
                cout << evenCount(vec) << endl;
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: vectors_a2_pp
            :numbered: left
            :adaptive:

            Fix the function below so that it returns how many even numbers are in ``nums``.
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            int evenCount (const vector<int> &vec) {
            =====
                int count = 0;
            =====
                int count; #distractor
            =====
                for (int i = 0; i < vec.size(); i++) {
            =====
                    if (vec[i] % 2 == 0) {
            =====
                    if (vec[i] % 2 != 0) { #paired
            =====
                        count++;
            =====
                    }
            =====
                }
            =====
                return count;
            =====
            }

.. tabbed:: vectors_a4_q

    .. tab:: Activecode

        .. activecode::  vectors_a4
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Someone could have COVID-19 if their temperature is above 99.9 degrees Fahrenheit.  Finish 
            the code below so that it counts and prints how many students in the class may have been exposed.
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>


            using namespace std;

            int main () {
                vector<double> temps = {98.6, 97.8, 100.3, 97.2, 98.7, 97.8, 99.8, 96.9, 98.2, 99.1, 99.9};

                int covid_count = 0;
                for (int i = 0; i < temps.size(); i++) {
                    

                }
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: vectors_a4_pp
            :numbered: left
            :adaptive:

            Someone could have COVID-19 if their temperature is above 99.9 degrees Fahrenheit.  Finish 
            the code below so that it counts and prints how many students in the class may have been exposed.
            Use the lines to construct the code, then go back to complete the Activecode tab.
            -----
            #include <iostream>
            #include <vector>
            using namespace std;
            =====
            int main() {
            =====
                vector<double> temps = {98.6, 97.8, 100.3, 97.2, 98.7, 97.8, 99.8, 96.9, 98.2, 99.1, 99.9};
            =====
                int covid_count = 0;
            =====
                for (int i = 0; i < temps.size(); i++) {
            =====
                    if (temps[i] > 99.9) {
            =====
                        covid_count++;
            =====
                    }
            =====
                }
            =====
                cout << covid_count << endl;
            =====
            }

.. tabbed:: vectors_a6_q

    .. tab:: Activecode

        .. activecode::  vectors_a6
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write the function ``endsEven`` that takes a vector and removes elements from the end of the vector until
            it ends with an even number. Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            // Write the endsEven function here

            
            int main() {
                vector<int> vec{1,2,3,4,5,6,7,7,9};
                endsEven(vec);
                for(int unsigned i = 0; i < vec.size(); i++) {
                    cout << vec[i] << endl;
                }
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: vectors_a6_pp
            :numbered: left
            :adaptive:

            Write the function ``endsEven`` that takes a vector and removes elements from the end of the vector until
            it ends with an even number. Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            void endsEven (vector<int> &vec) {
            =====
            vector endsEven (vector<int> &vec) { #distractor
            =====
                while (vec.back() % 2 != 0) {
            =====
                for (int i = 0; i < vec.size(); i++) { #paired
            =====
                    vec.pop_back();
            =====
                }
            =====
            }

.. tabbed:: vectors_a8_q

    .. tab:: Activecode

        .. activecode::  vectors_a8
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write the function ``randomNums`` that takes two integers: ``num`` which is the number of random numbers
            you wish to generate, and ``max``, which is the maximum value of random number you wish to generate.  Your
            function should return a vector of ``num`` integers that are between 1 and ``max``, inclusive.
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            #include <cstdlib>
            #include <vector>
            using namespace std;

            // Write the randomNums function here


            int main() {
                int num = 10;
                int max = 100;
                randomNums(num,max);
                for (int i = 0; i < randomNums(num,max).size(); i++) {
                    cout << randomNums(num,max)[i] << endl;
                }
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: vectors_a8_pp
            :numbered: left
            :adaptive:

            Write the function ``randomNums`` that takes two integers: ``num`` which is the number of random numbers
            you wish to generate, and ``max``, which is the maximum value of random number you wish to generate.  Your
            function should return a vector of ``num`` integers that are between 1 and ``max``, inclusive.
            Use the lines to construct the code, then go back to complete the Activecode tab.
            -----
            vector<int> randomNums (int num, int max) {
            =====
                vector<int> randomVec(num);
            =====
                for (int i = 0; i < num; i++) {
            =====
                for (int i = 0; i <= randomVec.size(); i++) { #paired
            =====
                    randomVec[i] = rand() % max + 1;
            =====
                }
            =====
                return randomVec;
            =====
                return randomVec[i]; #distractor
            =====
            }

.. tabbed:: vectors_a10_q

    .. tab:: Activecode

       .. activecode::  vectors_a10
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write the function ``hundyBundy`` that returns a count of all numbers in the passed vector
            ``vec`` that are divisible by 100. Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std; 

            // Write the hundyBundy function here


            int main() {
                vector<int> vec{ 100,10,300,400,21,1000 };
                cout << hundyBundy(vec) << endl;
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: vectors_a10_pp
            :numbered: left
            :adaptive: 

            Write the function ``hundyBundy`` that returns a count of all numbers in the passed vector
            ``vec`` that are divisible by 100. Use the lines to construct the code, then go back to complete the Activecode tab.

            -----    
            int hundyBundy (const vector<int> vec) {
            =====
            vector<int> hundyBundy (const vector<int> vec) { #paired
            =====
                int count = 0;
            =====
                for (int i = 0; i < vec.size(); i++) {
            =====
                for (int i = 0; i < count(); i++) { #distractor
            =====
                    if (vec[i] % 100 == 0) {
            =====
                        count++;
            =====
                    }
            =====
                }
            =====
                return count;
            =====
            }

.. tabbed:: vectors_a12_q

    .. tab:: Activecode

        .. activecode::  vectors_a12
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write the function ``weird_print`` that prints the first half of a vector of integers in reverse order
            and then prints the second half in the order present in the vector.
            If we had ``vec = {1,2,3,4,5,6}``
            we would print ``3 2 1 4 5 6``.
            You can assume the size of the vector will always be even.
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            // Write the weird_print function here


            int main() {
                vector<int> vec{1,2,3,4,5,6};
                weird_print(vec);
            } 

    .. tab:: Parsonsprob

        .. parsonsprob:: vectors_a12_pp
            :numbered: left
            :adaptive: 

            Write the function ``weird_print`` that prints the first half of a vector of integers in reverse order
            and then prints the second half in the order present in the vector.
            If we had ``vec = {1,2,3,4,5,6}``
            we would print ``3 2 1 4 5 6``.
            You can assume the size of the vector will always be even.
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            void weird_print (vector<int> vec) {
            =====
                int half = vec.size() / 2;
            =====
                for (int i = vec.size() - 1; i >= half; i--){
            =====
                    cout << vec[i-half] << ' ';
            =====
                }
            =====
                for (int h = 0; h < half; h++) {
            =====
                    cout << vec[h + half] << ' ';
            =====
                }
            =====
                cout << endl;
            =====
            }