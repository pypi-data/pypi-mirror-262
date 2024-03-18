Activecode Exercises
--------------------

Answer the following **Activecode** questions to
assess what you have learned in this chapter.


.. tabbed:: cond_rec_a2_q

    .. tab:: Activecode

        .. activecode:: cond_rec_a2
            :language: cpp

            You are part of a class where everyone passes, but it's very hard
            to pass with an A.  Fix the function so it prints your letter grade
            according to this scheme.  [0, 50) = C, [50, 85) = B, and [85, 100] = A.
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            string whichDoor (double grade) {
                s = "";
                if (grade < 50) {
                    s = "C";
                }
                if (grade < 85) {
                    s = "B";
                }
                if (grade >= 85) {
                    s = "A";
                }
                cout << s;
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cond_rec_a2_pp
            :numbered: left
            :adaptive:

            You are part of a class where everyone passes, but it's very hard
            to pass with an A.  Fix the function so it prints your letter grade
            according to this scheme.  [0, 50) = C, [50, 85) = B, and [85, 100] = A.
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            string whichDoor (double grade) {
            =====
            void whichDoor (double grade) { #paired
            =====
                string s = "";
            =====
                s = ""; #paired
            =====
                if (grade < 50) {
                    s = "C";
                }
            =====
                if (grade < 85 && grade >= 50) {
                    s = "B";
                }
            =====
                if (grade < 85 || grade >= 50) { #paired
                    s = "B";
                }
            =====
                if (grade >= 85) {
                    s = "A";
                }
            =====
                cout << s;
            }


.. tabbed:: cond_rec_a4_q

    .. tab:: Activecode

        .. activecode:: cond_rec_a4
            :language: cpp

            Finish the code below so that it prints true if ``x`` is even
            and false if ``x`` is odd. Select the Parsonsprob tab for hints
            for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            void is_even (int num) {
                if (num % 2 == 0) {
                    cout << true;
                }
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cond_rec_a4_pp
            :numbered: left
            :adaptive:

            Finish the code below so that it prints true if ``x`` is even
            and false if ``x`` is odd. Use the lines to construct the code,
            then go back to complete the Activecode tab.

            -----
            void is_even (int num) {
            =====
                if (num % 2 == 0) {
                    cout << "true";
                }
            =====
                if (num % 2 == 0) { #paired
                    cout << true;
                }
            =====
                else {
                    cout << "false";
                }
            =====
                else { #paired
                    cout << false;
                }
            =====
            }


.. tabbed:: cond_rec_a6_q

    .. tab:: Activecode

        .. activecode:: cond_rec_a6
            :language: cpp

            Write the function ``greaterThan`` that prints true
            if the first ``double`` argument is greater than the
            second ``double`` argument.  Be sure to include any
            necessary headers. Select the Parsonsprob tab for hints
            for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            void greaterThan () {

            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cond_rec_a6_pp
            :numbered: left
            :adaptive:

            Write the function ``greaterThan`` that prints true
            if the first ``double`` argument is greater than the
            second ``double`` argument.  Be sure to include any
            necessary headers. Use the lines to construct the code,
            then go back to complete the Activecode tab.

            -----
            void greaterThan (double a, double b) {
            =====
            void greaterThan (int a , int b) { #paired
            =====
                if (a > b) {
                    cout << "true";
                }
            =====
                if (a < b) {
                    cout << true;
                }
            =====
                else {
                    cout << "false";
                }
            =====
                if (double a > double b) { #distractor
                    cout << true;
                }
            =====
            }


.. tabbed:: cond_rec_a8_q

    .. tab:: Activecode

        .. activecode:: cond_rec_a8
            :language: cpp

            Write the function ``exclusiveOr`` that prints true If
            either ``a`` OR ``b`` is true, and prints false otherwise.
            Be sure to include any necessary headers. Select the Parsonsprob
            tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            void exclusiveOr (bool a, bool b) {

            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cond_rec_a8_pp
            :numbered: left
            :adaptive:

            Write the function ``exclusiveOr`` that prints true If
            either ``a`` OR ``b`` is true, and prints false otherwise.
            Be sure to include any necessary headers. Use the lines to
            construct the code, then go back to complete the Activecode tab.

            -----
            void exclusiveOr (bool a, bool b) {
            =====
                if (a == true || b == true) {
                    cout << "true";
                }
            =====
                if (a == true && b == true) { #paired
                    cout << "true";
                }
            =====
                else {
                    cout << "false";
                }
            =====
            }


.. tabbed:: cond_rec_a10_q

    .. tab:: Activecode

        .. activecode:: cond_rec_a10
            :language: cpp

            Write the function ``printNegativeNum`` that asks the user
            for a negative number.  If the user does not provide a negative
            number, it should contine asking until the user provides one.
            It should then print the negative number. Select the Parsonsprob
            tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            void printNegativeNum () {

            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cond_rec_a10_pp
            :numbered: left
            :adaptive:

            Write the function ``printNegativeNum`` that asks the user
            for a negative number.  If the user does not provide a negative
            number, it should contine asking until the user provides one.
            It should then print the negative number. Use the lines to construct
            the code, then go back to complete the Activecode tab.

            -----
            void printNegativeNum () {
            =====
                int negative;
            =====
                cout << "Please provide a negative number." << endl;
            =====
                cin >> negative;
            =====
                if (negative >= 0) {
                    printNegativeNum();
                }
            =====
                if (negative >= 0) { #paired
                    cout << "Please provide a negative nunber." << endl;
                }
            =====
                cout << negative << endl;
            =====
            }
