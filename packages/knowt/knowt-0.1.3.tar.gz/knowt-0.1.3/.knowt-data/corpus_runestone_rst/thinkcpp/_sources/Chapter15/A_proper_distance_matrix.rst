A proper distance matrix
------------------------

Although this code works, it is not as well organized as it should be.
Now that we have written a prototype, we are in a good position to
evaluate the design and improve it.

What are some of the problems with the existing code?

#. We did not know ahead of time how big to make the distance matrix, so
   we chose an arbitrary large number (50) and made it a fixed size. It
   would be better to allow the distance matrix to expand in the same
   way a ``Set`` does. The ``matrix`` class has a function called
   ``resize`` that makes this possible.

#. The data in the distance matrix is not well-encapsulated. We have to
   pass the set of city names and the matrix itself as arguments to
   ``processLine``, which is awkward. Also, use of the distance matrix
   is error prone because we have not provided accessor functions that
   perform error-checking. It might be a good idea to take the ``Set``
   of city names and the ``matrix`` of distances, and combine them
   into a single object called a ``DistMatrix``.

Here is a draft of what the header for a ``DistMatrix`` might look like:

::

   class DistMatrix {
   private:
     Set cities;
     matrix<int> distances;

   public:
     DistMatrix (int rows);

     void add (const string& city1, const string& city2, int dist);
     int distance (int i, int j) const;
     int distance (const string& city1, const string& city2) const;
     string cityName (int i) const;
     int numCities () const;
     void print ();
   };

Using this interface simplifies ``main``:

::

   #include <iostream>
   #include <fstream>
   using namespace std;


   int main ()
   {
     string line;
     ifstream infile ("distances");
     DistMatrix distances (2);

     while (true) {
       getline (infile, line);
       if (infile.eof()) break;
       processLine (line, distances);
     }

     distances.print ();
     return 0;
   }

It also simplifies ``processLine``:

::

   void processLine (const string& line, DistMatrix& distances)
   {
     char quote = '\"';
     vector<int> quoteIndex (4);
     quoteIndex[0] = line.find (quote);
     for (int i=1; i<4; i++) {
       quoteIndex[i] = find (line, quote, quoteIndex[i-1]+1);
     }

     // break the line up into substrings
     int len1 = quoteIndex[1] - quoteIndex[0] - 1;
     string city1 = line.substr (quoteIndex[0]+1, len1);
     int len2 = quoteIndex[3] - quoteIndex[2] - 1;
     string city2 = line.substr (quoteIndex[2]+1, len2);
     int len3 = line.length() - quoteIndex[2] - 1;
     string distString = line.substr (quoteIndex[3]+1, len3);
     int distance = convertToInt (distString);

     // add the new datum to the distances matrix
     distances.add (city1, city2, distance);
   }

I will leave it as an exercise to you to implement the member functions
of ``DistMatrix``.
