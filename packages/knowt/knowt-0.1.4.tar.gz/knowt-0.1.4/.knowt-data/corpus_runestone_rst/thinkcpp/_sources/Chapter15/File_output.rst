File output
-----------

Sending output to a file is similar. For example, we could modify the
previous program to copy lines from one file to another.


::

    #include <iostream>
    using namespace std;

    int main () {
     ifstream infile ("input-file");
     ofstream outfile ("output-file");

     if (infile.good() == false || outfile.good() == false) {
       cout << "Unable to open one of the files." << endl;
       exit (1);
     }

     while (true) {
       getline (infile, line);
       if (infile.eof()) break;
       outfile << line << endl;
     }
    }

.. parsonsprob:: question15_4_1
   :adaptive:
   :numbered: left

   Create a code block that sends output to a file. First, make sure that both the input file and the output file are able to be opened.
   -----
   int main () {
   =====
    ifstream in_file ("input_file_name");
    ofstream out_file ("input_file_name");
   =====
    if (in_file.good() == false || out_file.good() == false) {
   =====
      cout << "Unable to open one of the files." << endl;
   =====
      exit(1);
    }
   =====
    while (true) {
   =====
      getline(in_file, line);
   =====
      if (in_file.eof()) break;
   =====
      outfile << line << endl;
    }
   }


.. mchoice:: question15_4_2
   :answer_a: Create two "for" loops instead of an if-statement so that the statement loops through both conditions once.
   :answer_b: Create a "while" loop instead of an if-statement so that the statement loops through both conditions separately until the body of the loop is reached.
   :answer_c: Create two "if" statements, one that check whether in_file.good() is false, and another that checks whether out_file.good() is false, instead of putting them together in one "if" statement.
   :correct: c
   :feedback_a: Try again!
   :feedback_b: Try again!
   :feedback_c: Correct!

   The code from the previous problem checks whether the files open or not. It doesn't specify which one, if any, doesn't open. How could you specify which file does not open?

.. fillintheblank:: question15_4_3

    Finish the statement: |blank| ``outfile ("output-file");``.

    - :(?:o|O)(?:f|f)(?:s|S)(?:t|T)(?:r|R)(?:e|E)(?:A|a)(?:m|M): Correct!
      :.*: Try again!
