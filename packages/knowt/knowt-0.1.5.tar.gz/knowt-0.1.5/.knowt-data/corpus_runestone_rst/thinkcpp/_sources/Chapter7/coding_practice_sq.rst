Coding Practice
---------------

.. tabbed:: cp_7_AC_2q_q

    .. tab:: Activecode

        .. activecode:: cp_7_AC_2q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
            :practice: T

            How much does Bubba love shrimp? Probably a lot. But how many times does the word "shrimp" come
            up in his monologue? Write a function ``countWord`` that counts the number of times a given word 
            appears in a given string. ``countWord`` should take two strings ``input`` and ``word`` as parameters and return an ``int``.
            Feel free to use the ``stringToLower`` function we wrote earlier. Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            #include "ctype.h"
            using namespace std;

            void stringToLower (string &input) {
                int i = 0;
                while (i < input.length()) {
                    if (isalpha(input[i]) && isupper(input[i])) {
                        input[i] = tolower(input[i]);
                    }
                    i++;
                }
            }

            int countWord (string input, string word) {
                // Write your implementation here.
            }

            int main() {
                string quote =
                    "Anyway, like I was sayin', shrimp is the fruit of the sea. You can "
                    "barbecue it, boil it, broil it, bake it, saute it. Dey's uh, "
                    "shrimp-kabobs, shrimp creole, shrimp gumbo. Pan fried, deep fried, "
                    "stir-fried. There's pineapple shrimp, lemon shrimp, coconut shrimp, "
                    "pepper shrimp, shrimp soup, shrimp stew, shrimp salad, shrimp and "
                    "potatoes, shrimp burger, shrimp sandwich. That- that's about "
                    "it.";
                cout << "Your output: " << countWord(quote, "shrimp") << ", Correct output: 14" << endl; 
            }
    
    .. tab:: Parsonsprob

        .. parsonsprob:: cp_7_AC_2q_pp
            :numbered: left
            :adaptive:

            How much does Bubba love shrimp? Probably a lot. But how many times does the word "shrimp" come
            up in his monologue? Write a function ``countWord`` that counts the number of times a given word 
            appears in a given string. ``countWord`` should take two strings ``input`` and ``word`` as parameters and return an ``int``.
            Feel free to use the ``stringToLower`` function we wrote earlier. Use the lines to construct the code, then go back to complete the Activecode tab.
            
            -----
            int countWord (string input, string word) {
            =====
                int count = 0;
            =====
                for (int i = 0; i < input.length() - 1; i++) {
                    int j = 0;
                    int k = i;
            =====
                for (int i = 0; i < input.length(); i++) { #paired
                    int j = 0;
                    int k = i;
            =====
                    for (int l = 0; l < word.length(); l++) {
            =====
                        if (input[k] == word[l]) {
                            j++;
                        }
                        k++;
            =====
                    if (m == word.length()) {
                        count ++
                    }
            =====
                    }
                }
                return count;
            }

.. tabbed:: cp_7_AC_4q_q

    .. tab:: Activecode

        .. activecode:: cp_7_AC_4q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
            :practice: T

            Write a void function ``removeWord`` that removes a given word from a given string and prints
            out the new string. ``removeWord`` should take two strings ``input`` and ``word`` as parameters
            and prints out ``input`` with every occurence of ``word`` removed. Use string concatenation and the C++
            string function ``substr``. ``substr`` takes two parameters, a starting index and a length. For example, 
            if ``string greeting = "hello world"``, then ``greeting.substr(6, 5)`` returns the string ``"world"``.  
            Test your function in main. Select the Parsonsprob tab for hints for the construction of the code.
            The output should be:
            
            :: 

                Gucci , Gucci , Gucci , Gucci
            ~~~~
            #include <iostream>
            #include <string>
            using namespace std;

            void removeWord (string input, string word) {
                // Write your implementation here.
            }

            int main() {
                removeWord ("Gucci gang, Gucci gang, Gucci gang, Gucci gang", "gang");
            }
    
    .. tab:: Parsonsprob

        .. parsonsprob:: cp_7_AC_4q_pp
            :numbered: left
            :adaptive:

            Write a void function ``removeWord`` that removes a given word from a given string and prints
            out the new string. ``removeWord`` should take two strings ``input`` and ``word`` as parameters
            and prints out ``input`` with every occurence of ``word`` removed. Use string concatenation and the C++
            string function ``substr``. ``substr`` takes two parameters, a starting index and a length. For example, 
            if ``string greeting = "hello world"``, then ``greeting.substr(6, 5)`` returns the string ``"world"``.  
            Test your function in main. Use the lines to construct the code, then go back to complete the Activecode tab.
            The output should be:
            
            :: 

                Gucci , Gucci , Gucci , Gucci

            -----
            void removeWord (string input, string word) {
            =====
                for (int i = 0; i < word.length(); i++) {
            =====
                for (int i = 0; i < input.length(); i++) { #paired
            =====
                    int pos = input.find(word);
            =====
                    if (pos != input.length()) {
            =====
                    if (pos == input.length()) { #paired
            =====
                        input.erase(pos, word.length());
            =====
                    }
                }
                cout << input;
            }

.. tabbed:: cp_7_AC_6q_q

    .. tab:: Activecode

        .. activecode:: cp_7_AC_6q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
            :practice: T

            Write the function ``reverseString`` which takes a ``string input``, reverses it,
            and returns the reversed ``string``. Run and test your code! Select the Parsonsprob 
            tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            string reverseWord (string input) {
                // Write your implementation here.
            }
            ====
            #define CATCH_CONFIG_MAIN
            #include <catch.hpp>

            TEST_CASE("reverseWord function") {
                REQUIRE(reverseWord ("hello") == "olleh"); 
                REQUIRE(reverseWord ("world") == "dlrow"); 
                REQUIRE(reverseWord ("racecar") == "racecar"); 
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_7_AC_6q_pp
            :numbered: left
            :adaptive:

            Write the function ``reverseString`` which takes a ``string input``, reverses it,
            and returns the reversed ``string``. Use the lines to construct 
            the code, then go back to complete the Activecode tab.

            -----
            string reverseWord (string input) {
            =====
                int len = input.length();
            =====
                string reverse;
            =====
                for (int i = len - 1; i >= 0; i--) {
            =====
                for (int i = len; i >= 0; i--) { #paired
            =====
                    reverse.push_back(input[i]);
            =====
                }
            =====
                return reverse;
            }

.. tabbed:: cp_7_AC_8q_q

    .. tab:: Activecode

        .. activecode:: cp_7_AC_8q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
            :practice: T

            Write the function ``countVowels`` which takes a ``string input`` and returns
            the number of vowels in the ``string``. Remember, 'a', 'e', 'i', 'o', and 'u'
            are vowels. Run and test your code! Select the Parsonsprob tab for hints for 
            the construction of the code.
            ~~~~
            #include <iostream>
            using namespace std;

            int countVowels (string input) {
                // Write your implementation here.
            }
            ====
            #define CATCH_CONFIG_MAIN
            #include <catch.hpp>

            TEST_CASE("countVowels function") {
                REQUIRE(countVowels ("onomatopoeia") == 8); 
                REQUIRE(countVowels ("cysts") == 0); 
                REQUIRE(countVowels ("vowels") == 2); 
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_7_AC_8q_pp
            :numbered: left
            :adaptive:

            Write the function ``countVowels`` which takes a ``string input`` and returns
            the number of vowels in the ``string``. Remember, 'a', 'e', 'i', 'o', and 'u'
            are vowels. Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            int countVowels (string input) {
            =====
                int count = 0;
            =====
                for (int i = 0; i < input.length; i++) {
            =====
                    if (input[i] == 'a' || input[i] == 'e' || input[i] == 'i' || input[i] == 'o' || input[i] == 'u') {
            =====
                    if (input[i] == 'a' && input[i] == 'e' && input[i] == 'i' && input[i] == 'o' && input[i] == 'u') { #paired
            =====
                        count++;
            =====
                    }
            =====
                }
            =====
                return count;
            }

.. tabbed:: cp_7_AC_10q_q

    .. tab:: Activecode
    
        .. activecode:: cp_7_AC_10q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
            :practice: T

            Camel case is the practice of writing phrases without spaces or punctuation,
            indicating the separation of words using capital letter. For example, "camel case"
            in camel case is "camelCase". Snake case is the practice of writing phrases
            where each space is replaced by an underscore. For example, "snake case"
            in snake case is "snake_case". Write the functions ``snakeToCamel`` and ``camelToSnake``.
            Each function takes a ``string input`` and returns the input using the other stylization.
            Feel free to use any ``string`` functions you'd like. Run and test your code!
            Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            #include <string>
            #include "ctype.h"
            using namespace std;

            string snakeToCamel (string input) {
                // Write your implementation here.
            }

            string camelToSnake (string input) {
                // Write your implementation here.
            }
            ====
            #define CATCH_CONFIG_MAIN
            #include <catch.hpp>

            TEST_CASE("snakeToCamel function") {
                REQUIRE(snakeToCamel ("turn_this_into_camel_case") == "turnThisIntoCamelCase"); 
                REQUIRE(snakeToCamel ("hello_world") == "helloWorld"); 
                REQUIRE(snakeToCamel ("code") == "code"); 
            }

            TEST_CASE("camelToSnake function") {
                REQUIRE(camelToSnake ("turnThisIntoSnakeCase") == "turn_this_into_snake_case"); 
                REQUIRE(camelToSnake ("helloWorld") == "hello_world"); 
                REQUIRE(camelToSnake ("code") == "code"); 
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_7_AC_10q_pp
            :numbered: left
            :adaptive:

            Camel case is the practice of writing phrases without spaces or punctuation,
            indicating the separation of words using capital letter. For example, "camel case"
            in camel case is "camelCase". Snake case is the practice of writing phrases
            where each space is replaced by an underscore. For example, "snake case"
            in snake case is "snake_case". Write the functions ``snakeToCamel`` and ``camelToSnake``.
            Each function takes a ``string input`` and returns the input using the other stylization.
            Feel free to use any ``string`` functions you'd like. Use the lines to construct the code,
            then go back to complete the Activecode tab.

            -----
            // snakeToCamel function
            string snakeToCamel (string input) {
            =====
                int len = input.length();
            =====
                for (int i = 0; i < len; i++) {
            =====
                    if (input[i] == '_') {
                        input[i+1] = toupper(input[i+1]);
                        input.erase(i,1);
                    }
            =====
                }
                return input;
            }
            =====
            // camelToSnake function
            string camelToSnake (string input) {
            =====
                int len = input.length();
            =====
                for (int i = 0; i < len; i++) {
            =====
                    if (isupper(input.at(i))){
                        input.at(i) = tolower(input.at(i));
                        input.insert(i, "_");
                    }
            =====
                }
                return input;
            }