Activecode Exercises
----------------------

Answer the following **Activecode** questions to assess what you have learned in this chapter.

.. tabbed:: mucp_14_1_ac

    .. tab:: Question

        .. activecode:: mucp_14_1_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the class definition for ``Circle``. ``Circle`` should have its
            radius stored in a private member variable. Also write the constructor 
            for ``Circle``, which takes a radius as a parameter, in addition to the
            public member function ``calculateArea``, which returns the area of 
            the ``Circle``. Make sure to include the ``private`` and ``public`` keywords!
            Use 3.14 for the value of pi. 
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_14_11_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to wrte the class definition and constructor for ``Circle``.
            ~~~~
            #include <iostream>
            using namespace std;

            class Circle {   
                private:
                    double radius;
                public:
                    Circle (double r) { radius = r; }
                    double calculateArea () { return 3.14 * radius * radius; }
            };

.. tabbed:: mucp_14_2_ac

    .. tab:: Question

        .. activecode:: mucp_14_2_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Now that we have our ``Circle`` class, let's write some accessor
            functions! Write the ``Circle`` member functions ``getRadius`` 
            and ``setRadius``. It doesn't make sense for a ``Circle``'s
            radius to be negative, so in your ``setRadius`` function,
            output an error message if the given radius is negative.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_14_2_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the accessor functions for ``getRadius`` and ``setRadius``.
            ~~~~
            #include <iostream>
            using namespace std;

            class Circle {   
                private:
                    double radius;
                public:
                    Circle (double r) { radius = r; }
                    double calculateArea () { return 3.14 * radius * radius; }
                    double getRadius () {
                        return radius;
                    }
                    void setRadius (double r) {
                        if (r < 0) { cout << "Error! Cannot have a negative radius!" << endl; }
                        else { radius = r; }
                    }
            };

.. tabbed:: mucp_14_3_ac

    .. tab:: Question

        .. activecode:: mucp_14_3_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write a ``main``. In ``main``, create a ``Circle`` with radius 2.4
            and output the radius. Then change the radius to 3.6 and output
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_14_3_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the code.
            ~~~~
            #include <iostream>
            using namespace std;

            class Circle {   
                private:
                    double radius;
                public:
                    Circle (double r) { radius = r; }
                    double calculateArea () { return 3.14 * radius * radius; }
                    double getRadius () {
                        return radius;
                    }
                    void setRadius (double r) {
                        if (r < 0) { cout << "Error! Cannot have a negative radius!" << endl; }
                        else { radius = r; }
                    }
            };

            int main() {
                Circle c(2.4);
                cout << "Radius: " << c.getRadius () << endl;
                c.setRadius (3.6);
                cout << "New radius: " << c.getRadius () << endl;
            }

.. tabbed:: mucp_14_4_ac

    .. tab:: Question

        .. activecode:: mucp_14_4_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            A ``Rectangle`` can be constructed given only two points. First,
            write the class definition for ``Point``, which stores an x and 
            a y value in private member variables. Also write the default constructor, which
            sets x and y to 0, and a constructor that takes in an xVal and yVal. 
            In addition, write its accessor functions, 
            ``getX``, ``getY``, ``setX``, and ``setY``.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_14_4_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the code.
            ~~~~
            #include <iostream>
            using namespace std;

            class Point {   
                private:
                    double x, y;
                public:
                    Point () { x = 0; y = 0; }
                    Point (double xVal, double yVal) { x = xVal; y = yVal; }
                    double getX () { return x; }
                    double getY () { return y; }
                    void setX (double xVal) { x = xVal; }
                    void setY (double yVal) { y = yVal; }
            };

.. tabbed:: mucp_14_5_ac

    .. tab:: Question

        .. activecode:: mucp_14_5_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Now that we've defined the ``Point`` class, we can go back to
            writing the ``Rectangle`` class. ``Rectangle`` should store 
            it's upper-left and lower-right points as private member variables. 
            Write accessor functions for these variables after the constructor.
            It should also have length and height stored as public member variables.
            Also write a constructor that
            takes an upper-left point and a lower-right point as parameters. 
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer 

        .. activecode:: mucp_14_5_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the ``Rectangle`` class.
            ~~~~
            #include <iostream>
            using namespace std;

            class Point {   
                private:
                    double x, y;
                public:
                    Point () { x = 0; y = 0; }
                    Point (double xVal, double yVal) { x = xVal; y = yVal; }
                    double getX () { return x; }
                    double getY () { return y; }
                    void setX (double xVal) { x = xVal; }
                    void setY (double yVal) { y = yVal; }
            };

            class Rectangle {   
                private:
                    Point upperLeft, lowerRight;
                public:
                    double length, height;
                    Rectangle (Point upLeft, Point lowRight) { upperLeft = upLeft; lowerRight = lowRight; }
                    Point getUpperLeft () { return upperLeft; }
                    Point getLowerRight () { return lowerRight; }
                    void setUpperLeft (Point p) { upperLeft = p; }
                    void setLowerRight (Point p) { lowerRight = p; }
            };

.. tabbed:: mucp_14_6_ac

    .. tab:: Question

        .. activecode:: mucp_14_6_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write the ``Rectangle`` member function ``calculateSides``, which finds
            the length and height of the rectangle using the stored ``Point``s.
            Afterwards, write the ``Rectangle`` member function ``calculateArea``,
            which returns the area of the rectangle.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE

    
    .. tab:: Answer

        .. activecode:: mucp_14_6_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the ``calculateSides`` and ``calculateArea`` member functions.
            ~~~~
            #include <iostream>
            using namespace std;

            class Point {   
                private:
                    double x, y;
                public:
                    Point () { x = 0; y = 0; }
                    Point (double xVal, double yVal) { x = xVal; y = yVal; }
                    double getX () { return x; }
                    double getY () { return y; }
                    void setX (double xVal) { x = xVal; }
                    void setY (double yVal) { y = yVal; }
            };

            class Rectangle {   
                private:
                    Point upperLeft, lowerRight;
                public:
                    double length, height;
                    Rectangle (Point upLeft, Point lowRight) { upperLeft = upLeft; lowerRight = lowRight; }
                    Point getUpperLeft () { return upperLeft; }
                    Point getLowerRight () { return lowerRight; }
                    void setUpperLeft (Point p) { upperLeft = p; }
                    void setLowerRight (Point p) { lowerRight = p; }
            };

            void Rectangle::calculateSides () {
                
            double Rectangle::calculateSides () {
                length = getLowerRight().getX() - getUpperLeft().getX();
                height = getUpperLeft().getY() - getLowerRight().getY();
            }

            double Rectangle::calculateArea () {
                return length * height;
            }

.. tabbed:: mucp_14_7_ac

    .. tab:: Question

        .. activecode:: mucp_14_7_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write a ``main`` In ``main``, create a ``Rectangle`` with corners
            at (2.5, 7.5) and (8, 1.5). Print out the length and height, calculate the area,
            and print out the area. Then change the upperLeft corner to be at (4.2, 10.7) and 
            print out the new area.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE

    .. tab:: Answer

        .. activecode:: mucp_14_7_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to create this ``Rectangle``.
            ~~~~
            #include <iostream>
            using namespace std;

            class Point {   
                private:
                    double x, y;
                public:
                    Point () { x = 0; y = 0; }
                    Point (double xVal, double yVal) { x = xVal; y = yVal; }
                    double getX () { return x; }
                    double getY () { return y; }
                    void setX (double xVal) { x = xVal; }
                    void setY (double yVal) { y = yVal; }
            };

            class Rectangle {   
                private:
                    Point upperLeft, lowerRight;
                public:
                    double length, height;
                    Rectangle (Point upLeft, Point lowRight) { upperLeft = upLeft; lowerRight = lowRight; }
                    Point getUpperLeft () { return upperLeft; }
                    Point getLowerRight () { return lowerRight; }
                    void setUpperLeft (Point p) { upperLeft = p; }
                    void setLowerRight (Point p) { lowerRight = p; }
            };

            void Rectangle::calculateSides () {
                
            double Rectangle::calculateSides () {
                length = getLowerRight().getX() - getUpperLeft().getX();
                height = getUpperLeft().getY() - getLowerRight().getY();
            }

            double Rectangle::calculateArea () {
                return length * height;
            }

            int main() {
                Point p1(2.5, 7.5);
                Point p2(8, 1.5);
                Rectangle r(p1, p2);
                r.calculateSides();
                cout << "Length: " << r.length << ", Height: " << r.height << endl;
                cout << "Area: " << r.calculateArea() << endl;
                Point p3(4.2, 10.7);
                r.setUpperLeft(p3);
                r.calculateSides();
                cout << "New area: " << r.calculateArea() << endl;
            }

.. tabbed:: mucp_14_8_ac

    .. tab:: Question

        .. activecode:: mucp_14_8_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the ``Date`` class. ``Date`` stores information 
            about the day, month, and year in private variables, in addition to a ``vector``
            of the number of days in each month. Write accessor functions
            for each variable, keeping in mind the valid values each variable can take. 
            In addition, write the default constructor, which initializes 
            the date to January 1, 2000. Write another constructor which takes in a day,
            month, and year in that order.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_14_8_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the ``Date`` class and addtional constructors.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            class Date {   
                private:
                    int day, month, year;
                    vector<int> daysInMonth = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
                public:
                    Date () { day = 1; month = 1; year = 2000; }
                    Date (int d, int m, int y) { day = d; month = m; year = y; }
                    int getDay () { return day; }
                    int getMonth () { return month; }
                    int getYear () { return year; }
                    void setDay (int d) { if (d > 0 && d < 32) day = d; }
                    void setMonth (int m) { if (m > 0 && m < 13) month = m; }
                    void setYear (int y) { year = y; }
            };

.. tabbed:: mucp_14_9_ac

    .. tab:: Question

        .. activecode:: mucp_14_9_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the ``Date`` member function, ``printDate``,
            which prints the date out in the following format: month/day/year CE/BCE
            depending on whether the year is negative or not.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_14_9_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the ``printDate`` member function.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            class Date {   
                private:
                    int day, month, year;
                    vector<int> daysInMonth = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
                public:
                    Date () { day = 1; month = 1; year = 2000; }
                    Date (int d, int m, int y) { day = d; month = m; year = y; }
                    int getDay () { return day; }
                    int getMonth () { return month; }
                    int getYear () { return year; }
                    void setDay (int d) { if (d > 0 && d < 32) day = d; }
                    void setMonth (int m) { if (m > 0 && m < 13) month = m; }
                    void setYear (int y) { year = y; }
            };

            void Date::printDate () {
                if (getYear() < 0) {
                    cout << getMonth() << "/" << getDay() << "/" << -getYear() << " BCE" << endl;
                }
                else {
                    cout << getMonth() << "/" << getDay() << "/" << getYear() << " CE" << endl;
                }
            }

.. tabbed:: mucp_14_10_ac

    .. tab:: Question

        .. activecode:: mucp_14_10_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Write the ``Date`` member function ``isLeapYear``, which returns true if 
            the year is a leap year. Then write the ``Date`` member function ``lastDayInMonth``,
            which returns the last day in the ``Date``'s month.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_14_10_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is onne way to write the ``isLeapYear`` and ``lastDayInMonth`` member functions.
            ~~~~
            #include <iostream> 
            #include <vector>
            using namespace std;

            class Date {   
                private:
                    int day, month, year;
                    vector<int> daysInMonth = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
                public:
                    Date () { day = 1; month = 1; year = 2000; }
                    Date (int d, int m, int y) { day = d; month = m; year = y; }
                    int getDay () { return day; }
                    int getMonth () { return month; }
                    int getYear () { return year; }
                    void setDay (int d) { if (d > 0 && d < 32) day = d; }
                    void setMonth (int m) { if (m > 0 && m < 13) month = m; }
                    void setYear (int y) { year = y; }
            };

            bool Date::isLeapYear () {
                if (getYear() % 4 != 0) { return false; }
                else if (getYear() % 100 != 0) { return true; }
                else if (getYear() % 400 != 0) { return false; }
                else { return true; }
            }
            
            int Date::lastDayInMonth () {
                if (isLeapYear() && getMonth() == 2) {
                    return daysInMonth[getMonth() - 1] + 1;
                else {
                    return daysInMonth[getMonth() - 1];
                }
            }