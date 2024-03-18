Mixed Up Code Practice
----------------------

.. parsonsprob:: mucp_14_1
   :numbered: left
   :adaptive:
   :noindent:
   :practice: T

   Let's write the class definition for ``Circle``. ``Circle`` should have its
   radius stored in a private member variable. Also write the constructor 
   for ``Circle``, which takes a radius as a parameter, in addition to the
   public member function ``calculateArea``, which returns the area of 
   the ``Circle``. Make sure to include the ``private`` and ``public`` keywords!
   Use 3.14 for the value of pi. Put the necessary
   blocks of code in the correct order.
   -----
   class Circle {   
   =====
   struct Circle {  #distractor
   =====
      private:
   =====
      private {  #distractor
   =====
      }  #distractor
   =====
         double radius;
   =====
      public:
   =====
         Circle (double r) { radius = r; }
   =====
         Circle (int r) { radius = r; }  #distractor
   =====
         double calculateArea () { return 3.14 * radius * radius; }
   };

.. parsonsprob:: mucp_14_2
   :numbered: left
   :adaptive:
   :noindent:

   Now that we have our ``Circle`` class, let's write some accessor
   functions! Write the ``Circle`` member functions ``getRadius`` 
   and ``setRadius``. It doesn't make sense for a ``Circle``'s
   radius to be negative, so in your ``setRadius`` function,
   output an error message if the given radius is negative.
   Put the necessary blocks of code in the correct order.
   -----
   class Circle {   
      private:
         double radius;
      public:
         Circle (double r) { radius = r; }
         double calculateArea () { return 3.14 * radius * radius; }
   =====
         double getRadius () {
   =====
         void getRadius () {  #distractor
   =====
            return radius;
   =====
         }
   =====
         void setRadius (double r) {
   =====
         double setRadius (double r) {  #distractor
   =====
            if (r < 0) { cout << "Error! Cannot have a negative radius!" << endl; }
   =====
            else { radius = r; }
   =====
         }
   =====
   };

.. parsonsprob:: mucp_14_3
   :numbered: left
   :adaptive:
   :noindent:

   Write a ``main``. In ``main``, create a ``Circle`` with radius 2.4
   and output the radius. Then change the radius to 3.6 and output
   the new radius. Put the necessary blocks of code in the correct order.
   -----
   int main() {
   =====
      Circle c(2.4);
   =====
      Circle c;  #distractor
   =====
      c.radius = 2.4;  #distractor
   =====
      cout << "Radius: " << c.getRadius () << endl;
   =====
      cout << "Radius: " << c.radius << endl;  #distractor
   =====
      c.radius = 3.6;  #distractor
   =====
      s.setRadius (3.6);
   =====
      cout << "New radius: " << c.getRadius () << endl;
   =====
      cout << "New radius: " << c.radius << endl;  #distractor
   =====
   }

.. parsonsprob:: mucp_14_4
   :numbered: left
   :adaptive:

   A ``Rectangle`` can be constructed given only two points. First,
   write the class definition for ``Point``, which stores an x and 
   a y value in private member variables. Also write the default constructor, which
   sets x and y to 0, and a constructor that takes in an xVal and yVal. 
   In addition, write its accessor functions, 
   ``getX``, ``getY``, ``setX``, and ``setY``.
   Put the necessary blocks of code in the correct order.
   -----
   class Point {   
   =====
      private:
   =====
         double x, y;
   =====
      public:
   =====
         Point () { x = 0; y = 0; }
   =====
         Point (double xVal, double yVal) { x = xVal; y = yVal; }
   =====
         double getX () { return x; }
   =====
         double getY () { return y; }
   =====
         void setX (double xVal) { x = xVal; }
   =====
         void setY (double yVal) { y = yVal; }
   =====
   };

.. parsonsprob:: mucp_14_5
   :numbered: left
   :adaptive:

   Now that we've defined the ``Point`` class, we can go back to
   writing the ``Rectangle`` class. ``Rectangle`` should store 
   it's upper-left and lower-right points as private member variables. 
   Write accessor functions for these variables after the constructor.
   It should also have length and height stored as public member variables.
   Also write a constructor that
   takes an upper-left point and a lower-right point as parameters. 
   -----
   class Rectangle {   
   =====
      private:
   =====
         Point upperLeft, lowerRight;
   =====
      public:
   =====
         double length, height;
   =====
         Rectangle (Point upLeft, Point lowRight) { upperLeft = upLeft; lowerRight = lowRight; }
   =====
         Point getUpperLeft () { return upperLeft; }
   =====
         Point getLowerRight () { return lowerRight; }
   =====
         void setUpperLeft (Point p) { upperLeft = p; }
   =====
         void setLowerRight (Point p) { lowerRight = p; }
   =====
   };

.. parsonsprob:: mucp_14_6
   :numbered: left
   :adaptive:

   Write the ``Rectangle`` member function ``calculateSides``, which finds
   the length and height of the rectangle using the stored ``Point``s.
   Afterwards, write the ``Rectangle`` member function ``calculateArea``,
   which returns the area of the rectangle.
   -----
   void Rectangle::calculateSides () {
   =====
   double Rectangle::calculateSides () {
   =====
      length = getLowerRight().getX() - getUpperLeft().getX();
   =====
      height = getUpperLeft().getY() - getLowerRight().getY();
   =====
      length = lowerRight.x - upperLeft.x;  #distractor
   =====
      height = upperLeft.y - lowerRight.y;  #distractor
   =====
      return length;  #distractor
   =====
      return height;  #distractor
   =====
   }
   =====
   double Rectangle::calculateArea () {
   =====
      return length * height;
   =====
      return getLength() * getHeight();  #distractor
   =====
   }

.. parsonsprob:: mucp_14_7
   :numbered: left
   :adaptive:

   Write a ``main`` In ``main``, create a ``Rectangle`` with corners
   at (2.5, 7.5) and (8, 1.5). Print out the length and height, calculate the area,
   and print out the area. Then change the upperLeft corner to be at (4.2, 10.7) and 
   print out the new area.
   -----
   int main() {
   =====
      Point p1(2.5, 7.5);
   =====
      Point p2(8, 1.5);
   =====
      Rectangle r(p1, p2);
   =====
      Rectangle r(p2, p1);  #distractor
   =====
      r.calculateSides();
   =====
      cout << "Length: " << r.length << ", Height: " << r.height << endl;
   =====
      cout << "Length: " << r.getLength() << ", Height: " << r.getHeight() << endl;  #distractor
   =====
      cout << "Area: " << r.calculateArea() << endl;
   =====
      Point p3(4.2, 10.7);
   =====
      r.setUpperLeft(p3);
   =====
      r.upperLeft = p3;  #distractor
   =====
      r.calculateSides();
   =====
      cout << "New area: " << r.calculateArea() << endl;
   =====
   }

.. parsonsprob:: mucp_14_8
   :numbered: left
   :adaptive:

   Let's write the ``Date`` class. ``Date`` stores information 
   about the day, month, and year in private variables, in addition to a ``vector``
   of the number of days in each month. Write accessor functions
   for each variable, keeping in mind the valid values each variable can take. 
   In addition, write the default constructor, which initializes 
   the date to January 1, 2000. Write another constructor which takes in a day,
   month, and year in that order.
   -----
   class Date {   
   =====
      private:
   =====
         int day, month, year;
   =====
         vector<int> daysInMonth = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
   =====
      public:
   =====
         Date () { day = 1; month = 1; year = 2000; }
   =====
         Date () { day = 0; month = 0; year = 0; }  #distractor
   =====
         Date (int d, int m, int y) { day = d; month = m; year = y; }
   =====
         int getDay () { return day; }
   =====
         int getMonth () { return month; }
   =====
         int getYear () { return year; }
   =====
         void setDay (int d) { if (d > 0 && d < 32) day = d; }
   =====
         void setMonth (int m) { if (m > 0 && m < 13) month = m; }
   =====
         void setYear (int y) { year = y; }
   =====
         void setDay (int d) { if (d > 1 && d < 31) day = d; }  #distractor
   =====
         void setMonth (int m) { if (m >= 0 && m <= 12) month = m; }  #distractor
   =====
         void setYear (int y) { if (y >= 2000 && y < 3000) year = y; }  #distractor
   =====
   };

.. parsonsprob:: mucp_14_9
   :numbered: left
   :adaptive:

   Let's write the ``Date`` member function, ``printDate``,
   which prints the date out in the following format: month/day/year CE/BCE
   depending on whether the year is negative or not.
   -----
   void Date::printDate () {
   =====
      if (getYear() < 0) {
   =====
         cout << getMonth() << "/" << getDay() << "/" << -getYear() << " BCE" << endl;
   =====
         cout << month << "/" << day << "/" << year << " BCE" << endl;  #distractor
   =====
         cout << getMonth() << "/" << getDay() << "/" << getYear() << " BCE" << endl;  #distractor
   =====
      }
   =====
      else {
   =====
         cout << getMonth() << "/" << getDay() << "/" << getYear() << " CE" << endl;
   =====
      }
   =====
   }

.. parsonsprob:: mucp_14_10
   :numbered: left
   :adaptive:

   Write the ``Date`` member function ``isLeapYear``, which returns true if 
   the year is a leap year. Then write the ``Date`` member function ``lastDayInMonth``,
   which returns the last day in the ``Date``'s month.
   -----
   bool Date::isLeapYear () {
   =====
      if (getYear() % 4 != 0) { return false; }
   =====
      if (getYear() % 4 == 0) { return false; }  #distractor
   =====
      else if (getYear() % 100 != 0) { return true; }
   =====
      else if (getYear() % 400 != 0) { return false; }
   =====
      else { return true; }
   =====
      else { return false; }  #distractor
   =====
   }
   =====
   int Date::lastDayInMonth () {
   =====
      if (isLeapYear() && getMonth() == 2) {
   =====
      if (isLeapYear()) {  #distractor
   =====
         return daysInMonth[getMonth() - 1] + 1;
   =====
      else {
   =====
         return daysInMonth[getMonth() - 1];
   =====
         return daysInMonth[getMonth()];  #distractor
   =====
      }
   =====
   }