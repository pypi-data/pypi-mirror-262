Boolean Variables
-----------------
..	index::
	  pair: types; bool types

As usual, for every type of value, there is a corresponding type of
variable. In C++ the boolean type is called **bool**. Boolean variables
work just like the other types:

::

    bool fred;
    fred = true;
    bool testResult = false;

The first line is a simple variable declaration; the second line is an
assignment, and the third line is a combination of a declaration and as
assignment, called an initialization.

As I mentioned, the result of a comparison operator is a boolean, so you
can store it in a bool variable

::

    bool evenFlag = (n % 2 == 0);     // true if n is even
    bool plusFlag = (x > 0);    // true if x is positive

and then use it as part of a conditional statement later

::

    if (evenFlag) {
      cout << "n was even when I checked it";
    }

..	index::
	  single: flag

A variable used in this way is called a **flag**, since it flags the
presence or absence of some condition.


.. dragndrop:: bool_var_1
   :feedback: Try again!
   :match_1: x * 2 > 4|||false
   :match_2: x >= 2|||true

   Match the conditional statement to the correct boolean, given x = 2.


.. dragndrop:: bool_var_2
   :feedback: Try again!
   :match_1: bool fred;|||variable declaration
   :match_2: fred = true;|||assignment
   :match_3: bool testResult = false;|||initialization

   Match the statement to the word that describes it best.


.. mchoice:: bool_var_3
   :answer_a: n was even when I checked it x was positive when I checked it
   :answer_b: x was positive when I checked it n was even when I checked it
   :answer_c: x was positive when I checked it
   :answer_d: n was even when I checked itx was positive when I checked it
   :answer_e: x was positive when I checked itn was even when I checked it
   :correct: a
   :feedback_a: Great!
   :feedback_b: Make sure you follow the correct order of execution.  Also, a space is not automatically added.
   :feedback_c: Take another look at the result from the modulus operator.
   :feedback_d: Both flags are made, But A space is after it.
   :feedback_e: Make sure you follow the correct order of execution.

   What will print?

   ::

       int n = 16;
       int x = 4;

       bool evenFlag = (n % 2 == 0);
       bool plusFlag = (x > 0);

       if (evenFlag) {
         cout << "n was even when I checked it ";
       }

       if (plusFlag) {
         cout << "x was positive when I checked it";
       }

.. mchoice:: bool_var_4

    What will print?

    .. code-block::

        bool low_battery=true;
        bool power_outage=true;

        if(low_battery){

          if(power_outage){
              power_outage=!power_outage;
          }
          else{
              low_battery=false;
          }

          if(!power_outage){
            
            if(low_battery){
                cout<<"Charging your phone"<<endl;
            }
            else{
                cout<<"Battery is charged"<<endl;
            }

          }
          else{
            cout<<"There is no power"<<endl>>;
          }
        }


    -   nothing will print

        -   The value of ``low_battery`` is true so we enter the first ``if`` block.

    -   "Charging your phone"

        +   correct! ``low_battery`` stays true and we set ``power_outage`` to false.

    -   "Battery is charged"

        -   ``low_battery`` is true so we don't reach this ``else``.

    -   "There is no power"

        -   We change the value of ``power_outage`` to false before hand.
