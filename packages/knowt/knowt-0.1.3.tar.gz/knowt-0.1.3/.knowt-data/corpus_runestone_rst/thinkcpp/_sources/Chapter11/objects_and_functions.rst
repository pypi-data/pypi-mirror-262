Objects and functions
=====================

.. index::
   single: object-oriented programming

C++ is generally considered an **object-oriented programming** language,
which means that it provides features that support object-oriented
programming.

It’s not easy to define object-oriented programming, but we have already
seen some features of it:

#. Programs are made up of a collection of structure definitions and
   function definitions, where most of the functions operate on specific
   kinds of structures (or objects).

#. Each structure definition corresponds to some object or concept in
   the real world, and the functions that operate on that structure
   correspond to the ways real-world objects interact.

For example, the ``Time`` structure we defined in
:numref:`time` obviously corresponds to the way people
record the time of day, and the operations we defined correspond to the
sorts of things people do with recorded times. Similarly, the ``Point``
and ``Rectangle`` structures correspond to the mathematical concept of a
point and a rectangle.

So far, though, we have not taken advantage of the features C++ provides
to support object-oriented programming. Strictly speaking, these
features are not necessary. For the most part they provide an alternate
syntax for doing things we have already done, but in many cases the
alternate syntax is more concise and more accurately conveys the
structure of the program.

For example, in the ``Time`` program, there is no obvious connection
between the structure definition and the function definitions that
follow. With some examination, it is apparent that every function takes
at least one ``Time`` structure as a parameter.

.. index::
   single: member function

This observation is the motivation for **member functions**. Member
function differ from the other functions we have written in two ways:

.. index::
   single: invoke

#. When we call the function, we **invoke** it on an object, rather than
   just call it. People sometimes describe this process as “performing
   an operation on an object,” or “sending a message to an object.”

#. The function is *declared* inside the ``struct`` definition, in order
   to make the relationship between the structure and the function
   explicit.

In the next few sections, we will take the functions from
:numref:`time` and transform them into member functions. One
thing you should realize is that this transformation is purely
mechanical; in other words, you can do it just by following a sequence
of steps.

.. index::
   single: free-standing function

As I said, anything that can be done with a member function can also be
done with a nonmember function (sometimes called a **free-standing**
function). But sometimes there is an advantage to one over the other. If
you are comfortable converting from one form to another, you will be
able to choose the best form for whatever you are doing.


.. mchoice:: objects_and_functions_1
   :answer_a: object-oriented programming
   :answer_b: data-oriented programming
   :answer_c: structured programming
   :answer_d: structural programming
   :correct: a
   :feedback_a: Correct!
   :feedback_b: Incorrect! Data-oriented programming focuses on how data is touched and processed.
   :feedback_c: Incorrect! Structured programming makes use of structured control flow using block structures (if/else, for/while).
   :feedback_d: Incorrect! This is not one of the types of programming.

   What is do we call programming that makes use of data structures and functions that interact with them?

.. mchoice:: objects_and_functions_2
   :answer_a: all
   :answer_b: some
   :answer_c: none
   :correct: a
   :feedback_a: Correct! But sometimes there is an advantage to using one over the other!
   :feedback_b: Incorrect! The answer might surprise you!
   :feedback_c: Incorrect! Quite the opposite, actually!
   
   Free-standing functions can perform __________ of the operation(s) that a member function can.

.. mchoice:: objects_and_functions_3
   :answer_a: before the structure definition
   :answer_b: inside of the structure definition
   :answer_c: after the structure definition
   :answer_d: anywhere in the program
   :correct: b
   :feedback_a: Incorrect! You're very close!
   :feedback_b: Correct!
   :feedback_c: Incorrect! You're very close!
   :feedback_d: Incorrect! The purpose of a member function is to establish a relationship between the structure and the function.

   Member functions are declared __________.
