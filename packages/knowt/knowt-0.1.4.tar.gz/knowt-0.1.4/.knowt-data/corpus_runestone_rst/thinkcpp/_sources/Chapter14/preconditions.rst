Preconditions
-------------

.. index::
   single: precondition

Often when you write a function you make implicit assumptions about the
parameters you receive. If those assumptions turn out to be true, then
everything is fine; if not, your program might crash.

To make your programs more robust, it is a good idea to think about your
assumptions explicitly, document them as part of the program, and maybe
write code that checks them.

For example, let’s take another look at ``calculateCartesian``. Is there
an assumption we make about the current object? Yes, we assume that the
``polar`` flag is set and that ``mag`` and ``theta`` contain valid data.
If that is not true, then this function will produce meaningless
results.

One option is to add a comment to the function that warns programmers
about the **precondition**.

::

   void Complex::calculateCartesian ()
   // precondition: the current object contains valid polar coordinates
       and the polar flag is set
   // postcondition: the current object will contain valid Cartesian
       coordinates and valid polar coordinates, and both the cartesian
       flag and the polar flag will be set
   {
     real = mag * cos (theta);
     imag = mag * sin (theta);
     cartesian = true;
   }

.. index::
   single: postcondition

At the same time, I also commented on the **postconditions**, the things
we know will be true when the function completes.

These comments are useful for people reading your programs, but it is an
even better idea to add code that *checks* the preconditions, so that we
can print an appropriate error message:

::

   void Complex::calculateCartesian ()
   {
     if (polar == false) {
       cout <<
       "calculateCartesian failed because the polar representation is invalid"
        << endl;
       exit (1);
     }
     real = mag * cos (theta);
     imag = mag * sin (theta);
     cartesian = true;
   }

The ``exit`` function causes the program to quit immediately. The return
value is an error code that tells the system (or whoever executed the
program) that something went wrong.

This kind of error-checking is so common that C++ provides a built-in
function to check preconditions and print error messages. If you include
the ``cassert`` header file, you get a function called ``assert`` that
takes a boolean value (or a conditional expression) as an argument. As
long as the argument is true, ``assert`` does nothing. If the argument
is false, assert prints an error message and quits. Here’s how to use
it:

::

   void Complex::calculateCartesian ()
   {
     assert (polar);
     real = mag * cos (theta);
     imag = mag * sin (theta);
     cartesian = true;
     assert (polar && cartesian);
   }

The first ``assert`` statement checks the precondition (actually just
part of it); the second ``assert`` statement checks the postcondition.

In my development environment, I get the following message when I
violate an assertion:

::

   Complex.cpp:63: void Complex::calculatePolar(): Assertion `cartesian' failed.
   Abort

There is a lot of information here to help me track down the error,
including the file name and line number of the assertion that failed,
the function name and the contents of the assert statement.

.. activecode:: fourteenten
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   The active code below uses the updated ``calculateCartesian`` with assert statements.
   Notice how because ``c1`` is not in polar, the assert statement in ``calculateCartesian``
   fails and thus we get an error.
   ~~~~
   #include <iostream>
   #include <cmath>
   #include <cassert>
   using namespace std;

   class Complex
   {
     double real, imag;
     double mag, theta;
     bool cartesian, polar;

   public:
     Complex ();
     Complex (double r, double i);
     void calculateCartesian ();
     double getReal ();
     double getImag ();
     void calculatePolar ();
     double getMag ();
     double getTheta ();
     void printCartesian ();
     void printPolar ();
     void setPolar (double m, double t);
     void setCartesian (double r, double i);
   };

   Complex add (Complex& a, Complex& b);
   Complex subtract (Complex& a, Complex& b);
   Complex mult (Complex& a, Complex& b);

   int main() {
     Complex c1 (5.4, 3.2);
     // This will output an error statement stating that 
     // "Assertion 'polar' failed."
     c1.calculateCartesian();
   }
   ====
   Complex::Complex () { cartesian = false;  polar = false; }

   Complex::Complex (double r, double i) {
     real = r;  imag = i;
     cartesian = true;  polar = false;
   }

   void Complex::calculateCartesian () {
     assert (polar);
     real = mag * cos (theta);
     imag = mag * sin (theta);
     cartesian = true;
     assert (polar && cartesian);
   }

   double Complex::getReal () {
     if (cartesian == false) calculateCartesian ();
     return real;
   }

   double Complex::getImag () {
     if (cartesian == false) calculateCartesian ();
     return imag;
   }

   void Complex::calculatePolar () {
     mag = sqrt(pow(real, 2) + pow(imag, 2));
     theta = atan(imag / real);
     polar = true;
   }

   double Complex::getMag () {
     if (polar == false) {
       calculatePolar ();
     }
     return mag;
   }

   double Complex::getTheta () {
     if (polar == false) {
       calculatePolar ();
     }
     return theta;
   }

   void Complex::printCartesian () {
     cout << getReal() << " + " << getImag() << "i" << endl;
   }

   void Complex::printPolar () {
     cout << getMag() << " e^ " << getTheta() << "i" << endl;
   }

   Complex add (Complex& a, Complex& b) {
     double real = a.getReal() + b.getReal();
     double imag = a.getImag() + b.getImag();
     Complex sum (real, imag);
     return sum;
   }

   Complex subtract (Complex& a, Complex& b) {
     double real = a.getReal() - b.getReal();
     double imag = a.getImag() - b.getImag();
     Complex diff (real, imag);
     return diff;
   }

   void Complex::setPolar (double m, double t) {
     mag = m;  theta = t;
     cartesian = false;  polar = true;
   }

   Complex mult (Complex& a, Complex& b) {
     double mag = a.getMag() * b.getMag();
     double theta = a.getTheta() + b.getTheta();
     Complex product;
     product.setPolar (mag, theta);
     return product;
   }

   void Complex::setCartesian (double r, double i) {
     real = r;    imag = i;
     cartesian = true;  polar = false;
   }

.. mchoice:: question14_9_1
   :multiple_answers:
   :answer_a: Assume assumptions are always true.
   :answer_b: Only check the preconditions.
   :answer_c: Document assumptions explicitly as part of the program.
   :answer_d: Write code that checks assumptions, like using assert statements.
   :correct: c,d
   :feedback_a: Incorrect! Assumptions can turn out to be true or false.
   :feedback_b: Incorrect! In order to maintain invariance, we must ensure that postconditions are met as well.
   :feedback_c: Correct!
   :feedback_d: Correct!

   Which of the following are ways that we can make our code more robust?

.. fillintheblank:: question14_9_2

    What function causes the program to quit immediately?

    - :Exit|exit: Correct!
      :.*: Incorrect! Try again.
