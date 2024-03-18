Coding Practice
---------------

.. tabbed:: cp_14_1

    .. tab:: Question

        Below is the ``struct`` definition for ``Room``, which has a length,
        width, and height. It also has two member functions, ``calculateArea``
        and ``calculateVolume``. Turn this ``struct`` into a ``class`` with 
        private member variables.

        .. activecode:: cp_14_AC_1q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :practice: T

           #include <iostream>
           using namespace std;

           // Turn the struct definition of Room into a class definition.
           struct Room {
               int length;
               int width;
               int height;

               int calculateArea () {
                   return length * width;
               }

               int calculateVolume () {
                   return length * width * height;
               }
           };

    .. tab:: Answer

        Below is the ``class`` definition of ``Room``. As you can see, there isn't 
        a big difference between ``struct``\s and ``class``\es.

        .. activecode:: cp_14_AC_1a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:

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
           };

.. selectquestion:: cp_14_AC_2_sq
    :fromid: cp_14_AC_2q, cp_14_AC_2q_pp
    :toggle: lock

.. tabbed:: cp_14_3

    .. tab:: Question

        Below is the ``class`` definition for ``Temp``. Write
        the private member functions ``cToF`` and ``fToC``,
        which converts Celsius to Fahrenheit and vice versa
        and returns the conversion. Update ``getFahrenheit``
        and so that if ``is_celsius`` is
        true and a user calls ``getFahrenheit``, it will 
        call ``cToF`` and return the correct temperature
        in degrees Fahrenheit. Do the same for ``getCelsius``.

        .. activecode:: cp_14_AC_3q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :practice: T

           #include <iostream>
           using namespace std;

           class Temp {
               private:
                   double fahrenheit;
                   double celsius;
                   bool is_fahrenheit;
                   bool is_celsius;

                   // Write your implementation of cToF here.

                   // Write your implementation of fToC here.

               public:
                   double getFahrenheit () { return fahrenheit; }
                   double getCelsius () { return celsius; }
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

    .. tab:: Answer

        Below is one way to implement this. We use the correct conversions
        in ``cToF`` and ``fToC`` and then call these functions in 
        ``getFahrenheit`` and ``getCelsius`` if needed.

        .. activecode:: cp_14_AC_3a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:

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

.. selectquestion:: cp_14_AC_4_sq
    :fromid: cp_14_AC_4q, cp_14_AC_4q_pp
    :toggle: lock

.. tabbed:: cp_14_5

    .. tab:: Question

        We took a look at ``vector``\s in chapter 10, where we saw 
        how we could add data to the end of a ``vector`` and remove
        data from the end of a ``vector``. But what if we wanted to
        add and remove things at the beginning of a ``vector``? Or we wanted to 
        print out a ``vector`` without painfully constructing a 
        loop every time? We can create our own ``MyVector`` class! 
        Write the ``MyVector`` class, which has a ``vector`` of ``int``\s as a 
        private member variable. Also write the default constructor.

        .. activecode:: cp_14_AC_5q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :practice: T

           #include <iostream>
           #include <vector>
           using namespace std;

           // Write the class definition for MyVector here.

    .. tab:: Answer

        Below is the ``class`` definition of ``MyVector``. We use the ``public`` 
        and ``private`` keywords to separate public and private members of 
        our class. The default constructor sets size to 0.

        .. activecode:: cp_14_AC_5a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:

           #include <iostream>
           #include <vector>
           using namespace std;

           class MyVector {
               private: 
                   vector<int> elements;

               public:  
                   MyVector() {};
           };

.. selectquestion:: cp_14_AC_6_sq
    :fromid: cp_14_AC_6q, cp_14_AC_6q_pp
    :toggle: lock

.. tabbed:: cp_14_7

    .. tab:: Question

        The reason why we have ``elements`` as a private member variable is that
        people using our ``MyVector`` class don't need to know how we implemented
        our class, so we can implement it however we want. 
        This means for functions ``MyVector`` has that overlap with 
        functions that ``vector`` has, we can just call the same function 
        on our ``elements`` vector. Write the ``MyVector`` functions 
        ``size``, ``push_back``, ``pop_back``, and ``at``. ``size`` returns
        the size of our ``MyVector``. ``push_back`` takes an 
        ``int`` and adds it to the end of our ``MyVector``. ``pop_back``
        removes the last element. ``at`` takes an index and returns the
        data stored at that index. Use existing ``vector`` functions to 
        implement these ``MyVector`` functions!

        .. activecode:: cp_14_AC_7q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :practice: T

           #include <iostream>
           #include <vector>
           using namespace std;

           class MyVector {
               private: 
                   vector<int> elements;

               public:  
                   MyVector() {};
                   MyVector(vector<int> vec);

                   // Write the size function here.
                   
                   // Write the push_back function here.

                   // Write the pop_back function here.

                   // Write the at function here.
           };

           int main() {
               vector<int> data = { 2, 4, 1, 5, 2, 6 };
               MyVector myVec(data);
               cout << "The first element is " << myVec.at(0) << endl;
               myVec.pop_back();
               myVec.pop_back();
               myVec.push_back(12);
               cout << "The size of myVec is " << myVec.size() << endl;
               cout << "The last three elements are " << myVec.at(2) << ", " 
                    << myVec.at(3) << ", and " << myVec.at(4) << endl;
           } 
           ====
           MyVector::MyVector (vector<int> vec) {
               elements = vec;
           }

    .. tab:: Answer

        Below is one way to implement these functions. Since these
        functions are defined for ``vector``\s, we can call them 
        on ``elements``.

        .. activecode:: cp_14_AC_7a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:

           #include <iostream>
           #include <vector>
           using namespace std;

           class MyVector {
               private: 
                   vector<int> elements;

               public:  
                   MyVector() {};
                   MyVector(vector<int> vec);

                   int size() { return elements.size(); }
                   void push_back(int value) { elements.push_back(value); }
                   void pop_back() { elements.pop_back(); };
                   int at(int index) { return elements[index]; }
           };

           int main() {
               vector<int> data = { 2, 4, 1, 5, 2, 6 };
               MyVector myVec(data);
               cout << "The first element is " << myVec.at(0) << endl;
               myVec.pop_back();
               myVec.pop_back();
               myVec.push_back(12);
               cout << "The size of myVec is " << myVec.size() << endl;
               cout << "The last three elements are " << myVec.at(2) << ", " 
                    << myVec.at(3) << ", and " << myVec.at(4) << endl;
           } 
           ====
           MyVector::MyVector (vector<int> vec) {
               elements = vec;
           }

.. selectquestion:: cp_14_AC_8_sq
    :fromid: cp_14_AC_8q, cp_14_AC_8q_pp
    :toggle: lock

.. tabbed:: cp_14_9

    .. tab:: Question

        Let's write the ``MyVector`` member function ``push_front`` and
        ``pop_front``. ``push_front`` should take a value and add it
        to the front of our ``MyVector``, and ``pop_front`` should
        remove the first element.

        .. activecode:: cp_14_AC_9q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :practice: T

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
                   void print();
           };

           // Write your implementation of push_front here.

           // Write your implementation of pop_front here.

           int main() {
               vector<int> data = { 2, 14, 5 };
               MyVector myVec(data);
               myVec.pop_front();
               myVec.push_front(5);
               myVec.push_front(10);
               cout << "The new size is " << myVec.size(); << endl;
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

           void MyVector::print() {
               cout << "[";
               for (size_t i = 0; i < elements.size() - 1; ++i) {
                   cout << elements[i] << ", ";
               }
               cout << elements[elements.size() - 1] << "]" << endl;
           }

    .. tab:: Answer

        Below is one way to implement these functions. For push_front,
        we can create a temporary vector and add the new element to the
        front before pushing the rest of the old elements to the back.
        For pop_front, we can shift all elements up by one index and 
        pop the last element off. 

        .. activecode:: cp_14_AC_9a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:

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
                   void print();
           };

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

           int main() {
               vector<int> data = { 2, 14, 5 };
               MyVector myVec(data);
               myVec.pop_front();
               myVec.push_front(5);
               myVec.push_front(10);
               cout << "The new size is " << myVec.size() << endl;
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

           void MyVector::print() {
               cout << "[";
               for (size_t i = 0; i < elements.size() - 1; ++i) {
                   cout << elements[i] << ", ";
               }
               cout << elements[elements.size() - 1] << "]" << endl;
           }

.. selectquestion:: cp_14_AC_10_sq
    :fromid: cp_14_AC_10q, cp_14_AC_10q_pp
    :toggle: lock