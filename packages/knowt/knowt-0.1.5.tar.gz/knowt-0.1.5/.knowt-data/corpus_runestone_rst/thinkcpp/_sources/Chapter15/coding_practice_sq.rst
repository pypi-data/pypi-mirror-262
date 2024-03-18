Coding Practice
---------------

.. tabbed:: cp_15_2_q

   .. tab:: Activecode

      .. activecode:: cp_15_AC_2q
         :language: cpp
         :practice: T
         :datafile: speech.txt
         :stdin: speech.txt

         Write a program that prompts a user for the name of an input file
         and for an integer ``n``. Then open the file and output the first 
         ``n`` lines of the file with each line reversed. For example,
         if you read in the line "hello world" you should print out
         "dlrow olleh" to the terminal. Include proper file error checking.
         Select the Parsonsprob tab for hints for the construction of the code.
         ~~~~
         #include <iostream>
         #include <fstream>
         using namespace std;

         // Write your code here.

   .. tab:: Parsonsprob

      .. parsonsprob:: cp_15_AC_2q_pp
         :numbered: left
         :adaptive:

         Write a program that prompts a user for the name of an input file
         and for an integer ``n``. Then open the file and output the first 
         ``n`` lines of the file with each line reversed. For example,
         if you read in the line "hello world" you should print out
         "dlrow olleh" to the terminal. Include proper file error checking.
         Use the lines to construct the code, then go back to complete the Activecode tab.

         -----
         int main () {
         =====
            string fileIn;
         =====
            int n;
         =====
            string line;
         =====
            cout << "Enter the name of the file: ";
            cin >> fileIn;
            cout << fileIn << endl;
         =====
            cout << "Enter an integer: ";
            cin >> n;
            cout << n << endl;
         =====
            ifstream inFile(fileIn.c_str());
         =====
            if (inFile.good() == false) {
               cout << "Unable to open the file named " << fileIn << " and output " << n << " lines." << endl;
               exit(1);
            }
         =====
            for (int i = 0; i < n; i++) {
         =====
               getline(inFile, line);
         =====
               cout << line << endl;
         =====
            }
         =====
         }

   .. tab:: Input File

      Below are the contents of the input file.

      ::

         We choose to go to the Moon. We choose to go to the Moon...
         We choose to go to the Moon in this decade and do the other things, 
         not because they are easy, but because they are hard; because that goal 
         will serve to organize and measure the best of our energies and skills, 
         because that challenge is one that we are willing to accept, one we are 
         unwilling to postpone, and one we intend to win, and the others, too.

.. tabbed:: cp_15_4_q

   .. tab:: Activecode

      .. activecode:: cp_15_AC_4q
         :language: cpp
         :practice: T
         :datafile: powers.txt

         Write a program that prompts a user for an integer ``n`` and print the first ``n``
         powers of 2 to an output file called ``powers.txt``. Include proper file error checking.
         To simulate what your output file would look like, the contents of your output file 
         will be displayed on the terminal. Select the Parsonsprob tab for hints for the construction of the code.
         ~~~~
         #include <iostream>
         #include <fstream>
         #include <cmath>
         using namespace std;

         int main() { 
            // Write your code here.





            // Do not modify the code below
            ifstream student_output("powers.txt");
            if (!student_output.good()) {
                  cout << "Error opening student's output." << endl;
            }
            string answer;
            while (getline(student_output, answer)) {
                  cout << answer << endl;
            }
         }

   .. tab:: Parsonsprob

      .. parsonsprob:: cp_15_AC_4q_pp
         :numbered: left
         :adaptive:

         Write a program that prompts a user for an integer ``n`` and print the first ``n``
         powers of 2 to an output file called ``powers.txt``. Include proper file error checking.
         To simulate what your output file would look like, the contents of your output file 
         will be displayed on the terminal. Use the lines to construct the code, then go back
         to complete the Activecode tab.

         -----
         int main() {
         =====
            int n;
         =====
            cout << "Enter an integer: ";
         =====
            cin >> n;
         =====
            cout << n << endl;
         =====
            ofstream outfile ("powers.txt");
         =====
            if (outfile.good() == false) {
               cout << "Unable to open output file." << endl;
               exit (1);
            }
         =====
            while (true) {
         =====
               for (int i = 0; i < n; i++) {
         =====
                     outfile << pow(2,i) << endl;
         =====
               }
         =====
            }
         =====
            ifstream student_output("powers.txt");
         =====
            if (!student_output.good()) {
               cout << "Error opening student's output." << endl;
            }
         =====
            string answer;
         =====
            while (getline(student_output, answer)) {
               cout << answer << endl;
            }
         =====
         }

.. tabbed:: cp_15_6_q

   .. tab:: Activecode

      .. activecode:: cp_15_AC_6q
         :language: cpp
         :practice: T
         :datafile: dream.txt

         Write a program that takes an input file called "dream.txt" and outputs
         the number of times the string "you" appears in the file to the terminal.
         Include proper file error checking.
         Select the Parsonsprob tab for hints for the construction of the code.
         ~~~~
         #include <iostream>
         #include <fstream>
         using namespace std;

         // Write your code here.


   .. tab:: Parsonsprob

      .. parsonsprob:: cp_15_AC_6q_pp
         :numbered: left
         :adaptive:

         Write a program that takes an input file called "dream.txt" and outputs
         the number of times the string "you" appears in the file to the terminal.
         Include proper file error checking. Use the lines to construct the code,
         then go back to complete the Activecode tab.

         -----
         int main() {
         =====
            int count = 0;
         =====
            char w[ ] = {'y', 'o', 'u'};
         =====
            ifstream inFile("dream.txt");
         =====
            string line;
         =====
            if (!inFile.good()) {
               cout << "Unable to open file." << endl;
               exit(1);
            }
         =====
            while (getline(inFile,line)) {
         =====
               for (int unsigned i = 0; i < line.size(); i++) {
         =====
                     if (line.at(i) == w[0]) {
         =====
                        if (line.at(i+1) == w[1]) {
         =====
                           if (line.at (i+2) == w[2]) {
         =====
                                 count++;
         =====
                           }
         =====
                        }
         =====
                     }
         =====
               }
         =====
            }
         =====
            cout << count << endl;
         =====
         }

   .. tab:: Input File

      Below are the contents of the input file.

      ::

         Have you ever had a dream that you, 
         um, you had, your, you- you could, 
         you’ll do, you- you wants, you, you 
         could do so, you- you’ll do, you could- 
         you, you want, you want them to do you 
         so much you could do anything?

.. tabbed:: cp_15_8_q

   .. tab:: Activecode

        .. activecode:: cp_15_AC_8q
           :language: cpp
           :practice: T
           :datafile: shrimp.txt

           Write a program that takes an input file called "shrimp.txt" and outputs
           the quote with "shrimp" replaced by a word that the user inputs to the terminal.
           Include proper file error checking. 
           Select the Parsonsprob tab for hints for the construction of the code.
           ~~~~
           #include <iostream>
           #include <fstream>
           using namespace std;

           // Write your code here.

   .. tab:: Parsonsprob

      .. parsonsprob:: cp_15_AC_8q_pp
         :numbered: left
         :adaptive:

         Write a program that takes an input file called "shrimp.txt" and outputs
         the quote with "shrimp" replaced by a word that the user inputs to the terminal.
         Include proper file error checking. 
         Use the lines to construct the code, then go back to complete the Activecode tab.

         -----
         int main() {
         =====
            string word;
         =====
            cout << "Enter word to replace 'shrimp': ";
         =====
            cin >> word;
         =====
            cout << word << endl;
         =====
            string replace = "shrimp";
         =====
            ifstream inFile("shrimp.txt");
         =====
            string line;
         =====
            for (int i = 0; i < 4; i++) {
         =====
               getline(inFile,line);
         =====
               for (int unsigned j = 0; j < line.size(); j++) {
         =====
                  size_t pos = line.find(replace);
         =====
                  if (pos != std::string::npos) {
         =====
                     line.replace(pos,replace.length(),word);
         =====
                  }
         =====
               }
         =====
               cout << line<< endl;
         =====
            }
         =====
         }

   .. tab:: Input File

        Below are the contents of the input file.

        ::

            There's pineapple shrimp, lemon shrimp, coconut shrimp, 
            pepper shrimp, shrimp soup, shrimp stew, shrimp salad, 
            shrimp and potatoes, shrimp burger, shrimp sandwich. 
            That- that's about it.

.. tabbed:: cp_15_10_q

   .. tab:: Activecode

      .. activecode:: cp_15_AC_10q
         :language: cpp
         :practice: T

         Write a program that computes the product of two matrices.
         Take a look at the example below. Two find the product of two
         matrices, take the ith row from the first matrix and the jth column
         from the second matrix, find the summation of the product of each component,
         and that's the value that goes into the (i, j) location of the new matrix.
         The product of an mxn and an nxp matrix is an mxp matrix.
         Select the Parsonsprob tab for hints for the construction of the code.
         ~~~~
         #include <iostream>
         #include <fstream>
         using namespace std;

         int main() { 
            /*
               2x3 matrix A  X 3x2 matrix B                2x2 matrix C      
            [ a    b    c ]    [ g    h ]       [ ag + bi + cl    ah + bj + cm ]
            [ d    e    f ]    [ i    j ]   =   [ dg + ei + fl    dh + ej + fm ]
                                 [ l    m ]
            */
            
            // Write your code here.
         }

   .. tab:: Parsonsprob

      .. parsonsprob:: cp_15_AC_10q_pp
         :numbered: left
         :adaptive:

         Write a program that computes the product of two matrices.
         Take a look at the example below. To find the product of two
         matrices, take the ith row from the first matrix and the jth column
         from the second matrix, find the summation of the product of each component,
         and that's the value that goes into the (i, j) location of the new matrix.
         The product of an mxn and an nxp matrix is an mxp matrix.
         Use the lines to construct the code, then go back to complete the Activecode tab.

         -----
         int main() {
         =====
         matrix<int> A(2,3);
         =====
         matrix<int> B(3,2);
         =====
         matrix<int> C(2,2);
         =====
         C[0,0] = (A[0,0] * B[0,0]) + (A[0,1] * B[1,0]) + (A[0,2] * B[2,0]);
         =====
         C[0,1] = (A[0,0] * B[0,1]) + (A[0,1] * B[1,1]) + (A[0,2] * B[2,1]);
         =====
         C[1,0] = (A[1,0] * B[0,0]) + (A[1,1] * B[1,0]) + (A[1,2] * B[2,0]);
         =====
         C[1,1] = (A[1,0] * B[0,1]) + (A[1,1] * B[1,1]) + (A[1,2] * B[2,1]);
         =====
         }
