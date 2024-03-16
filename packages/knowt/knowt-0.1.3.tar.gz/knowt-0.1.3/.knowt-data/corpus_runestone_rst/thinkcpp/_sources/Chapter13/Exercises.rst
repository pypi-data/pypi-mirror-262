Multiple Choice Exercises
-------------------------

.. mchoice:: mce_13_1
    :practice: T

    What is the output of the code below?

    .. code-block:: cpp

        enum Month { JAN = 1, FEB, MAR, APR, 
        MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC };

        int main() {
          Month m1 = JUL;
          Month m2 = NOV;
          cout << m1 << " " << m2 << endl;
        }

    - JULY NOVEMBER

      - What are the actual values of ``JUL`` and ``NOV``?

    - JUL NOV
    
      - What do the values of enumerated types map to?

    - 7 11
    
      + Since we defined ``JAN`` to start at 1, ``JUL`` and ``NOV`` map to 7 and 11.

    - 6 10
    
      - Take a closer look at our enumerated type definition.

.. mchoice:: mce_13_2
    :practice: T

    What is the output of the code below?

    .. code-block:: cpp

        int main() {
          string s = "summer";
          switch (s) {
            case "spring":
              cout << "It's spring!";
              break;
            case "summer":
              cout << "It's summer!";
            case "fall":
              cout << "It's fall!";
              break;
            case "winter":
              cout << "It's winter!";
            default:
              cout << "Invalid season!";
              break;
          }
        }

    - summer

      - Although that is the value of ``s``, is that printed?

    - It's summer!It's fall!
    
      - This would be the correct answer if this ``switch`` statement worked.

    - It's summer!It's fall!It's winter!Invalid season!
    
      - Where are the ``break`` statements?

    - Compile error.
    
      + ``switch`` statements can't be used on ``string``\s.

.. mchoice:: mce_13_3
    :practice: T

    What is the output of the code below?

    .. code-block:: cpp

        enum Season { SPRING, SUMMER, FALL, WINTER };

        int main() {
          Season s = SUMMER;
          switch (s) {
            case SPRING:
              cout << "It's spring!";
              break;
            case SUMMER:
              cout << "It's summer!";
            case FALL:
              cout << "It's fall!";
              break;
            case WINTER:
              cout << "It's winter!";
            default:
              cout << "Invalid season!";
              break;
          }
        }

    - SUMMER

      - Although that is the value of ``s``, is that printed?

    - It's summer!It's fall!
    
      + Since there is no ``break`` statement after the case for summer but there is one after fall, this is correct.

    - It's summer!It's fall!It's winter!Invalid season!
    
      - Where are the ``break`` statements?

    - Compile error.
    
      - Since ``s`` is an enumerated type, the ``Season``\s are mapped to ``int``\s, which are valid for ``switch`` statements.

.. mchoice:: mce_13_4
    :practice: T

    Take a look at the ``struct`` definition of ``Entry``. If we wanted to make a
    ``struct`` called ``Dictionary``, how can we create a ``vector`` of ``Entry``\s
    as a member variable?

    .. code-block:: cpp

        struct Entry {
          string word;
          int page;
        }

    - ``vector<Entry> entries;``

      + We create a ``vector`` with type ``Entry``.

    - ``Entry entries``
    
      - This only creates one ``Entry``.

    - ``vector<Dictionary> Entry``
    
      - This creates a ``vector`` of ``Dictionary``\s called ``Entry``.

    - We can't make an object that contains a ``vector``.
    
      - We can have ``vector``\s inside objects.

.. mchoice:: mce_13_5
    :practice: T

    What is wrong with the code below?

    .. code-block:: cpp

        struct Card {
          int suit, rank;

          Card ();
          Card (int s, int r);

          void print () const;
          bool isGreater (const Card& c2) const;
          int find (const Deck& deck) const;
        };

        struct Deck {
          vector<Card> cards;

          Deck ();
          Deck (int n);
          void print () const;
          int find (const Card& card) const;
        };

    - We can't have a ``vector`` in ``Deck``.

      - We are allowed to have ``vector``\s in objects.

    - The definition of ``Card::find()`` is invalid.
    
      + The definition references ``Deck``, but ``Deck`` is defined after ``Card``.

    - We can't define ``print()`` in both ``Card`` and in ``Deck``.
    
      - Although they have the same name, these are two different ``print()`` functions.

    - Nothing is wrong with the code.
    
      - There is an error in the code. Can you find it?

.. mchoice:: mce_13_6
    :practice: T

    Why can't we code our ``shuffle`` function to work the exact same way humans shuffle cards?

    - Our code can't split the deck exactly in half.

      - We can split the deck exactly in half.

    - The way our code would shuffle cards would be unpredictable.
    
      - Part of the problem is that the cards would be shuffled in a predictable manner.

    - Our code would result in an infinite loop.
    
      - There's no reason to loop infinitely.

    - Our code would perform a perfect shuffle.
    
      + Because the cards are shuffled perfectly, the exact ordering of the cards is predictable and thus the cards aren't really shuffled.

.. mchoice:: mce_13_7
    :practice: T

    What is true about helper functions?

    - They are longer than the bigger functions since they do all the work.

      - Most helper functions are shorter than the bigger function.

    - They are simpler functions that help the bigger function.
    
      + As the name implies, they help a bigger function.

    - They shorten the code used in bigger functions.
    
      + Usually the bigger function has repetitive code, which is then put into a helper function to help shorten the bigger function.

    - They make debugging easier.
    
      + Since helper functions break down the bigger function into smaller parts, it's easier to isolate and identify issues.

.. mchoice:: mce_13_8
    :practice: T

    Using pseudocode to figure out what helper functions are needed is a characteristic of what?

    - Encapsulation

      - This is the process of wrapping up a sequence of instructions in a function.

    - Generalization
    
      - This is the process of taking something specific and making it more general.

    - Top-down design
    
      + This is the process of using pseudocode to sketch solutions to large problems and design the interfaces of helper functions.

    - Bottom-up design
    
      - This is the process of writing small, useful functions and then assembling them into larger solutions.

.. mchoice:: mce_13_9
    :practice: T

    Which of the following can lead to off by one errors?

    - Running a for loop too little or too many times.

      - This can lead to too few iterations or too many iterations.

    - Forgetting that indexing starts at 0.
    
      - This can lead you to have values that are shifted by one.

    - Using less than instead of less than or equal to in a while loop.
    
      - This can lead to running the while loop one less times than what you wanted.

    - All of the above.
    
      + These can all lead to off by one errors.

.. mchoice:: mce_13_10
    :practice: T

    What is the amount of time that mergeSort takes?

    - n log n

      + This makes mergeSort faster than our previous version of selection sort.

    - n!
    
      - mergeSort runs faster than factorial time.

    - logn
    
      - mergeSort runs slower than logarithmic time.

    - n^2
    
      - This is the time complexity of selection sort.

.. mchoice:: mce_13_11
    :practice: T

    What kind of sorting algorithm is our ``sortDeck`` function? You are encouraged to search up these different sorting algorithms!

    - Bubble sort

      - Bubble sort swaps adjacent items and "bubbles" the lightest items to the top.

    - Insertion sort
    
      - Insertion sort selects an item from the unsorted section and puts it in the right location in the sorted section.

    - Selection sort
    
      + Selection sort finds the smallest item at each iteration i and puts it at the ith location.

    - Quicksort
    
      - Quicksort uses recursive calls to partition a list.