Multiple Choice Exercises
-------------------------

.. mchoice:: mce_11_1
    :practice: T

    Select all the true statements.

    - In C++, anything done with a member function can also be done by a free-standing function

      + Though sometimes there may be an advantage of one over the other this process is doable and converting from one form to the other is a mechanical process

    - In a function that operates on 3 structures, 2 are accessed with dot notation
    
      + There is one implicit structure, and two structures that need to be accessed with dot notation.

    - The scope resolution operator should be used every time you work with data structures and implement member function inside the structure definition.

      - The scope resolution operator need not be used everytime one works with structures and is used to implement member functions outside the class definition.

    - The ``this`` keyword is used to refer to the current object

      + The ``this`` keyword is a pointer to the current object.

.. mchoice:: mce_11_2
    :practice: T

    What is the correct way to declare a member function called ``student_email`` outside the structure definition and takes a ``Student`` object as a parameter by reference?
    
    - ``Student::student_email(const Student& s1)``

      + This is the proper way to declare a member function ``student_email`` that passes a ``Student`` object by reference.

    - ``student_email(Student)``
    
      - This is not the proper way to pass a ``Student`` object and declare a member function.

    - ``Student::student_email(Student s1)``
    
      - Close! Look closely at the answer choices again and the methos of passing the parameter.

    - ``student_email(Student& s1)``
    
      - This is not the proper way to declare a member function.
      
.. mchoice:: mce_11_3
    :practice: T

    Which of the following options should replace the blank in the following code?

    .. code-block:: cpp

      struct StarWars {
        string name;
        int num_appearences;
        bool isJedi;
        
        bool isMainCast ();
      };

      ______________________ {
         if (character.num_appearences >= 3) {
            return true;
         }
         else {
             return false;
         }
      }
      
      int main () {
        StarWars character;
        character = (StarWars){ "Rey", 3, true};
        character.isMaincast();
      }

    - ``bool StarWars::isMainCast ()``

      + Correct!

    - ``void StarWars::isMainCast ()``

      - Pay close attention to the function implementation adn return type

    - ``bool isMainCast ()``

      - As the function was implemented outside the class definition a scope resolution operator must be used.

    - ``bool isMainCast (StarWars& character)``

      - As the function was implemented outside the class definition a scope resolution operator must be used. Additionally, the object is passed implicitly.

.. mchoice:: mce_11_4
    :practice: T

    What is the output of the code below?

    .. code-block:: cpp

      struct Cube {
        int mass;
        int density;
        
        
        //function to check if the current cude has a higher density than another
        int greater_density (const Cube& cube2) {
            if (density > cube2.density) {
               return true;
            }
            else  {
               return false;
            }
        }
      };

      int main() {
        Cube c;
        Cube c1;
        c.mass = 128;
        c1.mass = 120
        c.density = 2;
        c1.density = 50;
        cout << c.greater_density(c1) << endl;
      }

    - True

      - The output of a ``bool`` is either a 0 or 1.

    - False

      - The output of a ``bool`` is either a 0 or 1.

    - 0

      + Then density of c (2) is not greater than that of c1 (50).

    - 1

      - Is density of ``c`` greater than ``c1``?

.. mchoice:: mce_11_5
    :practice: T

    What are the values stored in the p1 object below?

    .. code-block:: cpp

      struct Penguin {
        int age;
        string gender;
        
        Penguin();
      };
      
      Penguin::Penguin () {
        age = 1;
        gender = "female";
      }

      int main() {
        Penguin p1;
      }

    - 1 and "female"

      + Correct! The constructor was called to store age as 1 and gender as female in p1.

    - No values, the constructor cannot be invoked as it is out of the struct

      - The scope resolution operator allows for a member function outside the structure definition to be invoked by the class type.

    - 0 and ""

      - In such a scenario a default constructor is not called. Pay attention to the constructor values implemented.

    - No values, nothing was assigned to ``age`` and ``gender`` and the constructor was never called

      - Upon creation of the Penguin p1 the constructor initialises the object automatically

.. mchoice:: mce_11_6
    :practice: T

     Will the following program run and if so, what does this program aptly depict?

    .. code-block:: cpp

      struct Penguin {
        int age;
        string gender;
        
        Penguin();
        Penguin(int age_in, string gender_in);
      };
      
      Penguin::Penguin () {
        age = 1;
        gender = "female";
      }
      
      Penguin::Penguin(int age_in, string gender_in) {
        age = age_in;
        gender = gender_in;
      }

      int main() {
        Penguin p1;
        Penguin p2(3, "male");
      }

    - This program does not run as the presence of two constructors will throw a compile error.

      - Constructor overloading is possible.

    - Friend constructors

      - "Friend" constructors are constructors that are private except to the friend class.

    - Constructor overriding

      - Overriding is the ability of an inherited class to rewrite the methods of the base class at runtime. Constructors cannot be overwritten

    - Overloading

      + Correct! The constructors are overloaded as they have the same the name but different number of arguments.

.. mchoice:: mce_11_7
    :practice: T

    What statements are true based on the following  ``Stundent.h`` header file?

    .. code-block:: cpp

      struct Student {
        // Instance variables
        int age, id;
        string year;
      
        // Constructors
        Student (int age, int id, string year);
        Student (string year);

        // Modifiers
        void increment (int age);

        // Functions
        void print () const;
        bool isJunior (const Student& student2) const;
        Student add (const Student& s2) const;
      };

    - The Student.cpp file will have the definitions of the member functions.

      + This is true!

    - Student.cpp needs to #include the header file.

      + This is true!

    - The Student.cpp file must implement the member functions in the same order as the declarations.

      - This is not necessary.

    - Header files contain the structure/function definitions and by splitting the program into multiple files one can compile the files seperately and link it to a single program later.

      + This is true!

.. mchoice:: mce_11_8
    :practice: T

    What is the output of the code below?

    .. code-block:: cpp

      struct Penguin {
        int age;
        string gender;
        
        Penguin();
        Penguin(int age_in, string gender_in);
      };
      
      Penguin::Penguin () {
        age = 1;
        gender = "female";
      }
      
      Penguin::Penguin(int age_in, string gender_in) {
        age = age_in;
        gender = gender_in;
      }

      int main() {
        Penguin p1;
        Penguin p2(3, "male");
        cout << p2.age << " " << p1.gender << endl;
      }

    - 3

      - p1 is initialised using the Penguin() constructor, its gender variable would not be null.
      
    - 3 female

      + Correct!
      
    - 1 male

      - Pay closer attention to the values being printed!

    - No output. The code won't compile.

      - Constructor overloading is allowed!
      
.. mchoice:: mce_11_9
    :practice: T

    What is the output of the code below?

    .. code-block:: cpp

      struct Point3D {
        int x, y, z;
      
        Point3D () {
          x = 4;
          y = 2;
          z = 3;
          cout << "Sum of relevant variables = " << x+x+y << endl;
        }
      };
      
      int main() {
      Point3D p1;
      }

    - Sum of relevant variables =

      - Take a closer look Point3D ( )

    - Sum of relevant variables = 9

      - Take a closer look at what is outputted in Point3D ( )

    - Sum of relevant variables = 10

      + Correct!

    - No output is printed.

      - Remember what you clearned about constructors and when they're called

.. mchoice:: mce_11_10
    :practice: T

    Select all the true statements.

    - When we call a member function we invoke the function on the data structure

      + When called, the member function is invoked on the data structure

    - In a member function, you should declare the implicit parameter to be const before the parameter list
    
      - The implicit parameter should be declared const after the parameter list

    - In the example ``x::y`` the scope resolution operator indicates that a function named ``y`` can be invoked on a structure ``x``

      + When defining a member function outside of the sturucture definition the ``::`` operator is used to indicate that an object of that class type can call the function is question.

    - Implicit variable access in member functions allows us to access member variables without the dot notation

      + Correct! Implicit variable access allows us to access variables directly

