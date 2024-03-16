Coding Practice
---------------

.. tabbed:: cp_11_1

    .. tab:: Question

        .. activecode:: cp_11_AC_1q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :practice: T

           Write the ``Cake`` structure, which has instance variables name, weight and member function has_icing function that returns a bool. Use the ``Cake`` object initialised below to invoke the has_icing function.
           ~~~~
           #include <iostream>
           using namespace std;

           // Write your code for the struct Cake here.

           int main() {
               Cake c = { "Choco lava", 3.5};
               // Write your code to invoke the has_icing function here
           }


    .. tab:: Answer

        .. activecode:: cp_11_AC_1a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:

           Below is one way to implement the program. We declare the ``Cake`` struct and list the instance
           variables in order.
           ~~~~
           #include <iostream>
           using namespace std;

           struct Cake {
               string name;
               double weight;
               bool has_icing;
           };

           int main() {
                Cake c = { "Choco lava", 3.5};
                cout << c.has_icing() << endl;
           }
           
.. tabbed:: cp_11_2

    .. tab:: Question

        .. activecode:: cp_11_AC_2q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :practice: T

           The ``Cake`` structure has instance variables name, weight and member function has_icing. Write the has_icing function which returns true when the weight is greater than 10.
           ~~~~
           #include <iostream>
           using namespace std;

           struct Cake {
               string name;
               double weight;
               bool has_icing ();
           };
           
           // Write your code for the has_icing function

           int main() {
                Cake c = {"Choco lava", 3.5};
           }


    .. tab:: Answer

        .. activecode:: cp_9_AC_2a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:

           Below is one way to implement the program.
           ~~~~
           #include <iostream>
           using namespace std;

           struct Cake {
               string name;
               double weight;
               bool has_icing();
           };

           bool Cake::has_icing() {
                if (weight > 10) {
                  return true;
                }
                else {
                  return false;
                }
           }
           
           int main() {
                Cake c ("Choco lava", 3.5);
           }

.. tabbed:: cp_11_3

    .. tab:: Question

        .. activecode:: cp_11_AC_3q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :practice: T

           Create the ``Music`` structure, with member variables num_sold and year, and member functions ``sold`` and ``is_new``. The ``sold`` function should print twice the num_sold while the ``is_new`` function should return true if the year is greater than 2012.
           ~~~~
           #include <iostream>
           using namespace std;

           // Write your code for the struct Music here.

           // Write the implementation for the member functions here
           
           int main() {
               Music m = {4, 2013};
           }


    .. tab:: Answer

        .. activecode:: cp_11_AC_3a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:
           
           Below is one way to implement the program.
           ~~~~
           #include <iostream>
           using namespace std;

           struct Music {
               int num_sold;
               int year;
               void sold (int num_sold);
               bool is_new (int year);
           };

           void Music::sold (int num_sold) {
              cout << 2 * num_sold << endl;
           }
           
           bool Music:: is_new (int year) {
              if (year > 2012) {
                return true;
              }
              else {
                return false;
              }
           }

           int main() {
               Music m = {4, 2013};
           }

.. tabbed:: cp_11_4

    .. tab:: Question

        .. activecode:: cp_11_AC_4q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :practice: T
           
           Create the ``Music`` structure, with member variables num_sold and year, and member function ``latest``. The ``latest`` function operates on two ``Music`` objects, and returns true if the current object's year is greater than the other's.
           ~~~~
           #include <iostream>
           using namespace std;

           // Write your code for the struct Music here.

           // Write the implementation for the member function latest here
           
           int main() {
               Music m = {4, 2013};
               Music m_other = {198, 2009};
               bool is_newer = m.latest(m_other);
           }


    .. tab:: Answer

        .. activecode:: cp_11_AC_4a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:

           Below is one way to implement the program.
           ~~~~
           #include <iostream>
           using namespace std;

           struct Music {
               int num_sold;
               int year;
               bool latest (const &Music m_other) const;
           };
           
           bool Music:: latest (const &Music m_other) const {
              if (year > m_other.year) {
                return true;
              }
              else {
                return false;
              }
           }

           int main() {
               Music m = {4, 2013};
               Music m_other = {198, 2009};
               bool is_newer = m.latest(m_other);
           }

.. tabbed:: cp_11_5

    .. tab:: Question

        .. activecode:: cp_11_AC_5q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write the function ``printInfo``, which prints the music album's information in the format
            "This is a ``artist``, ``year`` album with/without featured artists." If ``artist`` has the value "n/a", ``printInfo`` prints out "Unknown ``artist``! Your album is from ``year``."
            ~~~~
            #include <iostream>
            using namespace std;

            struct Music {
                string artist;
                int year;
                bool has_featured;
            };

            // Write your code for the printInfo function here.

            int main() {
                Music m1 = { "n/a", 2007, true };
                printInfo (m1);
                Cake c2 = { "Drake", 2016, false };
                printInfo (m2);
            }

    .. tab:: Answer

        .. activecode:: cp_11_AC_5a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
            :optional:

            Below is one way to implement the program.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Music {
                string artist;
                int year;
                bool has_featured;
            };

            void printInfo (Music m) {
                if (m.artist == "n/a") {
                    cout << "Unknown artist! Your album is from " << m.year << "." << endl;
                }
                else {
                    if (m.has_featured == true) {
                        cout << "This is a " << m.artist << ", " << m.year << " album with featured artists." << endl;
                    }
                    if (m.has_featured == false) { 
                        cout << "This is a " << m.artist << ", " << m.year << " album without featured artists." << endl;
                    }
                }
            }

            int main() {
                Music m1 = { "n/a", 2007, true };
                printInfo (m1);
                Music m2 = { "Drake", 2016, false };
                printInfo (m2);
            }

.. tabbed:: cp_11_6

    .. tab:: Question

        .. activecode:: cp_11_AC_6q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :practice: T

           The ``Music`` structure has instance variables name, weight and member function has_icing. Write the has_icing function which returns true when the weight is greater than 10.
           ~~~~
           #include <iostream>
           using namespace std;

           struct Cake {
               string name;
               double weight;
               bool has_icing ();
           };
           
           // Write your code for the has_icing function

           int main() {
                Cake c = {"Choco lava", 3.5};
           }


    .. tab:: Answer

        .. activecode:: cp_11_AC_6a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:

           Below is one way to implement the program.
           ~~~~
           #include <iostream>
           using namespace std;

           struct Cake {
               string name;
               double weight;
               bool has_icing();
           };

           bool Cake::has_icing() {
                if (weight > 10) {
                  return true;
                }
                else {
                  return false;
                }
           }
           
           int main() {
                Cake c ("Choco lava", 3.5);
           }

.. tabbed:: cp_11_7

    .. tab:: Question

        .. activecode:: cp_11_AC_7q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :practice: T

           Write the ``Pants`` structure, which has instance variables size and material. Also write a constructor for ``Pants`` that would be called when p1 is declred. The constructor sets the size to L and material to cotton.
           ~~~~
           #include <iostream>
           using namespace std;

           // Write your code for the struct Pants here.
           
           // Write your code for the constructor here

           int main() {
               Pants p = { 'S', "denim" };
               Pants p1;
           }


    .. tab:: Answer

        .. activecode:: cp_11_AC_7a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:

           Below is one way to implement the program. We declare the ``Pants`` struct and list the instance
           variables in order. In addition, we write a default constructor.
           ~~~~
           #include <iostream>
           using namespace std;

           struct Pants {
               char size;
               string material;
               Pants();
           };
           
           Pants::Pants () {
              size = 'L';
              material = "cotton";
           }

           int main() {
               Pants p = { 'S', "denim" };
               Pants p1;
           }

.. tabbed:: cp_11_8

    .. tab:: Question
            
        .. activecode:: cp_11_AC_8q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :practice: T

           Implement 2 constructors for the struct ``Book``, which has the instance variables name and publish_year. One should be a default constructor  that sets name to N/A and publish_year to 0. The other constructor should take arguments
           ~~~~
           #include <iostream>
           using namespace std;

           struct Book {
               string name;
               int publish_year;
               bool is_famous ();
               Book ();
               Book (string name_in, int publish_year_in);
           };
           
           // Write your code for the default constructor here
           
           // Write the constructor for the argument taking constructor here

           int main() {
               Book b1;
               Book b2 ("Kane and Abel", 1979);
           }


    .. tab:: Answer    

        .. activecode:: cp_11_AC_8a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:

           Below is one way to implement the program.
           ~~~~
           #include <iostream>
           using namespace std;

           struct Book {
               string name;
               int year;
               bool is_famous ();
               Book ();
               Book (string name_in, int publish_year_in);
           };
           
           Book::Book () {
              name = "N/A";
              publish_year = 0;
           }
           
           Book::Book (string name_in, int publish_year_in) {
              name = name_in;
              publish_year = publish_year_in ;
           }
           
           int main() {
               Book b1;
               Book b2 ("Kane and Abel", 1979);
           }

.. tabbed:: cp_11_9

    .. tab:: Question
            
        .. activecode:: cp_11_AC_9q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :practice: T

           Implement the struct ``Book`` as would appear in the Book.h header file and the following necessary statement in main.cpp in order for thr program to run
           ~~~~
           struct Book {
               // Group and label the following as instance variables, constructors, modifiers or functions as would be seen in a header (Book.h) file
               string name;
               int publish_year;
               bool is_famous ();
               Book ();
               Book (string name_in, int publish_year_in);
           };
           

           #include <iostream>
           using namespace std;
           // Write the inclusion of the header file that is needed in main.cpp
           
           int main() {
               Book b1;
               Book b2 ("Kane and Abel", 1979);
           }


    .. tab:: Answer      

        .. activecode:: cp_11_AC_9a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:

           Below is one way to implement the program.
           ~~~~
           struct Book {
               // Instance variables
               string name;
               int publish_year;
               // Functions
               bool is_famous ();
               // Constructors
               Book ();
               Book (string name_in, int publish_year_in);
           };
           

           #include <iostream>
           using namespace std;
           #include "Book.h"
           
           int main() {
               Book b1;
               Book b2 ("Kane and Abel", 1979);
           }

.. tabbed:: cp_11_10

    .. tab:: Question

        .. activecode:: cp_11_AC_10q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :practice: T

           Implement the struct ``Instrument`` struct along with 2 constructors for the same (default and one that takes parameters). ``Instrument`` has the instance variables name, year_made and function is_popular(). The default constructor sets name to guitar and year_made to 2000.
           ~~~~
           #include <iostream>
           using namespace std;
           
           // Write your struct definition and constructors here
           
           int main() {
               Instrument first;
               Instrument second ("ukulele", 2012);
           }


    .. tab:: Answer       

        .. activecode:: cp_11_AC_10a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:

           Below is one way to implement the program.
           ~~~~
           #include <iostream>
           using namespace std;

           struct Instrument {
               string name;
               int year_made;
               bool is_popular ();
               Instrument ();
               Instrument (string name_in, int year_made_in);
           };
           
           Instrument::Instrument () {
              name = "guitar";
              publish_year = 2000;
           }
           
           Instrument::Instrument (string name_in, int year_made_in) {
              name = name_in;
              year_made = year_made_in;
           }
           
           int main() {
               Instrument first;
               Instrument second ("ukulele", 2012);
           }
