::: {#navbar .navbar .navbar-default .navbar-fixed-top role="navigation"}
::: {.container}
::: {.navbar-header}
[]{.icon-bar} []{.icon-bar} []{.icon-bar}

<div>

[![](../_static/img/RAIcon.png)](/runestone/default/user/login){.brand-logo}
[fopp](../index.html){#rs-book-toc-link .navbar-brand}

</div>
:::

::: {.navbar-collapse .collapse .navbar-ex1-collapse}
-   
-   []{#ad_warning}
-   []{#browsing_warning}
-   
-   [*[Search]{.visuallyhidden
    aria-label="Search"}*](#){.dropdown-toggle}
    -   [Table of Contents](../index.html)

    -   [Book Index](../genindex.html)

    -   

    -   ::: {.input-group}
        :::
-   
-   [*[User]{.visuallyhidden aria-label="User"}*](#){.dropdown-toggle}
    -   []{.loggedinuser}

    -   

    -   [Course Home](/ns/course/index)

    -   [Assignments](/assignment/student/chooseAssignment)

    -   [Practice](/runestone/assignments/practice)

    -   [[Peer Instruction
        (Instructor)](/runestone/peer/instructor.html)]{#inst_peer_link}

    -   [Peer Instruction (Student)](/runestone/peer/student.html)

    -   

    -   [Change Course](/runestone/default/courses)

    -   

    -   [[Instructor\'s
        Page](/runestone/admin/index)]{#ip_dropdown_link}

    -   [Progress Page](/runestone/dashboard/studentreport)

    -   

    -   [Edit Profile](/runestone/default/user/profile){#profilelink}

    -   [Change
        Password](/runestone/default/user/change_password){#passwordlink}

    -   [Register](/runestone/default/user/register){#registerlink}

    -   [Login](#)

    -   ::: {.slider .round}
        :::

        Dark Mode
-   
-   [[*[Scratch Activecode]{.visuallyhidden
    aria-label="Scratch Activecode"}*](javascript:runestoneComponents.popupScratchAC())]{#scratch_ac_link}
-   
-   [*[Help]{.visuallyhidden aria-label="Help"}*](#){.dropdown-toggle}
    -   [FAQ](http://runestoneinteractive.org/pages/faq.html)
    -   [Instructors Guide](https://guide.runestone.academy)
    -   
    -   [About Runestone](http://runestoneinteractive.org)
    -   [Report A
        Problem](/runestone/default/reportabug?course=fopp&page=NestedIterationImageProcessing)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [7.1 Introduction: Iteration](intro-Iteration.html){.reference
        .internal}
    -   [7.2 The for Loop](TheforLoop.html){.reference .internal}
    -   [7.3 Flow of Execution of the for
        Loop](FlowofExecutionoftheforLoop.html){.reference .internal}
    -   [7.4 Strings and for loops](Stringsandforloops.html){.reference
        .internal}
    -   [7.5 Lists and for loops](Listsandforloops.html){.reference
        .internal}
    -   [7.6 The Accumulator
        Pattern](TheAccumulatorPattern.html){.reference .internal}
    -   [7.7 Traversal and the for Loop: By
        Index](TraversalandtheforLoopByIndex.html){.reference .internal}
    -   [7.8 Nested Iteration: Image
        Processing](NestedIterationImageProcessing.html){.reference
        .internal}
    -   [7.9 👩‍💻 Printing Intermediate
        Results](WPPrintingIntermediateResults.html){.reference
        .internal}
    -   [7.10 👩‍💻 Naming Variables in For
        Loops](WPNamingVariablesinForLoops.html){.reference .internal}
    -   [7.11 The Gory Details:
        Iterables](GeneralizedSequences.html){.reference .internal}
    -   [7.12 👩‍💻 Keeping Track of Your Iterator Variable and Your
        Iterable](WPKeepingTrackofYourIteratorVariableYourIterable.html){.reference
        .internal}
    -   [7.13 Glossary](Glossary.html){.reference .internal}
    -   [7.14 Exercises](Exercises.html){.reference .internal}
    -   [7.15 Chapter Assessment](week2a2.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#nested-iteration-image-processing .section}
[]{#image-proc}

[7.8. ]{.section-number}Nested Iteration: Image Processing[¶](#nested-iteration-image-processing "Permalink to this heading"){.headerlink}
==========================================================================================================================================

Two dimensional tables have both rows and columns. You have probably
seen many tables like this if you have used a spreadsheet program.
Another object that is organized in rows and columns is a digital image.
In this section we will explore how iteration allows us to manipulate
these images.

A **digital image** is a finite collection of small, discrete picture
elements called **pixels**. These pixels are organized in a
two-dimensional grid. Each pixel represents the smallest amount of
picture information that is available. Sometimes these pixels appear as
small "dots".

Each image (grid of pixels) has its own width and its own height. The
width is the number of columns and the height is the number of rows. We
can name the pixels in the grid by using the column number and row
number. However, it is very important to remember that computer
scientists like to start counting with 0! This means that if there are
20 rows, they will be named 0,1,2, and so on through 19. This will be
very useful later when we iterate using range.

In the figure below, the pixel of interest is found at column **c** and
row **r**.

![](../_images/image.png)

::: {#the-rgb-color-model .section}
[7.8.1. ]{.section-number}The RGB Color Model[¶](#the-rgb-color-model "Permalink to this heading"){.headerlink}
---------------------------------------------------------------------------------------------------------------

Each pixel of the image will represent a single color. The specific
color depends on a formula that mixes various amounts of three basic
colors: red, green, and blue. This technique for creating color is known
as the **RGB Color Model**. The amount of each color, sometimes called
the **intensity** of the color, allows us to have very fine control over
the resulting color.

The minimum intensity value for a basic color is 0. For example if the
red intensity is 0, then there is no red in the pixel. The maximum
intensity is 255. This means that there are actually 256 different
amounts of intensity for each basic color. Since there are three basic
colors, that means that you can create 256^3^ distinct colors using the
RGB Color Model.

Here are the red, green and blue intensities for some common colors.
Note that "Black" is represented by a pixel having no basic color. On
the other hand, "White" has maximum values for all three basic color
components.

> <div>
>
>   Color     Red   Green   Blue
>   --------- ----- ------- ------
>   Red       255   0       0
>   Green     0     255     0
>   Blue      0     0       255
>   White     255   255     255
>   Black     0     0       0
>   Yellow    255   255     0
>   Magenta   255   0       255
>
> </div>

In order to manipulate an image, we need to be able to access individual
pixels. This capability is provided by a module called **image**,
provided in ActiveCode [[\[]{.fn-bracket}1[\]]{.fn-bracket}](#id2){#id1
.footnote-reference .brackets}. The image module defines two classes:
`Image`{.docutils .literal .notranslate} and `Pixel`{.docutils .literal
.notranslate}.

[[\[]{.fn-bracket}[1](#id1)[\]]{.fn-bracket}]{.label}

If you want to explore image processing on your own outside of the
browser you can install the cImage module from <http://pypi.org>.

Each Pixel object has three attributes: the red intensity, the green
intensity, and the blue intensity. A pixel provides three methods that
allow us to ask for the intensity values. They are called
`getRed`{.docutils .literal .notranslate}, `getGreen`{.docutils .literal
.notranslate}, and `getBlue`{.docutils .literal .notranslate}. In
addition, we can ask a pixel to change an intensity value using its
`setRed`{.docutils .literal .notranslate}, `setGreen`{.docutils .literal
.notranslate}, and `setBlue`{.docutils .literal .notranslate} methods.

> <div>
>
>   Method Name    Example            Explanation
>   -------------- ------------------ ---------------------------------------------------------
>   Pixel(r,g,b)   Pixel(20,100,50)   Create a new pixel with 20 red, 100 green, and 50 blue.
>   getRed()       r = p.getRed()     Return the red component intensity.
>   getGreen()     r = p.getGreen()   Return the green component intensity.
>   getBlue()      r = p.getBlue()    Return the blue component intensity.
>   setRed()       p.setRed(100)      Set the red component intensity to 100.
>   setGreen()     p.setGreen(45)     Set the green component intensity to 45.
>   setBlue()      p.setBlue(156)     Set the blue component intensity to 156.
>
> </div>

In the example below, we first create a pixel with 45 units of red, 76
units of green, and 200 units of blue. We then print the current amount
of red, change the amount of red, and finally, set the amount of blue to
be the same as the current amount of green.

::: {.runestone .explainer .ac_section}
::: {#ac14_7_1 component="activecode" question_label="7.8.1.1"}
::: {#ac14_7_1_question .ac_question}
:::
:::
:::

**Check your understanding**

::: {.runestone}
-   [Dark red]{#question14_7_1_opt_a}
-   Because all three values are close to 0, the color will be dark. But
    because the red value is higher than the other two, the color will
    appear red.
-   [Light red]{#question14_7_1_opt_b}
-   The closer the values are to 0, the darker the color will appear.
-   [Dark green]{#question14_7_1_opt_c}
-   The first value in RGB is the red value. The second is the green.
    This color has no green in it.
-   [Light green]{#question14_7_1_opt_d}
-   The first value in RGB is the red value. The second is the green.
    This color has no green in it.
:::
:::

::: {#image-objects .section}
[7.8.2. ]{.section-number}Image Objects[¶](#image-objects "Permalink to this heading"){.headerlink}
---------------------------------------------------------------------------------------------------

To access the pixels in a real image, we need to first create an
`Image`{.docutils .literal .notranslate} object. Image objects can be
created in two ways. First, an Image object can be made from the files
that store digital images. The image object has an attribute
corresponding to the width, the height, and the collection of pixels in
the image.

It is also possible to create an Image object that is "empty". An
`EmptyImage`{.docutils .literal .notranslate} has a width and a height.
However, the pixel collection consists of only "White" pixels.

We can ask an image object to return its size using the
`getWidth`{.docutils .literal .notranslate} and `getHeight`{.docutils
.literal .notranslate} methods. We can also get a pixel from a
particular location in the image using `getPixel`{.docutils .literal
.notranslate} and change the pixel at a particular location using
`setPixel`{.docutils .literal .notranslate}.

The Image class is shown below. Note that the first two entries show how
to create image objects. The parameters are different depending on
whether you are using an image file or creating an empty image.

> <div>
>
>   Method Name           Example                           Explanation
>   --------------------- --------------------------------- ----------------------------------------------------
>   Image(filename)       img = image.Image("cy.png")       Create an Image object from the file cy.png.
>   EmptyImage()          img = image.EmptyImage(100,200)   Create an Image object that has all "White" pixels
>   getWidth()            w = img.getWidth()                Return the width of the image in pixels.
>   getHeight()           h = img.getHeight()               Return the height of the image in pixels.
>   getPixel(col,row)     p = img.getPixel(35,86)           Return the pixel at column 35, row 86.
>   setPixel(col,row,p)   img.setPixel(100,50,mp)           Set the pixel at column 100, row 50 to be mp.
>
> </div>

Consider the image shown below. Assume that the image is stored in a
file called "luther.jpg". Line 2 opens the file and uses the contents to
create an image object that is referred to by `img`{.docutils .literal
.notranslate}. Once we have an image object, we can use the methods
described above to access information about the image or to get a
specific pixel and check on its basic color intensities.

![image of Luther College bell
picture](../_static/LutherBellPic.jpg){#luther.jpg}

::: {.runestone .explainer .ac_section}
::: {#ac14_7_2 component="activecode" question_label="7.8.2.1"}
::: {#ac14_7_2_question .ac_question}
:::
:::
:::

When you run the program you can see that the image has a width of 400
pixels and a height of 244 pixels. Also, the pixel at column 45, row 55,
has RGB values of 165, 161, and 158. Try a few other pixel locations by
changing the `getPixel`{.docutils .literal .notranslate} arguments and
rerunning the program.

**Check your understanding**

::: {.runestone}
-   [149 132 122]{#question14_7_2_opt_a}
-   These are the values for the pixel at row 30, column 100. Get the
    values for row 100 and column 30 with p = img.getPixel(30, 100).
    (Note that the first argument to getPixel is the column, not the
    row.)
-   [183 179 170]{#question14_7_2_opt_b}
-   Yes, the RGB values are 183 179 170 at row 100 and column 30.
-   [165 161 158]{#question14_7_2_opt_c}
-   These are the values from the original example (row 45, column 55).
    Get the values for row 100 and column 30 with p = img.getPixel(30,
    100).
-   [201 104 115]{#question14_7_2_opt_d}
-   These are simply made-up values that may or may not appear in the
    image. Get the values for row 100 and column 30 with p =
    img.getPixel(30, 100).
:::
:::

::: {#image-processing-and-nested-iteration .section}
[7.8.3. ]{.section-number}Image Processing and Nested Iteration[¶](#image-processing-and-nested-iteration "Permalink to this heading"){.headerlink}
---------------------------------------------------------------------------------------------------------------------------------------------------

**Image processing** refers to the ability to manipulate the individual
pixels in a digital image. In order to process all of the pixels, we
need to be able to systematically visit all of the rows and columns in
the image. The best way to do this is to use **nested iteration**.

Nested iteration simply means that we will place one iteration construct
inside of another. We will call these two iterations the **outer
iteration** and the **inner iteration**. To see how this works, consider
the iteration below.

::: {.highlight-python .notranslate}
::: {.highlight}
    for i in range(5):
        print(i)
:::
:::

We have seen this enough times to know that the value of `i`{.docutils
.literal .notranslate} will be 0, then 1, then 2, and so on up to 4. The
`print`{.docutils .literal .notranslate} will be performed once for each
pass. However, the body of the loop can contain any statements including
another iteration (another `for`{.docutils .literal .notranslate}
statement). For example,

::: {.highlight-python .notranslate}
::: {.highlight}
    for i in range(5):
        for j in range(3):
            print(i, j)
:::
:::

The `for i`{.docutils .literal .notranslate} iteration is the outer
iteration and the `for j`{.docutils .literal .notranslate} iteration is
the inner iteration. Each pass through the outer iteration will result
in the complete processing of the inner iteration from beginning to end.
This means that the output from this nested iteration will show that for
each value of `i`{.docutils .literal .notranslate}, all values of
`j`{.docutils .literal .notranslate} will occur.

Here is the same example in activecode. Try it. Note that the value of
`i`{.docutils .literal .notranslate} stays the same while the value of
`j`{.docutils .literal .notranslate} changes. The inner iteration, in
effect, is moving faster than the outer iteration.

::: {.runestone .explainer .ac_section}
::: {#ac14_7_3 component="activecode" question_label="7.8.3.1"}
::: {#ac14_7_3_question .ac_question}
:::
:::
:::

Another way to see this in more detail is to examine the behavior with
codelens. Step through the iterations to see the flow of control as it
occurs with the nested iteration. Again, for every value of
`i`{.docutils .literal .notranslate}, all of the values of `j`{.docutils
.literal .notranslate} will occur. You can see that the inner iteration
completes before going on to the next pass of the outer iteration.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="7.8.3.2"}
::: {#clens14_7_1_question .ac_question}
:::

::: {#clens14_7_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 7.8.3.2 (clens14\_7\_1)]{.runestone_caption_text}
:::
:::

Our goal with image processing is to visit each pixel. We will use an
iteration to process each row. Within that iteration, we will use a
nested iteration to process each column. The result is a nested
iteration, similar to the one seen above, where the outer
`for`{.docutils .literal .notranslate} loop processes the rows, from 0
up to but not including the height of the image. The inner
`for`{.docutils .literal .notranslate} loop will process each column of
a row, again from 0 up to but not including the width of the image.

The resulting code will look like the following. We are now free to do
anything we wish to each pixel in the image.

::: {.highlight-python .notranslate}
::: {.highlight}
    for row in range(img.getHeight()):
        for col in range(img.getWidth()):
            # do something with the pixel at position (col,row)
:::
:::

One of the easiest image processing algorithms will create what is known
as a **negative** image. A negative image simply means that each pixel
will be the opposite of what it was originally. But what does opposite
mean?

In the RGB color model, we can consider the opposite of the red
component as the difference between the original red and 255. For
example, if the original red component was 50, then the opposite, or
negative red value would be `255-50`{.docutils .literal .notranslate} or
205. In other words, pixels with a lot of red will have negatives with
little red and pixels with little red will have negatives with a lot. We
do the same for the blue and green as well.

The program below implements this algorithm using the previous image
(luther.jpg). Run it to see the resulting negative image. Note that
there is a lot of processing taking place and this may take a few
seconds to complete. In addition, here are two other images that you can
use (cy.png and goldygopher.png).

![image of Cy the Cardinal, mascot of the Iowa State
University](../_static/cy.png){#cy.png}

#### cy.png {#cy.png style="text-align: center;"}

![image of Goldy Gopher, mascot of the University of Minnesota-Twin
Cities](../_static/goldygopher.png){#goldygopher.png}

#### goldygopher.png {#goldygopher.png style="text-align: center;"}

Change the name of the file in the `image.Image()`{.docutils .literal
.notranslate} call to see how these images look as negatives. Also, note
that there is an `exitonclick`{.docutils .literal .notranslate} method
call at the very end which will close the window when you click on it.
This will allow you to "clear the screen" before drawing the next
negative.

::: {.runestone .explainer .ac_section}
::: {#ac14_7_4 component="activecode" question_label="7.8.3.3"}
::: {#ac14_7_4_question .ac_question}
:::
:::
:::

Let's take a closer look at the code. After importing the image module,
we create an image object called `img`{.docutils .literal .notranslate}
that represents a typical digital photo. We will update each pixel in
this image from top to bottom, left to right, which you should be able
to observe. You can change the values in `setDelay`{.docutils .literal
.notranslate} to make the program progress faster or slower.

Lines 8 and 9 create the nested iteration that we discussed earlier.
This allows us to process each pixel in the image. Line 10 gets an
individual pixel.

Lines 12-14 create the negative intensity values by extracting the
original intensity from the pixel and subtracting it from 255. Once we
have the `newred`{.docutils .literal .notranslate}, `newgreen`{.docutils
.literal .notranslate}, and `newblue`{.docutils .literal .notranslate}
values, we can create a new pixel (Line 15).

Finally, we need to replace the old pixel with the new pixel in our
image. It is important to put the new pixel into the same location as
the original pixel that it came from in the digital photo.

Try to change the program above so that the outer loop iterates over the
columns and the inner loop iterates over the rows. We still create a
negative image, but you can see that the pixels update in a very
different order.

::: {.admonition-other-pixel-manipulation .admonition}
Other pixel manipulation

There are a number of different image processing algorithms that follow
the same pattern as shown above. Namely, take the original pixel,
extract the red, green, and blue intensities, and then create a new
pixel from them. The new pixel is inserted into an empty image at the
same location as the original.

For example, you can create a **gray scale** pixel by averaging the red,
green and blue intensities and then using that value for all
intensities.

From the gray scale you can create **black white** by setting a
threshold and selecting to either insert a white pixel for a black pixel
into the empty image.

You can also do some complex arithmetic and create interesting effects,
such as [Sepia
Tone](http://en.wikipedia.org/wiki/Sepia_tone#Sepia_toning){.reference
.external}
:::

**Check your understanding**

::: {.runestone}
-   [Output a]{#question14_7_3_opt_a}
-   i will start with a value of 0 and then j will iterate from 0 to 1.
    Next, i will be 1 and j will iterate from 0 to 1. Finally, i will be
    2 and j will iterate from 0 to 1.
-   [Output b]{#question14_7_3_opt_b}
-   The inner for-loop controls the second digit (j). The inner for-loop
    must complete before the outer for-loop advances.
-   [Output c]{#question14_7_3_opt_c}
-   The inner for-loop controls the second digit (j). Notice that the
    inner for-loop is over the list \[0, 1\].
-   [Output d]{#question14_7_3_opt_d}
-   The outer for-loop runs 3 times (0, 1, 2) and the inner for-loop
    runs twice for each time the outer for-loop runs, so this code
    prints exactly 6 lines.
:::

::: {.runestone}
-   [It would look like a red-washed version of the bell
    image]{#question14_7_4_opt_a}
-   Because we are removing the green and the blue values, but keeping
    the variation of the red the same, you will get the same image, but
    it will look like it has been bathed in red.
-   [It would be a solid red rectangle the same size as the original
    image]{#question14_7_4_opt_b}
-   Because the red value varies from pixel to pixel, this will not look
    like a solid red rectangle. For it to look like a solid red
    rectangle each pixel would have to have exactly the same red value.
-   [It would look the same as the original
    image]{#question14_7_4_opt_c}
-   If you remove the blue and green values from the pixels, the image
    will look different, even though there does not appear to be any
    blue or green in the original image (remember that other colors are
    made of combinations of red, green and blue).
-   [It would look the same as the negative image in the example
    code]{#question14_7_4_opt_d}
-   Because we have changed the value of the pixels from what they were
    in the original ActiveCode box code, the image will not be the same.
:::
:::
:::

::: {style="width: 100%"}
::: {ea-publisher="runestoneacademy" ea-type="image" style="display: flex; justify-content: center"}
:::
:::

::: {#scprogresscontainer}
You have attempted []{#scprogresstotal} of []{#scprogressposs}
activities on this page

::: {#subchapterprogress aria-label="Page progress"}
:::
:::

-   [[](TraversalandtheforLoopByIndex.html)]{#relations-prev}
-   [[](WPPrintingIntermediateResults.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
