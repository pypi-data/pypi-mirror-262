A function on ``Complex`` numbers
---------------------------------

A natural operation we might want to perform on complex numbers is
addition. If the numbers are in Cartesian coordinates, addition is easy:
you just add the real parts together and the imaginary parts together.
If the numbers are in polar coordinates, it is easiest to convert them
to Cartesian coordinates and then add them.

Again, it is easy to deal with these cases if we use the accessor
functions:

::

   Complex add (Complex& a, Complex& b)
   {
     double real = a.getReal() + b.getReal();
     double imag = a.getImag() + b.getImag();
     Complex sum (real, imag);
     return sum;
   }

Notice that the arguments to ``add`` are not ``const`` because they
might be modified when we invoke the accessors. To invoke this function,
we would pass both operands as arguments:

::

     Complex c1 (2.0, 3.0);
     Complex c2 (3.0, 4.0);

     Complex sum = add (c1, c2);
     sum.printCartesian();

The output of this program is

::

   5 + 7i

.. activecode:: fourteenseven
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   The active code below uses the ``add`` function for ``Complex`` objects.
   As an exercise, write the ``subtract`` function for ``Complex`` objects
   in the commented area of the active code. If you get stuck, you can reveal 
   the extra problem at the end for help. Once you are finished, feel 
   free to modify the code and experiment around!
   ~~~~
   #include <iostream>
   #include <cmath>
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
   };

   Complex add (Complex& a, Complex& b);
   Complex subtract (Complex& a, Complex& b) {
     // ``subtract`` should subtract b from a and return
     // the difference of the two ``Complex`` objects.
     // Delete the existing code and write your implementation here.
     Complex c (0,0); return c;
   }

   int main() {
     Complex c1 (2.0, 3.0);
     Complex c2 (3.0, 4.0);
     Complex sum = add (c1, c2);
     sum.printCartesian();

     // Difference should be 1 + 1i
     Complex diff = subtract(c2, c1);
     diff.printCartesian();
   }
   ====
   Complex::Complex () { cartesian = false;  polar = false; }

   Complex::Complex (double r, double i) {
     real = r;  imag = i;
     cartesian = true;  polar = false;
   }

   void Complex::calculateCartesian () {
     real = mag * cos (theta);
     imag = mag * sin (theta);
     cartesian = true;
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

.. reveal:: 14_6_1
   :showtitle: Reveal Problem
   :hidetitle: Hide Problem

   .. parsonsprob:: question14_6_1
      :numbered: left
      :adaptive:

      Let's write the code for the ``subtract`` function,
      which should return the difference of two ``Complex`` objects.
      -----
      Complex subtract (Complex& a, Complex& b) {
      =====
      Complex subtract (Complex& a) {                         #paired
      =====
         double real = a.getReal() - b.getReal();
      =====
         double real = a.getReal() + b.getReal();                         #paired
      =====
         double imag = a.getImag() - b.getImag();
      =====
         Complex diff (real, imag);
      =====
         Complex diff (imag, real);                         #paired
      =====
         return diff;
      }
      =====
         return sum;                         #paired
      }

.. mchoice:: question14_6_2
   :practice: T
   :answer_a: 3.1i + 1.9i
   :answer_b: 1.9i + 3.1
   :answer_c: 3.0 + 1.9i
   :answer_d: 3.1 + 1.9i
   :correct: d
   :feedback_a: Incorrect! Try using the active code above.
   :feedback_b: Incorrect! Try using the active code above.
   :feedback_c: Incorrect! Try using the active code above.
   :feedback_d: Correct!

   What is the correct output of the code below?

   .. code-block:: cpp

      int main() {
        Complex c1 (2.5, 1.3);
        Complex c2 (3.9, 4.4);
        Complex c3 (9.5, 7.6);
        Complex sum = add (c1, c2);
        Complex diff = subtract(c3, sum);
        diff.printCartesian();
      }
   