Mixed Up Code Practice
----------------------

.. parsonsprob:: mucp_12_1
   :numbered: left
   :adaptive:
   :noindent:
   :practice: T

   Let's write the struct definition for Song. Song should have
   instance variables title, artist, and numLikes. Put the necessary
   blocks of code in the correct order.
   -----
   struct Song {
   =====
   Struct Song {  #distractor
   =====
      string title;
   =====
      string artist;
   =====
      int numLikes;
   =====
   };
   =====
   }  #distractor

.. parsonsprob:: mucp_12_2
   :numbered: left
   :adaptive:
   :noindent:
   :practice: T

   Let's make an album! Write the struct definition for
   Album, which should have instance variables name, year and
   a vector of Songs. Put the necessary
   blocks of code in the correct order.
   -----
   struct Album {
   =====
   string Album {  #distractor
   =====
      string title;  #distractor
   =====
      string name;
   =====
      int year;
   =====
      Song song;  #distractor
   =====
      vector&#60Song&#62 songs;
   =====
      vector&#60string&#62 Song;  #distractor
   =====
   };
   =====
   }  #distractor

.. parsonsprob:: mucp_12_3
   :numbered: left
   :adaptive:
   :noindent:
   :practice: T

   Two Songs are equal if the title and artist of the Songs are equal.
   Write the function songEqual, which takes two Songs as parameters
   and returns true if they are equal. Put the necessary
   blocks of code in the correct order.
   -----
   bool songEqual (const Song& a, const &Song b) {
   =====
   bool songEqual (Song const &a, Song const &b) {  #distractor
   =====
   bool Song::songEqual (const Song& song) {  #distractor
   =====
      if (a.title == b.title && a.artist == b.artist) { 
   =====
      if (title == b.title && artist == b.artist) {  #distractor
   =====
         return true;
   =====
      }
   =====
      else {
   =====
         return false;
   =====
      }
   =====
   }

.. parsonsprob:: mucp_12_4
   :numbered: left
   :adaptive:

   What if we'd like to search an album for our favorite song?
   Write the Album member function searchAlbum which takes a 
   Song as a parameter and returns the location of the Song in
   the album. If the song isn't found, return -1. Use the
   songEqual function we defined earlier! Put the necessary
   blocks of code in the correct order.
   -----
   int Album::searchAlbum (const Song& a) {
   =====
   int searchAlbum (const Album& album, const Song& a) {  #distractor
   =====
   bool searchAlbum (Song const &a) {  #distractor
   =====
      for (size_t i = 0; i < songs.size(); ++i) { 
   =====
      for (size_t i = 0; i < album.size(); ++i) {  #distractor
   =====
      for (size_t i = 0; i < Song.size(); ++i) {  #distractor
   =====
         if (songEqual (songs[i], a)) {
   =====
         if (songs[i] == a) {  #distractor
   =====
         if (album.song == a) {  #distractor
   =====
         if (Song[i] == a) {  #distractor
   =====
            return i;
   =====
            return true;  #distractor
   =====
         }
   =====
      }
   =====
      return -1;
   =====
      return false;  #distractor
   =====
   }

.. parsonsprob:: mucp_12_5
   :numbered: left
   :adaptive:

   What's the most popular Song within an Album? Let's write
   the Album member function mostLikedSong, which prints out
   the information of the most liked Song in the format "The most
   liked song is title by artist with numLikes likes." Put the necessary
   blocks of code in the correct order.
   -----
   void Album::mostLikedSong () {
   =====
   int Album::mostLikedSong () {  #distractor
   =====
   void Album::mostLikedSong (const Song& a) {  #distractor
   =====
      int maxIndex = 0;
   =====
      int maxLikes = 0;
   =====
      for (size_t i = 0; i < songs.size(); ++i) { 
   =====
      for (size_t i = 0; i < album.size(); ++i) {  #distractor
   =====
         if (songs[i].numLikes > maxLikes) {
   =====
            maxIndex = i;
   =====
            maxLikes = songs[i].numLikes;
   =====
            i = maxLikes;  #distractor
   =====
            maxLikes = numLikes;  #distractor
   =====
         }
   =====
      }
   =====
      cout << "The most liked song is " << songs[maxIndex].title;
   =====
      cout << " by " << songs[maxIndex].artist << " with ";
   =====
      cout << songs[maxIndex].numLikes << " likes." << endl;
   =====
   }

.. parsonsprob:: mucp_12_6
   :numbered: left
   :adaptive:
   :practice: T

   Let's write the struct definition for Product. Product should have
   instance variables name and price. Put the necessary
   blocks of code in the correct order.
   -----
   struct Product {
   =====
   struct product {  #distractor
   =====
      string name;
   =====
      double price;
   =====
      int price;  #distractor
   =====
   };
   =====
   }  #distractor

.. parsonsprob:: mucp_12_7
   :numbered: left
   :adaptive:
   :practice: T

   Let's make a shopping list! Write the struct definition for
   List, which should have instance variables type and
   a vector of Products. Put the necessary
   blocks of code in the correct order.
   -----
   struct List {
   =====
   Struct List {  #distractor
   =====
      string type;
   =====
      Product type;  #distractor
   =====
      vector&#60Product&#62 products;
   =====
      vector&#60&#62 Product;  #distractor
   =====
   };
   =====
   }  #distractor

.. parsonsprob:: mucp_12_8
   :numbered: left
   :adaptive:

   Two Products are equal if the name and price of the Products are equal.
   Write the function productEqual, which takes two Products as parameters
   and returns true if they are equal. What if we want to check to see if
   we have bananas in our shopping list? Write the List member function
   searchList, which takes a Product as a parameter and returns the location
   of the Product in the List. Return -1 if it's not in the List. Put the necessary
   blocks of code in the correct order.
   -----
   bool productEqual (const Product& a, const &Product b) {
   =====
   bool productEqual (Product const &a, Product const &b) {  #distractor
   =====
      if (a.name == b.name) {  #distractor
   =====
      if (a.name == b.name && a.price == b.price) {
   =====
         return true;
   =====
      }
   =====
      else {
   =====
         return false;
   =====
      }
   =====
   }
   =====
   int List::searchList (const Product& a) {
   =====
   int searchList (const Product& a) {  #distractor
   =====
      for (size_t i = 0; i < products.size(); ++i) { 
   =====
      for (size_t i = 0; i < numProducts; ++i) {  #distractor
   =====
         if (productEqual (products[i], a)) {
   =====
         if (album.song == a) {  #distractor
   =====
            return i;
   =====
         }
   =====
      }
   =====
      return -1;
   =====
      return 1;  #distractor
   =====
   }


.. parsonsprob:: mucp_12_9
   :numbered: left
   :adaptive:

   Time to checkout! Write the List member function totalPrice
   which calculates and returns the total price of all the Products.
   Put the necessary blocks of code in the correct order.
   -----
   double List::totalPrice () {
   =====
   double List : totalPrice () {  #distractor
   =====
   int totalPrice () {  #distractor
   =====
      double total = 0;
   =====
      double total;  #paired
   =====
      for (size_t i = 0; i < products.size(); ++i) {
   =====
      for (double i = 0; i < products.size(); ++i) {  #distractor
   =====
      for (size_t i = 0; i > products.size(); ++i) {  #distractor
   =====
         total += products[i].price;
   =====
         total += products.price;  #paired
   =====
      }
   =====
      return total;
   =====
   }

.. parsonsprob:: mucp_12_10
   :numbered: left
   :adaptive:

   Oops! We made a mistake and grabbed pineapple pizza. 
   What if we want to remove an Product from our List?
   Write the List member function removeProduct, which takes
   an index as a parameter and removes it. Then it fills
   the gap with the last product in the List. Put the necessary
   blocks of code in the correct order.
   -----
   =====
   void List::removeProduct (int index) {
   =====
   void removeProduct (int index) {  #distractor
   =====
   void List::removeProduct (const Product& a) {  #distractor
   =====
      products[index] = products[products.size() - 1];
   =====
      for (size_t i = 0; i < products.size(); ++i) {  #distractor
   =====
      }  #distractor
   =====
      Product remove = products[index];  #distractor
   =====
      products[i] = products[products.size() - 1];  #distractor
   =====
   }