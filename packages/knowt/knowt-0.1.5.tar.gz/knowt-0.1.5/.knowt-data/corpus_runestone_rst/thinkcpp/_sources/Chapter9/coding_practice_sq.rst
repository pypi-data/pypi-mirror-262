Coding Practice
---------------

.. tabbed:: cp_9_AC_2q_q

    .. tab:: Activecode

        .. activecode:: cp_9_AC_2q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write the function ``printCakeInfo``, which prints the cake's information in the format
            "This is a ``color``, ``diameter`` inch diameter cake with/without icing." If ``name`` does not
            have the value "n/a", ``printCakeInfo`` prints out "Happy birthday ``name``! Your cake is ``color``,
            has a ``diameter`` inch diameter, and comes with/without icing." Select the Parsonsprob tab for hints
            for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Cake {
                string name;
                string color;
                double diameter;
                bool has_icing;
            };

            // Write your code for the printCakeInfo function here.

            int main() {
                Cake c1 = { "n/a", "red", 12.5, true };
                printCakeInfo (c1);
                Cake c2 = { "Tom", "white", 10, false };
                printCakeInfo (c2);
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_9_AC_2q_pp
            :numbered: left
            :adaptive:

            Write the function ``printCakeInfo``, which prints the cake's information in the format
            "This is a ``color``, ``diameter`` inch diameter cake with/without icing." If ``name`` does not
            have the value "n/a", ``printCakeInfo`` prints out "Happy birthday ``name``! Your cake is ``color``,
            has a ``diameter`` inch diameter, and comes with/without icing." Use the lines to construct the code,
            then go back to complete the Activecode tab.

            -----
            void printCakeInfo (Cake c) {
            =====
            string printCakeInfo (Cake c) { #paired
            =====
                if (c.name == "n/a") {
            =====
                    if (c.has_icing) {
                        cout << "This is a " << c.color << "," << c.diameter << " inch diameter cake with icing." << endl;
                    }
            =====
                    else {
                        cout << "This is a " << c.color << "," << c.diameter << " inch diameter cake without icing." << endl;
                    }
            =====
                }
            =====
                else {
            =====
                    if (c.has_icing) {
                        cout << "Happy birthday " << c.name << "! Your cake is " << c.color << ", has a " << c.diameter << " inch diameter, and comes with icing." << endl;
                    }
            =====
                    else {
                        cout << "Happy birthday " << c.name << "! Your cake is " << c.color << ", has a " << c.diameter << " inch diameter, and comes without icing." << endl;
                    }
            =====
                }
            }

.. tabbed:: cp_9_AC_4q_q

    .. tab:: Activecode

        .. activecode:: cp_9_AC_4q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write the function ``changeCakeDiameter``, which takes a ``Cake`` and a ``double`` as a parameter.
            ``changeCakeDiameter`` then multiplies the original diameter by the double and modifies the cake
            to have this new diameter. Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Cake {
                string name;
                string color;
                double diameter;
                bool has_icing;
            };

            void printCakeInfo (Cake c);
            Cake makeCake ();

            // Write your code for the changeCakeDiameter function here.

            int main() {
                Cake original = { "John", "green", 8.5, true };
                changeCakeDiameter (original, 2);
                printCakeInfo (original);
            }
            ====
            void printCakeInfo (Cake c) {
                if (c.name == "n/a") {
                    if (c.has_icing) {
                        cout << "This is a " << c.color << "," << c.diameter << " inch diameter cake with icing." << endl;
                    }
                    else {
                        cout << "This is a " << c.color << "," << c.diameter << " inch diameter cake without icing." << endl;
                    }
                }
                else {
                    if (c.has_icing) {
                        cout << "Happy birthday " << c.name << "! Your cake is " << c.color << ", has a " << c.diameter << " inch diameter, and comes with icing." << endl;
                    }
                    else {
                        cout << "Happy birthday " << c.name << "! Your cake is " << c.color << ", has a " << c.diameter << " inch diameter, and comes without icing." << endl;
                    }
                }
            }

            Cake makeCake () {
                Cake input;
                string name, color;
                double diameter;
                char icing;
                cout << "Name: ";
                cin >> name;
                input.name = name;
                cout << "Color: ";
                cin >> color;
                input.color = color;
                cout << "Diameter: ";
                cin >> diameter;
                input.diameter = diameter;
                cout << "Icing? (y/n) ";
                cin >> icing;
                if (icing == 'y') {
                    input.has_icing = true;
                }
                else {
                    input.has_icing = false;
                }
                return input;
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_9_AC_4q_pp
            :numbered: left
            :adaptive:

            Write the function ``changeCakeDiameter``, which takes a ``Cake`` and a ``double`` as a parameter.
            ``changeCakeDiameter`` then multiplies the original diameter by the double and modifies the cake
            to have this new diameter. Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            void changeCakeDiameter (Cake &c, double scale) {
            =====
            void changeCakeDiameter (Cake c, double scale) { #paired
            =====
            string changeCakeDiameter (Cake c, double scale) { #paired
            =====
                c.diameter *= scale;
            =====
                c.diameter; #distractor
            =====
                c.diameter = c.diameter * 2; #distractor
            =====
            }

.. tabbed:: cp_9_AC_6q_q

    .. tab:: Activecode

        .. activecode:: cp_9_AC_6q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write the struct ``Shirt``, which has the instance variables color and size.
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            // Write your code for the struct Shirt here.

            int main () {
                Shirt t = { "blue", 'L' };
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_9_AC_6q_pp
            :numbered: left
            :adaptive:

            Write the struct ``Shirt``, which has the instance variables color and size.
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            struct Shirt {
            =====
                string color;
            =====
                char size;
            =====
                string size; #distractor
            =====
            };
            =====
            } #distractor

.. tabbed:: cp_9_AC_8q_q

    .. tab:: Activecode

        .. activecode:: cp_9_AC_8q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write the struct ``Outfit``, which is a nested structure that has a ``Shirt``, ``Pants``, and has_hat.
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Pants {
                char size;
                string material;
            };

            struct Shirt {
                string color;
                char size;
            };
            // Write your code for the struct Outfit here.

            int main () {
                Shirt t = { "blue", 'L' };
                Pants p = { 'S', "denim" };
                Outfit o = { t, p, true };
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_9_AC_8q_pp
            :numbered: left
            :adaptive:

            Write the struct ``Outfit``, which is a nested structure that has a ``Shirt``, ``Pants``, and has_hat.
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            struct Outfit {
            =====
                Shirt s;
            =====
                Pants p;
            =====
                bool has_hat;
            =====
                int has_hat; #distractor
            =====
            };

.. tabbed:: cp_9_AC_10q_q

    .. tab:: Activecode

        .. activecode:: cp_9_AC_10q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write the ``changeShirts`` and ``changePants`` functions, which both take an ``Outfit`` as a parameter. ``changeShirts`` also
            takes a ``Shirt`` as a parameter and ``changePants`` also takes a ``Pants`` as a parameter. Each function modifies the ``Outfit``
            and changes the shirt or pants to the new input. Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            void printOutfit(Outfit o);

            struct Shirt {
                string color;
                char size;
            };

            struct Pants {
                char size;
                string material;
            };

            struct Outfit {
                Shirt s;
                Pants p;
                bool has_hat;
            };

            // Write your code for the changeShirts function here.

            // Write your code for the changePants function here.

            int main() {
                Shirt t = { "blue", 'L' };
                Pants p = { 'S', "denim" };
                Outfit o = { t, p, true };
                printOutfit (o);
                Shirt newShirt = { "red", 'M' };
                Pants newPants = { 'M', "khakis" };
                changeShirts (o, newShirt);
                changePants (o, newPants);
                printOutfit (o);
            }
            ====
            void printOutfit (Outfit o) {
                cout << "Shirt: " << o.s.color << " and " << o.s.size << "; Pants: " << o.p.size << " and " << o.p.material << "; ";
                if (o.has_hat) {
                    cout << "has hat" << endl;
                }
                else {
                    cout << "does not have hat" << endl;
                }
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_9_AC_10q_pp
            :numbered: left
            :adaptive:

            Write the ``changeShirts`` and ``changePants`` functions, which both take an ``Outfit`` as a parameter. ``changeShirts`` also
            takes a ``Shirt`` as a parameter and ``changePants`` also takes a ``Pants`` as a parameter. Each function modifies the ``Outfit``
            and changes the shirt or pants to the new input. Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            // changeShirts function
            void changeShirts (Outfit &outfit, Shirt shirt) {
            =====
                outfit.s = shirt;
            =====
            }
            =====
            // changePants function
            void changePants (Outfit &outfit, Pants p) {
            =====
                outfit.p = pants;
            =====
            }
