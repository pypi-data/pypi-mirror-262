Getting user input
------------------

The programs we have written so far are pretty predictable; they do the
same thing every time they run. Most of the time, though, we want
programs that take input from the user and respond accordingly.

There are many ways to get input, including keyboard input, mouse
movements and button clicks, as well as more exotic mechanisms like
voice control and retinal scanning. In this text we will consider only
keyboard input.

In the header file ``iostream``, C++ defines an object named ``cin``
that handles input in much the same way that ``cout`` handles output. To
get an integer value from the user:

::

     int x;
     cin >> x;

The ``>>`` operator causes the program to stop executing and wait for
the user to type something. If the user types a valid integer, the
program converts it into an integer value and stores it in ``x``.

If the user types something other than an integer, C++ doesn’t report an
error, or anything sensible like that. Instead, it puts some meaningless
value in ``x`` and continues.

.. index::
   single: stream state

Fortunately, there is a way to check and see if an input statement
succeeds. We can invoke the ``good`` function on ``cin`` to check what
is called the **stream state**. ``good`` returns a ``bool``: if true,
then the last input statement succeeded. If not, we know that some
previous operation failed, and also that the next operation will fail.

Thus, getting input from the user might look like this:

.. activecode:: getting_user_input_AC_1
  :language: cpp
  :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
  :stdin: 42

  The active code below is an example of what getting input from the
  user might look like. Feel free to change 42 to other values!
  ~~~~
  #include <iostream>
  using namespace std;

  int main () {
      int x;

      // prompt the user for input
      cout << "Enter an integer: ";

      // get input
      cin >> x;

      // check and see if the input statement succeeded
      if (cin.fail()) {
          cout << "That was not an integer." << endl;
          return -1;
      }

      // print the value we got from the user
      cout << x << endl;
      return 0;
  }

``cin`` can also be used to input a ``string``:

::

     string name;

     cout << "What is your name? ";
     cin >> name;
     cout << name << endl;

Unfortunately, this statement only takes the first word of input, and
leaves the rest for the next input statement. So, if you run this
program and type your full name, it will only output your first name.

Because of these problems (inability to handle errors and funny
behavior), I avoid using the ``>>`` operator altogether, unless I am
reading data from a source that is known to be error-free.

Instead, I use a function in the header ``string`` called ``getline``.

::

     string name;

     cout << "What is your name? ";
     getline (cin, name);
     cout << name << endl;

The first argument to ``getline`` is ``cin``, which is where the input
is coming from. The second argument is the name of the ``string`` where
you want the result to be stored.

``getline`` reads the entire line until the user hits Return or Enter.
This is useful for inputting strings that contain spaces.

.. activecode:: getting_user_input_AC_2
  :language: cpp
  :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
  :stdin: Harry Potter

  The active code below is an example of what getting input from the
  user might look like using ``getline``. Feel free to change "Harry Potter"
  to other values!
  ~~~~
  #include <iostream>
  #include <string>
  using namespace std;

  int main () {
     string name;

     cout << "What is your full name? ";
     getline (cin, name);
     cout << "Hello " << name << "!" << endl;
  }

In fact, ``getline`` is generally useful for getting input of any kind.
For example, if you wanted the user to type an integer, you could input
a string and then check to see if it is a valid integer. If so, you can
convert it to an integer value. If not, you can print an error message
and ask the user to try again.

To convert a string to an integer you can use the ``atoi`` function
defined in the header file ``cstdlib``. We will get to that in
:numref:`parsing`.

.. mchoice:: getting_user_input_1
   :practice: T

   What is the difference between ``cin`` and ``getline`` for a string?

   - ``getline`` only takes the first word of input while ``cin`` reads the entire line until the user hits Return or Enter.

     - Try again!

   - ``cin`` only takes the first word of input while ``getline`` reads the entire line until the user hits Return or Enter.

     + Correct!

   - ``cin`` only takes the first two words of input while ``getline`` reads the entire line until there is a space.

     - Try again!

.. mchoice:: getting_user_input_2
   :practice: T

   The user types in ``John Doe``. What prints?

   .. code-block:: cpp

      int main() {
        char name;
        cout << "What is your name? ";
        cin >> name;
        cout << name << endl;
      }

   - ``John``

     - Try again! Pay attention to the data type of name.

   - ``J``

     + Correct!

   - ``John Doe``

     - Try again! Pay attention to the manner of getting user input.


.. mchoice:: getting_user_input_3
   :practice: T

   The user types in ``John Doe``. What prints?

   .. code-block:: cpp

      int main() {
        string name;
        cout << "What is your name? ";
        cin >> name;
        cout << name << endl;
      }

   - ``John``

     + Correct!

   - ``J``

     - Try again! Pay attention to the data type of name.

   - ``John Doe``

     - Try again! Pay attention to the manner of getting user input.


.. mchoice:: getting_user_input_4
   :practice: T


   The user types in ``John Doe``. What prints?

   .. code-block:: cpp

      int main() {
        string name;
        cout << "What is your name? ";
        getline (cin, name);
        cout << name << endl;
      }

   - ``John``

     - Try again! Pay attention to the manner of getting user input.

   - ``J``

     - Try again! Pay attention to the manner of getting user input.

   - ``John Doe``

     + Correct!


.. mchoice:: getting_user_input_5
   :practice: T

   The user types in ``John Doe`` and then ``530 S State St.``. What prints?

   .. code-block:: cpp

      int main() {
        string first_name;
        string last_name;
        string address;
        cout << "What is your name? ";
        cin >> first_name >> last_name;
        cout << "What is your address? ";
        getline (cin, address);
        cout << first_name << " " << last_name << " lives at " << address << endl;
      }

   - ``John Doe lives at 530 S State St.``

     + Correct!

   - ``J D lives at 530 S State St.``

     - Try again! Pay attention to the manner of getting user input.

   - ``John Doe lives at 530``

     - Try again! Pay attention to the manner of getting user input.

