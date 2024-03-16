Coding Practice
---------------

.. tabbed:: cp_14_2_q

    .. tab:: Activecode

        .. activecode:: cp_14_AC_2q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            There are errors in the code below. Modify the code so that ``main`` runs
            successfully. Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            class Room {
                private: 
                    int length;
                    int width;
                    int height;

                public:  
                    int calculateArea () {
                        return length * width;
                    }

                    int calculateVolume () {
                        return length * width * height;
                    }

                    // Add any necessary functions here.
            };

            int main() {
                Room r;
                r.length = 12;
                r.width = 14;
                r.height = 10;
                cout << "The room with dimensions " << r.length ", " << r.width 
                    << ", and " << r.height << " has an area of " << r.calculateArea() 
                    << " and a volume of " << r.calculateVolume << endl;
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_14_AC_2q_pp
            :numbered: left
            :adaptive:

            There are errors in the code below. Modify the code so that ``main`` runs
            successfully. Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            class Room {
                private:
                    int length;
                    int width;
                    int height;
            =====
                public:
                    int calculateArea () {
                        return length * width;
                    }
            =====
                    int calculateVolume () {
                        return length * width * height;
                    }
            =====
                    void setLength (int l) {
                        length = l;
                    }
            =====
                    int getLength () const {
                        return length;
                    }
            =====
                    void setWidth (int w) {
                        width = w;
                    }
            =====
                    int getWidth () const {
                        return width;
                    }
            =====
                    void setHeight (int h) {
                        height = h;
                    }
            =====
                    int getHeight () const {
                        return height;
                    }
            =====
            };
            =====
            int main() {
            =====
                Room r;
            =====
                r.setLength(12);
            =====
                r.setWidth(14);
            =====
                r.setHeight(10);
            =====
                cout << "The room with dimensions " << r.getLength() << ", " << r.getWidth()
                    << ", and " << r.getHeight() << " has an area of " << r.calculateArea()
                    << " and a volume of " << r.calculateVolume() << endl;
            =====
            }

.. tabbed:: cp_14_4_q

    .. tab:: Activecode

        .. activecode:: cp_14_AC_4q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            In ``main`` create a ``Temp`` object to calculate 
            what 100 degrees Celsius is in Fahrenheit.
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            class Temp {
                private:
                    double fahrenheit;
                    double celsius;
                    bool is_fahrenheit;
                    bool is_celsius;

                    double cToF() {
                        return celsius * 9/5 + 32;
                    }

                    double fToC() {
                        return (fahrenheit - 32) * 5/9;
                    }

                public:
                    double getFahrenheit () { 
                        if (is_celsius) { return cToF(); }
                        else { return fahrenheit; }
                    }
                    double getCelsius () { 
                        if (is_fahrenheit) { return fToC(); }
                        else { return celsius; }
                    }
                    void setFahrenheit (double f) { fahrenheit = f; is_fahrenheit = true; is_celsius = false; }
                    void setCelsius (double c) { celsius = c; is_celsius = true; is_fahrenheit = false; }
                    void printTemp () {
                        if (is_fahrenheit) {
                            cout << "It is " << getFahrenheit() << " degrees Fahrenheit" << endl;
                        }
                        else {
                            cout << "It is " << getCelsius() << " degrees Celsius" << endl;
                        }
                    }
            };

            int main() {
                // Write your code here.
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_14_AC_4q_pp
            :numbered: left
            :adaptive:

            In ``main`` create a ``Temp`` object to calculate 
            what 100 degrees Celsius is in Fahrenheit.
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            int main() {
            =====
                Temp t;
            =====
                t.setCelsius(100);
            =====
                t.setFahrenheit(t.getFahrenheit());
            =====
                t.printTemp();
            =====
            }

.. tabbed:: cp_14_6_q

    .. tab:: Activecode

        .. activecode:: cp_14_AC_6q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            What if we had an existing ``vector`` with data that we want to copy
            into our ``MyVector``? Write a constructor that takes a ``vector``
            and copies the data into the ``elements`` vector. 
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            class MyVector {
                private: 
                    vector<int> elements;

                public:  
                    MyVector() {};
                    // Write your constructor here.
            };

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_14_AC_6q_pp
            :numbered: left
            :adaptive:

            What if we had an existing ``vector`` with data that we want to copy
            into our ``MyVector``? Write a constructor that takes a ``vector``
            and copies the data into the ``elements`` vector.
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            MyVector (vector<int> vec) {
            =====
               elements = vec;
            =====
            }

.. tabbed:: cp_14_8_q

    .. tab:: Activecode

        .. activecode:: cp_14_AC_8q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Now we can write some of our own fun functions! No longer
            do we need to write ``for`` loops every time we want to
            print out a ``vector``. With ``MyVector``, we can just
            call the member function ``print``! Write the ``MyVector``
            member function ``print``, which prints out the contents
            of ``MyVector``. For example, if our ``MyVector`` contained 
            the elements 2, 5, 1, and 8, ``print`` should print out
            [2, 5, 1, 8] followed by a newline.
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            class MyVector {
                private: 
                    vector<int> elements;

                public:  
                    MyVector() {};
                    MyVector(vector<int> vec);

                    int size();
                    void push_back(int value);
                    void pop_back();
                    int at(int index);

                    // Write your print function here.
            };

            int main() {
                MyVector myVec;
                myVec.push_back(13);
                myVec.push_back(2);
                myVec.push_back(4);
                myVec.push_back(7);
                myVec.push_back(9);
                myVec.push_back(24);
                myVec.print();
            }
            ====
            MyVector::MyVector (vector<int> vec) {
                elements = vec;
            }

            int MyVector::size() { return elements.size(); }

            void MyVector::push_back(int value) { elements.push_back(value); }

            void MyVector::pop_back() { elements.pop_back(); };

            int MyVector::at(int index) { return elements[index]; }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_14_AC_8q_pp
            :numbered: left
            :adaptive:

            Now we can write some of our own fun functions! No longer
            do we need to write ``for`` loops every time we want to
            print out a ``vector``. With ``MyVector``, we can just
            call the member function ``print``! Write the ``MyVector``
            member function ``print``, which prints out the contents
            of ``MyVector``. For example, if our ``MyVector`` contained 
            the elements 2, 5, 1, and 8, ``print`` should print out
            [2, 5, 1, 8] followed by a newline. Use the lines to construct
            the code, then go back to complete the Activecode tab.

            -----
            void print() {
            =====
               cout << "[";
            =====
               for (size_t i = 0; i < elements.size() - 1; ++i) {
            =====
                   cout << elements[i] << ", ";
            =====
               }
            =====
               cout << elements[elements.size() - 1] << "]" << endl;
            =====
            }

.. tabbed:: cp_14_10_q

    .. tab:: Activecode

        .. activecode:: cp_14_AC_10q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            What if we wanted to return the largest and smallest elements in our
            ``MyVector``? Write the public member functions ``max`` and ``min``
            which calls the private member functions ``findMax`` and ``findMin``.
            ``findMax`` and ``findMin`` return the indices of the max and min
            values, and ``max`` and ``min`` call these private member functions
            and return the max and min values. Select the Parsonsprob tab for hints
            for the construction of the code.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            class MyVector {
                private: 
                    vector<int> elements;

                    // Write your findMax function here.

                    // Write your findMin function here.

                public:  
                    MyVector() {};
                    MyVector(vector<int> vec);

                    int size();
                    void push_back(int value);
                    void pop_back();
                    int at(int index);
                    void print();
                    void push_front(int value);
                    void pop_front();
            };

            // Write your max function here.

            // Write your min function here.

            int main() {
                vector<int> vec = { 8, 1, 5, 87, 23, 64 };
                MyVector myVec(vec);
                cout << "The largest element is " << myVec.max() << endl;
                cout << "The smallest element is " << myVec.min() << endl;
            }
            ====
            MyVector::MyVector (vector<int> vec) {
                elements = vec;
            }

            int MyVector::size() { return elements.size(); }

            void MyVector::push_back(int value) { elements.push_back(value); }

            void MyVector::pop_back() { elements.pop_back(); };

            int MyVector::at(int index) { return elements[index]; }

            void MyVector::print() {
                cout << "[";
                for (size_t i = 0; i < elements.size() - 1; ++i) {
                    cout << elements[i] << ", ";
                }
                cout << elements[elements.size() - 1] << "]" << endl;
            }

            void MyVector::push_front(int value) {
                vector<int> temp;
                temp.push_back(value);
                for (size_t i = 0; i < elements.size(); ++i) {
                    temp.push_back(elements[i]);
                } 
                elements = temp;
            }

            void MyVector::pop_front() {
                for (size_t i = 1; i < elements.size(); ++i) {
                    elements[i - 1] = elements[i];
                }
                elements.pop_back();
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_14_AC_10q_pp
            :numbered: left
            :adaptive:

            What if we wanted to return the largest and smallest elements in our
            ``MyVector``? Write the public member functions ``max`` and ``min``
            which calls the private member functions ``findMax`` and ``findMin``.
            ``findMax`` and ``findMin`` return the indices of the max and min
            values, and ``max`` and ``min`` call these private member functions
            and return the max and min values. Use the lines to construct the code, 
            then go back to complete the Activecode tab. Be sure to declare the ``max`` and ``min``
            functions in ``public`` when you complete the Activecode.

            -----
            // findMax private member function
            int findMax (vector<int> vec) {
            =====
                int inMax;
            =====
                int max = vec[0];
            =====
                for (size_t i = 0; i < vec.size() - 1; i++) {
            =====
                    if (vec[i] > max) {
            =====
                        max = vec[i];
            =====
                        inMax = i;
            =====
                    }
            =====
                }
            =====
                return inMax;
            =====
            }
            =====
            // findMin private member function
            int findMin (vector<int> vec) {
            =====
                int inMin;
            =====
                int min = vec[0];
            =====
                for (size_t i = 0; i < vec.size(); i++) {
            =====
                    if (vec[i] < min) {
            =====
                        min = vec[i];
            =====
                        inMin = i;
            =====
                    }
            =====
                }
            =====
                return inMin;
            =====
            }
            =====
            // max public member function
            int MyVector::max () {
            =====
                return elements[findMax(elements)];
            =====
            }
            =====
            // min public member function
            int MyVector::min () {
            =====
                return elements[findMin(elements)];
            =====
            }