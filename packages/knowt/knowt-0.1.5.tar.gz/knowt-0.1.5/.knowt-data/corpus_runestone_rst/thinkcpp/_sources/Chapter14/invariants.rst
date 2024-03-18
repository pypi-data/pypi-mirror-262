Invariants
----------

There are several conditions we expect to be true for a proper
``Complex`` object. For example, if the ``cartesian`` flag is set then
we expect ``real`` and ``imag`` to contain valid data. Similarly, if
``polar`` is set, we expect ``mag`` and ``theta`` to be valid. Finally,
if both flags are set then we expect the other four variables to be
consistent; that is, they should be specifying the same point in two
different formats.

.. index::
   single: invariant

These kinds of conditions are called ``invariants``, for the obvious
reason that they do not vary—they are always supposed to be true. One of
the ways to write good quality code that contains few bugs is to figure
out what invariants are appropriate for your classes, and write code
that makes it impossible to violate them.

One of the primary things that data encapsulation is good for is helping
to enforce invariants. The first step is to prevent unrestricted access
to the instance variables by making them private. Then the only way to
modify the object is through accessor functions and modifiers. If we
examine all the accessors and modifiers, and we can show that every one
of them maintains the invariants, then we can prove that it is
impossible for an invariant to be violated.

Looking at the ``Complex`` class, we can list the functions that make
assignments to one or more instance variables:

::

   the second constructor
   calculateCartesian
   calculatePolar
   setCartesian
   setPolar

In each case, it is straightforward to show that the function maintains
each of the invariants I listed. We have to be a little careful, though.
Notice that I said “maintain” the invariant. What that means is “If the
invariant is true when the function is called, it will still be true
when the function is complete.”

That definition allows two loopholes. First, there may be some point in
the middle of the function when the invariant is not true. That’s ok,
and in some cases unavoidable. As long as the invariant is restored by
the end of the function, all is well.

The other loophole is that we only have to maintain the invariant if it
was true at the beginning of the function. Otherwise, all bets are off.
If the invariant was violated somewhere else in the program, usually the
best we can do is detect the error, output an error message, and exit.

.. mchoice:: question14_8_1
   :answer_a: It prevents unrestricted access to the instance variables by making them private.
   :answer_b: It allows users to directly modify private member variables.
   :answer_c: It makes it so that private data members can never be modified by any function.
   :answer_d: It eliminates the need for invariants.
   :correct: a
   :feedback_a: Correct! Users must instead use accessor functions to access them.
   :feedback_b: Incorrect! Try again.
   :feedback_c: Incorrect! Try again.
   :feedback_d: Incorrect! Try again.

   How does data encapsulation help us enforce invariants? 

.. mchoice:: question14_8_2
   :answer_a: True
   :answer_b: False
   :correct: a
   :feedback_a: Correct! The invariant just has to be true when the function is complete, given that it's true at the start.
   :feedback_b: Incorrect! Try again.

   An invariant can be false in the middle of a function as long as it is true at the start and end. 

.. mchoice:: question14_8_3
   :answer_a: True
   :answer_b: False
   :correct: b
   :feedback_a: Incorrect! Try again.
   :feedback_b: Correct! We only have to maintain the invariant if it was true at the start. If it's false, all bets are off.

   If an invariant is false at the start of the function, the function must fix it to be true by the end. 

.. mchoice:: question14_8_4
   :multiple_answers:
   :answer_a: The interior angles of a ``Triangle`` object must add up to 180 degrees.
   :answer_b: The sum of two sides of a ``Triangle`` object must be greater than the third.
   :answer_c: All angles of a ``Triangle`` object must be 60 degrees.
   :answer_d: The greatest angle in a ``Triangle`` object must be less than 90 degrees.
   :correct: a,b
   :feedback_a: Correct! 
   :feedback_b: Correct!
   :feedback_c: Incorrect! An equilateral triangle is only one possible kind of triangle.
   :feedback_d: Incorrect! We are allowed to have obtuse triangles.

   If we create a ``Triangle`` class, which of the following are invariants we must maintain?
