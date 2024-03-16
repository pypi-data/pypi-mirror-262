Coding Practice
---------------

.. tabbed:: cp_12_1

    .. tab:: Question

        .. activecode:: cp_12_AC_1q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :practice: T
           
           A pixel is the smallest controllable element of a picture represented on the screen. Images
           are comprised of numerous individual pixels, and each pixel's color sample has three numerical
           RGB (red, green, blue) components to represent the color of that pixel. The intensity value of 
           each RGB component ranges from 0 to 255, where 0 is no intensity and 255 is highest intensity.
           Write the ``struct`` definition for ``Pixel``, which has values for each component r, g, and b.
           ~~~~
           #include <iostream>
           #include <vector>
           using namespace std;

           // Write your code for the struct Pixel here.

    .. tab:: Answer

        .. activecode:: cp_12_AC_1a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:

           Below is one way to implement the program. We declare the ``Pixel`` struct
           and create the instance variables in order.
           ~~~~
           #include <iostream>
           #include <vector>
           using namespace std;

           struct Pixel {
               int r;
               int g;
               int b;
           };

.. selectquestion:: cp_12_AC_2_sq
    :fromid: cp_12_AC_2q, cp_12_AC_2_pp
    :toggle: lock

.. tabbed:: cp_12_3

    .. tab:: Question

        .. activecode:: cp_12_AC_3q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :practice: T

           Let's print out a ``Pixel``! Write the ``Pixel`` member function ``printPixel``,
           which prints out the values of the ``Pixel`` in this form: (r, g, b).
           ~~~~
           #include <iostream>
           #include <vector>
           using namespace std;

           struct Pixel {
               int r;
               int g;
               int b;
               void printPixel();
           };

           // Write your implementation of printPixel here.

           int main() {
               Pixel p = {0, 0, 0};
               p.printPixel();
           }

    .. tab:: Answer

        .. activecode:: cp_12_AC_3a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]
           :optional:

           Below is one way to implement the program. We use the scope resolution
           operator to make ``printPixel`` a ``Pixel`` member function.
           ~~~~
           #include <iostream>
           #include <vector>
           using namespace std;

           struct Pixel {
               int r;
               int g;
               int b;
               void printPixel();
           };

           void Pixel::printPixel() {
               cout << "("<< r << ", " << g << ", " << b << ")";
           }

           int main() {
               Pixel p = {0, 0, 0};
               p.printPixel();
           }

.. selectquestion:: cp_12_AC_4_sq
    :fromid: cp_12_AC_4q, cp_12_AC_4_pp
    :toggle: lock

.. tabbed:: cp_12_5

    .. tab:: Question

        .. activecode:: cp_12_AC_5q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

           Somebody photobombed our image! What if we wanted to crop the photobomber out?
           Let's write the ``Image`` member function ``cropImage``, which takes four paramenters,
           a start and stop row and a start and stop column. It then modifies the matrix to the
           cropped matrix. 
           ~~~~
           #include <iostream>
           #include <vector>
           using namespace std;

           struct Pixel {
               int r;
               int g;
               int b;
               void printPixel();
           };

           struct Image {
               int height;
               int width;
               vector<vector<Pixel> > matrix;
               void printImage();
               void cropImage(int startRow, int stopRow, int startCol, int stopCol);
           };

           // Write your implementation of cropImage here.

           int main() {
               vector<vector<Pixel> > matrix = { { { 0, 255, 255 }, { 0, 0, 0 }, { 255, 255, 255 } }, 
                                                 { { 30, 60, 50 }, { 20, 135, 200 }, { 60, 80, 125 } },
                                                 { { 10, 0, 50 }, { 30, 65, 225 }, { 25, 105, 125 } },
                                                 { { 255, 60, 0 }, { 20, 25, 255 }, { 65, 55, 0 } } };
               Image image = { 4, 3, matrix };
               image.printImage();
               cout << endl;
               image.cropImage(2, 3, 1, 2);
               image.printImage();
           }
           ====
           void Pixel::printPixel() {
               cout << "("<< r << ", " << g << ", " << b << ")";
           }

           void Image::printImage() {
               for (int r = 0; r < height; ++r) {
               for (int c = 0; c < width; ++ c) {
                   matrix[r][c].printPixel();
                   cout << " ";
               }
               cout << endl;
               }
           }

    .. tab:: Answer

        .. activecode:: cp_12_AC_5a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

           Below is one way to implement the program. First we make a new matrix
           with the correct amount of rows. Then we push back the pixels we want 
           into the new matrix. Afterwards, we must update the height and width 
           of the ``Image`` and set the ``Image``\'s matrix equal to the new one
           we created.
           ~~~~
           #include <iostream>
           #include <vector>
           using namespace std;

           struct Pixel {
               int r;
               int g;
               int b;
               void printPixel();
           };

           struct Image {
               int height;
               int width;
               vector<vector<Pixel> > matrix;
               void printImage();
               void cropImage(int startRow, int stopRow, int startCol, int stopCol);
           };

           void Image::cropImage(int startRow, int stopRow, int startCol, int stopCol) {
               vector<vector<Pixel> > newMatrix(stopRow - startRow + 1);
               for (int r = startRow - 1; r < stopRow; ++r) {
                   for (int c = startCol - 1; c < stopCol; ++c) {
                       newMatrix[r - (startRow - 1)].push_back(matrix[r][c]);
                   }
               }
               height = stopRow - startRow + 1;
               width = stopCol - startCol + 1;
               matrix = newMatrix;
           }

           int main() {
               vector<vector<Pixel> > matrix = { { { 0, 255, 255 }, { 0, 0, 0 }, { 255, 255, 255 } }, 
                                                 { { 30, 60, 50 }, { 20, 135, 200 }, { 60, 80, 125 } },
                                                 { { 10, 0, 50 }, { 30, 65, 225 }, { 25, 105, 125 } },
                                                 { { 255, 60, 0 }, { 20, 25, 255 }, { 65, 55, 0 } } };
               Image image = { 4, 3, matrix };
               image.printImage();
               cout << endl;
               image.cropImage(2, 3, 1, 2);
               image.printImage();
           }
           ====
           void Pixel::printPixel() {
               cout << "("<< r << ", " << g << ", " << b << ")";
           }

           void Image::printImage() {
               for (int r = 0; r < height; ++r) {
               for (int c = 0; c < width; ++ c) {
                   matrix[r][c].printPixel();
                   cout << " ";
               }
               cout << endl;
               }
           }

.. selectquestion:: cp_12_AC_6_sq
    :fromid: cp_12_AC_6q, cp_12_AC_6_pp
    :toggle: lock

.. tabbed:: cp_12_7

    .. tab:: Question

        .. activecode:: cp_12_AC_7q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

           When you take a selfie on your phone, the image is mirrored. 
           We can do the same to an image by flipping it horizontally.
           Write the ``Image`` member function ``flipHorizontal``, 
           which flips an image horizontally. Use the ``swapPixel``
           function we created previously.
           ~~~~ 
           #include <iostream>
           #include <vector>
           using namespace std;

           struct Pixel {
               int r;
               int g;
               int b;
               void printPixel();
           };

           struct Image {
               int height;
               int width;
               vector<vector<Pixel> > matrix;
               void printImage();
               void cropImage(int startRow, int stopRow, int startCol, int stopCol);
               void swapPixel(int row1, int col1, int row2, int col2);
               void flipHorizontal();
           };

           // Write your implementation of flipHorizontal here.

           int main() {
               vector<vector<Pixel> > matrix = { { { 0, 0, 0 }, { 10, 10, 10 }, { 255, 255, 255 } }, 
                                                 { { 50, 50, 50 }, { 10, 10, 10 }, { 255, 255, 255 } },
                                                 { { 100, 100, 100 }, { 10, 10, 10 }, { 255, 255, 255 } },
                                                 { { 150, 150, 150 }, { 10, 10, 10 }, { 255, 255, 255 } } };
               Image image = { 4, 3, matrix };
               image.printImage();
               cout << endl;
               image.flipHorizontal();
               image.printImage();
           }
           ====
           void Pixel::printPixel() {
               cout << "("<< r << ", " << g << ", " << b << ")";
           }

           void Image::printImage() {
               for (int r = 0; r < height; ++r) {
               for (int c = 0; c < width; ++ c) {
                   matrix[r][c].printPixel();
                   cout << " ";
               }
               cout << endl;
               }
           }

           void Image::cropImage(int startRow, int stopRow, int startCol, int stopCol) {
               vector<vector<Pixel> > newMatrix(stopRow - startRow + 1);
               for (int r = startRow - 1; r < stopRow; ++r) {
                   for (int c = startCol - 1; c < stopCol; ++c) {
                       newMatrix[r - (startRow - 1)].push_back(matrix[r][c]);
                   }
               }
               height = stopRow - startRow + 1;
               width = stopCol - startCol + 1;
               matrix = newMatrix;
           }

           void Image::swapPixel(int row1, int col1, int row2, int col2) {
               Pixel temp = { matrix[row1][col1].r, matrix[row1][col1].g,  matrix[row1][col1].b };
               matrix[row1][col1] = matrix[row2][col2];
               matrix[row2][col2] = temp;
           }

    .. tab:: Answer

        .. activecode:: cp_12_AC_7a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

           Below is one way to implement the program. We loop through
           each row in the matrix. We create start and end indices and
           repeatedly swap pixels, moving both indices toward the middle.
           Once they meet in the middle, we have finished flipping the image. 
           ~~~~ 
           #include <iostream>
           #include <vector>
           using namespace std;

           struct Pixel {
               int r;
               int g;
               int b;
               void printPixel();
           };

           struct Image {
               int height;
               int width;
               vector<vector<Pixel> > matrix;
               void printImage();
               void cropImage(int startRow, int stopRow, int startCol, int stopCol);
               void swapPixel(int row1, int col1, int row2, int col2);
               void flipHorizontal();
           };

           void Image::flipHorizontal() {
               for (int r = 0; r < height; ++r) {
                   int start = 0;
                   int end = width - 1;
                   while (start < end) {
                       swapPixel(r, start, r, end);
                       ++start;
                       --end;
                   }
               }
           }

           int main() {
               vector<vector<Pixel> > matrix = { { { 0, 0, 0 }, { 10, 10, 10 }, { 255, 255, 255 } }, 
                                                 { { 50, 50, 50 }, { 10, 10, 10 }, { 255, 255, 255 } },
                                                 { { 100, 100, 100 }, { 10, 10, 10 }, { 255, 255, 255 } },
                                                 { { 150, 150, 150 }, { 10, 10, 10 }, { 255, 255, 255 } } };
               Image image = { 4, 3, matrix };
               image.printImage();
               cout << endl;
               image.flipHorizontal();
               image.printImage();
           }
           ====
           void Pixel::printPixel() {
               cout << "("<< r << ", " << g << ", " << b << ")";
           }

           void Image::printImage() {
               for (int r = 0; r < height; ++r) {
               for (int c = 0; c < width; ++ c) {
                   matrix[r][c].printPixel();
                   cout << " ";
               }
               cout << endl;
               }
           }

           void Image::cropImage(int startRow, int stopRow, int startCol, int stopCol) {
               vector<vector<Pixel> > newMatrix(stopRow - startRow + 1);
               for (int r = startRow - 1; r < stopRow; ++r) {
                   for (int c = startCol - 1; c < stopCol; ++c) {
                       newMatrix[r - (startRow - 1)].push_back(matrix[r][c]);
                   }
               }
               height = stopRow - startRow + 1;
               width = stopCol - startCol + 1;
               matrix = newMatrix;
           }

           void Image::swapPixel(int row1, int col1, int row2, int col2) {
               Pixel temp = { matrix[row1][col1].r, matrix[row1][col1].g,  matrix[row1][col1].b };
               matrix[row1][col1] = matrix[row2][col2];
               matrix[row2][col2] = temp;
           }

.. selectquestion:: cp_12_AC_8_sq
    :fromid: cp_12_AC_8q, cp_12_AC_8_pp
    :toggle: lock

.. tabbed:: cp_12_9

    .. tab:: Question

        .. activecode:: cp_12_AC_9q
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

           Let's write the ``Image`` member function called ``createBorder``,
           which sets the ``Pixel``\s on the edge of an ``Image`` to a given
           ``Pixel``.
           ~~~~ 
           #include <iostream>
           #include <vector>
           using namespace std;

           struct Pixel {
               int r;
               int g;
               int b;
               void printPixel();
           };

           struct Image {
               int height;
               int width;
               vector<vector<Pixel> > matrix;
               void printImage();
               void cropImage(int startRow, int stopRow, int startCol, int stopCol);
               void swapPixel(int row1, int col1, int row2, int col2);
               void flipHorizontal();
               void flipVertical();
               void createBorder(Pixel p);
           };

           // Write your implementation of createBorder here.

           int main() {
               vector<vector<Pixel> > matrix = { { { 25, 65, 23 }, { 73, 56, 24 }, { 255, 255, 255 }, { 253, 61, 56 } }, 
                                                 { { 50, 50, 50 }, { 145, 52, 102 }, { 2, 0, 25 }, { 52, 47, 35 } },
                                                 { { 45, 34, 100 }, { 213, 67, 45 }, { 2, 45, 255 }, { 34, 16, 76 } },
                                                 { { 2, 2, 78 }, { 164, 16, 23 }, { 5, 255, 25 }, { 32, 65, 34 } },
                                                 { { 150, 150, 150 }, { 241, 42, 64 }, { 1, 4, 255 }, { 16, 73, 84 } } };
               Image image = { 5, 4, matrix };
               image.printImage();
               cout << endl;
               Pixel p = { 0, 0, 0 };
               image.createBorder(p);
               image.printImage();
           }
           ====
           void Pixel::printPixel() {
               cout << "("<< r << ", " << g << ", " << b << ")";
           }

           void Image::printImage() {
               for (int r = 0; r < height; ++r) {
               for (int c = 0; c < width; ++ c) {
                   matrix[r][c].printPixel();
                   cout << " ";
               }
               cout << endl;
               }
           }

           void Image::cropImage(int startRow, int stopRow, int startCol, int stopCol) {
               vector<vector<Pixel> > newMatrix(stopRow - startRow + 1);
               for (int r = startRow - 1; r < stopRow; ++r) {
                   for (int c = startCol - 1; c < stopCol; ++c) {
                       newMatrix[r - (startRow - 1)].push_back(matrix[r][c]);
                   }
               }
               height = stopRow - startRow + 1;
               width = stopCol - startCol + 1;
               matrix = newMatrix;
           }

           void Image::swapPixel(int row1, int col1, int row2, int col2) {
               Pixel temp = { matrix[row1][col1].r, matrix[row1][col1].g,  matrix[row1][col1].b };
               matrix[row1][col1] = matrix[row2][col2];
               matrix[row2][col2] = temp;
           }

           void Image::flipHorizontal() {
               for (int r = 0; r < height; ++r) {
                   int start = 0;
                   int end = width - 1;
                   while (start < end) {
                       swapPixel(r, start, r, end);
                       ++start;
                       --end;
                   }
               }
           }

           void Image::flipVertical() {
               for (int c = 0; c < width; ++c) {
                   int start = 0; 
                   int end = height - 1;
                   while (start < end) {
                       swapPixel(start, c, end, c);
                       ++start;
                       --end;
                   }
               }
           }

    .. tab:: Answer

        .. activecode:: cp_12_AC_9a
           :language: cpp
           :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

           Below is one way to implement the program. We set the first and last 
           row and first and last column of ``Pixel``\s in the ``Image`` to the 
           given ``Pixel``.
           ~~~~ 
           #include <iostream>
           #include <vector>
           using namespace std;

           struct Pixel {
               int r;
               int g;
               int b;
               void printPixel();
           };

           struct Image {
               int height;
               int width;
               vector<vector<Pixel> > matrix;
               void printImage();
               void cropImage(int startRow, int stopRow, int startCol, int stopCol);
               void swapPixel(int row1, int col1, int row2, int col2);
               void flipHorizontal();
               void flipVertical();
               void createBorder(Pixel p);
           };

           void Image::createBorder(Pixel p) {
               for (int r = 0; r < height; ++r) {
                   matrix[r][0] = p;
                   matrix[r][width - 1] = p;
               }
               for (int c = 0; c < width; ++c) {
                   matrix[0][c] = p;
                   matrix[height - 1][c] = p;
               }
           }

           int main() {
               vector<vector<Pixel> > matrix = { { { 25, 65, 23 }, { 73, 56, 24 }, { 255, 255, 255 }, { 253, 61, 56 } }, 
                                                 { { 50, 50, 50 }, { 145, 52, 102 }, { 2, 0, 25 }, { 52, 47, 35 } },
                                                 { { 45, 34, 100 }, { 213, 67, 45 }, { 2, 45, 255 }, { 34, 16, 76 } },
                                                 { { 2, 2, 78 }, { 164, 16, 23 }, { 5, 255, 25 }, { 32, 65, 34 } },
                                                 { { 150, 150, 150 }, { 241, 42, 64 }, { 1, 4, 255 }, { 16, 73, 84 } } };
               Image image = { 5, 4, matrix };
               image.printImage();
               cout << endl;
               Pixel p = { 0, 0, 0 };
               image.createBorder(p);
               image.printImage();
           }
           ====
           void Pixel::printPixel() {
               cout << "("<< r << ", " << g << ", " << b << ")";
           }

           void Image::printImage() {
               for (int r = 0; r < height; ++r) {
               for (int c = 0; c < width; ++ c) {
                   matrix[r][c].printPixel();
                   cout << " ";
               }
               cout << endl;
               }
           }

           void Image::cropImage(int startRow, int stopRow, int startCol, int stopCol) {
               vector<vector<Pixel> > newMatrix(stopRow - startRow + 1);
               for (int r = startRow - 1; r < stopRow; ++r) {
                   for (int c = startCol - 1; c < stopCol; ++c) {
                       newMatrix[r - (startRow - 1)].push_back(matrix[r][c]);
                   }
               }
               height = stopRow - startRow + 1;
               width = stopCol - startCol + 1;
               matrix = newMatrix;
           }

           void Image::swapPixel(int row1, int col1, int row2, int col2) {
               Pixel temp = { matrix[row1][col1].r, matrix[row1][col1].g,  matrix[row1][col1].b };
               matrix[row1][col1] = matrix[row2][col2];
               matrix[row2][col2] = temp;
           }

           void Image::flipHorizontal() {
               for (int r = 0; r < height; ++r) {
                   int start = 0;
                   int end = width - 1;
                   while (start < end) {
                       swapPixel(r, start, r, end);
                       ++start;
                       --end;
                   }
               }
           }

           void Image::flipVertical() {
               for (int c = 0; c < width; ++c) {
                   int start = 0; 
                   int end = height - 1;
                   while (start < end) {
                       swapPixel(start, c, end, c);
                       ++start;
                       --end;
                   }
               }
           }

.. selectquestion:: cp_12_AC_10_sq
    :fromid: cp_12_AC_10q, cp_12_AC_10_pp
    :toggle: lock