Coding Practice
---------------

.. tabbed:: cp_8_1

    .. tab:: Question

        Write the function ``rectangleInfo`` which prompts the user for the width
        and height of a rectangle. Then ``rectangleInfo`` prints out the area and 
        perimeter of the rectangle.

        .. activecode:: cp_8_AC_1q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :practice: T
           :stdin: 4, 6

           #include <iostream>
           using namespace std;

           void rectangleInfo () {
               // Write your implementation here.
           }

           int main() {
               rectangleInfo ();
           }


    .. tab:: Answer

        Below is one way to implement the program. We prompt the user for input
        using ``cin`` before printing the area and perimeter.

        .. activecode:: cp_8_AC_1a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:

           #include <iostream>
           using namespace std;

           void rectangleInfo () {
               int height, width;
               cout << "Please enter the height and width of a rectangle separated by spaces: ";
               cin >> height >> width;
               cout << "The area of the rectangle is " << height * width << endl;
               cout << "The perimeter of the rectangle is " << 2 * (height + width) << endl;
           }

           int main() {
               rectangleInfo ();
           }

.. selectquestion:: cp_8_AC_2q_sq
    :fromid: cp_8_AC_2q, cp_8_AC_2q_pp
    :toggle: lock

.. tabbed:: cp_8_3

    .. tab:: Question

        In the not so distant future, robots have replaced humans to do any kind of imaginable
        work or chore. Define the ``Robot`` structure, which has instance variables ``string name``,
        ``string model``, ``int serialNumber``, ``int batteryLevelPercentage``,
        and ``string task`` in that order. Then write the ``printRobotData`` function, which
        takes a ``Robot`` as a parameter and prints out the robot's data in the following format: 
        ``name`` (``model`` ``serialNumber``) has ``batteryLevelPercentage`` 
        percent battery and is currently executing the task "``task``".

        .. activecode:: cp_8_AC_3q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :practice: T

           #include <iostream>
           using namespace std;

           // Write your code for the struct Robot here.

           // Write your code for the function printRobotData here.

           int main() {
               Robot rob = { "Rob", "XLV", 9800, 45, "washing dishes" };
               cout << "Your output:" << endl;
               printRobotData (rob); 
               cout << "Correct output:" << endl;
               cout << "Rob (XLV 9800) has 45 percent battery and is currently executing the task \"washing dishes\"";
           }


    .. tab:: Answer

        Below is one way to implement the program. First we declare the instance variables
        in the ``struct`` definition. Next, we use dot notation to access
        the instance variables and output them using ``cout``.

        .. activecode:: cp_8_AC_3a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:

           #include <iostream>
           using namespace std;

           struct Robot {
               string name;
               string model;
               int serialNumber;
               int batteryLevelPercentage;
               string task;
           };

           void printRobotData (Robot r) {
                cout << r.name << " (" << r.model << " " << r.serialNumber 
                     << ") has " << r.batteryLevelPercentage 
                     << " percent battery and is currently executing the task \"" 
                     << r.task << "\"" << endl;
           }

           int main() {
               Robot rob = { "Rob", "XLV", 9800, 45, "washing dishes" };
               cout << "Your output:" << endl;
               printRobotData (rob); 
               cout << "Correct output:" << endl;
               cout << "Rob (XLV 9800) has 45 percent battery and is currently executing the task \"washing dishes\"";
           }

.. selectquestion:: cp_8_AC_4q_sq
    :fromid: cp_8_AC_4q, cp_8_AC_4q_pp
    :toggle: lock

.. tabbed:: cp_8_5

    .. tab:: Question

        In case a robot malfunctions, let's write the function ``resetRobot``. ``resetRobot`` 
        takes a ``Robot`` as a parameter and resets its name to "EnterAName",
        recharges the battery to 100 percent, and resets the task to "Idle".

        .. activecode:: cp_8_AC_5q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

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

           // Write your code for the function resetRobot here.

           int main() {
               Robot a = { "Bot", "RSO", 1985, 32, "gardening" };
               resetRobot (a);
               cout << "Your output:" << endl;
               printRobotData (a); 
               cout << "Correct output:" << endl;
               cout << "EnterAName (RSO 1985) has 100 percent battery and is currently executing the task \"Idle\"";
           }
           ====
           void printRobotData (Robot r) {
                cout << r.name << " (" << r.model << " " << r.serialNumber 
                     << ") has " << r.batteryLevelPercentage 
                     << " percent battery and is currently executing the task \"" 
                     << r.task << "\"" << endl;
           }


    .. tab:: Answer

        Below is one way to implement the program. We can create another ``Robot`` 
        with the settings after being reset. Then we set ``r`` equal to the new
        ``Robot`` we created. Notice we use dot notation to ensure that the 
        ``model`` and ``serialNumber`` are the same.

        .. activecode:: cp_8_AC_5a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:

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

           void resetRobot(Robot& r) {
               Robot reset = { "EnterAName", r.model, r.serialNumber, 100, "Idle" };
               r = reset;
           }

           int main() {
               Robot a = { "Bot", "RSO", 1985, 32, "gardening" };
               resetRobot (a);
               cout << "Your output:" << endl;
               printRobotData (a); 
               cout << "Correct output:" << endl;
               cout << "EnterAName (RSO 1985) has 100 percent battery and is currently executing the task \"Idle\"";
           }
           ====
           void printRobotData (Robot r) {
                cout << r.name << " (" << r.model << " " << r.serialNumber 
                     << ") has " << r.batteryLevelPercentage 
                     << " percent battery and is currently executing the task \"" 
                     << r.task << "\"" << endl;
           }    

.. selectquestion:: cp_8_AC_6q_sq
    :fromid: cp_8_AC_6q, cp_8_AC_6q_pp
    :toggle: lock

.. tabbed:: cp_8_7

    .. tab:: Question

        Now write the ``Trainer`` structure, which has instance variables 
        ``string trainerName``, ``char gender``, ``int numBadges``, and six ``Pokemon`` objects 
        named ``first``, ``second``, etc., in that order. Then, write the function 
        ``printTrainerInfo``, which takes a ``Trainer`` as a parameter and outputs the
        trainer's info. For example, the code below should print:

        :: 

           Trainer Red has 8 badges and Red's team consists of 
           Pikachu (Lv. 81, 100% HP)
           Espeon (Lv. 72, 100% HP)
           Snorlax (Lv. 75, 100% HP)
           Venusaur (Lv. 77, 100% HP)
           Charizard (Lv. 77, 100% HP)
           Blastoise (Lv. 77, 100% HP)

        .. activecode:: cp_8_AC_7q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

           #include <iostream>
           using namespace std;

           struct Pokemon {
               string pokeName;
               string type;
               int level;
               int healthPercentage;
           };

           // Write your code for the struct Trainer here.

           void printPokeInfo(Pokemon p);

           // Write your code for the function printTrainerInfo here.

           int main() {
               Pokemon pikachu = { "Pikachu", "Electric", 81, 100 };
               Pokemon espeon = { "Espeon", "Psychic", 72, 100 };
               Pokemon snorlax = { "Snorlax", "Normal", 75, 100 };
               Pokemon venusaur = { "Venusaur", "Grass & Poison", 77, 100 };
               Pokemon charizard = { "Charizard", "Fire & Flying", 77, 100 };
               Pokemon blastoise = { "Blastoise", "Water", 77, 100 };
               Trainer red = { "Red", 'M', 8, pikachu, espeon, snorlax, venusaur, charizard, blastoise };
               printTrainerInfo (red);
           }  
           ====
           void printPokeInfo(Pokemon p) {
               cout << p.pokeName << " (Lv. " << p.level << ", " << p.healthPercentage << "% HP)" << endl;
           }


    .. tab:: Answer

        Below is one way to implement the program. First we declare the instance variables
        in the ``struct`` definition. Next, we call ``printPokeInfo`` on each ``Pokemon``
        in ``Trainer`` and output the trainer's info in the correct format.

        .. activecode:: cp_8_AC_7a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:

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

           int main() {
               Pokemon pikachu = { "Pikachu", "Electric", 81, 100 };
               Pokemon espeon = { "Espeon", "Psychic", 72, 100 };
               Pokemon snorlax = { "Snorlax", "Normal", 75, 100 };
               Pokemon venusaur = { "Venusaur", "Grass & Poison", 77, 100 };
               Pokemon charizard = { "Charizard", "Fire & Flying", 77, 100 };
               Pokemon blastoise = { "Blastoise", "Water", 77, 100 };
               Trainer red = { "Red", 'M', 8, pikachu, espeon, snorlax, venusaur, charizard, blastoise };
               printTrainerInfo (red);
           }  
           ====
           void printPokeInfo(Pokemon p) {
               cout << p.pokeName << " (Lv. " << p.level << ", " << p.healthPercentage << "% HP)" << endl;
           }

.. selectquestion:: cp_8_AC_8q_sq
    :fromid: cp_8_AC_8q, cp_8_AC_8q_pp
    :toggle: lock

.. tabbed:: cp_8_9

    .. tab:: Question

        Now write the function ``pokeCenter`` which takes a ``Trainer`` as a parameter and 
        prompts the user if they'd like to heal their Pokemon. Below are the 
        possible outputs (y, n, or an invalid input). If user inputs 'y', call ``healPokemon``
        and output the correct dialogue. If user inputs 'n', don't call ``healPokemon``
        and output the correct dialogue. If user inputs an invalid character, output the error message.

        :: 

           Welcome to the Pokémon Center. Would you like me to take your Pokémon? (y/n) y
           Okay, I'll take your Pokémon for a few seconds.
           Your Pokémon are now healed. We hope to see you again. 

           or

           Welcome to the Pokémon Center. Would you like me to take your Pokémon? (y/n) n
           We hope to see you again.

           or

           Welcome to the Pokémon Center. Would you like me to take your Pokémon? (y/n) h
           Sorry, not a valid input.

        .. activecode:: cp_8_AC_9q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :stdin: y

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
           void healPokemon(Trainer& t);

           // Write your code for the function pokeCenter here.

           int main() {
               Pokemon exeggutor = {"Exeggutor", "Grass & Psychic", 58, 78};
               Pokemon alakazam = {"Alakazam", "Psychic", 54, 0};
               Pokemon arcanine = {"Arcanine", "Fire", 58, 24};
               Pokemon rhydon = {"Rhydon", "Ground & Rock", 56, 55};
               Pokemon gyarados = {"Gyarados", "Water & Flying", 58, 100};
               Pokemon pidgeot = {"Pidgeot", "Normal & Flying", 56, 35};
               Trainer blue = {"Blue", 'M', 8, exeggutor, alakazam, arcanine, rhydon, gyarados, pidgeot};
               printTrainerInfo(blue);
               pokeCenter(blue);
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

           void healPokemon(Trainer& t) { 
               t.first.healthPercentage = 100;
               t.second.healthPercentage = 100;
               t.third.healthPercentage = 100;
               t.fourth.healthPercentage = 100;
               t.fifth.healthPercentage = 100;
               t.sixth.healthPercentage = 100;
           }

    .. tab:: Answer

        Below is one way to implement the program. We use conditionals to perform 
        the correct output and operation depending on the user's input.

        .. activecode:: cp_8_AC_9a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :stdin: y
           :optional:

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
           void healPokemon(Trainer& t);

           void pokeCenter(Trainer& t) {
               char response;
               cout << "Welcome to the Pokémon Center. Would you like me to take your Pokémon? (y/n) ";
               cin >> response;
               if (response == 'y') {
                   cout << "Okay, I'll take your Pokémon for a few seconds." << endl;
                   healPokemon(t);
                   cout << "Your Pokémon are now healed. We hope to see you again." << endl;
               }
               else if (response == 'n') {
                   cout << "We hope to see you again." << endl;
               }
               else {
                   cout << "Sorry, not a valid input." << endl;
               }
           }

           int main() {
               Pokemon exeggutor = {"Exeggutor", "Grass & Psychic", 58, 78};
               Pokemon alakazam = {"Alakazam", "Psychic", 54, 0};
               Pokemon arcanine = {"Arcanine", "Fire", 58, 24};
               Pokemon rhydon = {"Rhydon", "Ground & Rock", 56, 55};
               Pokemon gyarados = {"Gyarados", "Water & Flying", 58, 100};
               Pokemon pidgeot = {"Pidgeot", "Normal & Flying", 56, 35};
               Trainer blue = {"Blue", 'M', 8, exeggutor, alakazam, arcanine, rhydon, gyarados, pidgeot};
               printTrainerInfo(blue);
               pokeCenter(blue);
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

           void healPokemon(Trainer& t) { 
               t.first.healthPercentage = 100;
               t.second.healthPercentage = 100;
               t.third.healthPercentage = 100;
               t.fourth.healthPercentage = 100;
               t.fifth.healthPercentage = 100;
               t.sixth.healthPercentage = 100;
           }

.. selectquestion:: cp_8_AC_10q_sq
    :fromid: cp_8_AC_10q, cp_8_AC_10q_pp
    :toggle: lock