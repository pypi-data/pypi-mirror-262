Coding Practice
---------------

.. tabbed:: cp_8_AC_2q_q

    .. tab:: Activecode

        .. activecode:: cp_8_AC_2q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
            :stdin: Captain America

            Write a simple function called ``greetUser`` which prompts the user 
            for their full name. Then the function outputs "Hello ``fullName``!".
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            void greetUser () {
                // Write your implementation here.
            }

            int main() {
                greetUser ();
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_8_AC_2q_pp
            :numbered: left
            :adaptive:

            Write a simple function called ``greetUser`` which prompts the user 
            for their full name. Then the function outputs "Hello ``fullName``!".
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            void greetUser () {
            =====
                string fullName;
            ===== 
                string fullName = "Captain America"; #distractor
            =====
                cout << "Please enter your full name!" << endl;
            =====
                getline(cin, fullName);
            =====
                cin << fullName; #paired
            =====
                cout << "Hello " << fullName << "!" << endl;
            =====
            }

.. tabbed:: cp_8_AC_4q_q

    .. tab:: Activecode

        .. activecode:: cp_8_AC_4q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Robots will naturally deplete their charge as they carry out tasks.
            Write a function called ``chargeRobot`` which takes a ``Robot`` as 
            a parameter and charges the robot to 100 percent. Then output the statement
            "Robot ``name`` is fully charged!". Select the Parsonsprob tab for hints for 
            the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Robot {
                string name;
                string model;
                int serialNumber;
                int batteryLevelPercentage;
                string task;
            };

            void printRobotData (Robot r);

            // Write your code for the function chargeRobot here.

            int main() {
                Robot bob = { "Bob", "MKZ", 143, 65, "sweeping floors" };
                chargeRobot (bob);
                cout << "Your output:" << endl;
                printRobotData (bob); 
                cout << "Correct output:" << endl;
                cout << "Bob (MKZ 143) has 100 percent battery and is currently executing the task \"sweeping floors\"";
            }
            ====
            void printRobotData (Robot r) {
                cout << r.name << " (" << r.model << " " << r.serialNumber 
                        << ") has " << r.batteryLevelPercentage 
                        << " percent battery and is currently executing the task \"" 
                        << r.task << "\"" << endl;
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_8_AC_4q_pp
            :numbered: left
            :adaptive:

            Robots will naturally deplete their charge as they carry out tasks.
            Write a function called ``chargeRobot`` which takes a ``Robot`` as 
            a parameter and charges the robot to 100 percent. Then output the statement
            "Robot ``name`` is fully charged!". Use the lines to construct the code, then
            go back to complete the Activecode tab.

            -----
            void chargeRobot (Robot &r) {
            =====
            void chargeRobot (Robot r) { #paired
            =====
                r.batteryLevelPercentage = 100;
            =====
                r.batteryLevelPercentage = 100%; #distractor
            =====
                cout << "Robot " << r.name << " is fully charged!" << endl;
            =====
            }

.. tabbed:: cp_8_AC_6q_q

    .. tab:: Activecode

        .. activecode:: cp_8_AC_6q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
            :practice: T

            Write the ``Pokemon`` structure, which has instance variables ``string pokeName``,
            ``string type``, ``int level``, and ``int healthPercentage`` in that order. 
            Next, write the function ``printPokeInfo``, which takes a ``Pokemon`` as a parameter and outputs the
            Pokemon's info in the following format: ``pokeName`` (Lv. ``level``, ``healthPercentage``\% HP). 
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            // Write your code for the struct Pokemon here.

            // Write your code for the function printPokeInfo here.

            int main() {
                Pokemon magikarp = { "Magikarp", "Water", 12, 100 };
                cout << "Your output:" << endl;
                printPokeInfo (magikarp); 
                cout << "Correct output:" << endl;
                cout << "Magikarp (Lv. 12, 100% HP)";
            }  

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_8_AC_6q_pp
            :numbered: left
            :adaptive:

            Write the ``Pokemon`` structure, which has instance variables ``string pokeName``,
            ``string type``, ``int level``, and ``int healthPercentage`` in that order. 
            Next, write the function ``printPokeInfo``, which takes a ``Pokemon`` as a parameter and outputs the
            Pokemon's info in the following format: ``pokeName`` (Lv. ``level``, ``healthPercentage``\% HP).
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            // Pokemon struct creation
            struct Pokemon {
            =====
                string pokeName;
            =====
                string type;
            =====
                int level;
            =====
                int healthPercentage;
            =====
            };
            =====
            // printPokeInfo function creation
            void printPokeInfo (Pokemon p) {
            =====
            string printPokeInfo (Pokemon p) { #paired
            =====
                cout << p.pokeName << " (Lv. " << p.level << ", " << p.healthPercentage << "% HP)" << endl;
            =====
            }

.. tabbed:: cp_8_AC_8q_q

    .. tab:: Activecode

        .. activecode:: cp_8_AC_8q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            When Pokemon are injured, they can be healed up at the Pokemon Center.
            Write the function ``healPokemon``, which takes a ``Trainer`` as a parameter
            and heals the Trainer's Pokemon to 100 percent health. Select the Parsonsprob 
            tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Pokemon {
                string pokeName;
                string type;
                int level;
                int healthPercentage;
            };

            struct Trainer {
                string trainerName;
                char gender;
                int numBadges;
                Pokemon first, second, third, fourth, fifth, sixth;
            };

            void printPokeInfo(Pokemon p);
            void printTrainerInfo(Trainer t);

            // Write your code for the function healPokemon here.

            int main() {
                Pokemon exeggutor = {"Exeggutor", "Grass & Psychic", 58, 78};
                Pokemon alakazam = {"Alakazam", "Psychic", 54, 0};
                Pokemon arcanine = {"Arcanine", "Fire", 58, 24};
                Pokemon rhydon = {"Rhydon", "Ground & Rock", 56, 55};
                Pokemon gyarados = {"Gyarados", "Water & Flying", 58, 100};
                Pokemon pidgeot = {"Pidgeot", "Normal & Flying", 56, 35};
                Trainer blue = {"Blue", 'M', 8, exeggutor, alakazam, arcanine, rhydon, gyarados, pidgeot};
                printTrainerInfo(blue);
                healPokemon(blue);
                printTrainerInfo(blue);  // Pokemon should now all be healed to 100% health
            }  
            ====
            void printPokeInfo(Pokemon p) {
                cout << p.pokeName << " (Lv. " << p.level << ", " << p.healthPercentage << "% HP)" << endl;
            }

            void printTrainerInfo(Trainer t) {
                cout << "Trainer " << t.trainerName << " has " << t.numBadges
                    << " badges and " << t.trainerName << "'s team consists of " << endl;
                printPokeInfo(t.first);
                printPokeInfo(t.second);
                printPokeInfo(t.third);
                printPokeInfo(t.fourth);
                printPokeInfo(t.fifth);
                printPokeInfo(t.sixth);
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_8_AC_8q_pp
            :numbered: left
            :adaptive:

            When Pokemon are injured, they can be healed up at the Pokemon Center.
            Write the function ``healPokemon``, which takes a ``Trainer`` as a parameter
            and heals the Trainer's Pokemon to 100 percent health. Use the lines to construct 
            the code, then go back to complete the Activecode tab.

            -----
            void healPokemon (Trainer &t) {
            =====
            void healPokemon (Trainer t) { #paired
            =====
                t.first.healthPercentage = 100;
            =====
                t.second.healthPercentage = 100;
            =====
                t.third.healthPercentage = 100;
            =====
                t.fourth.healthPercentage = 100;
            =====
                t.fifth.healthPercentage = 100;
            =====
                t.sixth.healthPercentage = 100;
            =====
            }
        
.. tabbed:: cp_8_AC_10q_q

    .. tab:: Activecode

        .. activecode:: cp_8_AC_10q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
            :stdin: 145 2
            :practice: T

            Ever wanted to know how much you'd weigh on each planet? Write the ``convertWeight``
            function, which takes a ``double earthWeight`` and ``int planet`` as parameters. First, 
            in ``main``, prompt the user to enter their weight in pounds and a number corresponding to
            a planet (Mercury is 1, Venus is 2, etc.). Next, call the ``convertWeight`` function using
            the user's input. Finally, print out their weight on that planet.
            If the user inputs an invalid planet, print out an error message. 
            The weight conversion are as follows (multiply the number by ``earthWeight`` to get the weight on that planet):
            Mercury - 0.38, Venus - 0.91, Earth - 1.00, Mars - 0.38, Jupiter - 2.34, Saturn - 1.06, Uranus - 0.92, and Neptune - 1.19.
            Select the Parsonsprob tab for hints for the construction of the code.
            Below are some examples.

            :: 

                Please enter your weight in pounds: 145.6
                Please select a planet: 3
                Your weight on Earth is 145.6 pounds.

                or

                Please enter your weight in pounds: 170
                Please select a planet: 1
                Your weight on Mercury is 64.6 pounds.

                or

                Please enter your weight in pounds: 170
                Please select a planet: 23
                Error, not a valid planet.
            ~~~~
            #include <iostream>
            using namespace std;

            // Write your code for the function convertWeight here.

            int main() {
                // Write your implementation here.
            }  

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_8_AC_10q_pp
            :numbered: left
            :adaptive:

            Ever wanted to know how much you'd weigh on each planet? Write the ``convertWeight``
            function, which takes a ``double earthWeight`` and ``int planet`` as parameters. First, 
            in ``main``, prompt the user to enter their weight in pounds and a number corresponding to
            a planet (Mercury is 1, Venus is 2, etc.). Next, call the ``convertWeight`` function using
            the user's input. Finally, print out their weight on that planet.
            If the user inputs an invalid planet, print out an error message. 
            The weight conversion are as follows (multiply the number by ``earthWeight`` to get the weight on that planet):
            Mercury - 0.38, Venus - 0.91, Earth - 1.00, Mars - 0.38, Jupiter - 2.34, Saturn - 1.06, Uranus - 0.92, and Neptune - 1.19.
            Use the lines to construct the code, then go back to complete the Activecode tab.
            Below are some examples.

            :: 

                Please enter your weight in pounds: 145.6
                Please select a planet: 3
                Your weight on Earth is 145.6 pounds.

                or

                Please enter your weight in pounds: 170
                Please select a planet: 1
                Your weight on Mercury is 64.6 pounds.

                or

                Please enter your weight in pounds: 170
                Please select a planet: 23
                Error, not a valid planet.

            -----
            // convertWeight function creation
            void convertWeight (double earthWeight, int planet) {
            =====
                if (planet== 1) {
                    cout << "Your weight on Mercury is " << earthWeight * .38 << " pounds." << endl;
                }
            =====
                else if(planet == 2) {
                    cout << "Your weight on Venus is " << earthWeight * .91 << " pounds." << endl;
                }
            =====
                else if (planet == 3) {
                    cout << "Your weight on Earth is " << earthWeight * 1 << " pounds." << endl;
                }
            =====
                else if(planet == 4) {
                    cout << "Your weight on Mars is " << earthWeight * .38 << " pounds." << endl;
                }
            =====
                else if(planet == 5) {
                    cout << "Your weight on Jupiter is " << earthWeight * 2.34 << " pounds." << endl;
                }
            =====
                else if(planet == 6) {
                    cout << "Your weight on Saturn is " << earthWeight * 1.06 << " pounds." << endl;
                }
            =====
                else if(planet == 7) {
                    cout << "Your weight on Uranus is " << earthWeight * .92 << " pounds." << endl;
                }
            =====
                else if(planet == 8) {
                    cout << "Your weight on Neptune is " << earthWeight * 1.19 << " pounds." << endl;
                }
            =====
                else {
                    cout << "Error, not a valid planet." << endl;
                }
            =====
            }
            =====
            // main implementation
            int main() {
            =====
                double earthWeight;
            =====
                int planet;
            =====
                cout << "Please enter your weight in pounds: ";
                cin >> earthWeight;
                cout << earthWeight << endl;
            =====
                cout << "Please select a planet: ";
                cin >> planet;
                cout << planet << endl;
            =====
                convertWeight(earthWeight, planet);
            =====
            }