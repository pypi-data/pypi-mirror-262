Mixed Up Code Practice
----------------------

Answer the following **Mixed-Up Code** questions to assess what you have learned in this chapter.


.. parsonsprob:: mucp_11_1
   :numbered: left
   :adaptive:
   :noindent:
   :practice: T

     Construct a block of code that would make the print function into a member function.
   
     .. code-block:: cpp
     
        struct Student {
             int id, year;
             string name;
        };

        void printStudent (const Student& stu) {
             cout << stu.id << ":" << stu.year << ":" << stu.name << endl;
        }

        int main ( ) {
              Student s1 = { 56673, 2023, "Bob" };
              printStudent (s1);
        }

   -----
   struct Student {
   =====
   int id, year;
   string name;
   =====
   void print ();
   =====
   };
   =====
   } #distractor
   =====
   void Student::print () {
   =====
   void Student::print (const Student& stu) { #distractor
   =====
   Student stu = *this;
   =====
   cout << stu.id << ":" << stu.year << ":" << stu.name << endl;
   }
   =====
   int main () {
   Student s1 = { 56673, 2023, "Bob" };
   =====
   printStudent (s1); #distractor
   =====
   s1.print();
   =====
   }

.. parsonsprob:: mucp_11_2
   :numbered: left
   :adaptive:
   :noindent:
   :practice: T

   Let's make an album! Write the struct definition for
   Album, which should have instance variables name and year.
   Include a member function called check that returns true if
   the song was released after 2015.
   -----
   struct Album {
   =====
   string Album {  #distractor
   =====
      string name;
   =====
      int year;
   =====
      bool check ();
   =====
      void check (); #paired
   =====
   };
   =====
   void Album::check () { #distractor
   =====
   bool Album::check () {
   =====
   if (year > 2015) {
     return true;
   }
   else {
     return false;
   }
   =====
   }

.. parsonsprob:: mucp_11_3
   :numbered: left
   :adaptive:
   :noindent:
   :practice: T

   Put the necessary blocks of code in the correct order to establish
   the convertToSeconds member function.
   -----
   double convertToSeconds (const Time& time) { #distractor
   =====
   double Time::convertToSeconds () const {
   =====
   double Time::convertToSeconds () { #distractor
   =====
   int minutes = time.hour * 60 + time.minutes;
   double seconds = minutes * 60 + time.second;
   =====
   int minutes = hour * 60 + minutes;
   double seconds = minutes * 60 + second; #paired
   =====
    return seconds;
   }
   =====
   

.. parsonsprob:: mucp_11_4
   :numbered: left
   :adaptive:

   Create the Student::is_older() function as it would be defined INSIDE
   of the Student structure definition. This function checks if the current
   Student is older than another Student. The function is invoked on the
   current Student.

   -----
   bool is_older(const Student& stu) const {
   =====
   bool is_older(Student& stu) { #distractor
   =====
   bool Student::is_older(const Student& stu, const Student& s1) { #distractor
   =====
   bool Student::is_older(const Student& stu) { #distractor
   =====
   Student stu = *this; #distractor
   =====
   if (age > stu.age) {return true;}
   =====
   if (stu.age > s1.age) {return true;} #paired
   =====
   else {return false;}
   =====
   }; #distractor
   =====
   }
 
.. parsonsprob:: mucp_11_5
   :numbered: left
   :adaptive:

   Put the necessary blocks of code in the correct order to initialise
   a constructor for type Days that takes in the number of days and
   initialises the member variables days, weeks, years.
   -----
   Days::Days (int num_days) {
   =====
   void Days::Days (int num_days) { #distractor
   =====
   Construct::Days (int num_days) { #distractor
   =====
   Days (int num_days) { #distractor
   =====
   years = num_days / 365;
   =====
   Days day;
   =====
   num_days -= years * 365;
   =====
   weeks = num_days / 7;
   =====
   num_days -= weeks * 60.0;
   =====
   days = num_days;
   =====
   }; #distractor
   =====
   }

.. parsonsprob:: mucp_11_6
   :numbered: left
   :adaptive:
   :practice: T

   Let's write two constructors for Student. One with no arguments and
   one with arguments. Put the necessary blocks of code in
   the correct order.
   -----
   Student::Student () {
   =====
   void Student::Student () {
   =====
   id = 123456789;
   year = 2020;
   name = "Alice";
   }
   =====
   stu.id = 123456789;
   stu.year = 2020;
   stu.name = "Alice";
   }                     #distractor
   =====
   Student::Student (int id_in, int year_in, string name_in) {
   =====
   Student::Student construct(int id_in, int year_in, string name_in) {
   =====
   id = id_in;
   =====
   year = year_in;
   =====
   name = name_in;
   =====
   };  #distractor
   =====
   }

.. parsonsprob:: mucp_11_7
   :numbered: left
   :adaptive:
   :practice: T

   Implement two constructors for the Penguin structure. One should
   be a default constructor, the other should take arguments. The
   weight needs to be converted from pounds to kilograms in the second constructor
   -----
   struct Penguin {
   =====
   int age;
   int weight;
   =====
   Penguin ();
   =====
   void Penguin (); #paired
   =====
   Penguin (int age_in; int weight_in);
   =====
   void Penguin (int age_in; int weight_in); #distractor
   =====
   };
   =====
   Penguin::Penguin () {
   =====
   age = 1;
   weight = 24;
   =====
   }
   =====
   Penguin::Penguin (int age_in, int weight_in) {
   =====
   age = age_in;
   weight = weight_in;
   =====
   penguin.age = age_in;
   penguin.weight = weight_in; #distractor
   =====
   }


.. parsonsprob:: mucp_11_8
   :numbered: left
   :adaptive:

   Put the necessary blocks of code in the correct order to make the
   AddDays function below a member function a member function.
   
   Days AddDays (const Days& d1, const Days& d2) {
   int days = convertToDays (d1) + convertToDays(d2);
   return makeDays (days);
   }
   -----
   Days Days::add (const Days& d2) const {
   =====
   Days Days::add (const Days& d2) { #distractor
   =====
   Days Days::add () { #distractor
   =====
   int days = convertToDays () + d2.convertToDays ();
   =====
   int days = d1.convertToDays () + d2.convertToDays (); #distractor
   =====
   Days day (days);
   =====
   return day;
   }


.. parsonsprob:: mucp_11_9
   :numbered: left
   :adaptive:

   
   Put the necessary blocks of code in the correct order to create a struct
   Penguin that stores name and age. In addition have 2 constructors and
   declare Penguins in main such that both are called.
   
   -----
   struct Penguin {
    int age;
    string name;
   =====
    Penguin ();
    Penguin (int age_in, string name);
   };
   =====
    void Penguin ();
    void Penguin (int age_in, string name);
   };                                         #distractor
   =====
   Penguin::Penguin () {
   age = 1;
   name = "Alice";
   }
   =====
   Penguin::Penguin () const {
   p1.age = 1;
   p1.name = "Alice";
   }                                     #distractor
   =====
   Penguin::Penguin (int age_in, string name_in) {
   age = age_in;
   name = name_in;
   }
   =====
   void Penguin::Penguin (int age_in, string name_in) const {
   age = age_in;
   name = name_in;
   }                                #distractor
   =====
   Penguin::Penguin (int age_in, string name_in) {
   p1.age = age_in;
   p1.name = name_in;
   }                                    #distractor
   =====
   int main () {
   =====
   Penguin p1 ();
   Penguin p2 (3, "Bob");
   =====
   Penguin p1 ();
   Penguin p2 (age_in, name_in);        #distractor
   =====
   }

.. parsonsprob:: mucp_11_10
   :numbered: left
   :adaptive:

   Put the necessary blocks of code in the correct order in order to write
   a header (.h) file for the struct Student.
   
   -----
   struct Student {
   =====
   // instance variables
   int id, year;
   string name;
   =====
   // constructors
   Student (int id, int year, string name);
   Student ();
   =====
   // constructors
   Student::Student () const;
   Student::Student (int id, int year, string name);      #distractor
   =====
   // functions
   void print () const;
   bool after (const Student& stu) const;
   =====
   int main () {                        #distractor
   =====
   Student s1;                  #distractor
   =====
   }                            #distractor
   =====
   };
