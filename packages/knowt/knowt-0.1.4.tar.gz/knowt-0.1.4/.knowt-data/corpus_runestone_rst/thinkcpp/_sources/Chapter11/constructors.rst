Constructors
------------

Another function we wrote in :numref:`time` was
``makeTime``:

::

   Time makeTime (double secs) {
     Time time;
     time.hour = int (secs / 3600.0);
     secs -= time.hour * 3600.0;
     time.minute = int (secs / 60.0);
     secs -= time.minute * 60.0;
     time.second = secs;
     return time;
   }

.. index::
   single: constructor

Of course, for every new type, we need to be able to create new objects.
In fact, functions like ``makeTime`` are so common that there is a
special function syntax for them. These functions are called
**constructors** and the syntax looks like this:

::

   Time::Time (double secs) {
     hour = int (secs / 3600.0);
     secs -= hour * 3600.0;
     minute = int (secs / 60.0);
     secs -= minute * 60.0;
     second = secs;
   }

First, notice that the constructor has the same name as the class, and
no return type. The arguments haven’t changed, though.

Second, notice that we don’t have to create a new time object, and we
don’t have to return anything. Both of these steps are handled
automatically. We can refer to the new object—the one we are
constructing—using the keyword ``this``, or implicitly as shown here.
When we write values to ``hour``, ``minute`` and ``second``, the
compiler knows we are referring to the instance variables of the new
object.

To invoke the constructor, you use syntax that is a cross between a
variable declaration and a function call:

::

     Time time (seconds);

This statement declares that the variable ``time`` has type ``Time``,
and it invokes the constructor we just wrote, passing the value of
``seconds`` as an argument. The system allocates space for the new
object and the constructor initializes its instance variables. The
result is assigned to the variable ``time``.

.. fillintheblank:: constructors_1

    The member function that initializes objects automatically when they are created is called a(n) __________.

    - :([Cc]onstructor|CONSTRUCTOR): Correct!
      :.*: Incorrect!

.. mchoice:: constructors_2
   :answer_a: They initialize the instance variables of an object.
   :answer_b: They have the same name as the class.
   :answer_c: They return an instance of an object.
   :answer_d: We refer to the objects they initialize implicitly, or using keyword this.
   :answer_e: They have the same name as the class, no return type and unchanged parameters.
   :correct: c
   :feedback_a: Incorrect! This statement is true!
   :feedback_b: Incorrect! This statement is true!
   :feedback_c: Correct! Constructors do not have a return type.
   :feedback_d: Incorrect! This statment is true!
   :feedback_e: Incorrect! This statement is true!

   Which statment is **false** about constructors?

.. fillintheblank:: constructors_3

    Write code to initialize the variable ``lunch`` that has type ``Time`` and a value of 1800 seconds.

    - :(\s*Time\s+lunch\s*\(\s*1800\s*\)\s*;?): Correct!
      :.*: Incorrect!
