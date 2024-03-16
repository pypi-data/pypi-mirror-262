Accessor functions
------------------

By convention, accessor functions have names that begin with ``get`` and
end with the name of the instance variable they fetch. The return type,
naturally, is the type of the corresponding instance variable.

In this case, the accessor functions give us an opportunity to make sure
that the value of the variable is valid before we return it. Here’s what
``getReal`` looks like:

::

   double Complex::getReal ()
   {
     if (cartesian == false) calculateCartesian ();
     return real;
   }

If the ``cartesian`` flag is true then ``real`` contains valid data, and
we can just return it. Otherwise, we have to call ``calculateCartesian``
to convert from polar coordinates to Cartesian coordinates:

::

   void Complex::calculateCartesian ()
   {
     real = mag * cos (theta);
     imag = mag * sin (theta);
     cartesian = true;
   }

Assuming that the polar coordinates are valid, we can calculate the
Cartesian coordinates using the formulas from the previous section. Then
we set the ``cartesian`` flag, indicating that ``real`` and ``imag`` now
contain valid data.

As an exercise, write a corresponding function called ``calculatePolar``
and then write ``getMag`` and ``getTheta``. One unusual thing about
these accessor functions is that they are not ``const``, because
invoking them might modify the instance variables.

.. activecode:: fourteenfour
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   Take a look at the active code below, which uses the ``getReal``
   accessor function. 
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
     Complex () { cartesian = false;  polar = false; }
     Complex (double r, double i)
     {
       real = r;  imag = i;
       cartesian = true;  polar = false;
     }
     void calculateCartesian ()
     {
       real = mag * cos (theta);
       imag = mag * sin (theta);
       cartesian = true;
     }
     double getReal ()
     {
       if (cartesian == false) calculateCartesian ();
       return real;
     }
     double getImag ()
     {
       if (cartesian == false) calculateCartesian ();
       return imag;
     }
   };

   int main() {
     Complex c1 (5.0, 3.5);
     cout << c1.getReal() << ", " << c1.getImag() << endl;
   }

.. activecode:: fourteenfive
   :language: cpp
   :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

   Write your implementation of ``calculatePolar`` in the commented area of the active 
   code below. Once you're done with that, write the ``getMag`` and ``getTheta`` 
   accessor functions. Read the comments in ``main`` to see how we'll test if your
   functions works. If you get stuck, you can reveal the extra problem at the end for help. 
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
   };

   void Complex::calculatePolar () {
     // ``calculatePolar`` should convert the real and imaginary parts
     // into magnitude and theta. Use the formula in the previous section.
     // Write your implementation here.
   }

   double Complex::getMag () {
     // ``getMag`` should return the magnitude.
     // Delete the return 0 and write your implementation here.
     return 0;
   }

   double Complex::getTheta () {
     // ``getMag`` should return the theta.
     // Delete the return 0 and write your implementation here.
     return 0;
   }

   int main() {
     Complex c1 (0.0, 1.0);
     // Magnitude should be 1, theta should be pi/2, or about 1.5708
     cout << c1.getMag() << ", " << c1.getTheta() << endl;
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

.. reveal:: 14_4_1
   :showtitle: Reveal Problem
   :hidetitle: Hide Problem

   .. parsonsprob:: question14_4_1
      :numbered: left
      :adaptive:

      Let's write the code for the ``calculatePolar`` function. 
      Follow the format of the function ``calculateCartesian``.
      -----
      void Complex::calculatePolar () {
      =====
      void Complex::calculateCartesian () {                         #paired
      =====
         mag = sqrt(pow(real, 2) + pow(imag, 2));
      =====
         mag = pow(real, 2) + pow(imag, 2);                         #paired
      =====
         theta = atan(imag / real);
      =====
         polar = true;
      }
      =====
         cartesian = true;                                          #paired
      }

.. reveal:: 14_4_2
   :showtitle: Reveal Problem
   :hidetitle: Hide Problem

   .. parsonsprob:: question14_4_2
      :numbered: left
      :adaptive:

      Let's write the code for the ``getMag`` function,
      which should return the magnitude of a ``Complex`` object.
      -----
      double Complex::getMag () {
      =====
      void Complex::getMag () {                         #paired
      =====
         if (polar == false) {
      =====
            calculatePolar ();
         }
      =====
         return mag;
      }

.. reveal:: 14_4_3
   :showtitle: Reveal Problem
   :hidetitle: Hide Problem

   .. parsonsprob:: question14_4_3
      :numbered: left
      :adaptive:

      Let's write the code for the ``getTheta`` function,
      which should return the magnitude of a ``Complex`` object.
      -----
      double Complex::getTheta () {
      =====
      double Complex::getMag () {                         #paired
      =====
         if (polar == false) {
      =====
            calculatePolar ();
         }
      =====
            calculateCartesian ();                         #paired
         }
      =====
         return theta;
      }