Activecode Exercises
-----------------------

Answer the following **Activecode** questions to assess what you have learned in this chapter.

.. tabbed:: mucp_15_1_ac

    .. tab:: Question

        .. activecode:: mucp_15_1_ac_q
            :language: cpp

            We have a file called "locations.txt" that we want to read data from. 
            Check to make sure that the file was opened properly; if it wasn't,
            display an error message and exit with a status of 1.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_15_1_ac_a
            :language: cpp

            Below is one way to write code that makes sure the file was opened properly.
            ~~~~
            #include <iostream>
            using namespace std;

            int main() {   
                ifstream infile("locations.txt");
                if (infile.good() == false) {
                    cout << "Unable to open the file." << endl;
                    exit(1);
                }
            }


.. tabbed:: mucp_15_2_ac

    .. tab:: Question

        .. activecode:: mucp_15_2_ac_q
            :language: cpp

            Let's write a program that prompts the user for a filename and
            opens that file. 
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_15_2_ac_a
            :language: cpp

            Below is one way to write the program.
            ~~~~
            #include <iostream>
            using namespace std;

            int main() {   
                string filename;
                cout << "Enter the name of the file: ";
                cin >> filename;
                ifstream infile(filename.c_str());
                if (infile.good() == false) {
                    cout << "Unable to open the file." << endl;
                    exit(1);
                }
            }


.. tabbed:: mucp_15_3_ac

    .. tab:: Question

        .. activecode:: mucp_15_3_ac_q
            :language: cpp

            Now let's write some output to a file. Write a program that prompts
            a user for a list of 5 integers separated by spaces, calculates the 
            average of those integers, and outputs "The average is ``average``"
            to an output file called "average.txt". Put the necessary blocks 
            of code in the correct order. Declare the output file first and 
            check that it is opened correctly.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

      .. activecode:: mucp_15_3_ac_a
         :language: cpp

         Below is one way to write the program.
         ~~~~
         #include <iostream>
         using namespace std;

         int main() {   
            ofstream outfile("average.txt");
            if (outfile.good() == false) {
               cout << "Unable to open the file." << endl;
               exit(1);
            }
            int sum = 0;
            int n1, n2, n3, n4, n5;
            cout << "Enter five integers separated by spaces: ";
            cin >> n1 >> n2 >> n3 >> n4 >> n5;
            sum = n1 + n2 + n3 + n4 + n5;
            outfile << "The average is " << sum / 5.0 << endl;
         }


.. tabbed:: mucp_15_4_ac

    .. tab:: Question

        .. activecode:: mucp_15_4_ac_q
            :language: cpp

            We are given a file called "data.txt" with an unknown number of 
            ``double`` values. Write a program that finds the minimum, maximum,
            and number of data and outputs these values to a file called 
            "summary.txt". 
            Declare the input and output files first, and check to see that 
            both are opened correctly before dealing with data. Increment the 
            number of data points before checking for the min and max.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_15_4_ac_a
            :language: cpp

            Below is one way to write the code.
            ~~~~
            #include <iostream>
            using namespace std;

            int main() {   
                ifstream infile("data.txt");
                ofstream outfile("summary.txt");
                if (infile.good() == false || outfile.good() == false) {
                    cout << "Unable to open a file." << endl;
                    exit(1);
                }
                int numData = 1;
                double min, max, value;
                infile >> value;
                min = value;
                max = value;
                while (infile >> value) {
                    ++numData;
                    if (value < min) { min = value; }
                    if (value > max) { max = value; }
                }
                outfile << "Number of data: " << numData << ", min: " << min << ", max: " << max << endl;
            }


.. tabbed:: mucp_15_5_ac

    .. tab:: Question

        .. activecode:: mucp_15_5_ac_q
            :language: cpp

            You are given a file called "employee_data.txt" and you want to store
            the information from that file into a vector of data. The file contains
            information about an employee's first and last name, age, phone number,
            and email. Write the definition of an ``Employee`` before you write your
            ``main`` function. Open and check the file before working with the data.
            ~~~~
            #include <iostream>
            #include <string>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_15_5_ac_a
            :language: cpp

            Below is one way to define ``Employee``.
            ~~~~
            #include <iostream>
            #include <string>
            #include <vector>
            using namespace std;

            struct Employee {
                string fname;
                string lname;
                int age;
                int phone;
                string email;
                Employee(string f, string l, int a, int p, string e) {
                    fname = f;
                    lname = l;
                    age = a;
                    phone = p;
                    email = e;
                }
            };
            
            int main() {   
                ifstream infile("employee_data.txt");
                if (infile.good() == false) {
                    cout << "Unable to open the file." << endl;
                    exit(1);
                }
                vector<Employee> data;
                string fname, lname, email;
                int age, phone;
                while (infile >> fname >> lname >> age >> phone >> email) {
                    Employee e(fname, lname, age, phone, email);
                    data.push_back(e);
                }
            }


.. tabbed:: mucp_15_6_ac

    .. tab:: Question

        .. activecode:: mucp_15_6_ac_q
            :language: cpp

            You are given a file but it appears that someone's capslock key was stuck
            because everything is in uppercase. Write a program that takes the input from
            the file "UPPER.txt" and converts all the words to lowercase and prints
            out the modified message to a file called "lower.txt". Write the definition
            of the function ``toLower`` first. Separate the words with spaces.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_15_6_ac_a
            :language: cpp

            Below is one way to write the program and ``toLower`` function.
            ~~~~
            #include <iostream>
            #include <string>
            using namespace std;

            string upperToLower(string upper) {
                for (size_t i = 0; i < upper.length(); ++i) {
                    upper[i] = toupper(upper[i]);
                }
                return upper;
            }

            int main() {   
                ifstream infile("UPPER.txt");
                ofstream outfile("lower.txt");
                if (infile.good() == false || outfile.good() == false) {
                    cout << "Unable to open a file." << endl;
                    exit(1);
                }
                string word;
                while (infile >> word) {
                    string upper = upperToLower(word);
                    outfile << upper << " ";
                }
            }


.. tabbed:: mucp_15_7_ac

    .. tab:: Question

        .. activecode:: mucp_15_7_ac_q
            :language: cpp

            Nobody ever put a limit on how many files we can work with. Does 
            this mean we can open two or more files at once? Yes we can! 
            Write a program that combines two files "odds.txt" and "evens.txt"
            into one output file "numbers.txt". You should combine them in a 
            way such that "numbers.txt" contains the first odd number then
            the first even number then the second odd number and so on. You
            are guaranteed that there are equal amounts of odd and even numbers.
            ~~~~
            #include <iostream> 
            using namespace std;
            // YOUR CODE HERE 


    .. tab:: Answer

        .. activecode:: mucp_15_7_ac_a
            :language: cpp

            Below is one way to write the prgram.
            ~~~~
            #include <iostream>
            using namespace std;

            int main() {   
                ifstream odds("odds.txt");
                ifstream evens("evens.txt");
                ofstream outfile("numbers.txt");
                if (!odds.good() || !evens.good() || !outfile.good()) {
                    cout << "Unable to open a file." << endl;
                    exit(1);
                }
                int odd, even;
                while (odds >> odd && evens >> even) {
                    outfile << odd << " " << even << " ";
                }
            }


.. tabbed:: mucp_15_8_ac

    .. tab:: Question

        .. activecode:: mucp_15_8_ac_q
            :language: cpp

            In chapter 15.7 we defined the ``Set`` data structure.
            Write a function ``vectorToSet`` which takes a ``vector``
            of data and returns a ``Set`` object with the data. 
            Put the ``Set`` definition first in your answer.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_15_8_ac_a
            :language: cpp

            Below is one way to write the ``vectorToSet`` function.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            class Set {
                private:
                    vector<string> elements;
                    int numElements;

                public:
                    Set (int n);

                    int getNumElements () const;
                    string getElement (int i) const;
                    int find (const string& s) const;
                    int add (const string& s);
            };

            Set vectorToSet(vector<string> data) {   
                Set s(data.size());
                for (size_t i = 0; i < data.size(); ++i) {
                    s.add(data[i]);
                }
            }


.. tabbed:: mucp_15_9_ac

    .. tab:: Question

        .. activecode:: mucp_15_9_ac_q
            :language: cpp

            Let's write the struct definition for a ``Matrix``! The underlying
            data structure is a ``vector`` of vectors of ``int``s. Write 
            the constructor and ``at`` function, which returns the data stored
            at a given row and column. 
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_15_9_ac_a
            :language: cpp

            Below is one way to define ``Matrix`` and write the functions.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            class Matrix {
                private:
                    vector<vector<int> > elements;
                public:
                    Matrix (int numRows, int numCols) {
                        vector<int> row(numCols);
                        for (int i = 0; i < numRows; ++i) {
                        elements.push_back(row);
                        }
                    }
                    int at(int row, int col) {
                        return elements[row][col];
                    }
            };


.. tabbed:: mucp_15_10_ac

    .. tab:: Question

        .. activecode:: mucp_15_10_ac_q
            :language: cpp

            Now that we have the basic structure of a ``Matrix``, let's write
            a function that allows us to add data to a matrix. Write the ``Matrix``
            member function ``setData`` which takes a row and column index as well
            as a data value and stores the data value in the ``Matrix`` at the 
            given location. Then read data in from a file called ``data.txt``.
            The first line contains the number of rows and columns, separated by a space.
            Data values begin on the next line. 
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_15_10_ac_a
            :language: cpp

            Below is one way to ``setData`` member function.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            class Matrix {
                private:
                    vector<vector<int> > elements;
                public:
                    Matrix (int numRows, int numCols) {
                        vector<int> row(numCols);
                        for (int i = 0; i < numRows; ++i) {
                        elements.push_back(row);
                        }
                    }
                    int at(int row, int col) {
                        return elements[row][col];
                    }
            };

            void Matrix::setData (int row, int col, int value) {
                elements[row][col] = value;
            }
            
            int main() {
                ifstream infile("data.txt");
                if (!odds.good() || !evens.good() || !outfile.good()) {
                    cout << "Unable to open a file." << endl;
                    exit(1);
                }
                int numRows, numCols, data;
                infile >> numRows >> numCols;
                Matrix mat(numRows, numCols);
                while (infile >> data) {
                    for (int i = 0; i < numRows; ++i) {
                        for (int j = 0; j < numCols; ++j) {
                        mat.setData(i, j, data);
                        }
                    }
                }
            }

