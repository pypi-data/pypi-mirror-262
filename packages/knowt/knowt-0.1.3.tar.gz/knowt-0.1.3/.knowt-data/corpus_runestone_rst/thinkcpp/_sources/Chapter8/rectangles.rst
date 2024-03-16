Rectangles
----------

Now let’s say that we want to create a structure to represent a
rectangle. The question is, what information do I have to provide in
order to specify a rectangle? To keep things simple let’s assume that
the rectangle will be oriented vertically or horizontally, never at an
angle.

There are a few possibilities: I could specify the center of the
rectangle (two coordinates) and its size (width and height), or I could
specify one of the corners and the size, or I could specify two opposing
corners.

The most common choice in existing programs is to specify the upper left
corner of the rectangle and the size. To do that in C++, we will define
a structure that contains a ``Point`` and two doubles.

::

   struct Rectangle {
     Point corner;
     double width, height;
   };

Notice that one structure can contain another. In fact, this sort of
thing is quite common. Of course, this means that in order to create a
``Rectangle``, we have to create a ``Point`` first:

::

     Point corner = { 0.0, 0.0 };
     Rectangle box = { corner, 100.0, 200.0 };

This code creates a new ``Rectangle`` structure and initializes the
instance variables. The figure shows the effect of this assignment.

.. figure:: Images/8.8stackdiagram.png
   :scale: 50%
   :align: center
   :alt: image

We can access the ``width`` and ``height`` in the usual way:

::

     box.width += 50.0;
     cout << box.height << endl;

In order to access the instance variables of ``corner``, we can use a
temporary variable:

::

     Point temp = box.corner;
     double x = temp.x;

Alternatively, we can compose the two statements:

::

     double x = box.corner.x;

It makes the most sense to read this statement from right to left:
“Extract ``x`` from the ``corner`` of the ``box``, and assign it to the
local variable ``x``.”

While we are on the subject of composition, I should point out that you
can, in fact, create the ``Point`` and the ``Rectangle`` at the same
time:

::

     Rectangle box = { { 0.0, 0.0 }, 100.0, 200.0 };

.. index::
   pair: structure; nested structure

The innermost squiggly braces are the coordinates of the corner point;
together they make up the first of the three values that go into the new
``Rectangle``. This statement is an example of **nested structure**.

.. activecode:: rectangles_AC_1
  :language: cpp
  :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

  The active code below uses the ``Rectangle`` structure. Feel free to
  modify the code and experiment around!
  ~~~~
  #include <iostream>
  using namespace std;

  struct Point {
      double x, y;
  };

  struct Rectangle {
      Point corner;
      double width, height;
  };

  int main() {
      Rectangle box = { { 0.0, 0.0 }, 100.0, 200.0 };
      box.width += 50.0;
      cout << box.height << endl;
      cout << box.width << endl;
  }


.. mchoice:: rectangles_1
   :practice: T

   How can you combine these two statements into one?

   .. code-block:: cpp

      Point temp = box.corner;
      double y = temp.y;


   - ``double y = corner.box.y;``

     - Try again.

   - ``double y = box.corner.y;``

     + Correct!

   - ``double y = corner.y;``

     - Try again.

   - ``double y = box.y;``

     - Try again.


.. clickablearea:: rectangles_2
    :question: Click on the legal ways to create a Point and Rectangle structure, assuming that the Point and Rectangle structures are declared above the main function in the same way as in the active code above.
    :iscode:
    :feedback: Re-read the text above and try again.

    :click-incorrect:def main() {:endclick:
        :click-incorrect:Point corner = ( 0.0, 0.0 );:endclick:
        :click-incorrect:Rectangle box = { ( 0.0, 0.0 ), 100.0, 200.0 }:endclick:
        :click-correct:Rectangle box = { { 0.0, 0.0 }, 100.0, 200.0 };:endclick:
        :click-correct:Point corner = { 0.0, 0.0 };:endclick:
        :click-correct:Rectangle box = { corner, 100.0, 200.0 };:endclick:
    }

