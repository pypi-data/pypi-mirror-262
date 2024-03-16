Initialize or construct?
------------------------

Earlier we declared and initialized some ``Time`` structures using
squiggly-braces:

::

     Time currentTime = { 9, 14, 30.0 };
     Time breadTime = { 3, 35, 0.0 };

Now, using constructors, we have a different way to declare and
initialize:

::

     Time time (seconds);

These two functions represent different programming styles, and
different points in the history of C++. Maybe for that reason, the C++
compiler requires that you use one or the other, and not both in the
same program.

If you define a constructor for a structure, then you have to use the
constructor to initialize all new structures of that type. The alternate
syntax using squiggly-braces is no longer allowed.

Fortunately, it is legal to overload constructors in the same way we
overloaded functions. In other words, there can be more than one
constructor with the same “name,” as long as they take different
parameters. Then, when we initialize a new object the compiler will try
to find a constructor that takes the appropriate parameters.

For example, it is common to have a constructor that takes one parameter
for each instance variable, and that assigns the values of the
parameters to the instance variables:

::

   Time::Time (int h, int m, double s) {
     hour = h;  minute = m;  second = s;
   }

To invoke this constructor, we use the same funny syntax as before,
except that the arguments have to be two integers and a ``double``:

::

     Time currentTime (9, 14, 30.0);

.. activecode:: initialize_or_construct_AC_1
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   In the active code below, you can experiment passing values into the two 
   different constructors that we have defined on this page and the previous
   page.
   ~~~~
   #include <iostream>
   using namespace std;

   struct Time {
       int hour, minute;
       double second;
       Time (double secs);
       Time (int h, int m, double s);
       void print ();
   };

   int main() {
       Time marathon (9000);
       cout << "My marathon time is "; marathon.print(); cout << "." << endl;
       Time race (7, 30, 0.0);
       cout << "My next race is at "; race.print(); cout << "." << endl;
   }

   ====

   Time::Time (double secs) {
     hour = int (secs / 3600.0);
     secs -= hour * 3600.0;
     minute = int (secs / 60.0);
     secs -= minute * 60.0;
     second = secs;
   }

   Time::Time (int h, int m, double s) {
     hour = h; minute = m; second = s;
   }

   void Time::print () {
     cout << hour << ":" << minute << ":" << second;
   }

.. mchoice:: initialize_or_construct_1
   :answer_a: When we initialize a new object, the compiler automatically finds the correct constructor to use.
   :answer_b: You can always initialize an object using squiggly-braces.
   :answer_c: You can have many constructors with the same name.
   :answer_d: Once you define a constructor for a structure, you MUST use it to initialize any new structures of that type.
   :correct: b
   :feedback_a: Incorrect! This statement is true!
   :feedback_b: Correct! Once you define a constructor, you can no longer use squiggly-braces to initialize an object.
   :feedback_c: Incorrect! This statement is true, as long as the constructors take different parameters.
   :feedback_d: Incorrect! This statement is true!

   Which statement is **false** about constructors?

.. mchoice:: initialize_or_construct_2
   :answer_a: friend constructors
   :answer_b: overriding
   :answer_c: overloading
   :answer_d: friend class
   :correct: c
   :feedback_a: Incorrect! "Friend" constructors are constructors that are private except to the friend class.
   :feedback_b: Incorrect! Overriding is the ability of an inherited class to rewrite the methods of the base class at runtime, not what we're looking for here.
   :feedback_c: Correct!
   :feedback_d: Incorrect! A friend class is a class that can access private members of another class, not what we're looking for here.

   What is the term for having multiple constructors with the same "name" that take different parameters?

.. parsonsprob:: initialize_or_construct_3
   :numbered: left
   :adaptive:

   Implement two constructors for the ``Dog`` structure. One should be a default constructor, the other should take
   arguments. The weight needs to be converted from pounds to kilograms in the second constructor (for
   reference, 1 kilogram is approximately 2.2 pounds).
   -----
   struct Dog {
   =====
    int age, weight;
    string breed;
   =====
    Dog();
    Dog(int age_in, int weight_in, string breed_in);
   =====
   };
   =====
   Dog::Dog() {
   =====
    breed = "mutt";
    age = 1;
    weight = 18;
   =====
   }
   =====
   Dog::Dog(int age_in, int weight_in, string breed_in) {
   =====
    breed = breed_in;
    age = age_in;
   =====
    weight = weight_in / 2.2;
   }
   =====
    weight = weight_in * 2.2;                         #paired
   }