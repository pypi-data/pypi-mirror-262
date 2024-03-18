
Functions with Results
----------------------

You might have noticed by now that some of the functions we are using,
like the math functions, yield results. Other functions, like ``newLine``,
perform an action but don’t return a value. That raises some questions:

-  What happens if you call a function and you don’t do anything with
   the result (i.e. you don’t assign it to a variable or use it as part
   of a larger expression)?

-  What happens if you use a function without a result as part of an
   expression, like ``newLine() + 7``?

-  Can we write functions that yield results, or are we stuck with
   things like newLine and printTwice?

The answer to the third question is “yes, you can write functions that
return values,” and we’ll do it in a couple of chapters. I will leave it
up to you to answer the other two questions by trying them out.

.. note::
   Any time you have a question about what is legal or illegal in C++, a
   good way to find out is to ask the compiler.  It will let you answer
   your question by throwing an error... or not!

.. fillintheblank:: fuwresults_1

   What will be **printed** when the following code runs? |blank|

   .. code-block:: cpp

        #include <iostream>
        using namespace std;

        void multiply (int x, int y) {
          cout << x*y;
        }

        int main() {
          int x = 2;
          int y = 4;
          multiply(x,y);
        }

   - :8: Yes! 2*4=8 so that will be printed but not returned
     :.*: Try again!

.. mchoice:: fuwresults_2

   Will the following code compile?

   .. code-block:: cpp

        #include <iostream>
        using namespace std;

        void multiply (int x, int y) {
          cout << x * y << endl;
        }

        int main() {
          int x = 2;
          int y = 4;
          cout << multiply(x,y);
        }

   - Yes

     - Can you print the result of a void function?

   - No

     + Correct! You can't print the result of a void function
