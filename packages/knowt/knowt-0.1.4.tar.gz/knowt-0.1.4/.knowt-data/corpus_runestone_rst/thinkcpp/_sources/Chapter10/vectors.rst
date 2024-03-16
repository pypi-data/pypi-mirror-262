Vectors
=======

.. index::
   single: vector

A **vector** is a set of values where each value is identified by a
number (called an index). An ``string`` is similar to a vector, since it
is made up of an indexed set of characters. The nice thing about vectors
is that they can be made up of any type of element, including basic
types like ``int``\ s and ``double``\ s, and user-defined types like
``Point`` and ``Time``.

.. note::
   All elements of a vector must have the same type.

The ``vector`` type is defined in the C++ Standard Template Library
(STL). In order to use it, you have to include the header file
``vector``; again, the details of how to do that depend on your
programming environment.

You can create a vector the same way you create other variable types:

::

     vector<int> count;
     vector<double> doubleVector;

The type that makes up the vector appears in angle brackets (``<`` and
``>``). The first line creates a vector of integers named ``count``; the
second creates a vector of ``double``\ s. Although these statements are
legal, they are not very useful because they create vectors that have no
elements (their size is zero). It is more common to specify the size of
the vector in parentheses:

::

     vector<int> count (4);

.. index::
   single: constructor

The syntax here is a little odd; it looks like a combination of a
variable declarations and a function call. In fact, that’s exactly what
it is. The function we are invoking is an ``vector`` constructor. A
**constructor** is a special function that creates new objects and
initializes their instance variables. In this case, the constructor
takes a single argument, which is the size of the new vector.

The following figure shows how vectors are represented in state
diagrams:

.. figure:: Images/10.1state_diagram.png
   :scale: 60%
   :align: center
   :alt: image

.. index::
   single: elements

The large numbers inside the boxes are the **elements** of the vector.
The small numbers outside the boxes are the indices used to identify
each box. When you allocate a new vector, the elements are not
initialized. They could contain any values.

There is another constructor for ``vector``\ s that takes two
parameters; the second is a “fill value,” the value that will be
assigned to each of the elements.

::

     vector<int> count (4, 0);

This statement creates a vector of four elements and initializes all of
them to zero. 

.. mchoice:: vectors_1

    How would you create a vector of five words and initialize all of them to empty strings?

    -   ``vector<string> words ("", 5);``

        -   Incorrect! Vector parameters are in the wrong order.

    -   ``vector<string> words (5);``

        +   Correct! Vector elements are default constructed to empty strings.

    -   ``vector<string> words (5, "");``

        +   Correct! We made a vector of strings with 5 elements, initialized to empty strings.

    -   ``vector<char> words (5, '');``

        -   Incorrect! words should be a vector of strings.

.. mchoice:: vectors_2
   :multiple_answers:
   :answer_a: 1
   :answer_b: "a"
   :answer_c: 'a'
   :answer_d: "word"
   :answer_e: "1"
   :correct: b,d,e
   :feedback_a: Incorrect! This is an integer, not a string.
   :feedback_b: Correct!
   :feedback_c: Incorrect! This is a character, not a string.
   :feedback_d: Correct!
   :feedback_e: Correct!

   **Multiple Response** Which of the following could be an element of **words**?

.. mchoice:: vectors_3
   :answer_a: initializer
   :answer_b: constructor
   :answer_c: creator
   :answer_d: instance function
   :correct: b
   :feedback_a: Incorrect! Go back and read to find the answer!
   :feedback_b: Correct!
   :feedback_c: Incorrect! Go back and read to find the answer!
   :feedback_d: Incorrect! Go back and read to find the answer!

   What do you call a function that creates an instance of a new object and initializes its instance variables?

.. mchoice:: vectors_4

    What are the values of ``number``'s elements after this declaration?
    
    .. code-block::
    
       vector<int> numbers(6);

    -   undefined (we don't know the values)

        -   Integers are default constructed to a known value.

    -   0

        +    Integers are default constructed to a zero value.

    -   6

        -   6 is the size we want the vector to be.
