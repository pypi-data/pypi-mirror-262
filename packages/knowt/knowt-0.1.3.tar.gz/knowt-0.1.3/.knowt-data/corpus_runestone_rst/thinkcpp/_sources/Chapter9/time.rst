
.. _time:

Time
----

As a second example of a user-defined structure, we will define a type
called ``Time``, which is used to record the time of day. The various
pieces of information that form a time are the hour, minute and second,
so these will be the instance variables of the structure.

The first step is to decide what type each instance variable should be.
It seems clear that ``hour`` and ``minute`` should be integers. Just to
keep things interesting, let’s make ``second`` a ``double``, so we can
record fractions of a second.

.. activecode:: time_AC_1
  :language: cpp
  :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

  The active code below shows what the structure definition looks like.
  We can create a ``Time`` object in the usual way.
  ~~~~
  #include <iostream>
  using namespace std;

  struct Time {
      int hour, minute;
      double second;
  };

  int main() {
      Time time = { 11, 59, 3.14159 };
      cout << time.hour << ":" << time.minute << ":" << time.second;
  }

The state diagram for this object looks like this:

.. figure:: Images/9.1stackdiagram.png
   :scale: 50%
   :align: center
   :alt: image

.. index::
   single: instance

The word **instance** is sometimes used when we talk about objects,
because every object is an instance (or example) of some type. The
reason that instance variables are so-named is that every instance of a
type has a copy of the instance variables for that type.


.. mchoice:: time_1
   :answer_a: sandwich, coffee, pastry
   :answer_b: dollar, cents
   :answer_c: Price, struct
   :correct: a
   :feedback_a: Correct!
   :feedback_b: Try again. We are looking for variable names not instances of a structure.
   :feedback_c: Try again. ``struct`` and ``Price`` are not variables.

   Which of the following words are variables of type ``Price``?

   .. code-block:: cpp

      struct Price {
        int dollar, cents;
      };

      int main() {
        Price sandwich = { 3, 45 };
        Price coffee = { 2, 50 };
        Price pastry = { 2, 0 };
      }

.. mchoice:: time_2
   :answer_a: sandwich, coffee, pastry
   :answer_b: dollar, cents
   :answer_c: Price, struct
   :correct: b
   :feedback_a: These are variables of type Price.
   :feedback_b: Correct!
   :feedback_c: Try again. ``struct`` and ``Price`` are not variables.

   Which of the following words are instance variables of the ``Price`` structure?

   .. code-block:: cpp

      struct Price {
        int dollar, cents;
      };

      int main() {
        Price sandwich = { 3, 45 };
        Price coffee = { 2, 50 };
        Price pastry = { 2, 0 };
      }

.. mchoice:: time_3
   :answer_a: sandwich, coffee, pastry
   :answer_b: dollar, cents
   :answer_c: Price
   :correct: c
   :feedback_a: These are variables of type Price.
   :feedback_b: These are instance variables of the Price structure.
   :feedback_c: Correct!

   Which of the following words are a user-defined structure?

   .. code-block:: cpp

      struct Price {
        int dollar, cents;
      };

      int main() {
        Price sandwich = { 3, 45 };
        Price coffee = { 2, 50 };
        Price pastry = { 2, 0 };
      }

.. activecode:: time_AC_2
  :language: cpp
  :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

  Try writing the ``printTime`` function in the commented section
  of the active code below. ``printTime`` should print out the time
  in the HOUR:MINUTE:SECONDS format. If you get stuck, you can reveal the extra problem
  at the end for help.
  ~~~~
  #include <iostream>
  using namespace std;

  struct Time {
      int hour, minute;
      double second;
  };

  void printTime(Time& time) {
      // ``printTime`` should print out the time in the
      // HOUR:MINUTE:SECONDS format. Write your implementation here.
  }

  int main() {
      Time time = { 11, 59, 3.14159 };

      // Should output "11:59:3.14159"
      printTime(time);
  }

.. reveal:: 9_1_1
   :showtitle: Reveal Problem
   :hidetitle: Hide Problem

   .. parsonsprob:: time_4
      :numbered: left
      :adaptive:
   
      Let's write the code for the ``printTime`` function. ``printTime``
      should print out the time in the HOUR:MINUTE:SECONDS format.
      -----
      void printTime(Time& time) {
      =====
      Time printTime(Time& time) {                         #paired
      =====
         cout << time.hour << ":" << time.minute << ":" << time.second;
      =====
         cout << hour << ":" << minute << ":" << second;                        #paired
      =====
      }

