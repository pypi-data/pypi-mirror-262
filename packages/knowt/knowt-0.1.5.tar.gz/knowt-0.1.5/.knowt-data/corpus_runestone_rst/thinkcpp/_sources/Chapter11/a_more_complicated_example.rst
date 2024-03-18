A more complicated example
--------------------------

Although the process of transforming functions into member functions is
mechanical, there are some oddities. For example, ``after`` operates on
two ``Time`` structures, not just one, and we can’t make both of them
implicit. Instead, we have to invoke the function on one of them and
pass the other as an argument.

Inside the function, we can refer to one of the them implicitly, but to
access the instance variables of the other we continue to use dot
notation.

::

   bool Time::after (const Time& time2) const {
     if (hour > time2.hour) return true;
     if (hour < time2.hour) return false;

     if (minute > time2.minute) return true;
     if (minute < time2.minute) return false;

     if (second > time2.second) return true;
     return false;
   }

To invoke this function:

::

     if (doneTime.after (currentTime)) {
       cout << "The bread will be done after it starts." << endl;
     }

You can almost read the invocation like English: “If the done-time is
after the current-time, then...”

.. activecode:: more_complicated_example_AC_1
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   The active code below is another practical example using the ``after`` function. 
   Feel free to modify the time that school gets out, and the time that the track meet starts, if you wish!
   ~~~~
   #include <iostream>
   using namespace std;

   struct Time {
       int hour, minute;
       double second;
       bool after (const Time& time2) const;
   };

   int main() {
       Time end_school = { 2, 20, 0.0 };
       Time track_meet = { 1, 30, 0.0 };
       if (track_meet.after (end_school)) {
           cout << "The track meet starts after school is dismissed." << endl;
       }
       else {
           cout << "The track meet starts before school gets out, athletes will get an early dismissal." << endl;
       }
   }

   ====

   bool Time::after (const Time& time2) const {
     if (hour > time2.hour) return true;
     if (hour < time2.hour) return false;

     if (minute > time2.minute) return true;
     if (minute < time2.minute) return false;

     if (second > time2.second) return true;
     return false;
   }

.. mchoice:: more_complicated_example_1
   :multiple_answers:
   :answer_a: There is only one Time parameter.
   :answer_b: The function operates on two Time objects.
   :answer_c: The function is invoked on time2.
   :answer_d: "hour" and "minute" refer to the hour and minute of the implicit Time object.
   :correct: b,d
   :feedback_a: Incorrect! There are actually two Time parameters, one of them is implicit.
   :feedback_b: Correct! There are two Time objects - the implicit one and time2.
   :feedback_c: Incorrect! The function is invoked on the implicit Time object.
   :feedback_d: Correct!

   Which is/are true about the ``Time::after`` member function?

.. mchoice:: more_complicated_example_2
   :answer_a: One
   :answer_b: Two
   :answer_c: Three
   :answer_d: Four
   :correct: c
   :feedback_a: Incorrect! There is One implicit structure.
   :feedback_b: Incorrect! Keep in mind there are 4 structures and 1 is implicit.
   :feedback_c: Correct!  There is One implicit structure, and three structures that need to be accessed with dot notation.
   :feedback_d: Incorrect! We shouldn't need to use dot notation for all of them!

   In a function that operates on **four** structures, how many of them are accessed with dot notation?

.. parsonsprob:: more_complicated_example_3
   :numbered: left
   :adaptive:

   Create the ``Dog::is_older()`` function as it would be defined INSIDE of the ``Dog`` structure definition.  This function
   checks if the current ``Dog`` is older than another ``Dog``.  The function is invoked on the current ``Dog``.
   
   -----
   bool Dog::is_older(const Dog& dog, const Dog& dog2) {                         #distractor
   =====
   bool is_older(const Dog& dog2) const {
   =====
   bool is_older(Dog& dog2) {                         #paired
   =====
    if (age > dog2.age) {
      return true;
    }
   =====
    if (dog.age > dog2.age) {                         #paired
      return true;
    }
   =====
    else {
      return false;
    }
   =====
   }
   =====
   };                         #paired
   =====
    Dog dog = *this;                         #distractor
   =====
   bool Dog::is_older(const Dog& dog2) {                         #distractor
