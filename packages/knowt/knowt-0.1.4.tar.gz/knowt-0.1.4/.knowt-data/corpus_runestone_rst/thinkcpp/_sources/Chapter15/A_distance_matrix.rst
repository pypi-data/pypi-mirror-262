A distance matrix
-----------------

Finally, we are ready to put the data from the file into a matrix.
Specifically, the matrix will have one row and one column for each city.

We’ll create the matrix in ``main``, with plenty of space to spare:

::

     matrix<int> distances (50, 50, 0);

Inside ``processLine``, we add new information to the matrix by getting
the indices of the two cities from the ``Set`` and using them as matrix
indices:

::

     int dist = convertToInt (distString);
     int index1 = cities.add (city1);
     int index2 = cities.add (city2);

     distances[index1][index2] = distance;
     distances[index2][index1] = distance;

Finally, in ``main`` we can print the information in a human-readable
form:

::

     for (int i=0; i<cities.getNumElements(); i++) {
       cout << cities.getElement(i) << "\t";

       for (int j=0; j<=i; j++) {
         cout << distances[i][j] << "\t";
       }
       cout << endl;
     }

     cout << "\t";
     for (int i=0; i<cities.getNumElements(); i++) {
       cout << cities.getElement(i) << "\t";
     }
     cout << endl;

This code produces the output shown at the beginning of the chapter. The
original data is available from this book’s web page.
