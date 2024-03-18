Decks and subdecks
------------------

Looking at the interface to ``findBisect``

::

   int findBisect (const Card& card, const vector<Card>& deck,
           int low, int high) {

it might make sense to treat three of the parameters, ``deck``, ``low``
and ``high``, as a single parameter that specifies a *subdeck*.

.. index::
   single: abstract
   single: abstraction
   single: abstract parameter

This kind of thing is quite common, and I sometimes think of it as an
**abstract parameter**. What I mean by **abstract,** is something that is
not literally part of the program text, but which describes the function
of the program at a higher level.

For example, when you call a function and pass a vector and the bounds
``low`` and ``high``, there is nothing that prevents the called function
from accessing parts of the vector that are out of bounds. So you are
not literally sending a subset of the deck; you are really sending the
whole deck. But as long as the recipient plays by the rules, it makes
sense to think of it, abstractly, as a subdeck.

There is one other example of this kind of abstraction that you might
have noticed in :numref:`objectops`, when I referred to
an “empty” data structure. The reason I put “empty” in quotation marks
was to suggest that it is not literally accurate. All variables have
values all the time. When you create them, they are given default
values. So there is no such thing as an empty object.

But if the program guarantees that the current value of a variable is
never read before it is written, then the current value is irrelevant.
Abstractly, it makes sense to think of such a variable as “empty.”

This kind of thinking, in which a program comes to take on meaning
beyond what is literally encoded, is a very important part of thinking
like a computer scientist. Sometimes, the word “abstract” gets used so
often and in so many contexts that it is hard to interpret.
Nevertheless, abstraction is a central idea in computer science (as well
as many other fields).

A more general definition of “abstraction” is “The process of modeling a
complex system with a simplified description in order to suppress
unnecessary details while capturing relevant behavior.”

.. mchoice:: decks_and_subdecks_1
   :answer_a: It uses binary search to locate the card in the deck.
   :answer_b: If the program user plays by the rules, we can think of deck, low, and high abstractly as a subdeck.
   :answer_c: It can only access the part of the deck that is between the bounds high and low.
   :answer_d: There is no such thing as an empty object.
   :correct: c
   :feedback_a: This is true. Binary search is very efficient.
   :feedback_b: This is true. If the user doesn't follow the rules, we might be in trouble.
   :feedback_c: This is false! findBisect() can access the entire deck, even when you pass high and low parameters.
   :feedback_d: This is true.  When you create an object, it is given default values.

   Which is false about the ``findBisect()`` funtion?

.. fillintheblank:: decks_and_subdecks_2

   When a programmer hides all unnecessary details from the user to reduce complexity and increase efficiency, this is called __________.

   - :[Aa][Bb][Ss][Tt][Rr][Aa][Cc][Tt][Ii][Oo][Nn]: Correct!
     :x: Incorrect! You may need to go back and read!
