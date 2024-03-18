Header files
------------

It might seem like a nuisance to declare functions inside the structure
definition and then define the functions later. Any time you change the
interface to a function, you have to change it in two places, even if it
is a small change like declaring one of the parameters ``const``.

.. index::
   single: header file

There is a reason for the hassle, though, which is that it is now
possible to separate the structure definition and the functions into two
files: the **header file**, which contains the structure definition, and
the implementation file, which contains the functions.

Header files usually have the same name as the implementation file, but
with the suffix ``.h`` instead of ``.cpp``. For the example we have been
looking at, the header file is called ``Time.h``, and it contains the
following:

::

   struct Time {
     // instance variables
     int hour, minute;
     double second;

     // constructors
     Time (int hour, int min, double secs);
     Time (double secs);

     // modifiers
     void increment (double secs);

     // functions
     void print () const;
     bool after (const Time& time2) const;
     Time add (const Time& t2) const;
     double convertToSeconds () const;
   };

Notice that in the structure definition I don’t include the prefix ``Time::``
at the beginning of every function name. The compiler knows that we are declaring 
functions that are members of the ``Time`` structure.

``Time.cpp`` contains the definitions of the member functions (I have
elided the function bodies to save space):

::

   #include <iostream>
   using namespace std;
   #include "Time.h"

   Time::Time (int h, int m, double s)  ...

   Time::Time (double secs) ...

   void Time::increment (double secs) ...

   void Time::print () const ...

   bool Time::after (const Time& time2) const ...

   Time Time::add (const Time& t2) const ...

   double Time::convertToSeconds () const ...

In this case the definitions in ``Time.cpp`` appear in the same order as
the declarations in ``Time.h``, although it is not necessary.

On the other hand, it is necessary to include the header file using an
``include`` statement. That way, while the compiler is reading the
function definitions, it knows enough about the structure to check the
code and catch errors.

.. note::
   Notice that *outside* of the structure definition, you **do** need to include the
   prefix ``Time::`` at the beginning of each function name!

Finally, ``main.cpp`` contains the function ``main`` along with any
functions we want that are not members of the ``Time`` structure (in
this case there are none):

::

   #include <iostream>
   using namespace std;
   #include "Time.h"

   int main () {
     Time currentTime (9, 14, 30.0);
     currentTime.increment (500.0);
     currentTime.print ();

     Time breadTime (3, 35, 0.0);
     Time doneTime = currentTime.add (breadTime);
     doneTime.print ();

     if (doneTime.after (currentTime)) {
       cout << "The bread will be done after it starts." << endl;
     }
     return 0;
   }

Again, ``main.cpp`` has to include the header file.

It may not be obvious why it is useful to break such a small program
into three pieces. In fact, most of the advantages come when we are
working with larger programs:

Reuse:
   Once you have written a structure like ``Time``, you might find it
   useful in more than one program. By separating the definition of
   ``Time`` from ``main.cpp``, you make is easy to include the ``Time``
   structure in another program.

Managing interactions:
   As systems become large, the number of interactions between
   components grows and quickly becomes unmanageable. It is often useful
   to minimize these interactions by separating modules like
   ``Time.cpp`` from the programs that use them.

Separate compilation:
   Separate files can be compiled separately and then linked into a
   single program later. The details of how to do this depend on your
   programming environment. As the program gets large, separate
   compilation can save a lot of time, since you usually need to compile
   only a few files at a time.

For small programs like the ones in this book, there is no great
advantage to splitting up programs. But it is good for you to know about
this feature, especially since it explains one of the statements that
appeared in the first program we wrote:

::

   #include <iostream>
   using namespace std;

``iostream`` is the header file that contains declarations for ``cin``
and ``cout`` and the functions that operate on them. When you compile
your program, you need the information in that header file.

The implementations of those functions are stored in a library,
sometimes called the “Standard Library” that gets linked to your program
automatically. The nice thing is that you don’t have to recompile the
library every time you compile a program. For the most part the library
doesn’t change, so there is no reason to recompile it.

.. mchoice:: header_files_1
   :answer_a: the file that contains structure/function definitions
   :answer_b: the file that contains structure/function implementation
   :answer_c: the file that contains int main()
   :answer_d: the first file that you write for any given project
   :correct: a
   :feedback_a: Correct! 
   :feedback_b: Incorrect! This is called the implementation file.
   :feedback_c: Incorrect! Header files are compiled separately and later linked to int main().
   :feedback_d: Incorrect! You are not required to write your programs in any specific order.

   What is a header file?

.. mchoice:: header_files_2


   If I have defined a structure in ``header.h``, how would I include it in the implementation file?

   - ``#include <header.h>``

     - Incorrect! This is how we include standard library headers.

   - ``#include <"header.h">``

     - Incorrect! You should get rid of those brackets!

   - ``#include header.h``

     - Incorrect! You're missing quotes!

   - ``#include "header.h"``

     + Correct!


.. mchoice:: header_files_3
   :answer_a: Files can be compiled separately and linked to a single program later.
   :answer_b: Separate compilation can be time-consuming, since you're working with more files.
   :answer_c: It minimizes interactions between components.
   :answer_d: It's easier to include your implementation in other program, besides your main.
   :correct: b
   :feedback_a: Incorrect! This is actually true!
   :feedback_b: Correct! Separate compilation actually saves time, since you only need to compile a few files at a time!
   :feedback_c: Incorrect! This is actually true!
   :feedback_d: Incorrect! This is actually true!

   Which is **false** about breaking a program into three pieces?
