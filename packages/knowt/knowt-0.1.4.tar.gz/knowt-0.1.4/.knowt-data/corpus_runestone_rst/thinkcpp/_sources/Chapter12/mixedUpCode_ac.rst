Activecode Exercises
----------------------

Answer the following **Activecode** questions to assess what you have learned in this chapter.

.. tabbed:: mucp_12_1_ac

    .. tab:: Question

        .. activecode:: mucp_12_1_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the struct definition for ``Song``. Song should have
            instance variables title, artist, and numLikes. 
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_12_1_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to define the ``Song`` struct.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Song {
                string title;
                string artist;
                int numLikes;
            };


.. tabbed:: mucp_12_2_ac

    .. tab:: Question

        .. activecode:: mucp_12_2_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's make an album! Write the struct definition for
            ``Album``, which should have instance variables name, year and
            a vector of Songs. 
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_12_2_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to define the ``Album`` struct.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            struct Song {
                string title;
                string artist;
                int numLikes;
            };

            struct Album {
                string name;
                int year;
                vector&#60Song&#62 songs;
            };


.. tabbed:: mucp_12_3_ac

    .. tab:: Question

        .. activecode:: mucp_12_3_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Two Songs are equal if the title and artist of the Songs are equal.
            Write the function ``songEqual``, which takes two Songs as parameters
            and returns true if they are equal. 
            ~~~~
            #include <iostream>
            using namespace std
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_12_3_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the ``songEqual`` function.
            ~~~~
            #include <iostream> 
            using namespace std

            struct Song {
                string title;
                string artist;
                int numLikes;
            };

            bool songEqual (const Song& a, const &Song b) {
                if (a.title == b.title && a.artist == b.artist) { 
                    return true;
                }
                else {
                    return false;
                }
            }


.. tabbed:: mucp_12_4_ac

    .. tab:: Question
        
        .. activecode:: mucp_12_4_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            What if we'd like to search an album for our favorite song?
            Write the ``Album`` member function searchAlbum which takes a 
            Song as a parameter and returns the location of the Song in
            the album. If the song isn't found, return -1. Use the
            songEqual function we defined earlier!
            ~~~~
            #include <iostream> 
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_12_4_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the ``Album`` member function.
            ~~~~
            #include <iostream> 
            #include <vector>
            using namespace std;

            struct Song {
                string title;
                string artist;
                int numLikes;
            };
                    
            struct Album {
                string name;
                int year;
                vector<Song> songs;
            };

            int Album::searchAlbum (const Song& a) {
                for (size_t i = 0; i < songs.size(); ++i) { 
                    if (songEqual (songs[i], a)) {
                        return i;
                    }
                }
                return -1;
            }


.. tabbed:: mucp_12_5_ac

    .. tab:: Question

        .. activecode:: mucp_12_5_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            What's the most popular Song within an Album? Let's write
            the ``Album`` member function mostLikedSong, which prints out
            the information of the most liked Song in the format "The most
            liked song is title by artist with numLikes likes." 
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_12_5_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the ``Album`` member function. 
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            struct Song {
                string title;
                string artist;
                int numLikes;
            };

            struct Album {
                string name;
                int year;
                vector<Song> songs;
            };

            void Album::mostLikedSong () {
                int maxIndex = 0;
                int maxLikes = 0;
                for (size_t i = 0; i < songs.size(); ++i) { 
                    if (songs[i].numLikes > maxLikes) {
                        maxIndex = i;
                        maxLikes = songs[i].numLikes;
                    }
                }
                cout << "The most liked song is " << songs[maxIndex].title;
                cout << " by " << songs[maxIndex].artist << " with ";
                cout << songs[maxIndex].numLikes << " likes." << endl;
            }


.. tabbed:: mucp_12_6_ac

    .. tab:: Question

        .. activecode:: mucp_12_6_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write the struct definition for ``Product``. ``Product`` should have
            instance variables name and price.
            ~~~~
            #include <iostream>
            using namespace std;
            // YOUR CODE HERE

    
    .. tab:: Answer

        .. activecode:: mucp_12_6_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to define the ``Product`` struct.
            ~~~~
            #include <iostream>
            using namespace std;

            struct Product {
                string name;
                double price;
            };


.. tabbed:: mucp_12_7_ac

    .. tab:: Question

        .. activecode:: mucp_12_7_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's make a shopping list! Write the struct definition for
            ``List``, which should have instance variables type and
            a vector of Products. 
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_12_7_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to define the ``List`` struct.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            struct Product {
                string name;
                double price;
            };

            struct List {
                string type;
                vector&#60Product&#62 products;
            };


.. tabbed:: mucp_12_8_ac

    .. tab:: Question

        .. activecode:: mucp_12_8_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Two Products are equal if the name and price of the Products are equal.
            Write the function productEqual, which takes two Products as parameters
            and returns true if they are equal. What if we want to check to see if
            we have bananas in our shopping list? Write the List member function
            ``searchList``, which takes a Product as a parameter and returns the location
            of the Product in the List. Return -1 if it's not in the List. 
            ~~~~
            #include <iostream>
            #include <vector> 
            using namespace std;
            // YOUR CODE HERE

    
    .. tab:: Answer

        .. activecode:: mucp_12_8_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the ``searchList`` member function.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            
            struct Product {
                string name;
                double price;
            };

            bool productEqual (const Product& a, const &Product b) {
                if (a.name == b.name && a.price == b.price) {
                    return true;
                }
                else {
                    return false;
                }
            }

            int List::searchList (const Product& a) {
                for (size_t i = 0; i < products.size(); ++i) { 
                    if (productEqual (products[i], a)) {
                        return i;
                    }
                }
                return -1;
            }


.. tabbed:: mucp_12_9_ac

    .. tab:: Question

        .. activecode:: mucp_12_9_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Time to checkout! Write the List member function ``totalPrice``
            which calculates and returns the total price of all the Products.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_12_9_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
            
            Below is one way to write the ``totalPrice`` member function.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            struct Product {
                string name;
                double price;
            };

            struct List {
                string type;
                vector<Product> products;
            };

            double List::totalPrice () {
                double total = 0;
                for (size_t i = 0; i < products.size(); ++i) {
                    total += products[i].price;
                }
                return total;
            }


.. tabbed:: mucp_12_10_ac

    .. tab:: Question

        .. activecode:: mucp_12_10_ac_q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Oops! We made a mistake and grabbed pineapple pizza. 
            What if we want to remove an Product from our List?
            Write the List member function ``removeProduct``, which takes
            an index as a parameter and removes it. Then it fills
            the gap with the last product in the List. 
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;
            // YOUR CODE HERE


    .. tab:: Answer

        .. activecode:: mucp_12_10_ac_a
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Below is one way to write the ``removeProduct`` member function.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            struct Product {
                string name;
                double price;
            };

            struct List {
                string type;
                vector&#60Product&#62 products;
            };
            
            void List::removeProduct (int index) {
                products[index] = products[products.size() - 1];
            }