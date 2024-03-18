Composition
-----------

.. index::
   single: composition

By now we have seen several examples of **composition** (the ability to
combine language features in a variety of arrangements). One of the
first examples we saw was using a function invocation as part of an
expression. Another example is the nested structure of statements: you
can put an ``if`` statement within a ``while`` loop, or within another
``if`` statement, etc.

Having seen this pattern, and having learned about vectors and objects,
you should not be surprised to learn that you can have vectors of
objects. In fact, you can also have objects that contain vectors (as
instance variables); you can have vectors that contain vectors; you can
have objects that contain objects, and so on.

In the next two chapters we will look at some examples of these
combinations, using ``Card`` objects as a case study.

.. mchoice:: composition_1
   :answer_a: You can have vectors that contain other vectors and objects that contain other objects.
   :answer_b: You can have vectors that contain other vectors, but you can never have objects that contain other objects.
   :answer_c: You can never have vectors that contain other vectors, but you can have objects that contain other objects.
   :answer_d: You can never have vectors that contain other vectors, nor objects that contain other objects.
   :correct: a
   :feedback_a: This is called composition!
   :feedback_b: In this chapter you will see how you can have objects that contain other objects.
   :feedback_c: In this chapter you will see how you can have vectors that contain other vectors.
   :feedback_d: Vectors and objects can have nested compositons!

   Which of the following statements is correct?

.. fillintheblank:: composition_2

    There are many different arrangements to combine language features.  This is called __________.

    - :([Cc]omposition)|(COMPOSITION): Correct!
      :.*: Incorrect!  Try again!