What is a class?
----------------

.. index::
   single: class

In most object-oriented programming languages, a **class** is a
user-defined type that includes a set of functions. As we have seen,
structures in C++ meet the general definition of a class.

But there is another feature in C++ that also meets this definition;
confusingly, it is called a ``class``. In C++, a class is just a
structure whose instance variables are private by default. For example,
I could have written the ``Card`` definition:

::

   class Card
   {
     int suit, rank;

   public:
     Card ();
     Card (int s, int r);

     int getRank () const { return rank; }
     int getSuit () const { return suit; }
     int setRank (int r) { rank = r; }
     int setSuit (int s) { suit = s; }
   };

I replaced the word ``struct`` with the word ``class`` and removed the
``private:`` label. This result of the two definitions is exactly the
same.

In fact, anything that can be written as a ``struct`` can also be
written as a ``class``, just by adding or removing labels. There is no
real reason to choose one over the other, except that as a stylistic
choice, most C++ programmers use ``class``.

Also, it is common to refer to all user-defined types in C++ as
“classes,” regardless of whether they are defined as a ``struct`` or a
``class``.

.. mchoice:: question14_2_1
   :answer_a: True
   :answer_b: False
   :correct: a
   :feedback_a: Correct! We can omit the ``private:`` label because the data members are private by default 
   :feedback_b: Incorrect! Try again.

   By default, the data members of a ``class`` are private. 

.. mchoice:: question14_2_2
   :practice: T
   :answer_a: Remove the ``private:`` label.
   :answer_b: Change ``struct`` to ``class`` and remove the ``public:`` label.
   :answer_c: Remove the ``public:`` label.
   :answer_d: Change ``struct`` to ``class``.
   :correct: d
   :feedback_a: Incorrect! ``Deck`` is still a ``struct``.
   :feedback_b: Incorrect! We don't want to make the constructors and all member functions private.
   :feedback_c: Incorrect! We don't want to make the constructors and all member functions private.
   :feedback_d: Correct! ``Deck`` is now a ``class`` and it's okay that we kept the ``private:`` label.

   How can we change ``Deck``, which is currently a ``struct``, into a ``class``? 

   .. code-block:: cpp

      struct Deck {
      private:
        vector<Card> cards;
      
      public:
        Deck ();
        Deck (int n);

        void print () const;
        void swapCards (int index1, int index2);
        int findLowestCard (int index);
        void shuffleDeck ();
        void sortDeck ();
        Deck subdeck (int low, int high) const;
        Deck mergeSort () const;
        Deck mergeSort (Deck deck) const;
      };

.. mchoice:: question14_2_3
   :answer_a: True
   :answer_b: False
   :correct: a
   :feedback_a: Correct! However, they cannot be accessed outside of the class. 
   :feedback_b: Incorrect! We can access private data members as long as we are in the class.

   Private data members can be accessed within the class.
