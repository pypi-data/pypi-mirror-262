Activecode Exercises
--------------------

Answer the following **Activecode** questions to
assess what you have learned in this chapter.


.. tabbed:: cond_rec_a1

   .. tab:: Question

      .. activecode:: cond_rec_a1q
         :language: cpp

         Fix the code below so that it prints "THE TEAM" "THE TEAM" 
         "THE TEAM" on three separate lines.
         ~~~~
         #include <iostream>
         using namespace std;
         
         int main() {
            int x = 8;
            int y = 8;
            
            if (x % 2 == 0) {
                cout << "THE TEAM";
            }
            else if (x >= y) {
                cout << "THE TEAM";
            }
            else if (y >= x) {
                cout << "THE TEAM";
            }
         }

   .. tab:: Answer

      .. activecode:: cond_rec_a1_a
         :language: cpp

         Below is one way to fix the program.  Since we want "THE TEAM"
         to print three times, we must check all three conditons.  this
         means changing the ``else if`` statements to ``if`` statements.
         ~~~~
         #include <iostream>
         using namespace std;
         int main(){
            int x = 8;
            int y = 8;
            
            if (x % 2 == 0) {
                cout << "THE TEAM" << endl;
            }
            if (x >= y) {
                cout << "THE TEAM" << endl;
            }
            if (y >= x) {
                cout <<< "THE TEAM" << endl;
            }
         }


.. selectquestion:: cond_rec_a2_sq
    :fromid: cond_rec_a2, cond_rec_a2_pp
    :toggle: lock 


.. tabbed:: cond_rec_a3

   .. tab:: Question

      .. activecode:: cond_rec_a3q
         :language: cpp

         Fix the infinite recursion in the code below.  The function
         should not count any numbers after 10 (the highest numbers
         that should print are 9 or 10).  When it is done counting,
         the function should print that.
         ~~~~
         #include <iostream>
         using namespace std;

         void countBy2 (int num) {
             if (num != 10) {
                 cout << num;
                 countBy2 (num + 2);
             }
             else {    
                 cout << num << endl;
                 cout << "Done counting!";
             }
         }

         int main () {
             countBy2(6);
         }

   .. tab:: Answer

      .. activecode:: cond_rec_a3_a
         :language: cpp

         Below is one way to fix the program.  The infinite recursion
         happens when we use an odd number as an argument.  By checking
         that a number is less than 99, the highest numbers to recurse
         are 98 and 97.  ``98 + 2 == 100`` and ``97 + 2 == 99``, so we
         never count past 100.
         ~~~~
         #include <iostream>
         using namespace std;

         void countBy2 (int num) {
             if (num < 9) {
                 cout << num;
                 countBy2 (num + 2);
             }
             else {    
                 cout << num << endl;
                 cout << "Done counting!";
             }
         }

         int main () {
             countBy2(6);
         }


.. selectquestion:: cond_rec_a4_sq
    :fromid: cond_rec_a4, cond_rec_a4_pp
    :toggle: lock


.. tabbed:: cond_rec_a5

   .. tab:: Question

      .. activecode:: cond_rec_a5q
         :language: cpp

         Finish the code below so that the function will continue to
         ask for input until the user guesses the word correctly.
         ~~~~
         #include <iostream>
         using namespace std;

         bool guessTheWord (string correct) {
             cout << "Guess the word!";
             string guess;
             cin >> guess;
             if (guess == correct) {
                 cout << "That's it!";
             }
         }


   .. tab:: Answer

      .. activecode:: cond_rec_a5a
         :language: cpp

         Below is one way to complete the program.
         ~~~~
         #include <iostream>
         using namespace std;

         bool guessTheWord (string correct) {
             cout << "Guess the word!";
             string guess;
             cin >> guess;
             if (guess == correct) {
                 cout << "That's it!";
             }
             else {
                 guessTheWord(correct);
             }
         }


.. selectquestion:: cond_rec_a6_sq
    :fromid: cond_rec_a6, cond_rec_a6_pp
    :toggle: lock


.. tabbed:: cond_rec_a7

   .. tab:: Question

      .. activecode:: cond_rec_a7q
         :language: cpp

         Write the function ``goodVibes`` that prints "I'm having a ``mood`` day!"
         depending on the value of ``mood``.  If ``mood`` is "bad", then the function
         should not do anything since it's good vibes only.  Be sure to
         include any necessary headers.
         ~~~~
         #include <iostream>
         using namespace std;

         void goodVibes (string mood) {
        
         }

   .. tab:: Answer

      .. activecode:: cond_rec_a7a
         :language: cpp

         Below is one way to write the program.  The return allows the
         function to exit if there are bad vibes in the room.  Otherise,
         the function prints as directed.
         ~~~~
         #include <iostream>
         using namespace std;
         
         void goodVibes (string mood) {
             if (mood == "bad") {
                 return;
             }
             cout << "I'm having a " << mood << " day";
         }


.. selectquestion:: cond_rec_a8_sq
    :fromid: cond_rec_a8, cond_rec_a8_pp
    :toggle: lock


.. tabbed:: cond_rec_a9

   .. tab:: Question

      .. activecode:: cond_rec_a9q
         :language: cpp

         Write the function ``countdown`` that takes a positive integer
         and decrements it until eaching zero, printing the number at each 
         step of the way.  Once it reaches zero, it should print "Blastoff!"
         ~~~~
         #include <iostream>
         using namespace std;

         void countdown (int num) {
        
         }

   .. tab:: Answer

      .. activecode:: cond_rec_a9a
         :language: cpp

         Below is one way to write the program.
         ~~~~
         #include <iostream>
         using namespace std;

         void countdown (int num) {
             if (num != 0){
                 cout << num << endl;
                 num -= 1;
                 countdown (num);
             }
             else {
                 cout << "Blastoff!";
             }
         }


.. selectquestion:: cond_rec_a10_sq
    :fromid: cond_rec_a10, cond_rec_a10_pp
    :toggle: lock