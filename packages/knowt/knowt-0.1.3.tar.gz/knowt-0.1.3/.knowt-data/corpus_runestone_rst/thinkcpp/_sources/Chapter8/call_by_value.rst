Call by value
-------------
.. index::
   single: call by value

When you pass a structure as an argument, remember that the argument and
the parameter are not the same variable. Instead, there are two
variables (one in the caller and one in the callee) that have the same
value, at least initially. For example, when we call ``printPoint``, the stack diagram looks like this:

.. figure:: Images/8.6stackdiagram.png
   :scale: 50%
   :align: center
   :alt: image

If ``printPoint`` happened to change one of the instance variables of
``p``, it would have no effect on ``blank``. Of course, there is no
reason for ``printPoint`` to modify its parameter, so this isolation
between the two functions is appropriate.

This kind of parameter-passing is called “pass by value” because it is
the value of the structure (or other type) that gets passed to the
function.

.. activecode:: call_by_value_AC_1
  :language: cpp
  :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

  Take a look at the active code below. Notice from the output of the code below how the
  function ``addTwo`` changes the instance variables, but not on ``blank`` itself.
  ~~~~
  #include <iostream>
  using namespace std;

  struct Point {
      double x, y;
  };

  void addTwo (Point p) {
      cout << "(" << p.x + 2 << ", " << p.y + 2 << ")" << endl;
  }

  int main() {
      Point blank = { 3.0, 4.0 };
      addTwo (blank);
      cout << "(" << blank.x << ", " << blank.y << ")" << endl;
  }

.. mchoice:: call_by_value_1
   :practice: T

   What will print?

   .. code-block:: cpp

      int addTwo(int x) {
        cout << x << " ";
        x = x + 2;
        cout << x << " ";
        return x;
      }

      int main() {
        int num = 2;
        addTwo(num);
        cout << num << endl;
      }

   - ``2 4``

     - Take a look at exactly what is being outputted.

   - ``2 4 2``

     + Correct!

   - ``4 4 2``

     - Take a look at exactly what is being outputted.

   - ``2 4 4``

     - Remember the rules of pass by value.


.. mchoice:: call_by_value_2
   :practice: T

   What will print?

   .. code-block:: cpp

      struct Point {
        int x, y;
      };

      void timesTwo (Point p) {
        p.x = p.x * 2;
        p.y = p.y * 2;
        cout << "(" << p.x << ", " << p.y << ")";
      }

      int main() {
        Point blank = { 3, 4 };
        timesTwo (blank);
        cout << ", " << blank.x << endl;
      }

   - ``(6, 8), 3``

     + Correct!

   - ``(6, 8), 6``

     - Remember the rules of pass by value.

   - ``(68),3``

     - Take a look at exactly what is being outputted.

   - ``68, 6``

     - Take a look at exactly what is being outputted.

