File Input/Output and ``matrix``\ es
---------------------------------------

In this chapter we will develop a program that reads and writes files,
parses input, and demonstrates the ``matrix`` class. We will also
implement a data structure called ``Set`` that expands automatically as
you add elements.

Aside from demonstrating all these features, the real purpose of the
program is to generate a two-dimensional table of the distances between
cities in the United States. The output is a matrix that looks like this:

::

   Atlanta 0
   Chicago 700     0
   Boston  1100    1000    0
   Dallas  800     900     1750    0
   Denver  1450    1000    2000    800     0
   Detroit 750     300     800     1150    1300    0
   Orlando 400     1150    1300    1100    1900    1200    0
   Phoenix 1850    1750    2650    1000    800     2000    2100    0
   Seattle 2650    2000    3000    2150    1350    2300    3100    1450    0
           Atlanta Chicago Boston  Dallas  Denver  Detroit Orlando Phoenix Seattle

The diagonal elements are all zero because that is the distance from a
city to itself. Also, because the distance from A to B is the same as
the distance from B to A, there is no need to print the top half of the
matrix.

.. mchoice:: question15_1_1
   :answer_a: Because we only need the half of the dataset contained by the triangle.
   :answer_b: Because triangles are the most effective shape to use when presenting data to others.
   :answer_c: Because matrices are triangles.
   :answer_d: Because the triangle contains the entire dataset.
   :correct: d
   :feedback_a: Incorrect! All of the data above the 0 diagonal is a mirror image of the triangle! So, the triangle contains the whole dataset.
   :feedback_b: Incorrect! Triangles do look cool, but they aren't necessarily the most effective shape to use when presenting data.
   :feedback_c: Incorrect! This triangle is PART OF an apmatrix.
   :feedback_d: Correct! The triangle contains all data points with no repeat data. If we included all datapoints, the would just be repeats of the points we already have.

   Why aren't we filling in every value in our table, who are we leaving blank space above the diagonal of 0's?

.. mchoice:: question15_1_2
   :answer_a: a geometric shape
   :answer_b: a two-dimensional vector
   :answer_c: a material in which something develops
   :answer_d: a mold used to shape things
   :correct: b
   :feedback_a: Incorrect! A matrix is not a geometric shape, although they ARE rectangles.
   :feedback_b: Correct!
   :feedback_c: Incorrect! This is a definition for matrix, but not in the programming sense.
   :feedback_d: Incorrect! This is a definition for matrix, but not in the programming sense.

   Based on how it is used to create the above table, what do you think a ``matrix`` is?

