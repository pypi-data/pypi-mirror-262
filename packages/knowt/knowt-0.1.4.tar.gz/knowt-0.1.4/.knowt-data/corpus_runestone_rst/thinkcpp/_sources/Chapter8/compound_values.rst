Compound values
---------------
.. index::
   pair: types; compound types

Most of the data types we have been working with represent a single
value—an integer, a floating-point number, a boolean value.
``string``\ s are different in the sense that they are made up of
smaller pieces, the characters. Thus, ``string``\ s are an example of a
**compound** type.

Depending on what we are doing, we may want to treat a compound type as
a single thing (or object), or we may want to access its parts (or
instance variables). This ambiguity is useful.

.. index::
   single: structures
   single: classes

It is also useful to be able to create your own compound values. C++
provides two mechanisms for doing that: **structures** and **classes**.
We will start out with structures and get to classes in
:numref:`class` (there is not much difference between
them).

.. fillintheblank:: compound_values_1
    :casei:

    Strings are made up of smaller pieces (the characters). This makes strings an example of a _____ type.

    - :compound: Correct!
      :.*: Try again!


.. fillintheblank:: compound_values_2
    :casei:

    One of the mechanisms for creating your own compound values is structures. What is the other?

    - :class(es)?: Correct!
      :.*: Try again!

.. mchoice:: compound_values_3
   :practice: T
   :answer_a: integer
   :answer_b: string
   :answer_c: floating-point number
   :answer_d: boolean value
   :correct: b
   :feedback_a: Try again!
   :feedback_b: Correct!
   :feedback_c: Try again!
   :feedback_d: Try again!

   Which is different from the others because it is does not represent a single value?
