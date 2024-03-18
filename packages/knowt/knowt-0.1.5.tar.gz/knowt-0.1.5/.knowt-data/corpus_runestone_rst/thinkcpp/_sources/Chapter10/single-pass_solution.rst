A single-pass solution
----------------------

Although this code works, it is not as efficient as it could be. Every
time it calls ``howMany``, it traverses the entire vector. In this
example we have to traverse the vector ten times!

It would be better to make a single pass through the vector. For each
value in the vector we could find the corresponding counter and
increment it. In other words, we can use the value from the vector as an
index into the histogram. Here’s what that looks like:

::

     vector<int> histogram (upperBound, 0);

     for (int i = 0; i < numValues; i++) {
       int index = vector[i];
       histogram[index]++;
     }

The first line initializes the elements of the histogram to zeroes. That
way, when we use the increment operator (``++``) inside the loop, we
know we are starting from zero. Forgetting to initialize counters is a
common error.

As an exercise, encapsulate this code in a function called ``histogram``
that takes a vector and the range of values in the vector (in this case
0 through 10), and that returns a histogram of the values in the vector.

.. mchoice:: single_pass_solution_1
   :multiple_answers:
   :answer_a: Your code runs without a problem because counters are automatically initialized to zero.
   :answer_b: Your code might run, but it probably won't produce the output you desire.
   :answer_c: You might get an error for using an uninitialized variable.
   :answer_d: Your program will crash.
   :correct: b,c
   :feedback_a: Incorrect! Variables are not automatically initialized.
   :feedback_b: Correct! C++ might assign unused memory to the uninitialized variable, which will allow the code to run, but counts may be off.
   :feedback_c: Correct! Depening on your compiler, you might be lucky enough to get an error message.
   :feedback_d: Incorrect! You might get a compile error, but your program will not crash.

   What happens if you don't initialize a counter?

.. parsonsprob:: single_pass_solution_2
   :numbered: left
   :adaptive:

   Construct a function called histogram that takes a vector and the range of values in the vector, and that returns a histogram of values in the vector.
   -----
   vector&#60;int&#62; histogram(const vector&#60;int&#62;& vec, int range) {
   =====
      vector&#60;int&#62; histogram (range, 0);
   =====
      vector&#60;int&#62; histogram (range);                         #paired
   =====
      for (int i = 0; i &#60; vec.size(); i++) {
   =====
      for (int i = 0; i &#60; range; i++) {                         #paired
   =====
         int index = vec[i];
   =====
         int index = i;                         #paired
   =====
         histogram[index]++;
   =====
      }
      return histogram;
   }
