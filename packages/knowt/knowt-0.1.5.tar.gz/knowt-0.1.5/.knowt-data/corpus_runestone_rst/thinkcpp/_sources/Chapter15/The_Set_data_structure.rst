The ``Set`` data structure
--------------------------

A data structure is a container for grouping a collection of data into a
single object. We have seen some examples already, including
``string``\ s, which are collections of characters, and
``vector``\ s which are collections of any type.

.. index::
   single: ordered set

An **ordered set** is a collection of items with two defining properties:

Ordering:
   The elements of the set have indices associated with them. We can use
   these indices to identify elements of the set.

Uniqueness:
   No element appears in the set more than once. If you try to add an
   element to a set, and it already exists, there is no effect.

In addition, our implementation of an ordered set will have the
following property:

Arbitrary size:
   As we add elements to the set, it expands to make room for new
   elements.

Both ``string``\ s and ``vector``\ s have an ordering; every element
has an index we can use to identify it. None of the data structures
we have seen so far have the properties of uniqueness or arbitrary size.

To achieve uniqueness, we have to write an ``add`` function that
searches the set to see if it already exists. To make the set expand as
elements are added, we can take advantage of the ``resize`` function on
``vector``\ s.

Here is the beginning of a class definition for a ``Set``.

::

   class Set {
   private:
     vector<string> elements;
     int numElements;

   public:
     Set (int n);

     int getNumElements () const;
     string getElement (int i) const;
     int find (const string& s) const;
     int add (const string& s);
   };

   Set::Set (int n)
   {
     vector<string> temp (n);
     elements = temp;
     numElements = 0;
   }

The instance variables are a ``vector`` of strings and an integer
that keeps track of how many elements there are in the set. Keep in mind
that the number of elements in the set, ``numElements``, is not the same
thing as the size of the ``vector``. Usually it will be smaller.

The ``Set`` constructor takes a single parameter, which is the initial
size of the ``vector``. The initial number of elements is always zero.

``getNumElements`` and ``getElement`` are accessor functions for the
instance variables, which are private. ``numElements`` is a read-only
variable, so we provide a ``get`` function but not a ``set`` function.

::

   int Set::getNumElements () const
   {
     return numElements;
   }

Why do we have to prevent client programs from changing
``getNumElements``? What are the invariants for this type, and how could
a client program break an invariant. As we look at the rest of the
``Set`` member function, see if you can convince yourself that they all
maintain the invariants.

When we use the ``[]`` operator to access the ``vector``, it checks to
make sure the index is greater than or equal to zero and less than the
length of the ``vector``. To access the elements of a set, though, we
need to check a stronger condition. The index has to be less than the
number of elements, which might be smaller than the length of the
``vector``.

::

   string Set::getElement (int i) const
   {
     if (i < numElements) {
       return elements[i];
     } else {
       cout << "Set index out of range." << endl;
       exit (1);
     }
   }

If ``getElement`` gets an index that is out of range, it prints an error
message (not the most useful message, I admit), and exits.

The interesting functions are ``find`` and ``add``. By now, the pattern
for traversing and searching should be old hat:

::

   int Set::find (const string& s) const
   {
     for (int i=0; i<numElements; i++) {
       if (elements[i] == s) return i;
     }
     return -1;
   }

So that leaves us with ``add``. Often the return type for something like
``add`` would be void, but in this case it might be useful to make it
return the index of the element.

::

   int Set::add (const string& s)
   {
     // if the element is already in the set, return its index
     int index = find (s);
     if (index != -1) return index;

     // if the vector is full, double its size
     if (numElements == elements.length()) {
       elements.resize (elements.length() * 2);
     }

     // add the new elements and return its index
     index = numElements;
     elements[index] = s;
     numElements++;
     return index;
   }

The tricky thing here is that ``numElements`` is used in two ways. It is
the number of elements in the set, of course, but it is also the index
of the next element to be added.

It takes a minute to convince yourself that that works, but consider
this: when the number of elements is zero, the index of the next element
is 0. When the number of elements is equal to the length of the
``vector``, that means that the vector is full, and we have to
allocate more space (using ``resize``) before we can add the new
element.

Here is a state diagram showing a ``Set`` object that initially contains
space for 2 elements.

Now we can use the ``Set`` class to keep track of the cities we find in
the file. In ``main`` we create the ``Set`` with an initial size of 2:

::

     Set cities (2);

Then in ``processLine`` we add both cities to the ``Set`` and store the
index that gets returned.

::

     int index1 = cities.add (city1);
     int index2 = cities.add (city2);

I modified ``processLine`` to take the ``cities`` object as a second
parameter.

.. activecode:: 15_7
   :language: cpp

   #include <iostream>
   #include <string>
   #include <vector>
   using namespace std;

   class Set {
   private:
     vector<string> elements;
     int numElements;

   public:
     Set (int n);

     int getNumElements () const;
     string getElement (int i) const;
     int find (const string& s) const;
     int add (const string& s);
   };

   Set::Set (int n)
   {
     vector<string> temp (n);
     elements = temp;
     numElements = 0;
   }

   int main() {
     Set cities(2);
     cities.add("Detroit");
     cities.add("Ann Arbor");
     cout << cities.getElement(0);
   }

   ====

   int Set::getNumElements () const {
     return numElements;
   }

   string Set::getElement (int i) const {
     if (i < numElements) {
       return elements[i];
     } 
     else {
      cout << "Set index out of range." << endl;
      exit (1);
     }
   }

   int Set::find (const string& s) const {
     for (int i=0; i<numElements; i++) {
       if (elements[i] == s) return i;
     }
     return -1;
   }

   int Set::add (const string& s) {
     int index = find (s);
     if (index != -1) return index;
     
     size_t num = numElements;

     if (num == elements.size()) {
       elements.resize (elements.size() * 2);
     }

     index = numElements;
     elements[index] = s;
     numElements++;
     return index;
   }


.. mchoice:: question15_7_1
   :multiple_answers:
   :answer_a: the set grows to accomodate any new elements we add
   :answer_b: the set is sorted in an order (ie alphabetically, numerically, e.t.c.)
   :answer_c: elements of the set have indices, which can be used to identify them
   :answer_d: there is a limit on how large a set can be
   :answer_e: there are no repeat elements in the set
   :correct: a,c,e
   :feedback_a: Correct! This is the "arbitrary size" property.
   :feedback_b: Incorrect! This is not a requirement of a set.
   :feedback_c: Correct! This is the "ordering" property.
   :feedback_d: Incorrect! This is not a requirement of a set... in fact, sets are always expanding with each added element!
   :feedback_e: Correct! This is the uniqueness property!

   Which of the following are properties of an ordered set?

.. mchoice:: question15_7_2
   :answer_a: numElements is a read-only variable.
   :answer_b: The user might pick a value for numElements that is out of range.
   :answer_c: numElements cannot be modified.
   :answer_d: We should provide a set function, we just haven't implemented it yet!
   :correct: a
   :feedback_a: Correct!
   :feedback_b: Incorrect! While this could happen, it just wouldn't make sense for the uer to interact with numElements at all!
   :feedback_c: Incorrect! numElements is modified, just not by the user.
   :feedback_d: Incorrect! There is no need for the user to have access to a set function.

   Why don't we provide a ``set()`` function for ``numElements``?

.. fillintheblank:: question15_7_3

    If the number of elements is 76, then the index of the next element is |blank|.

    - :(76): Correct!
      :.*: Incorrect! Go back and read to find the answer!

.. fillintheblank:: question15_7_4

    Suppose we have implemented the ``Set`` data structure as defined above, and we run the following code.

    ::
    
        Set cities(10);
        cities.add("Detroit");
        cities.add("Ann Arbor");
        cities.add("Ann Arbor");
        cities.add("East Lansing");
        cities.add("Grand Rapids");
        cities.add("Detroit");
        cities.add("Mackinac");
        cities.add("Mackinaw");
        string element = cities.getElement(4);  cout << element;
  
    Type the output exactly as it would appear in the terminal.

    - :(Mackinac): 
      :.*: Incorrect! Try modifying the active code!