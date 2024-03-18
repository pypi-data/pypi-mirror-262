Structures as parameters
------------------------

You can pass structures as parameters in the usual way. For example,

::

   void printPoint (Point p) {
     cout << "(" << p.x << ", " << p.y << ")" << endl;
   }

``printPoint`` takes a point as an argument and outputs it in the
standard format. If you call ``printPoint (blank)``, it will output
``(3, 4)``.

.. activecode:: structures_parameters_AC_1
  :language: cpp
  :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

  The active code below uses the ``printPoint`` function. Run the code to
  see the output!
  ~~~~
  #include <iostream>
  using namespace std;

  struct Point {
      double x, y;
  };

  void printPoint (Point p) {
      cout << "(" << p.x << ", " << p.y << ")" << endl;
  }

  int main() {
      Point blank = { 3.0, 4.0 };
      printPoint (blank);
  }

As a second example, we can rewrite the ``distance`` function from
:numref:`distance` so that it takes two ``Point``\ s as
parameters instead of four ``double``\ s.

::

   double distance (Point p1, Point p2) {
     double dx = p2.x - p1.x;
     double dy = p2.y - p1.y;
     return sqrt (dx*dx + dy*dy);
   }
   
.. activecode:: structures_parameters_AC_2
  :language: cpp
  :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

  The active code below uses the updated version of the ``distance`` function.
  Feel free to modify the code!
  ~~~~
  #include <iostream>
  #include <cmath>
  using namespace std;

  struct Point {
      double x, y;
  };

  double distance (Point p1, Point p2) {
      double dx = p2.x - p1.x;
      double dy = p2.y - p1.y;
      return sqrt (dx*dx + dy*dy);
  }

  int main() {
      Point origin = { 0.0, 0.0 };
      Point point = { 3.0, 4.0 };
      cout << "The distance from the point to the origin is " << distance (origin, point) << endl;
  }

.. mchoice:: structures_parameters_1
   :practice: T

   What will print?

   .. code-block:: cpp

      struct Coordinate {
        int x, y;
      };

      void printOppositeCoordinate (Coordinate p) {
        cout << "(" << -p.y << ", " << -p.x << ")" << endl;
      }

      int main() {
        Coordinate coord = { 2, 7 };
        printOppositeCoordinate (coord);
      }

   - ``(-2, -7)``

     - Take a close look at the printOppositeCoordinate function.

   - ``(2.0, 7.0)``

     - Take a close look at the printOppositeCoordinate function.

   - ``(-7, -2)``

     + Yes, this is the correct output.

   - ``(-7.0, -2.0)``

     - Take a close look at the Coordinate struct.


.. parsonsprob:: structures_parameters_2
   :numbered: left
   :adaptive:

   Construct a function that takes in three Point structures and prints the average of the x coordinates and the average of the y coordinates as a coordinate. Find the x average before the y average.
   -----
   void printAveragePoint(Point p1, Point p2, Point p3) {
   =====
    double avgX = (p1.x + p2.x + p3.x)/3;
   =====
    double avgY = (p1.y + p2.y + p3.y)/3;
   =====
    double avgY = (y.p1 + y.p2 + y.p3)/3; #distractor
   =====
    cout << "(" << avgX << "," << avgY << ")";
   =====
    cout << "(" << "avgX" << "," << "avgY" << ")"; #distractor
   =====
   }

