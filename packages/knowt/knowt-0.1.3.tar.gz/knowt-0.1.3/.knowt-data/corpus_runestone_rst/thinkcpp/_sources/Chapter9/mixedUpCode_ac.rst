Activecode Exercises
----------------------

Answer the following **Activecode** questions to
assess what you have learned in this chapter.

.. tabbed:: mucp_9_1_ac
   
    .. tab:: Question

        .. activecode:: mucp_9_1_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the code for the struct definition of ``Movie``. 
            The Movie structure will have the instance variables title, 
            director, and releaseYear in that order. 
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_9_1_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to define the ``Movie`` struct.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Movie {
                string title;
                string director;
                int releaseYear;
            };


.. tabbed:: mucp_9_2_ac

    .. tab:: Question

        .. activecode:: mucp_9_2_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
        
            Let's write the code for the ``printMovie`` function. 
            printMovie should print the information about a movie
            in the following format: "title" directed by director (releaseYear).
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_9_2_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the ``printMovie`` function.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Movie {
                string title;
                string director;
                int releaseYear;
            };

            void printMovie (const Movie& m) {
                cout << "\"" << m.title << "\" directed by ";
                cout << m.director << " (" << m.releaseYear << ")" << endl; 
            }


.. tabbed:: mucp_9_3_ac
   
    .. tab:: Question

        .. activecode:: mucp_9_3_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
            
            Let's write the code for the ``movieAge`` function. 
            movieAge should take a Movie and currentYear as a parameter and
            return how many years it has been since the releaseYear.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_9_3_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
            
            Below is one way to write the ``movieAge`` function.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Movie {
                string title;
                string director;
                int releaseYear;
            };

            int movieAge (const Movie& m, int currentYear) {
                return currentYear - m.releaseYear;
            }


.. tabbed:: mucp_9_4_ac

    .. tab:: Question

        .. activecode:: mucp_9_4_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
            
            Let's write the code for the struct definition of ``Date``.
            The Date structure will have three integer instance variables: day, 
            month, and year in that order. 
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE

        
    .. tab:: Answer

        .. activecode:: mucp_9_4_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to define the ``Date`` structure.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Date {
                int day;
                int month;
                int year;
            };


.. tabbed:: mucp_9_5_ac

    .. tab:: Question

        .. activecode:: mucp_9_5_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the code for the ``printDate`` function. 
            printDate should print the date in the following format: 
            month/date/year.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_9_5_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the ``printDate`` function.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Date {
                int day;
                int month;
                int year;
            };

            void printDate (const Date& d) {
                cout << d.month << "/" << d.day << "/" << d.year << endl;
            }


.. tabbed:: mucp_9_6_ac

    .. tab:: Question

        .. activecode:: mucp_9_6_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the code for the ``nextMonth`` function. 
            nextMonth should change the date to one month later.
            For example, 3/4/2020 gets modified to 4/4/2020, and 12/3/2020
            gets modified to 1/3/2021.
            ~~~~
            #include <iostream> 
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_9_6_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the nextMonth function.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Date {
                int day;
                int month;
                int year;
            };

            void nextMonth (Date& d) {
                if (d.month == 12) {
                    d.month = 1;
                    d.year++;
                    d.year = 1;
                }
                else {
                    d.month++;
                }
            }


.. tabbed:: mucp_9_7_ac

    .. tab:: Question

        .. activecode:: mucp_9_7_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the code for the struct definition of ``Length``. 
            Length should have the instance variables inches, feet, and yard.
            ~~~~
            #include <iostream> 
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_9_7_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
            
            Below is one way to defiine the ``Length`` structure.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Length {
                int inches;
                int feet;
                int yards;
            };


.. tabbed:: mucp_9_8_ac

    .. tab:: Question

        .. activecode:: mucp_9_8_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the code for the ``printLength`` function. 
            printLength should print the date in the following format: 
            yards yds, feet ft, inches in.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_9_8_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the ``printLength`` function.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Length {
                int inches;
                int feet;
                int yards;
            };
            
            void printLength (const Length& l) {
                cout << l.yards << " yds, " << l.feet << " feet, " << l.inches << " in" << endl;
            }


.. tabbed:: mucp_9_9_ac

    .. tab:: Question

        .. activecode:: mucp_9_9_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the code for the ``allInches`` function. 
            printLength should modify a Length object to convert all
            feet and yards to inches. For example, a Length with 1 yard, 2 feet, and 3
            inches is converted into a Length with 0 yards, 0 feet, and 63 inches.
            ~~~~
            #include <iostream> 
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer 

        .. activecode:: mucp_9_9_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the ``allInches`` function.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Length {
                int inches;
                int feet;
                int yards;
            };

            void allInches (Length& l) {
                l.inches += 36 * l.yards + 12 * l.feet;
            }


.. tabbed:: mucp_9_10_ac

    .. tab:: Question

        .. activecode:: mucp_9_10_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the code for the ``addLengths`` function. 
            addLengths should take three Lengths as parameters. 
            It should then add the first two Lengths and store the result
            in the third Length. If there is over 12 inches or over 3 feet,
            convert it to the proper amound of feet and yards (13 inches becomes 1 foot and 1 inch).
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE

            
    .. tab:: Answer

        .. activecode:: mucp_9_10_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the ``addLengths`` function.
            ~~~~
            #include <iostream> 
            using namespace std;

            struct Length {
                int inches;
                int feet;
                int yards;
            };
            
            void addLengths (const Length& first, const Length& second, Length& total) {
                total.inches = first.inches + second.inches;
                total.feet = first.feet + second.feet;
                total.yards = first.yards + second.yards;
                if (total.inches >= 12) {
                    int addFeet = total.inches % 12;
                    total.feet += addFeet;
                    total.inches = total.inches - addFeet * 12;
                }
                if (total.feet >= 3) {
                    int addYards = total.feet % 3;
                    total.yards += addYards;
                    total.feet = total.feet - addYards * 3;
                }
            }