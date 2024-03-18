``print``
---------

In :numref:`time` we defined a structure named ``Time`` and
wrote a function named ``printTime``

::

   struct Time {
     int hour, minute;
     double second;
   };

   void printTime (const Time& time) {
     cout << time.hour << ":" << time.minute << ":" << time.second << endl;
   }

To call this function, we had to pass a ``Time`` object as a parameter.

::

     Time currentTime = { 9, 14, 30.0 };
     printTime (currentTime);

To make ``printTime`` into a member function, the first step is to
change the name of the function from ``printTime`` to ``Time::print``.
The ``::`` operator separates the name of the structure from the name of
the function; together they indicate that this is a function named
``print`` that can be invoked on a ``Time`` structure.

The next step is to eliminate the parameter. Instead of passing an
object as an argument, we are going to invoke the function on an object.

.. index::
   single: current object
   single: this

As a result, inside the function, we no longer have a parameter named
``time``. Instead, we have a **current object**, which is the object the
function is invoked on. We can refer to the current object using the C++
keyword ``this``.

.. index::
   single: pointer

One thing that makes life a little difficult is that ``this`` is
actually a pointer to a structure, rather than a structure itself. A
**pointer** is similar to a reference, but I don’t want to go into the
details of using pointers yet. The only pointer operation we need for
now is the ``*`` operator, which converts a structure pointer into a
structure. In the following function, we use it to assign the value of
``this`` to a local variable named ``time``.

::

   void Time::print () {
     Time time = *this;
     cout << time.hour << ":" << time.minute << ":" << time.second << endl;
   }

The first two lines of this function changed quite a bit as we
transformed it into a member function, but notice that the output
statement itself did not change at all.

In order to invoke the new version of ``print``, we have to invoke it on
a ``Time`` object:

::

     Time currentTime = { 9, 14, 30.0 };
     currentTime.print ();

The last step of the transformation process is that we have to declare
the new function inside the structure definition:

::

   struct Time {
     int hour, minute;
     double second;

     void print ();
   };

.. note::
   You should only use the scope resolution operator ``::`` if you define a
   member function outside of its structure definition.  If you define a function
   *inside* of the structure definition, you define it as you would any other 
   function.

.. index::
   single: function declaration

.. index::
   single: function interface

A **function declaration** looks just like the first line of the
function definition, except that it has a semi-colon at the end. The
declaration describes the **interface** of the function; that is, the
number and types of the arguments, and the type of the return value.

.. index::
   single: function implementation

When you declare a function, you are making a promise to the compiler
that you will, at some point later on in the program, provide a
definition for the function. This definition is sometimes called the
**implementation** of the function, since it contains the details of how
the function works. If you omit the definition, or provide a definition
that has an interface different from what you promised, the compiler
will complain.

.. activecode:: print_AC_1
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   Feel free to mess around with input for ``currentTime`` in the active code below!
   ~~~~
   #include <iostream>
   using namespace std;

   struct Time {
       int hour, minute;
       double second;

       void print ();
   };

   int main() {
       Time currentTime = { 9, 14, 30.0 };
       currentTime.print ();
   }

   ====
   void Time::print () {
     cout << hour << ":" << minute << ":" << second << endl;
   }

.. fillintheblank:: print_1

    What keyword do we use to refer to the current object?

    - :([Tt]his|THIS): Correct! But be careful: this is actually a pointer to the current object!
      :.*: Incorrect!

.. mchoice:: print_2
   :multiple_answers:
   :answer_a: Change the name of the function to Dog::bark
   :answer_b: Remove the Dog parameter
   :answer_c: Operate on the current Dog object by using *this
   :answer_d: Declare the function inside of the Dog structure definition
   :correct: b,c,d
   :feedback_a: Incorrect! You don't need to rename the function unless you define it outside of the structure definition.
   :feedback_b: Correct! We no longer need to pass a Dog as an argument, since we are going to be invoking the function on a Dog object.
   :feedback_c: Correct! To get the current object, we need to dereference the this pointer using *.
   :feedback_d: Correct! Member functions are declared inside of structure definitions.

   We have a free-standing function called **dog_bark** which takes a **Dog** object as a parameter.  What step(s) do we need to take to convert ``dog_bark(const Dog& dog)`` to a member function of the ``Dog`` class?

.. parsonsprob:: print_3
   :numbered: left
   :adaptive:

   Create the ``Dog`` object with member functions ``bark`` and ``is_teacup_dog`` (if the weight of the dog is less than 4 pounds)  Write the functions
   in the same order they appear inside the structure.
   -----
   struct Dog {
   =====
    int age, weight;
    string breed;
   =====
    void bark();
    bool is_teacup_dog();
   =====
   };
   =====
   }                         #paired
   =====
   void Dog::bark() {
   =====
   void bark() {                         #paired
   =====
    cout << "RUFF!" << endl;
   }
   =====
   bool Dog::is_teacup_dog() {
   =====
   bool is_teacup_dog() {                          #paired
   =====
    Dog dog = *this;                          #distractor
   =====
    if (weight < 4) {
      return true;
    }
    return false;
   }
