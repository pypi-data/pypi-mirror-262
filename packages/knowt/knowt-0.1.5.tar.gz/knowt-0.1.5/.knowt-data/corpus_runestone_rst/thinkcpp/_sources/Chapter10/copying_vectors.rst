Copying vectors
---------------

There is one more constructor for ``vector``\ s, which is called a copy
constructor because it takes one ``vector`` as an argument and creates a
new vector that is the same size, with the same elements.

::

     vector<int> copy (count);

Although this syntax is legal, it is almost never used for ``vector``\ s
because there is a better alternative:

::

     vector<int> copy = count;

The ``=`` operator works on ``vector``\ s in pretty much the way you
would expect.

.. activecode:: copying_vectors_AC_1
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   Take a look at the active code below, which uses the copy constructor.
   ~~~~
   #include <iostream>
   #include <vector>
   using namespace std;

   void print_vec(vector<int> vec);

   int main() {
       vector<int> count = {1,2,3,4};
       cout << "count = "; print_vec(count);

       vector<int> copy_1 (count);
       vector<int> copy_2 = count;

       cout << "copy_1 = "; print_vec(copy_1);
       cout << "copy_2 = "; print_vec(copy_2);
       cout << "We just made two copies of count.  As you can see, both methods work the same!" << endl;
   }

   ====
   
   void print_vec(vector<int> vec) {
      size_t i = 0;
      cout << "[";
      while (i < vec.size()-1) {
          cout << vec[i] << ",";
          i++;
      }
      cout << vec[vec.size()-1];
      cout << "]" << endl;
   }


.. mchoice:: copying_vectors_1

    **Multiple Response** How would you make a copy of ``vector<double> decimals`` called **nums**?

    -   ``vector<double> nums = decimals;``

        +   This is one way to make a copy.

    -   ``vector<double> decimals = nums;``

        -   This makes a copy of nums called decimals.

    -   ``vector<double> nums (decimals);``

        +   This is one way to make a copy.

    -   ``vector<double> decimals (nums);``

        -   This makes a copy of nums called decimals.


.. fillintheblank:: copying_vectors_2

   What is the name of the function that takes a vector as an argument, and 
   creates a new vector of the same size and with the same elements?

   - :[Cc][Oo][Pp][Yy] [Cc][Oo][Nn][Ss][Tt][Rr][Uu][Cc][Tt][Oo][Rr]: Correct!
     :.*: incorrect! You can find the answer by re-reading the text above.