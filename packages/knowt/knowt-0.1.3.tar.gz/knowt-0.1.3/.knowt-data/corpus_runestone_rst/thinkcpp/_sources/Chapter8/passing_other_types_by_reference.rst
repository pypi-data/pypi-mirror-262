Passing other types by reference
--------------------------------

It’s not just structures that can be passed by reference. All the other
types we’ve seen can, too. For example, to swap two integers, we could
write something like:

::

   void swap (int& x, int& y) {
     int temp = x;
     x = y;
     y = temp;
   }

We would call this function in the usual way:

::

     int i = 7;
     int j = 9;
     swap (i, j);
     cout << i << j << endl;

The output of this program is ``97``. Draw a stack diagram for this
program to convince yourself this is true. If the parameters ``x`` and
``y`` were declared as regular parameters (without the ``&``\ s),
``swap`` would not work. It would modify ``x`` and ``y`` and have no
effect on ``i`` and ``j``.

.. activecode:: pass_others_reference_AC_1
  :language: cpp
  :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

  The active code below uses the ``swap`` function. Run the active code
  for the output!
  ~~~~
  #include <iostream>
  using namespace std;

  void swap (int& x, int& y) {
      int temp = x;
      x = y;
      y = temp;
  }

  int main() {
      int i = 7;
      int j = 9;
      swap (i, j);
      cout << i << j << endl;
  }

When people start passing things like integers by reference, they often
try to use an expression as a reference argument. For example:

::

     int i = 7;
     int j = 9;
     swap (i, j + 1);         // WRONG!!

This is not legal because the expression ``j+1`` is not a variable—it
does not occupy a location that the reference can refer to. It is a
little tricky to figure out exactly what kinds of expressions can be
passed by reference. For now a good rule of thumb is that reference
arguments have to be variables.

.. mchoice:: pass_others_reference_1
   :practice: T

   Which of the parameters in the following code block are pass-by-reference?

   .. code-block:: cpp

      void swap (int& x, int& y) {
        int temp = x;
        x = y;
        y = temp;
      }

      void add (int& z, int q) {
        z = z + y;
      }

      int multiply (int a, int b) {
        int total = a * b;
        return total;
      }

   - ``x``, ``y``, ``z``

     + Correct!

   - ``x``, ``y``, ``z``, ``q``

     - Pay attention to the placement of the ``&``

   - ``a``, ``b``

     - Pay attention to the placement of the ``&``


.. parsonsprob:: pass_others_reference_2
   :numbered: left
   :adaptive:

   Create a function called ``addNum`` that takes two parameters, an integer ``x`` and an integer ``y``. The function should add ``y`` to ``x``, then print ``x``. The variable ``x`` should be modified, while the variable ``y`` should not.
   -----
   void addNum(int& x, int y) {
   =====
   void addNum(int x, int y) { #distractor
   =====
   void addNum(int& x, int& y) { #distractor
   =====
      x = x + y;
   =====
      y = x + y; #distractor
   =====
      cout << x;
   =====
      return x; #distractor
   =====
   }

