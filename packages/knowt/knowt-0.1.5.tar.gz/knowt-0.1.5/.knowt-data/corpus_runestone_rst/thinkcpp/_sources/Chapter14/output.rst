Output
------

As usual when we define a new class, we want to be able to output
objects in a human-readable form. For ``Complex`` objects, we could use
two functions:

::

   void Complex::printCartesian ()
   {
     cout << getReal() << " + " << getImag() << "i" << endl;
   }

   void Complex::printPolar ()
   {
     cout << getMag() << " e^ " << getTheta() << "i" << endl;
   }

The nice thing here is that we can output any ``Complex`` object in
either format without having to worry about the representation. Since
the output functions use the accessor functions, the program will
compute automatically any values that are needed.

The following code creates a ``Complex`` object using the second
constructor. Initially, it is in Cartesian format only. When we invoke
``printCartesian`` it accesses ``real`` and ``imag`` without having to
do any conversions.

::

     Complex c1 (2.0, 3.0);

     c1.printCartesian();
     c1.printPolar();

When we invoke ``printPolar``, and ``printPolar`` invokes ``getMag``,
the program is forced to convert to polar coordinates and store the
results in the instance variables. The good news is that we only have to
do the conversion once. When ``printPolar`` invokes ``getTheta``, it
will see that the polar coordinates are valid and return ``theta``
immediately.

The output of this code is:

::

   2 + 3i
   3.60555 e^ 0.982794i

.. activecode:: fourteensix
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   The active code below uses the print functions for ``Complex`` objects.
   Feel free to modify the code and experiment around!
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

   int main() {
     Complex c1 (2.0, 3.0);
     c1.printCartesian();
     c1.printPolar();
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

.. mchoice:: question14_5_1
   :practice: T
   :answer_a: 5 e^ 0.927295i
   :answer_b: 3 + 4i
   :answer_c: 2 + 3i
   :answer_d: 5 e^ 1
   :correct: a
   :feedback_a: Correct!
   :feedback_b: Incorrect! Try using the active code above.
   :feedback_c: Incorrect! Try using the active code above.
   :feedback_d: Incorrect! Try using the active code above.

   What is the correct output of the code below?

   .. code-block:: cpp

      int main() {
        Complex c1 (3.0, 4.0);
        // c1.printCartesian();
        c1.printPolar();
      }
   