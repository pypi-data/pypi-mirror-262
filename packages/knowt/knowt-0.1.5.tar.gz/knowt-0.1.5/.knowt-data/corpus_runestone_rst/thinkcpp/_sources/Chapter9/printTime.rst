``printTime``
-------------

When we define a new type it is a good idea to write function that
displays the instance variables in a human-readable form, which you attempted on the page before. Your solution should have looked something like this.

::

   void printTime (Time& t) {
     cout << t.hour << ":" << t.minute << ":" << t.second << endl;
   }

.. activecode:: printTime_AC_1
  :language: cpp
  :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

  In the active code below, the output of this function, if we pass ``time`` an argument, is
  ``11:59:3.14159``.
  ~~~~
  #include <iostream>
  using namespace std;

  struct Time {
      int hour, minute;
      double second;
  };

  void printTime (Time& t) {
      cout << t.hour << ":" << t.minute << ":" << t.second << endl;
  }

  int main () {
      Time time = { 11, 59, 3.14159 };
      printTime(time);
  }

.. mchoice:: printTime_1

   Which of the following would be a correct way to display the price of an object and finish the ``printPrice``, which we saw on the previous page?

   .. code-block:: cpp

      struct Price {
        int dollar, cents;
      };

      void printPrice(Price& p) {
        // Implementation here
      }

      int main() {
        Price sandwich = { 3, 45 };
        Price coffee = { 2, 50 };
        Price pastry = { 2, 0 };
      }

   - ``cout << "Price is " << "p.dollar" << " dollars and" << "p.cents" << "cents." << endl;``

     - Try again. We want to print the values rather than statements.

   - ``cout << "Price is " << p.dollar << " dollars and " << p.cents << " cents." << endl;``

     + Correct!

   - ``cout << "Price is " << p.dollar << " dollars and " << p.cents << " cents." << endl``

     - This would not compile. There is an important character that ends nearly all statements in C++.
