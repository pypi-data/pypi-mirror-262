Enumerated types
----------------

In the previous chapter I talked about mappings between real-world
values like rank and suit, and internal representations like integers
and strings. Although we created a mapping between ranks and integers,
and between suits and integers, I pointed out that the mapping itself
does not appear as part of the program.

.. index::
   single: enumerated type

Actually, C++ provides a feature called an **enumerated type** that
makes it possible to (1) include a mapping as part of the program, and
(2) define the set of values that make up the mapping. For example, here
is the definition of the enumerated types ``Suit`` and ``Rank``:

::

   enum Suit { CLUBS, DIAMONDS, HEARTS, SPADES };

   enum Rank { ACE = 1, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE,
   TEN, JACK, QUEEN, KING };

.. note::
   By default, the first value in the enumerated type maps to 0, the 
   second to 1, and so on. 

Within the ``Suit`` type, the value ``CLUBS`` is represented by the integer
0, ``DIAMONDS`` is represented by 1, etc.

The definition of ``Rank`` overrides the default mapping and specifies
that ``ACE`` should be represented by the integer 1. The other values
follow in the usual way.

Once we have defined these types, we can use them anywhere. For example,
the instance variables ``rank`` and ``suit`` are can be declared with
type ``Rank`` and ``Suit``:

::

   struct Card {
     Rank rank;
     Suit suit;

     Card (Suit s, Rank r);
   };

The types of the parameters for the constructor have changed, too.
Now, to create a card, we can use the values from the enumerated type as
arguments:

::

     Card card (DIAMONDS, JACK);

By convention, the values in enumerated types have names with all
capital letters. This code is much clearer than the alternative using
integers:

::

     Card card (1, 11);

.. activecode:: enum_type_AC_1 
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
   
   The active code below uses the enumerated types created above to construct ``Card`` objects.  
   Feel free to modify the values that the cards are being initialized to in the constructor:  this will 
   change the output from the ``print`` function. Notice how this is much clearer than using integers.
   ~~~~
   #include <iostream>
   #include <string>
   #include <vector>
   using namespace std;

   enum Suit { CLUBS, DIAMONDS, HEARTS, SPADES };

   enum Rank { ACE=1, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE,
   TEN, JACK, QUEEN, KING };

   struct Card {
       Rank rank;
       Suit suit;
       Card (Suit s, Rank r);
       void print () const;
   };

   int main() {
       Card card1 (DIAMONDS, JACK);
       card1.print ();
       Card card2 (HEARTS, QUEEN);
       card2.print ();
       Card card3 (CLUBS, THREE);
       card3.print ();
   }

   ====
   Card::Card (Suit s, Rank r) {
       suit = s;  rank = r;
   }

   void Card::print () const {
       vector<string> suits (4);
       suits[0] = "Clubs";
       suits[1] = "Diamonds";
       suits[2] = "Hearts";
       suits[3] = "Spades";

       vector<string> ranks (14);
       ranks[1] = "Ace";
       ranks[2] = "2";
       ranks[3] = "3";
       ranks[4] = "4";
       ranks[5] = "5";
       ranks[6] = "6";
       ranks[7] = "7";
       ranks[8] = "8";
       ranks[9] = "9";
       ranks[10] = "10";
       ranks[11] = "Jack";
       ranks[12] = "Queen";
       ranks[13] = "King";

       cout << ranks[rank] << " of " << suits[suit] << endl;
   }

Because we know that the values in the enumerated types are represented
as integers, we can use them as indices for a vector. Therefore the old
``print`` function will work without modification. We have to make some
changes in ``buildDeck``, though:

::

     int index = 0;
     for (Suit suit = CLUBS; suit <= SPADES; suit = Suit(suit+1)) {
       for (Rank rank = ACE; rank <= KING; rank = Rank(rank+1)) {
         deck[index].suit = suit;
         deck[index].rank = rank;
         index++;
       }
     }

In some ways, using enumerated types makes this code more readable, but
there is one complication. Strictly speaking, we are not allowed to do
arithmetic with enumerated types, so ``suit++`` is not legal. On the
other hand, in the expression ``suit+1``, C++ automatically converts the
enumerated type to integer. Then we can take the result and typecast it
back to the enumerated type:

::

     suit = Suit(suit+1);
     rank = Rank(rank+1);

Actually, there is a better way to do this—we can define the ``++``
operator for enumerated types—but that is beyond the scope of this book.


.. mchoice:: enum_type_1
   :multiple_answers:
   :answer_a: Perform arithmetic.
   :answer_b: Include a mapping as part of the program.
   :answer_c: Use the same set of values in multiple mappings.
   :answer_d: Define the set of values that make up a mapping.
   :answer_e: Use them as indices for a vector.
   :correct: b,d,e
   :feedback_a: We are not allowed to do arithmetic with enumerated types.
   :feedback_b: This is the purpose of an enumerated type.
   :feedback_c: Variables in one enumeration type cannot be used in another enumeration type.
   :feedback_d: This is the purpose of an enumerated type.
   :feedback_e: Since the values in enumerated types are represented as integers, we can use them as vector indices.

   Multiple Response: What can we do with enumerated types?


.. mchoice:: enum_type_2
   :answer_a: Who ordered a triple scoop of Cookies 'n' Cream in a sugar cone?
   :answer_b: Who ordered a double scoop of Strawberry in a cake cone?
   :answer_c: Who ordered a double scoop of Cookies 'n' Cream in a sugar cone?
   :answer_d: Who ordered a triple scoop of Strawberry in a cake cone?
   :answer_e: Who ordered a triple scoop of Mint Chocolate Chip in a Waffle Cone?
   :correct: c
   :feedback_a: Remember that we performed an override for one of the enumerated types!
   :feedback_b: Remember that the default enumeration starts at 0.
   :feedback_c: 2 corresponds to "double", 3 corresponds to "Cookies 'n' Cream", and 2 corresponds to "sugar cone".
   :feedback_d: Remember that we performed an override for one of the enumerated types!  The default enumeration starts at 0.
   :feedback_e: Take another look at how we defined our enumerated types.

   Assume we have the following struct defined by this enumerated
   type.  What will be printed by the print function?

   ::

       enum Scoops { SINGLE = 1, DOUBLE, TRIPLE };
       enum Flavor { VANILLA, CHOCOLATE, STRAWBERRY, COOKIESNCREAM, MINTCHIP, COOKIEDOUGH };
       enum Order { CUP, CAKECONE, SUGARCONE, WAFFLECONE }

       struct iceCream {
          Scoops scoops;
          Flavor flavor;
          Order order;

          iceCream (Scoops s, Flavor f, Order o);
          printOrder () {
            // To save space, I didn't include the mapping.  I'm sure you can still figure it out.
            cout << "Who ordered a " << scoops[scoop] << " scoop of " << flavors[flavor] << " in a " << orders[order] << ?;
          }
       };

       int main () {
         iceCream icecream (2, 3, 2);
         iceCream.printOrder();
       }


.. fillintheblank:: enum_type_3

    Based on the ``Rank`` enumerated type, what integer value does ``QUEEN`` have?

    - :12|[Tt][Ww|[Ee][Ll][Vv][Ee]: Correct!
      :.*: Incorrect! Try again.
