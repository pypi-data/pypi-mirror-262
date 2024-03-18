Coding Practice
---------------

.. tabbed:: cp_12_AC_2_q

    .. tab:: Activecode

        .. activecode:: cp_12_AC_2q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            An image is just a matrix of pixels. Write the ``struct`` definition for ``Image``,
            which should store information about its height and width and contain a matrix 
            of ``Pixel``\s. Select the Parsonsprob tab for hints for the construction of the code.
            ~~~~
            #include <iostream>
            #include <vector>
            using namespace std;

            struct Pixel {
                int r;
                int g;
                int b;
            };

            // Write your code for the struct Image here.

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_12_AC_2_pp
            :numbered: left
            :adaptive:

            An image is just a matrix of pixels. Write the ``struct`` definition for ``Image``,
            which should store information about its height and width and contain a matrix 
            of ``Pixel``\s. Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            struct Image {
            =====
                int height;
            =====
                int width;
            =====
                vector<vector<Pixel>> matrix;
            =====
                vector<Pixel> matrix; #distractor
            =====
                vector<vector> matrix; #distractor
            =====
            };

.. tabbed:: cp_12_AC_4_q

    .. tab:: Activecode

        .. activecode:: cp_12_AC_4q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Now let's print an ``Image``. Unfortunately we can't print out the actual 
            image to the terminal, but we can print out the ``Pixel``\s in the ``Image``
            matrix. Write the ``Image`` member function ``printImage``. 
            Separate pixels in the same row with a space and add a new line 
            at the end of each row. Use the ``printPixel`` function we created previously. 
            Select the Parsonsprob tab for hints for the construction of the code.
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
                vector<vector<Pixel>> matrix;
                void printImage();
            };

            // Write your implementation of printImage here.

            int main() {
                vector<vector<Pixel> > matrix = { { { 0, 255, 255 }, { 0, 0, 0 }, { 255, 255, 255 } }, 
                                                { { 30, 60, 50 }, { 20, 135, 200 }, { 60, 80, 125 } } };
                Image image = { 2, 3, matrix };
                image.printImage();
            }
            ====
            void Pixel::printPixel() {
                cout << "("<< r << ", " << g << ", " << b << ")";
            }

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_12_AC_4_pp
            :numbered: left
            :adaptive:

            Now let's print an ``Image``. Unfortunately we can't print out the actual 
            image to the terminal, but we can print out the ``Pixel``\s in the ``Image``
            matrix. Write the ``Image`` member function ``printImage``. 
            Separate pixels in the same row with a space and add a new line 
            at the end of each row. Use the ``printPixel`` function we created previously. 
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            void Image::printImage() {
            =====
                for (int r = 0; r < height; ++r) {
            =====
                for (int c = 0; c < width; ++ c) {
            =====
                    matrix[r][c].printPixel();
            =====
                    cout << " ";
            =====
                }
            =====
                cout << endl;
            =====
                }
            =====
            }

.. tabbed:: cp_12_AC_6_q

    .. tab:: Activecode

        .. activecode:: cp_12_AC_6q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's write a ``swapPixel`` member function for ``Image``. ``swapPixel``
            takes two pairs of row indices and column indices from a matrix and swaps the two
            ``Pixel``\s at those locations. Note that these indices are 0-indexed, unlike the 
            previous ``cropIndex`` parameters. Select the Parsonsprob tab for hints for the construction of the code.
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
            };

            // Write your implementation of swapPixel here.

            int main() {
                vector<vector<Pixel> > matrix = { { { 0, 140, 255 }, { 0, 0, 0 }, { 15, 20, 255 } } };
                Image image = { 1, 3, matrix };
                image.printImage();
                cout << endl;
                image.swapPixel(0, 0, 0, 2);
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

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_12_AC_6_pp
            :numbered: left
            :adaptive:

            Let's write a ``swapPixel`` member function for ``Image``. ``swapPixel``
            takes two pairs of row indices and column indices from a matrix and swaps the two
            ``Pixel``\s at those locations. Note that these indices are 0-indexed, unlike the 
            previous ``cropIndex`` parameters.
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            void Image::swapPixel(int row1, int col1, int row2, int col2) {
            =====
                Pixel temp = { matrix[row1][col1].r, matrix[row1][col1].g,  matrix[row1][col1].b };
            =====
                matrix[row1][col1] = matrix[row2][col2];
            =====
                matrix[row2][col2] = temp;
            =====
            }

.. tabbed:: cp_12_AC_8_q

    .. tab:: Activecode

        .. activecode:: cp_12_AC_8q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Oops! Somehow our image came out upside down. Let's write
            the ``Image`` member function ``flipVertical``, which
            reverts an image to be right side up.
            Select the Parsonsprob tab for hints for the construction of the code.
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
            };

            // Write your implementation of flipVertical here.

            int main() {
                vector<vector<Pixel> > matrix = { { { 255, 255, 255 }, { 255, 255, 255 }, { 255, 255, 255 } }, 
                                                { { 50, 50, 50 }, { 10, 10, 10 }, { 50, 50, 50 } },
                                                { { 30, 30, 30 }, { 70, 70, 70 }, { 30, 30, 30 } },
                                                { { 0, 0, 0 }, { 0, 0, 0 }, { 0, 0, 0 } } };
                Image image = { 4, 3, matrix };
                image.printImage();
                cout << endl;
                image.flipVertical();
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

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_12_AC_8_pp
            :numbered: left
            :adaptive:

            Oops! Somehow our image came out upside down. Let's write
            the ``Image`` member function ``flipVertical``, which
            reverts an image to be right side up.
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            void Image::flipVertical() {
                for (int c = 0; c < width; ++c) {
            =====
                    int start = 0; 
            =====
                    int end = height - 1;
            =====
                    while (start < end) {
            =====
                        swapPixel(start, c, end, c);
            =====
                        ++start;
            =====
                        --end;
            =====
                    }
            =====
                }
            =====
            }

.. tabbed:: cp_12_AC_10_q

    .. tab:: Activecode

        .. activecode:: cp_12_AC_10q
            :language: cpp
            :compileargs: [ '-Wall', '-Werror', '-Wno-sign-compare' ]

            Let's return our image to the state of a clean slate. Write the 
            function ``clearImage``, which sets the color of every ``Pixel`` 
            to white. Select the Parsonsprob tab for hints for the construction of the code.
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
                void clearImage();
            };

            // Write your implementation of clearImage here.

            int main() {
                vector<vector<Pixel> > matrix = { { { 0, 0, 0 }, { 10, 10, 10 }, { 65, 70, 255 } }, 
                                                { { 26, 48, 205 }, { 43, 12, 15 }, { 45, 30, 70 } },
                                                { { 89, 36, 65 }, { 75, 43, 26 }, { 40, 75, 70 } } };
                Image image = { 3, 3, matrix };
                image.printImage();
                cout << endl;
                image.clearImage();
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

    .. tab:: Parsonsprob

        .. parsonsprob:: cp_12_AC_10_pp
            :numbered: left
            :adaptive:

            Let's return our image to the state of a clean slate. Write the 
            function ``clearImage``, which sets the color of every ``Pixel`` 
            to white.
            Use the lines to construct the code, then go back to complete the Activecode tab.

            -----
            void Image::clearImage () {
            =====
                for (int r = 0; r < height; r++) {
            =====
                    for (int c = 0; c < width; c++) {
            =====
                        matrix[r][c].r = 255;
            =====
                        matrix[r][c].g = 255;
            =====
                        matrix[r][c].b = 255;            
            =====
                    }
            =====
                }
            =====
            }