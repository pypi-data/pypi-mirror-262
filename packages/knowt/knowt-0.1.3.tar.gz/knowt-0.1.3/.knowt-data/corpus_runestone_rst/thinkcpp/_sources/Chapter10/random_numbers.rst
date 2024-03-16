.. _random:

Random numbers
--------------

[pseudorandom]

.. index::
   single: deterministic

Most computer programs do the same thing every time they are executed,
so they are said to be **deterministic**. Usually, determinism is a good
thing, since we expect the same calculation to yield the same result.
For some applications, though, we would like the computer to be
unpredictable. Games are an obvious example.

.. index::
   single: nondeterministic

Making a program truly **nondeterministic** turns out to be not so easy,
but there are ways to make it at least seem nondeterministic. One of
them is to generate pseudorandom numbers and use them to determine the
outcome of the program. Pseudorandom numbers are not truly random in the
mathematical sense, but for our purposes, they will do.

C++ provides a function called ``random`` that generates pseudorandom
numbers. It is declared in the header file ``cstdlib``, which contains a
variety of “standard library” functions, hence the name.

The return value from ``random`` is an integer between 0 and
``RAND_MAX``, where ``RAND_MAX`` is a large number (about 2 billion on
my computer) also defined in the header file. Each time you call
``random`` you get a different randomly-generated number. To see a
sample, run this loop:

.. activecode:: random_numbers_AC_1
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   Take a look at the active code below, which generates 4 random numbers.
   ~~~~
   #include <iostream>
   #include <cstdlib>
   using namespace std;

   int main () {
       for (int i = 0; i < 4; i++) {
           int x = random ();
           cout << x << endl;
       }
       return 0;
   }

On my machine I got the following output:

::

   1804289383
   846930886
   1681692777
   1714636915

You will probably get something similar, but different, on yours.

Of course, we don’t always want to work with gigantic integers. More
often we want to generate integers between 0 and some upper bound. A
simple way to do that is with the modulus operator. For example:

::

     int x = random ();
     int y = x % upperBound;

Since ``y`` is the remainder when ``x`` is divided by ``upperBound``,
the only possible values for ``y`` are between 0 and ``upperBound - 1``,
including both end points. 

.. note::
   Keep in mind, though, that ``y`` will never be equal to ``upperBound``.

.. activecode:: random_numbers_AC_2
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   The active code below generates random numbers between 1 and 7.
   ~~~~
   #include <iostream>
   #include <cstdlib>
   using namespace std;

   int main () {
       int upperBound = 8;
       cout << "Let's generate some random numbers between 0 and 7!" << endl;
       for (int i = 0; i < 10; i++) {
           int x = random ();
           int y = x % upperBound;
           cout << y << " ";
       }
   }

It is also frequently useful to generate random floating-point values. A
common way to do that is by dividing by ``RAND_MAX``. For example:

::

     int x = random ();
     double y = double(x) / RAND_MAX;

This code sets ``y`` to a random value between 0.0 and 1.0, including
both end points. As an exercise, you might want to think about how to
generate a random floating-point value in a given range; for example,
between 100.0 and 200.0.

.. activecode:: random_numbers_AC_3
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   The active code below generates random numbers between 0 and 1. Can you modify it 
   to generate random numbers between 100.0 and 200.0? If you're stuck you can 
   reveal the hint below!
   ~~~~
   #include <iostream>
   #include <cstdlib>
   using namespace std;

   int main () {
       cout << "Let's generate some random numbers between 0 and 1!" << endl;
       for (int i = 0; i < 10; i++) {
           int x = random ();
           double y = double(x) / RAND_MAX;
           cout << y << " ";
       }
   }

.. reveal:: 10_7_1
   :showtitle: Reveal Hint
   :hidetitle: Hide Hint

   The formula to generate random numbers between min and max is 
   min + (max - min) * double(x) / RAND_MAX. 

.. fillintheblank:: random_numbers_1

    Pseudorandom numbers are said to be __________, because different numbers are generated every time the program is executed.

    - :([Nn]ondeterministic|NONDETERMINISTIC): Correct!
      :([Dd]eterministic|DETERMINISTIC): Incorrect! Deterministic programs do the same thing every time they are executed.
      :.*: Incorrect!

.. mchoice:: random_numbers_2
   :answer_a: cstdlib
   :answer_b: random
   :answer_c: cmath
   :answer_d: iostream
   :correct: a
   :feedback_a: Correct!
   :feedback_b: Incorrect!
   :feedback_c: Incorrect!
   :feedback_d: Incorrect!

   What header file do we need to declare in order to use the ``random`` function?


.. mchoice:: random_numbers_3

    If we wanted to generate a random number between 0 and 12, and we have previously declared int ``int x = random ();``, what should be our next line of code?

    -   ``int y = x / 12``

        -   This returns some random number between 0 and x / 12, which is out of range.

    -   ``int y = x % 12``

        -   This returns a random number between 0 and 11.

    -   ``int y = x / 13``

        -   This returns some random number between 0 and x / 13, which is out of range.

    -   ``int y = x % 13``

        +   There are 13 numbers from 0 to 12 (the remainders of a division by 13).