.. _parsing:

Parsing input
-------------

In :numref:`formal` I defined “parsing” as the process of
analyzing the structure of a sentence in a natural language or a
statement in a formal language. For example, the compiler has to parse
your program before it can translate it into machine language.

In addition, when you read input from a file or from the keyboard you
often have to parse it in order to extract the information you want and
detect errors.

For example, I have a file called ``distances`` that contains
information about the distances between major cities in the United
States. I got this information from a randomly-chosen web page

::

   http://www.jaring.my/usiskl/usa/distance.html

so it may be wildly inaccurate, but that doesn’t matter. The format of
the file looks like this:

::

   "Atlanta"       "Chicago"       700
   "Atlanta"       "Boston"        1,100
   "Atlanta"       "Chicago"       700
   "Atlanta"       "Dallas"        800
   "Atlanta"       "Denver"        1,450
   "Atlanta"       "Detroit"       750
   "Atlanta"       "Orlando"       400

Each line of the file contains the names of two cities in quotation
marks and the distance between them in miles. The quotation marks are
useful because they make it easy to deal with names that have more than
one word, like “San Francisco.”

By searching for the quotation marks in a line of input, we can find the
beginning and end of each city name. Searching for special characters
like quotation marks can be a little awkward, though, because the
quotation mark is a special character in C++, used to identify string
values.

If we want to find the first appearance of a quotation mark, we have to
write something like:

::

     int index = line.find ('\"');

The argument here looks like a mess, but it represents a single
character, a double quotation mark. The outermost single-quotes indicate
that this is a character value, as usual. The backslash (``\``)
indicates that we want to treat the next character literally. The
sequence ``\"`` represents a quotation mark; the sequence ``\'``
represents a single-quote. Interestingly, the sequence ``\\`` represents
a single backslash. The first backslash indicates that we should take
the second backslash seriously.

Parsing input lines consists of finding the beginning and end of each
city name and using the ``substr`` function to extract the cities and
distance. ``substr`` is a ``string`` member function; it takes two
arguments, the starting index of the substring and the length.

::

   void processLine (const string& line)
   {
     // the character we are looking for is a quotation mark
     char quote = '\"';

     // store the indices of the quotation marks in a vector
     vector<int> quoteIndex (4);

     // find the first quotation mark using the built-in find
     quoteIndex[0] = line.find (quote);

     // find the other quotation marks using the find from Chapter 7
     for (int i=1; i<4; i++) {
       quoteIndex[i] = find (line, quote, quoteIndex[i-1]+1);
     }

     // break the line up into substrings
     int len1 = quoteIndex[1] - quoteIndex[0] - 1;
     string city1 = line.substr (quoteIndex[0]+1, len1);
     int len2 = quoteIndex[3] - quoteIndex[2] - 1;
     string city2 = line.substr (quoteIndex[2]+1, len2);
     int len3 = line.length() - quoteIndex[2] - 1;
     string distString = line.substr (quoteIndex[3]+1, len3);

     // output the extracted information
     cout << city1 << "\t" << city2 << "\t" << distString << endl;
   }

Of course, just displaying the extracted information is not exactly what
we want, but it is a good starting place.

.. mchoice:: question15_5_1
   :answer_a: to scan an entire program for errors
   :answer_b: to run a program start to finish and record the run time
   :answer_c: to analyze the structure of a statement in a formal language
   :answer_d: to search an entire program for a statement
   :correct: c
   :feedback_a: Incorrect! This is included in the debugging process.
   :feedback_b: Incorrect! This is included in the debugging process.
   :feedback_c: Correct! The compiler has to parse the program before it can translate it into machine language!
   :feedback_d: Incorrect! You can use control (command) + F to find a particular statement.

   What does **parsing** mean in the programming sense?

.. fillintheblank:: question15_5_2

    The |blank| character indicates that we want to match the next character literally.

    - :(\\)|([Bb][Aa][Cc][Kk][Ss][Ll][Aa][Ss][Hh]): Correct!
      :.*: Incorrect! Go back and read to find the answer!

.. fillintheblank:: question15_5_3

    The ``substr()`` takes |blank| and |blank| as its two arguments.

    - :([Ii][Nn][Dd][Ee][Xx]): Correct!
      :.*: Incorrect! Go back and read to find the answer!
    - :([Ll][Ee][Nn][Gg][Tt][Hh]): Correct!
      :.*: Incorrect! Go back and read to find the answer!

.. parsonsprob:: question15_5_4
   :adaptive:
   :numbered: left

   Create a block of code that takes a date written in the format "mm/dd/yyyyy" 
   as an argument, and that separates it into three separate integers: day,
   month, and year. Find the respective parts in this order: month, first slash,
   day, second slash, year.
   -----
   int main () {
   =====
    string month = date.substr(0, 2);
   =====
    string month = date.substr(2, 0);                              #paired
   =====
    int first_slash = date.find('/');
   =====
    string day = date.substr(first_slash + 1, 2);
   =====
    string day = date.substr(first_slash, 2);                              #paired
   =====
    int second_slash = date.find('/', first_slash + 1);
   =====
    int second_slash = date.find('/', first_slash);                              #paired
   =====
    int second_slash = date.find('/');                              #paired
   =====
    string year = date.substr(second_slash + 1, 4);
   =====
    string year = date.substr(second_slash, 4);                              #paired
   =====
    string year = date.substr(second_slash + 1, 2);                              #paired
   =====
   }
