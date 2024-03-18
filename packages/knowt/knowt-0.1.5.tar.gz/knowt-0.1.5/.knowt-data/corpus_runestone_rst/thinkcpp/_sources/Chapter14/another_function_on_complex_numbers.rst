Another function on ``Complex`` numbers
---------------------------------------

Another operation we might want is multiplication. Unlike addition,
multiplication is easy if the numbers are in polar coordinates and hard
if they are in Cartesian coordinates (well, a little harder, anyway).

In polar coordinates, we can just multiply the magnitudes and add the
angles. As usual, we can use the accessor functions without worrying
about the representation of the objects.

::

   Complex mult (Complex& a, Complex& b)
   {
     double mag = a.getMag() * b.getMag();
     double theta = a.getTheta() + b.getTheta();
     Complex product;
     product.setPolar (mag, theta);
     return product;
   }

A small problem we encounter here is that we have no constructor that
accepts polar coordinates. It would be nice to write one, but remember
that we can only overload a function (even a constructor) if the
different versions take different parameters. In this case, we would
like a second constructor that also takes two ``double``\ s, and we
can’t have that.

An alternative it to provide an accessor function that *sets* the
instance variables. In order to do that properly, though, we have to
make sure that when ``mag`` and ``theta`` are set, we also set the
``polar`` flag. At the same time, we have to make sure that the
``cartesian`` flag is unset. That’s because if we change the polar
coordinates, the cartesian coordinates are no longer valid.

::

   void Complex::setPolar (double m, double t)
   {
     mag = m;  theta = t;
     cartesian = false;  polar = true;
   }

As an exercise, write the corresponding function named ``setCartesian``.

To test the ``mult`` function, we can try something like:

::

     Complex c1 (2.0, 3.0);
     Complex c2 (3.0, 4.0);

     Complex product = mult (c1, c2);
     product.printCartesian();

The output of this program is

::

   -6 + 17i

.. activecode:: fourteeneight
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   The active code below uses the ``mult`` and ``setPolar`` functions.
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
     void setPolar (double m, double t);
   };

   Complex add (Complex& a, Complex& b);
   Complex subtract (Complex& a, Complex& b);
   Complex mult (Complex& a, Complex& b);

   int main() {
     Complex c1 (2.0, 3.0);
     Complex c2 (3.0, 4.0);
     Complex product = mult (c1, c2);
     product.printCartesian();
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

There is a lot of conversion going on in this program behind the scenes.
When we call ``mult``, both arguments get converted to polar
coordinates. The result is also in polar format, so when we invoke
``printCartesian`` it has to get converted back. Really, it’s amazing
that we get the right answer!

.. mchoice:: question14_7_1
   :practice: T
   :answer_a: 3.5 + 19.5i
   :answer_b: -3.5 + 19.5i
   :answer_c: -3.5 - 19.5i
   :answer_d: -3.5 + 19.5
   :correct: b
   :feedback_a: Incorrect! Try using the active code above.
   :feedback_b: Correct! 
   :feedback_c: Incorrect! Try using the active code above.
   :feedback_d: Incorrect! Try using the active code above.

   What is the correct output of the code below?

   .. code-block:: cpp

      int main() {
        Complex c1 (2.0, 3.0);
        Complex c2 (3.0, 4.0);
        Complex c3 (1.0, 0.0);
        Complex c4 (3.5, 2.5);
        Complex product = mult (c1, c2);
        Complex diff = subtract (c4, c3);
        Complex sum = add (product, diff);
        sum.printCartesian();
      }

.. activecode:: fourteennine
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   Now let's try implementing the ``setCartesian`` function. Write your 
   implementation in the commented area of the active code below.
   Read the comments in ``main`` to test out your code! If you get stuck, 
   you can reveal the extra problem at the end for help.
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
     void setPolar (double m, double t);
     void setCartesian (double r, double i);
   };

   void Complex::setCartesian (double r, double i) {
     // ``setCartesian`` should set real and imag to 
     // r and i respectively and set the cartesian flag.
     // Write your implementation here.
   }

   Complex add (Complex& a, Complex& b);
   Complex subtract (Complex& a, Complex& b);
   Complex mult (Complex& a, Complex& b);

   int main() {
     Complex c1 (2.0, 3.0);
     Complex c2 (3.0, 4.0);
     Complex product = mult (c1, c2);
     product.printCartesian();
     // Should output 1.5 + 2.7i
     product.setCartesian(1.5, 2.7);
     product.printCartesian();
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

.. reveal:: 14_7_1
   :showtitle: Reveal Problem
   :hidetitle: Hide Problem

   .. parsonsprob:: question14_7_2
      :numbered: left
      :adaptive:

      Let's write the code for the ``setCartesian`` function.
      -----
      void Complex::setCartesian (double r, double i) {
      =====
      Complex Complex::setCartesian (double r, double i) {                         #paired
      =====
         real = r;    imag = i;
      =====
         real = i;    imag = r;                         #paired
      =====
         cartesian = true;  polar = false;
      =====
         cartesian = false;  polar = true;                         #paired
      =====
      }
