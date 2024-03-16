Activecode Exercises
----------------------

Answer the following **Activecode** questions to assess what you have learned in this chapter.

.. tabbed:: mucp_11_1_ac

    .. tab:: Question

     .. activecode:: mucp_11_1_ac_q
        :language: cpp
        :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

        Suppose you have the following code. Construct a block of code that would make the print function into a member function.
        ~~~~
        #include <iostream>
        #include <string>
        using namespace std;

        // Edit this code
                struct Student {
             int id, year;
             string name;
        };

        void printStudent (const Student& stu) {
             cout << stu.id << ":" << stu.year << ":" << stu.name << endl;
        }

        int main () {
              Student s1 = { 56673, 2023, "Bob" };
              printStudent (s1);
        }

    .. tab:: Answer

        .. activecode:: mucp_11_1_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
            
            Below is one way to construct the code block
            ~~~~
            #include <iostream>
            #include <string>
            using namespace std;

            struct Student {
                int id, year;
                string name;
                void print ();
            };
            
            void Student::print () {
                Student stu = *this;
                cout << stu.id << ":" << stu.year << ":" << stu.name << endl;
            }

            int main () {
                Student s1 = { 56673, 2023, "Bob" };
                s1.print();
            }


.. tabbed:: mucp_11_2_ac

    .. tab:: Question

        .. activecode:: mucp_11_2_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's make an album! Write the struct definition for
            ``Album``, which should have instance variables name and year.
            Include a member function called check that returns true if
            the song was released after 2015.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_11_2_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to define the ``Album`` struct.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Album {
                string name;
                int year;
                bool check ();
            };

            bool Album::check () {
                if (year > 2015) {
                    return true;
                }
                else {
                    return false;
                }
            }


.. tabbed:: mucp_11_3_ac

    .. tab:: Question

        .. activecode:: mucp_11_3_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write the necessary of code to establish
            the ``convertToSeconds`` member function as a part of the ``Time`` struct.
            ~~~~
            #include <iostream> 
            using namespace std;
            // YOUR CODE HERE

        
    .. tab:: Answer

        .. activecode:: mucp_11_3_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the ``convertToSeconds`` member function.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Time {
                int hour;
                int minutes;
                int second;
            };

            double Time::convertToSeconds () const {
                int minutes = time.hour * 60 + time.minutes;
                double seconds = minutes * 60 + time.second;
                return seconds;
            }


.. tabbed:: mucp_11_4_ac

    .. tab:: Question

        .. activecode:: mucp_11_4_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Create the ``Student::is_older()`` function as it would be defined INSIDE
            of the Student structure definition. This function checks if the current
            Student is older than another Student. The function is invoked on the
            current Student.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_11_4_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to create the ``Student::is_older()`` function.
            ~~~~
            #include <iostream>
            using namespace std;

            bool is_older(const Student& stu) const {
                if (age > stu.age) {return true;}
                    else {return false;}
            }


.. tabbed:: mucp_11_5_ac

    .. tab:: Question

        .. activecode:: mucp_11_5_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write the necessary code to initialise
            a constructor for type ``Days`` that takes in the number of days and
            initialises the member variables ``days``, ``weeks``, ``years``.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_11_5_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to initialize the constructor.
            ~~~~
            #include <iostream>
            using namespace std;

            Days::Days (int num_days) {
                years = num_days / 365;
                Days day;
                num_days -= years * 365;
                weeks = num_days / 7;
                num_days -= weeks * 60.0;
                days = num_days;
            }


.. tabbed:: mucp_11_6_ac

    .. tab:: Question

        .. activecode:: mucp_11_6_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write two constructors for ``Student``. One with no arguments and
            one with arguments. 
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_11_6_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the two constructors.
            ~~~~
            #include <iostream>
            using namespace std;

            Student::Student () {
                void Student::Student () {
                    id = 123456789;
                    year = 2020;
                    name = "Alice";
                }
                Student::Student (int id_in, int year_in, string name_in) {
                    Student::Student construct(int id_in, int year_in, string name_in) {
                        id = id_in;
                        year = year_in;
                        name = name_in;
            }


.. tabbed:: mucp_11_7_ac

    .. tab:: Question

        .. activecode:: mucp_11_7_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Implement two constructors for the ``Penguin`` structure. One should
            be a default constructor, the other should take arguments. The
            weight needs to be converted from pounds to kilograms in the second constructor
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_11_7_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to implement the two constructors. 
            ~~~~
            #include <iostream>
            using namespace std;

            struct Penguin {
                int age; 
                int weight;
                Penguin ();
                Penguin (int age_in, int weight_in);
            };

            Penguin::Penguin () {
                age = 1;
                weight = 24;
            }
   
            Penguin::Penguin (int age_in, int weight_in) {
                age = age_in;
                weight = weight_in;
            }


.. tabbed:: mucp_11_8_ac

    .. tab:: Question

        .. code-block:: cpp

            Days AddDays (const Days& d1, const Days& d2) {
                int days = convertToDays (d1) + convertToDays(d2);
                return makeDays (days);
            }

        .. activecode:: mucp_11_8_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write the necessary blocks of code to make the
            ``AddDays`` function below a member function.
            ~~~~
            #include <iostream>
            using namespace std;
            // EDIT THE CODE BELOW

            Days AddDays (const Days& d1, const Days& d2) {
                int days = convertToDays (d1) + convertToDays(d2);
                return makeDays (days);
            }

    
    .. tab:: Answer

        .. activecode:: mucp_11_8_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to make the ``AddDays`` function a member function.
            ~~~~
            #include <iostream>
            using namespace std;

            Days Days::add (const Days& d2) const {
                int days = convertToDays () + d2.convertToDays ();
                Days day (days);
                return day;
            }


.. tabbed:: mucp_11_9_ac

    .. tab:: Question

        .. activecode:: mucp_11_9_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write the necessary blocks of code to create a struct
            ``Penguin`` that stores name and age. In addition have 2 constructors and
            declare Penguins in main such that both are called.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_11_9_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to creat the ``Penguin`` struct and the 2 constructors.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Penguin {
                int age;
                string name;
                Penguin ();
                Penguin (int age_in, string name);
            };

            Penguin::Penguin () {
                age = 1;
                name = "Alice";
            }

            Penguin::Penguin (int age_in, string name_in) {
                age = age_in;
                name = name_in;
            }

            int main () {
                Penguin p1 ();
                Penguin p2 (3, "Bob");
            }


.. tabbed:: mucp_11_10_ac

    .. tab:: Question

        .. activecode:: mucp_11_10_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write the necessary blocks of code in order to write
            a header (.h) file for the struct ``Student``.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE

        
    .. tab:: Answer

        .. activecode:: mucp_11_10_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the header file for the ``Student`` struct.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Student {
                // instance variables
                int id, year;
                string name;
                // constructors
                Student (int id, int year, string name);
                Student ();
                // functions
                void print () const;
                bool after (const Student& stu) const;
            };
