Activecode Exercises
----------------------

Answer the following **Activecode** questions to
assess what you have learned in this chapter.


.. tabbed:: mucp_8_1_ac

    .. tab:: Question

        .. activecode:: mucp_8_1_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the code for the struct definition of ``Song``.
            The Song structure will have the instance variables string title,
            string artist, string album, and int year in that order.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_8_1_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to define the struct definition of ``Song``.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Song {
                string title;
                string artist;
                string album;
                int year;
            };


.. tabbed:: mucp_8_2_ac

    .. tab:: Question

        .. activecode:: mucp_8_2_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            In main, create a Song object called ``fly`` which holds
            the data for Frank Sinatra's "Fly Me to the Moon" from his 1964 album "It Might as Well Be Swing".
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_8_2_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to create the object in the main function.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Song {
                string title;
                string artist;
                string album;
                int year;
            };

            int main() {
                Song fly;
                fly.title = "Fly Me to the Moon";
                fly.artist = "Frank Sinatra";
                fly.album = "It Might as Well Be Swing";
                fly.year = 1964;
            }


.. tabbed:: mucp_8_3_ac

    .. tab:: Question

        .. activecode:: mucp_8_3_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the code for the ``printSong`` function. printSong
            takes a Song as a parameter and prints out the instance variables
            in the following format: "title" by artist (album, year).
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_8_3_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the printSong function.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Song {
                string title;
                string artist;
                string album;
                int year;
            };

            void printSong (Song s) {
                cout << "\"" << s.title << "\" by " << s.artist;
                cout << " (" << s.album << ", " << s.year << ")" << endl;
            }

            int main() {
                Song fly;
                fly.title = "Fly Me to the Moon";
                fly.artist = "Frank Sinatra";
                fly.album = "It Might as Well Be Swing";
                fly.year = 1964;
            }


.. tabbed:: mucp_8_4_ac

    .. tab:: Question

        .. activecode:: mucp_8_4_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the code for the struct definition of ``Unicorn``.
            The Unicorn structure will have the instance variables name,
            age, hornLength, hairColor, and isSparkly in that order. A Unicorn's
            horn length is measured to the nearest tenth of a unit.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_8_4_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to define the struct ``Unicorn``.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Unicorn {
                string name;
                int age;
                double hornLength;
                string hairColor;
                bool isSparkly;
            };


.. tabbed:: mucp_8_5_ac

    .. tab:: Question

        .. activecode:: mucp_8_5_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the code for the ``convertToHumanAge`` function. convertToHumanAge
            takes a Unicorn as a parameter and returns the equivalent human age.
            If a unicorn is sparkly, then its equivalent human age is three times its age in unicorn years
            plus the length of its horn. If a unicorn is not sparkly, then its equivalent human age is
            four times its age in unicorn years plus twice the length of its horn.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_8_5_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the convertToHumanAge function.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Unicorn {
                string name;
                int age;
                double hornLength;
                string hairColor;
                bool isSparkly;
            };

            int convertToHumanAge (Unicorn u) {
                if (u.isSparkly) {
                    return 3 * u.age + u.hornLength;
                }
                else {
                    return 4 * u.age + 2 * u.hornLength;
                }
            }


.. tabbed:: mucp_8_6_ac

    .. tab:: Question

        .. activecode:: mucp_8_6_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the code for the ``unicornPower`` function. unicornPower
            takes a Unicorn as a parameter and
            sets isSparkly to true and changes the color to rainbow.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_8_6_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the unicornPower function.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Unicorn {
                string name;
                int age;
                double hornLength;
                string hairColor;
                bool isSparkly;
            };

            void unicornPower (Unicorn& u) {
                u.isSparkly = true;
                u.color = "rainbow";
            }


.. tabbed:: mucp_8_7_ac

    .. tab:: Question

        .. activecode:: mucp_8_7_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the code for the struct definitions of ``Address`` and ``Employee``.
            The Address structure will have the instance variables houseNumber,
            state (abbreviation), and postalAddress in that order. The Employee
            structure will be a nested structure with the instance variables name
            and Address address in that order.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_8_7_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to define the ``Address`` and ``Employee`` structs.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Address {
                int houseNumber;
                string state;
                int postalAddress;
            };

            struct Employee {
                string name;
                Address address;
            };


.. tabbed:: mucp_8_8_ac

    .. tab:: Question

        .. activecode:: mucp_8_8_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the code for the ``printAddress`` function. printAddress takes
            an Employee as a parameter and should print out the information of the employee in the
            following format: name (id) lives at houseNumber in state, postalAddress.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_8_8_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the printAddress function
            ~~~~
            #include <iostream>
            using namespace std;

            struct Address {
                int houseNumber;
                string state;
                int postalAddress;
            };

            struct Employee {
                string name;
                Address address;
                int id;
            };

            void printAddress (Employee e) {
                cout << e.name << " (" << e.id << ") lives at ";
                cout << e.address.houseNumber << " in" << e.address.state << " ," << e.address.postalAddress << endl;
            }


.. tabbed:: mucp_8_9_ac

    .. tab:: Question

        .. activecode:: mucp_8_9_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Sometimes employees will move around and thus we'll need to update their addresses.
            Let's write the code for the ``updateAddress`` function. updateAddress takes an
            Employee and a new Address as parameters and sets the employee's address to the new address.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_8_9_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the ``updateAddress`` function.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Address {
                int houseNumber;
                string state;
                int postalAddress;
            };

            struct Employee {
                string name;
                Address address;
            };

            void updateAdress (Employee& e, Address a) {
                e.address = a;
            }


.. tabbed:: mucp_8_10_ac

    .. tab:: Question

        .. activecode:: mucp_8_10_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the code for the ``storeEmployeeData`` function. storeEmployeeData doesn't
            take any parameters and prompts the user for information regarding their
            name, house number, state, and postal code. It then returns an Employee object with
            the stored data. Declare all variables before prompting the user.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_8_10_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the ``storeEmployeeData`` function.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Address {
                int houseNumber;
                string state;
                int postalCode;
            };

            struct Employee {
                string name;
                Address address;
            };

            void storeEmployeeData() {
                Employee e;
                cout << "What is your full name?";
                getline(cin, e.name);
                cout << "What is your house number?";
                cin >> e.address.houseNumber;
                cout << "What state do you live in?";
                cin >> e.address.state;
                cout << "What is your postal code?";
                cin >> e.address.postalCode;
                return e;
            }
