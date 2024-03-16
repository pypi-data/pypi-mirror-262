Mixed Up Code Practice
----------------------

.. parsonsprob:: mucp_13_1
   :numbered: left
   :adaptive:
   :noindent:
   :practice: T

   Below is the enumerated type Days which maps days of the week to integers
   starting at 1. Use a switch statement to determine whether or not day
   is a weekend or not. Check for cases in numerical order.
   -----
   enum Day { MON = 1, TUE, WED, THU, FRI, SAT, SUN };
   =====
   int main () {
   =====
      Day day = SUN;
   =====
      switch (day > 5) {
   =====
         case 0:
   =====
            cout << "It is not the weekend :(" << endl;
   =====
            break;
   =====
         case 1:
   =====
            cout << "It is the weekend :)" << endl;
   =====
            break;
   =====
         default:
   =====
            cout << "Invalid input." << endl;
   =====
            break;
   =====
      }
   =====
   }
.. parsonsprob:: mucp_13_2
   :numbered: left
   :adaptive:
   :noindent:
   :practice: T

   Use a switch statement to check and print out whether a number is divisible by two.
   Prompt and get input from the user. If input isn't valid,
   print out the default statement "Invalid input." Check for cases in numerical order.
   -----
   int main () {
   =====
      int input;
   =====
      cout << "Please enter an integer: ";
   =====
      cin >> input;
   =====
      switch (input % 2) {
   =====
         case 0:
   =====
            cout << input << " is even!" << endl;
   =====
            break;
   =====
         case 1:
   =====
            cout << input << " is odd!" << endl;
   =====
            break;
   =====
         default:
   =====
            cout << "Invalid input." << endl;
   =====
            break;
   =====
      }
   =====
   }

.. parsonsprob:: mucp_13_3
   :numbered: left
   :adaptive:
   :noindent:
   :practice: T

   Use a switch statement to check and print out the maximum between two numbers.
   Prompt and get input from the user for two integers. If input isn't valid,
   print out the default statement "Invalid input." Check for cases in numerical order.
   -----
   int main () {
   =====
      int input1;
   =====
      int input2;
   =====
      cout << "Please enter first integer: ";
   =====
      cin >> input1;
   =====
      cout << "Please enter second integer: ";
   =====
      cin >> input2;
   =====
      switch (input1 > input2) {
   =====
         case 0:
   =====
            cout << "The maximum is " << input2 << endl;
   =====
            break;
   =====
         case 1:
   =====
            cout << "The maximum is " << input1 << endl;
   =====
         default:
   =====
            cout << "Invalid input." << endl;
   =====
            break;
   =====
      }
   =====
   }

.. parsonsprob:: mucp_13_4
   :numbered: left
   :adaptive:
   :practice: T

   Below is the pseudocode for the implementation of mergeSort. 
   Put the blocks in the correct order!
   -----
   Deck Deck::mergeSort () const {
   =====
   Deck::mergeSort () const {  #distractor
   =====
      find the midpoint of the deck
   =====
      divide the deck into two subdecks
   =====
      sort the subdecks using sort
   =====
      merge the two halves and return the result
   =====
      use a for loop to traverse half the deck  #distractor
   =====
      divide each subdeck into two more subdecks
   =====
   }

.. parsonsprob:: mucp_13_5
   :numbered: left
   :adaptive:

   Let's revisit the Dictionary data structure defined in the previous section.
   Write the struct definitions for Entry, which has member variables word and page,
   and for Dictionary, which has a vector of Entries. Put the necessary
   blocks of code in the correct order.
   -----
   struct Entry {
   =====
      string word;
   =====
      int page;
   =====
      Entry word;  #distractor
   =====
   };
   =====
   struct Dictionary {
   =====
      vector<Entry> entries;
   =====
      vector<Word> entries;  #distractor
   =====
      Entry entries;  #distractor
   =====
   };

.. parsonsprob:: mucp_13_6
   :numbered: left
   :adaptive:

   Assume our dictionary is currently unsorted. Let's write a Dictionary member function find 
   that takes a string word as a parameter and returns the index of its corresponding
   entry. If the word isn't in the dictionary, return -1. 
   Put the necessary blocks of code in the correct order.
   -----
   int Dictionary::find (string word) {
   =====
   int Dictionary::find (Entry word) {  #paired
   =====
      for (size_t i = 0; i < entries.size(); ++i) {
   =====
      for (size_t i = 1; i < entries.size(); ++i) {  #distractor
   =====
      for (size_t i = 1; i < Dictionary.entries.size(); ++i) {  #distractor
   =====
         if (entries[i].word == word) {
   =====
         if (i.word == word) {  #distractor
   =====
            return i;
   =====
         }
   =====
      }
   =====
      return -1;
   =====
   }

.. parsonsprob:: mucp_13_7
   :numbered: left
   :adaptive:

   Of course, all dictionaries are in some sort of order. In order to do this, we
   must first write the Dictionary member function findFirstWord, which takes a starting
   index as a parameter returns the index of the Entry with the highest priority alphabetically
   (i.e. the Entry with a word that would come first in the alphabet). 
   Put the necessary blocks of code in the correct order.
   -----
   int Dictionary::findFirstWord (int start) {
   =====
   int Dictionary::findFirstWord (string word) {  #paired
   =====
      int min = start;
   =====
      for (size_t i = start; i < entries.size(); ++i) {
   =====
      for (size_t i = 0; i < entries.size(); ++i) {  #distractor
   =====
         if (entries[i].word < entries[min].word) {
   =====
         if (entries[i].word > entries[min].word) {  #distractor
   =====
            min = i;
   =====
         }
   =====
      }
   =====
      return min;
   =====
   }

.. parsonsprob:: mucp_13_8
   :numbered: left
   :adaptive:

   We also need a swap function. Write the Dictionary member function
   swap which takes two indices as parameters and swaps the Entries
   at those indices. 
   Put the necessary blocks of code in the correct order.
   -----
   void Dictionary::swap (int a, int b) {
   =====
   void Dictionary::swap () {  #paired
   =====
      Entry temp = entries[a];
   =====
      entries[a] = entries[b];
   =====
      entries[b] = temp;
   =====
   }

.. parsonsprob:: mucp_13_9
   :numbered: left
   :adaptive:

   Now let's write the Dictionary member function alphabetize, which
   sorts the Entries in the Dictionary in alphabetical order. Use
   the findFirstWord and swap functions we defined earlier! 
   Put the necessary blocks of code in the correct order.
   -----
   void Dictionary::alphabetize () {
   =====
   int Dictionary::alphabetize () {  #paired
   =====
      for (size_t i = 0; i < entries.size(); ++i) {
   =====
      for (size_t i = 0; i < entries.size() - 1; ++i) {  #distractor
   =====
         int min = findFirstWord (i);
   =====
         int min = findFirstWord (0);  #distractor
   =====
         swap (i, min);
   =====
         swap (0, min);  #distractor
   =====
      }
   =====
   }

.. parsonsprob:: mucp_13_10
   :numbered: left
   :adaptive:

   Let's check to see if our sorting worked! Write the Dictionary
   member function printDictionary, which prints out the word in each 
   Entry.
   Put the necessary blocks of code in the correct order.
   -----
   void Dictionary::printDictionary () {
   =====
      for (size_t i = 0; i < entries.size(); ++i) {
   =====
         cout << entries[i].word << endl;
   =====
         cout << entries[i].Entry << endl;  #distractor
   =====
         cout << Entry.word << endl;  #distractor
   =====
      }
   =====
   }