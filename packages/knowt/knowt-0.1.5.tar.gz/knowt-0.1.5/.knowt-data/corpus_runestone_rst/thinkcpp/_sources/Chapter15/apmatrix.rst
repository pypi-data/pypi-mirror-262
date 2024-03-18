``matrix``
------------

A ``matrix`` is similar to a ``vector`` except it is
two-dimensional. Instead of a length, it has two dimensions, called
``numrows`` and ``numcols``, for “number of rows” and “number of
columns.”

Each element in the matrix is indentified by two indices; one specifies
the row number, the other the column number.

To create a matrix, there are four constructors:

::

     matrix<char> m1;
     matrix<int> m2 (3, 4);
     matrix<double> m3 (rows, cols, 0.0);
     matrix<double> m4 (m3);

The first is a do-nothing constructor that makes a matrix with both
dimensions 0. The second takes two integers, which are the initial
number of rows and columns, in that order. The third is the same as the
second, except that it takes an additional parameter that is used to
initialized the elements of the matrix. The fourth is a copy constructor
that takes another ``matrix`` as a parameter.

Just as with ``vectors``, we can make ``matrix``\ es with any type
of elements (including ``vector``\ s, and even ``matrix``\ es).

To access the elements of a matrix, we use the ``[]`` operator to
specify the row and column:

::

     m2[0][0] = 1;
     m3[1][2] = 10.0 * m2[0][0];

If we try to access an element that is out of range, the program prints
an error message and quits.

The ``numrows`` and ``numcols`` functions get the number of rows and
columns. Remember that the row indices run from 0 to ``numrows() -1``
and the column indices run from 0 to ``numcols() -1``.

The usual way to traverse a matrix is with a nested loop. This loop sets
each element of the matrix to the sum of its two indices:

::

     for (int row=0; row < m2.numrows(); row++) {
       for (int col=0; col < m2.numcols(); col++) {
         m2[row][col] = row + col;
       }
     }

This loop prints each row of the matrix with tabs between the elements
and newlines between the rows:

::

     for (int row=0; row < m2.numrows(); row++) {
       for (int col=0; col < m2.numcols(); col++) {
         cout << m2[row][col] << "\t";
       }
       cout << endl;
     }

.. mchoice:: question15_8_1
   :multiple_answers:
   :answer_a: int
   :answer_b: string
   :answer_c: vector<int>
   :answer_d: vector<vector<int>>
   :answer_e: matrix
   :correct: a,b,c,d,e
   :feedback_a: Correct!
   :feedback_b: Correct!
   :feedback_c: Correct!
   :feedback_d: Correct! This is a technically type of matrix!
   :feedback_e: Correct! Matrices can be made of matrices.

   Which of the following data types are supported by matrix?

.. fillintheblank:: question15_8_2

    Suppose we have matrix ``mat``.  Then ``mat[9][17]`` would be accessing
    column |blank| and row |blank| of our matrix.

    - :(18): Correct!
      :x: Incorrect! Remember to use zero indexing!
    - :(10): Correct!
      :.*: Incorrect! Remember to use zero indexing!
