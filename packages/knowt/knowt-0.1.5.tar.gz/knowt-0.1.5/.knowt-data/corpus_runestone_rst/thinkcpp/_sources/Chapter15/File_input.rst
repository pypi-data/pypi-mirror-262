
.. _finput:

File input
----------

To get data from a file, we have to create a stream that flows from the
file into the program. We can do that using the ``ifstream``
constructor.

::

     ifstream infile ("file-name");

The argument for this constructor is a string that contains the name of
the file you want to open. The result is an object named ``infile`` that
supports all the same operations as ``cin``, including ``>>`` and
``getline``.

::

    #include <iostream>
    #include <fstream>
    using namespace std;

    int main ()
    {
     int x;
     string line;

     ifstream infile ("file-name");
     infile >> x;               // get a single integer and store in x
     getline (infile, line);    // get a whole line and store in line
    }

If we know ahead of time how much data is in a file, it is
straightforward to write a loop that reads the entire file and then
stops. More often, though, we want to read the entire file, but don’t
know how big it is.

There are member functions for ``ifstreams`` that check the status of
the input stream; they are called ``good``, ``eof``, ``fail`` and
``bad``. We will use ``good`` to make sure the file was opened
successfully and ``eof`` to detect the “end of file.”

Whenever you get data from an input stream, you don’t know whether the
attempt succeeded until you check. If the return value from ``eof`` is
``true`` then we have reached the end of the file and we know that the
last attempt failed. Here is a program that reads lines from a file and
displays them on the screen:


::

    #include <iostream>
    #include <fstream>
    using namespace std;

    int main ()
    {
     string fileName = ...;
     ifstream infile (fileName.c_str());

     if (infile.good() == false) {
       cout << "Unable to open the file named " << fileName;
       exit (1);
     }

     while (true) {
       getline (infile, line);
       if (infile.eof()) {
         break;
       }
       cout << line << endl;
     }
    }

The function ``c_str`` converts an ``string`` to a native C string.
Because the ``ifstream`` constructor expects a C string as an argument,
we have to convert the ``string``.

Immediately after opening the file, we invoke the ``good`` function. The
return value is ``false`` if the system could not open the file, most
likely because it does not exist, or you do not have permission to read
it.

The statement ``while(true)`` is an idiom for an infinite loop. Usually
there will be a ``break`` statement somewhere in the loop so that the
program does not really run forever (although some programs do). In this
case, the ``break`` statement allows us to exit the loop as soon as we
detect the end of file.

It is important to exit the loop between the input statement and the
output statement, so that when ``getline`` fails at the end of the file,
we do not output the invalid data in ``line``.

.. dragndrop:: question15_3_1
    :feedback: Try again!
    :match_1:  The constructor is|||ifstream.
    :match_2: The argument and the name of the file you want to open is|||"file-name".
    :match_3: The result of this code snippet is an object named|||infile.
    :match_4: The result of this code snippet supports the same operators as|||cin.

    Consider this code snippet:

    ::

       ifstream infile ("file-name");

    Finish each sentence.

.. fillintheblank:: question15_3_2

    The ``ifstream`` member function called |blank| makes sure the file was opened successfully, and
    member function |blank| detects the end of the file.

    - :(?:g|G)(?:o|O)(?:o|O)(?:d|D): Correct!
      :x: Try again!
    - :(?:e|E)(?:o|O)(?:f|F): Correct!
      :.*: Try again!

.. mchoice:: question15_3_3
   :answer_a: the ifstream constructor expects a C string as an argument.
   :answer_b: you need to make sure you have permission to read to/from the file.
   :answer_c: it will check whether you have an infinite loop or not.
   :answer_d: strings are not supported by C++.
   :correct: a
   :feedback_a: Correct!
   :feedback_b: Incorrect! Try reading again!
   :feedback_c: Incorrect! Try reading again!
   :feedback_d: Incorrect! strings are allowed in C++.

   We need to use the function ``c_str()`` to convert a string to a native C string because...


.. fillintheblank:: question15_3_4

    The __________ statement allows us to exit the loop as soon as we detect the end of the file.

    - :(?:b|B)(?:r|R)(?:e|E)(?:a|A)(?:k|K): Correct!
      :.*: Try again!

.. parsonsprob:: question15_3_5
   :adaptive:
   :numbered: left

   Create a code block that reads lines from "filename" and prints them out. First, make sure that the file is able to be opened.
   -----
   int main () {
   =====
    string name_of_file = "filename";
   =====
    ifstream in_file (name_of_file.c_str());
   =====
    if (in_file.good() == false) {
   =====
      cout << "Unable to open the file named " << name_of_file;
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
      cout << line << endl;
    }
   }
