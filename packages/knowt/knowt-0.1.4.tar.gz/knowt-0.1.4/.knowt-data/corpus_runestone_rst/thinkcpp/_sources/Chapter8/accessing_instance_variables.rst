Accessing instance variables
----------------------------

You can read the values of an instance variable using the same syntax we
used to write them:

::

       int x = blank.x;

The expression ``blank.x`` means “go to the object named ``blank`` and
get the value of ``x``.” In this case we assign that value to a local
variable named ``x``. Notice that there is no conflict between the local
variable named ``x`` and the instance variable named ``x``. The purpose
of dot notation is to identify *which* variable you are referring to
unambiguously.

You can use dot notation as part of any C++ expression, so the following
are legal.

::

     cout << blank.x << ", " << blank.y << endl;
     double distance = sqrt(blank.x * blank.x + blank.y * blank.y);

.. activecode:: accessing_instance_variables_AC_1
  :language: cpp
  :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

  In the active code below, we access the instance variables of ``Point`` object
  ``black`` using dot notation and output their values. Next, we output the
  distance from the origin.
  ~~~~
  #include <iostream>
  #include <cmath>
  using namespace std;

  struct Point {
      double x, y;
  };

  int main() {
      Point blank;
      blank.x = 3.0;
      blank.y = 4.0;
      cout << blank.x << ", " << blank.y << endl;
      double distance = sqrt(blank.x * blank.x + blank.y * blank.y);
      cout << distance << endl;
  }

.. mchoice:: accessing_instance_variables_1
   :practice: T

   In ``string x = thing.cube;``, what is the object and what is the instance variable we are reading the value of?

   - ``string`` is the instance variable, ``cube`` is the object

     - ``string`` is a data type.

   - ``x`` is the instance variable, ``thing`` is the object

     - ``x`` is the local variable.

   - ``thing`` is the instance variable, ``cube`` is the object
     
     - Consider the placement of ``thing`` -- it is before the ``.``


   - ``cube`` is the instance variable, ``thing`` is the object

     + Yes, we access the instance variable ``cube`` of the object ``thing`` using the dot operator.

   - ``cube`` is the instance variable, ``string`` is the object

     - ``string`` is a data type.


.. mchoice:: accessing_instance_variables_2
   :practice: T

   What will print?

   .. code-block:: cpp

      struct Blue {
        double x, y;
      };

      int main() {
        Blue blank;
        blank.x = 7.0;
        blank.y = 2.0;
        cout << blank.y << blank.x;
        double distance = blank.x * blank.x + blank.y * blank.y;
        cout << distance << endl;
      }


   - ``2.0 7.0 53``

     - Spaces need to be printed out like any other output.

   - ``2753``

     + There are no spaces in the correct output.

   - ``7253``

     - The order in which the variables are printed out do not need to match the order in which they are declared.

   - ``7.02.053``

     - The order in which the variables are printed out do not need to match the order in which they are declared.


.. mchoice:: accessing_instance_variables_3
   :practice: T

   You want to go to the object named ``circle`` and get the integer value of ``y``, then assign it to the local variable ``x``. How would you do that?

   - ``int y = circle.x();``

     -  No parentheses are needed.

   - ``int circle = x.y;``

     - You should be assigning to the local variable ``x``.

   - ``int y = circle.x;``

     - You should be assigning to the local variable ``x``.

   - ``int x = circle.y;``

     + This is the correct way to assign the value of ``y`` to ``x``.
