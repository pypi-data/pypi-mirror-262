Implicit variable access
------------------------

Actually, the new version of ``Time::print`` is more complicated than it
needs to be. We don’t really need to create a local variable in order to
refer to the instance variables of the current object.

If the function refers to ``hour``, ``minute``, or ``second``, all by
themselves with no dot notation, C++ knows that it must be referring to
the current object. So we could have written:

::

   void Time::print () {
     cout << hour << ":" << minute << ":" << second << endl;
   }

.. index::
   single: implicit variable access

This kind of variable access is called **implicit** because the name of
the object does not appear explicitly. Features like this are one reason
member functions are often more concise than nonmember functions.

.. mchoice:: implicit_variable_access_1
   :answer_a: after being granted permission
   :answer_b: only inside of that specific member function
   :answer_c: using dot notation
   :answer_d: directly, without dot notation
   :correct: d
   :feedback_a: Incorrect! You don't need "permission" to access member variables inside a member function.
   :feedback_b: Incorrect! You can access member variables implicitly inside any and all member functions.
   :feedback_c: Incorrect! You don't need to use dot notation to access variables implicitly.
   :feedback_d: Correct! Implicit variable access allows us to access variables directly-- without using dot notation.

   Implicit variable access in member functions allows us to access member variables __________.

.. mchoice:: implicit_variable_access_2
   :answer_a: Every time you are working with data structures!
   :answer_b: When you implement member functions inside of the structure definition.
   :answer_c: When you implement member functions outside of the structure definition.
   :answer_d: Never! It is bad practice!
   :correct: c
   :feedback_a: Incorrect! The scope resolution operator is not always necessary!
   :feedback_b: Incorrect! When you write member functions inside of the structure definition, you do not need to specify the scope.
   :feedback_c: Correct!  When you write member functions outside of the structure definition, you need to specify the scope, hence the :: operator!
   :feedback_d: Incorrect! The scope resolution operator is good practice when used correctly!

   When should you use the scope resolution operator ``::``?

