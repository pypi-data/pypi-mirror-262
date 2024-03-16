Streams
-------

To get input from a file or send output to a file, you have to create an
``ifstream`` object (for input files) or an ``ofstream`` object (for
output files). These objects are defined in the header file ``fstream``,
which you have to include.

.. index::
   single: stream

A **stream** is an abstract object that represents the flow of data from
a source like the keyboard or a file to a destination like the screen or
a file.

We have already worked with two streams: ``cin``, which has type
``istream``, and ``cout``, which has type ``ostream``. ``cin``
represents the flow of data from the keyboard to the program. Each time
the program uses the ``>>`` operator or the ``getline`` function, it
removes a piece of data from the input stream.

Similarly, when the program uses the ``<<`` operator on an ``ostream``,
it adds a datum to the outgoing stream.

.. fillintheblank:: question15_2_1

    You create an |blank| object to write data to a file, and a |blank| object to read data from a file.
    In order to define objects to input from a file or send output to a file, you must include the ``<`` |blank| ``>`` header file.

    - :(?:o|O)(?:f|F)(?:s|S)(?:t|T)(?:r|R)(?:e|E)(?:a|A)(?:m|M): Correct!
      :x: Incorrect! Try re-reading!
    - :(?:i|I)(?:f|F)(?:s|S)(?:t|T)(?:r|R)(?:e|E)(?:a|A)(?:m|M): Correct!
      :.*: Incorrect! Try re-reading!
    - :(?:f|F)(?:s|S)(?:t|T)(?:r|R)(?:e|E)(?:a|A)(?:m|M): Correct!
      :.*: Incorrect! Try re-reading!

.. mchoice:: question15_2_2
   :answer_a: an abstract object that works exclusively with cin and cout statements
   :answer_b: an abstract object on which input and ouput operations are performed
   :answer_c: an abstract object that works only with file data
   :answer_d: an abstract object that controls the flow of statements
   :correct: b
   :feedback_a: Incorrect! Stream objects do work with cin and cout, but that is not all that they do!
   :feedback_b: Correct!
   :feedback_c: Incorrect! Stream objects do work with file data, but they do other things too.
   :feedback_d: Incorrect! This is not at all what stream objects do, you should try re-reading to get a better understanding!

   What is a stream object?

.. dragndrop:: question15_1_3
    :feedback: Try again!
    :match_1: cin|||ifstream
    :match_2: cout|||ofstream

    Match the stream to its type.
