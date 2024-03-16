One last example
----------------

The final example we’ll look at is ``addTime``:

::

   Time addTime2 (const Time& t1, const Time& t2) {
     double seconds = convertToSeconds (t1) + convertToSeconds (t2);
     return makeTime (seconds);
   }

We have to make several changes to this function, including:

#. Change the name from ``addTime`` to ``Time::add``.

#. Replace the first parameter with an implicit parameter, which should
   be declared ``const``.

#. Replace the use of ``makeTime`` with a constructor invocation.

Here’s the result:

::

   Time Time::add (const Time& t2) const {
     double seconds = convertToSeconds () + t2.convertToSeconds ();
     Time time (seconds);
     return time;
   }

The first time we invoke ``convertToSeconds``, there is no apparent
object! Inside a member function, the compiler assumes that we want to
invoke the function on the current object. Thus, the first invocation
acts on ``this``; the second invocation acts on ``t2``.

The next line of the function invokes the constructor that takes a
single ``double`` as a parameter; the last line returns the resulting
object.

.. activecode:: one_last_example_AC_1
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   Feel free to try out the ``add`` function in the active code below!
   ~~~~
   #include <iostream>
   using namespace std;

   struct Time {
       int hour, minute;
       double second;
       Time (double secs);
       Time (int h, int m, double s);
       bool after (const Time& time2) const;
       Time add (const Time& t2) const;
       double convertToSeconds () const;
       void print ();
   };

   int main() {
       Time t1 (9, 20, 0.0); cout << "t1 = "; t1.print(); cout << endl;
       Time t2 (7, 30, 0.0); cout << "t2 = "; t2.print(); cout << endl;
       Time t3 = t1.add(t2);
       cout << "Time t1 + Time t2 = "; t3.print(); cout << endl;
   }

   ====

   Time::Time (double secs) {
     hour = int (secs / 3600.0);
     secs -= hour * 3600.0;
     minute = int (secs / 60.0);
     secs -= minute * 60.0;
     second = secs;
   }

   Time::Time (int h, int m, double s) {
     hour = h; minute = m; second = s;
   }

   void Time::print () {
     cout << hour << ":" << minute << ":" << second;
   }

   double Time::convertToSeconds () const {
     int minutes = hour * 60 + minute;
     double seconds = minutes * 60 + second;
     return seconds;
   }

   Time Time::add (const Time &t2) const {
     double seconds = convertToSeconds () + t2.convertToSeconds ();
     Time time (seconds);
     return time;
   }

   bool Time::after (const Time& time2) const {
     if (hour > time2.hour) return true;
     if (hour < time2.hour) return false;

     if (minute > time2.minute) return true;
     if (minute < time2.minute) return false;

     if (second > time2.second) return true;
     return false;
   }

.. fillintheblank:: one_last_example_1

    Inside a member function, the compiler assumes that we want to invoke the function
    on the __________ object.

    - :([Cc]urrent|CURRENT): Correct!
      :.*: Incorrect! It may help you to read the section again!

.. fillintheblank:: one_last_example_2

    We have previously initialized t1 and t2 using constructors ``Time t1 (8, 30, 45.0)``
    and ``Time t2 (1, 50, 13.0)``. What should be returned by ``t1.add(t2)``?

    - :(10:20:58): Correct!
      :.*: Incorrect! It will help you to modify the code above!

