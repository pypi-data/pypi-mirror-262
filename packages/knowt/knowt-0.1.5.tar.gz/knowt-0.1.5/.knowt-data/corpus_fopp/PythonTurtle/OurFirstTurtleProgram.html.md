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
        Problem](/runestone/default/reportabug?course=fopp&page=OurFirstTurtleProgram)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [5.1 Hello Little
        Turtles!](intro-HelloLittleTurtles.html){.reference .internal}
    -   [5.2 Our First Turtle
        Program](OurFirstTurtleProgram.html){.reference .internal}
    -   [5.3 Instances: A Herd of
        Turtles](InstancesAHerdofTurtles.html){.reference .internal}
    -   [5.4 Object Oriented Concepts](ObjectInstances.html){.reference
        .internal}
    -   [5.5 Repetition with a For
        Loop](RepetitionwithaForLoop.html){.reference .internal}
    -   [5.6 A Few More turtle Methods and
        Observations](AFewMoreturtleMethodsandObservations.html){.reference
        .internal}
    -   [5.7 Summary of Turtle
        Methods](SummaryOfTurtleMethods.html){.reference .internal}
    -   [5.8 👩‍💻 Incremental
        Programming](WPIncrementalProgramming.html){.reference
        .internal}
    -   [5.9 👩‍💻 Common turtle
        Errors](WPCommonTurtleErrors.html){.reference .internal}
    -   [5.10 Exercises](Exercises.html){.reference .internal}
    -   [5.11 Chapter Assessment - Turtle and Object
        Mechanics](week1a3.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#adcopy_1 .adcopy style="display: none;"}
#### Before you keep reading\...

Runestone Academy can only continue if we get support from individuals
like you. As a student you are well aware of the high cost of textbooks.
Our mission is to provide great books to you for free, but we ask that
you consider a \$10 donation, more if you can or less if \$10 is a
burden.

::: {.donateb}
[Support Runestone Academy Today](/runestone/default/donate?ad=1){.btn
.btn-info}
:::

::: {#adcopy_2 .adcopy style="display: none;"}
#### Before you keep reading\...

Making great stuff takes time and \$\$. If you appreciate the book you
are reading now and want to keep quality materials free for other
students please consider a donation to Runestone Academy. We ask that
you consider a \$10 donation, but if you can give more thats great, if
\$10 is too much for your budget we would be happy with whatever you can
afford as a show of support.

::: {.donateb}
[Support Runestone Academy Today](/runestone/default/donate?ad=2){.btn
.btn-info}
:::
:::
:::

::: {#our-first-turtle-program .section}
[]{#index-0}

[5.2. ]{.section-number}Our First Turtle Program[¶](#our-first-turtle-program "Permalink to this heading"){.headerlink}
=======================================================================================================================

Let's try a couple of lines of Python code to create a new turtle and
start drawing a simple figure like a rectangle. We will refer to our
first turtle using the variable name alex, but remember that you can
choose any name you wish as long as you follow the naming rules from the
previous chapter.

The program as shown will only draw the first two sides of the
rectangle. After line 4 you will have a straight line going from the
center of the drawing canvas towards the right. After line 6, you will
have a canvas with a turtle and a half drawn rectangle. Press the run
button to try it and see.

::: {.runestone .explainer .ac_section}
::: {#ac3_2_1 component="activecode" question_label="5.2.1"}
::: {#ac3_2_1_question .ac_question}
:::
:::
:::

Here are a couple of things you'll need to understand about this
program.

The first line tells Python to load a **module** named
`turtle`{.docutils .literal .notranslate}. That module brings us two new
types that we can use: the `Turtle`{.docutils .literal .notranslate}
type, and the `Screen`{.docutils .literal .notranslate} type. The dot
notation `turtle.Turtle`{.docutils .literal .notranslate} means *"The
Turtle type that is defined within the turtle module"*. (Remember that
Python is case sensitive, so the module name, `turtle`{.docutils
.literal .notranslate}, with a lowercase `t`{.docutils .literal
.notranslate}, is different from the type `Turtle`{.docutils .literal
.notranslate} because of the uppercase `T`{.docutils .literal
.notranslate}.)

We then create and open what the turtle module calls a screen (we would
prefer to call it a window, or in the case of this web version of Python
simply a canvas), which we assign to variable `wn`{.docutils .literal
.notranslate}. Every window contains a **canvas**, which is the area
inside the window on which we can draw.

In line 3 we create a turtle. The variable `alex`{.docutils .literal
.notranslate} is made to refer to this turtle. These first three lines
set us up so that we are ready to do some drawing.

In lines 4-6, we instruct the **object** alex to move and to turn. We do
this by **invoking** or activating alex's **methods** --- these are the
instructions that all turtles know how to respond to.

::: {.admonition-complete-the-rectangle .admonition}
Complete the rectangle ...

Modify the program by adding the commands necessary to have *alex*
complete the rectangle.
:::

**Check your understanding**

::: {.runestone}
-   [North]{#question3_2_1_opt_a}
-   Some turtle systems start with the turtle facing north, but not this
    one.
-   [South]{#question3_2_1_opt_b}
-   No, look at the first example with a turtle. Which direction does
    the turtle move?
-   [East]{#question3_2_1_opt_c}
-   Yes, the turtle starts out facing east.
-   [West]{#question3_2_1_opt_d}
-   No, look at the first example with a turtle. Which direction does
    the turtle move?
:::

**Mixed up programs**

::: {.runestone .parsons-container}
::: {#pp3_2_1 .parsons component="parsons"}
::: {.parsons_question .parsons-text}
The following program uses a turtle to draw a capital L as shown in the
picture to the left of this text:

[![image of a navigational compass and a letter L which is drawn by
Turtle](../_images/TurtleL4.png){.align-left}](../_images/TurtleL4.png){.reference
.internal .image-reference}

But the lines are mixed up. The program should do all necessary set-up:
import the turtle module, get the window to draw on, and create the
turtle. Remember that the turtle starts off facing east when it is
created. The turtle should turn to face south and draw a line that is
150 pixels long and then turn to face east and draw a line that is 75
pixels long. We have added a compass to the picture to indicate the
directions north, south, west, and east.

Drag the blocks of statements from the left column to the right column
and put them in the right order. Then click on *Check Me* to see if you
are right. You will be told if any of the lines are in the wrong order.
:::

``` {.parsonsblocks question_label="5.2.3" style="visibility: hidden;"}
        import turtle
window = turtle.Screen()
ella = turtle.Turtle()
---
ella.right(90)
ella.forward(150)
---
ella.left(90)
ella.forward(75)
        
```
:::
:::

::: {.runestone .parsons-container}
::: {#pp3_2_2 .parsons component="parsons"}
::: {.parsons_question .parsons-text}
The following program uses a turtle to draw a checkmark as shown to the
left,

[![image of a navigational compass and a checkmark which is drawn by
Turtle.](../_images/TurtleCheckmark4.png){.align-left}](../_images/TurtleCheckmark4.png){.reference
.internal .image-reference}

But the lines are mixed up. The program should do all necessary set-up:
import the turtle module, get the window to draw on, and create the
turtle. The turtle should turn to face southeast, draw a line that is 75
pixels long, then turn to face northeast, and draw a line that is 150
pixels long. We have added a compass to the picture to indicate the
directions north, south, west, and east. Northeast is between north and
east. Southeast is between south and east.

Drag the blocks of statements from the left column to the right column
and put them in the right order. Then click on Check Me to see if you
are right. You will be told if any of the lines are in the wrong order.
:::

``` {.parsonsblocks question_label="5.2.4" style="visibility: hidden;"}
        import turtle
---
window = turtle.Screen()
---
maria = turtle.Turtle()
---
maria.right(45)
maria.forward(75)
---
maria.left(90)
maria.forward(150)
        
```
:::
:::

::: {.runestone .parsons-container}
::: {#pp3_2_3 .parsons component="parsons"}
::: {.parsons_question .parsons-text}
The following program uses a turtle to draw a single line to the west as
shown to the left:

[![image of a line moving in west direction drawn by Turtle. Turtle uses
following steps: left turn of 180 degrees, and 75 pixels long
line](../_images/TurtleLineToWest.png){.align-left}](../_images/TurtleLineToWest.png){.reference
.internal .image-reference}

But the program lines are mixed up. The program should do all necessary
set-up: import the turtle module, get the window to draw on, and create
the turtle. The turtle should then turn to face west and draw a line
that is 75 pixels long.

Drag the blocks of statements from the left column to the right column
and put them in the right order. Then click on *Check Me* to see if you
are right. You will be told if any of the lines are in the wrong order.
:::

``` {.parsonsblocks question_label="5.2.5" style="visibility: hidden;"}
        import turtle
window = turtle.Screen()
jamal = turtle.Turtle()
jamal.left(180)
jamal.forward(75)
        
```
:::
:::

An object can have various methods --- things it can do --- and it can
also have **attributes** --- (sometimes called *properties*). For
example, each turtle has a *color* attribute. The method invocation
`alex.color("red")`{.docutils .literal .notranslate} will make alex red
and the line that it draws will be red too.

The color of the turtle, the width of its pen(tail), the position of the
turtle within the window, which way it is facing, and so on are all part
of its current **state**. Similarly, the window object has a background
color which is part of its state.

Quite a number of methods exist that allow us to modify the turtle and
window objects. In the example below, we show just show a couple and
have only commented those lines that are different from the previous
example. Note also that we have decided to call our turtle object
*tess*.

::: {.runestone .explainer .ac_section}
::: {#ac3_2_2 component="activecode" question_label="5.2.6"}
::: {#ac3_2_2_question .ac_question}
:::
:::
:::

The last line plays a very important role. The wn variable refers to the
window shown above. When we invoke its `exitonclick`{.docutils .literal
.notranslate} method, the program pauses execution and waits for the
user to click the mouse somewhere in the window. When this click event
occurs, the response is to close the turtle window and exit (stop
execution of) the Python program.

Each time we run this program, a new drawing window pops up, and will
remain on the screen until we click on it.

::: {.admonition-extend-this-program .admonition}
Extend this program ...

1.  Modify this program so that before it creates the window, it prompts
    the user to enter the desired background color.It should store the
    user's responses in a variable, and modify the color of the window
    according to the user's wishes. (Hint: you can find a list of
    permitted color names at
    <https://www.w3schools.com/colors/colors_names.asp>. It includes
    some quite unusual ones, like "PeachPuff" and "HotPink".)

2.  Do similar changes to allow the user, at runtime, to set tess'
    color.

3.  Do the same for the width of tess' pen. *Hint:* your dialog with the
    user will return a string, but tess' `pensize`{.docutils .literal
    .notranslate} method expects its argument to be an `int`{.docutils
    .literal .notranslate}. That means you need to convert the string to
    an int before you pass it to `pensize`{.docutils .literal
    .notranslate}.
:::

**Check your understanding**

::: {.runestone}
-   [It creates a new turtle object that can be used for
    drawing.]{#question3_2_2_opt_a}
-   The line &quotalex = turtle.Turtle()\" is what actually creates the
    turtle object.
-   [It defines the module turtle which will allow you to create a
    Turtle object and draw with it.]{#question3_2_2_opt_b}
-   This line imports the module called turtle, which has all the built
    in functions for drawing on the screen with the Turtle object.
-   [It makes the turtle draw half of a rectangle on the
    screen.]{#question3_2_2_opt_c}
-   This functionality is performed with the lines:
    &quotalex.forward(150)\", &quotlex.left(90)\", and
    &quotalex.forward(75)\"
-   [Nothing, it is unnecessary.]{#question3_2_2_opt_d}
-   If we leave it out, Python will give an error saying that it does
    not know about the name &quotturtle\" when it reaches the line
    &quotwn = turtle.Screen()\"
:::

::: {.runestone}
-   [This is simply for clarity. It would also work to just type
    \"Turtle()\" instead of \"turtle.Turtle()\".]{#question3_2_3_opt_a}
-   We must specify the name of the module where Python can find the
    Turtle object.
-   [The period (.) is what tells Python that we want to invoke a new
    object.]{#question3_2_3_opt_b}
-   The period separates the module name from the object name. The
    parentheses at the end are what tell Python to invoke a new object.
-   [The first \"turtle\" (before the period) tells Python that we are
    referring to the turtle module, which is where the object \"Turtle\"
    is found.]{#question3_2_3_opt_c}
-   Yes, the Turtle type is defined in the module turtle. Remember that
    Python is case sensitive and Turtle is different from turtle.
:::

::: {.runestone}
-   [True]{#question3_2_4_opt_a}
-   In this chapter you saw one named alex and one named tess, but any
    legal variable name is allowed.
-   [False]{#question3_2_4_opt_b}
-   A variable, including one referring to a Turtle object, can have
    whatever name you choose as long as it follows the naming
    conventions from Chapter 2.
:::

::: {.runestone}
-   [![right turn of 90 degrees before drawing, draw a line 150 pixels
    long, turn left 90, and draw a line 75 pixels
    long](../_static/test1Alt1.png)]{#question3_2_5_opt_a}
-   This code would turn the turtle to the south before drawing
-   [![left turn of 180 degrees before drawing, draw a line 150 pixels
    long, turn left 90, and draw a line 75 pixels
    long](../_static/test1Alt2.png)]{#question3_2_5_opt_b}
-   This code would turn the turtle to the west before drawing
-   [![left turn of 270 degrees before drawing, draw a line 150 pixels
    long, turn left 90, and draw a line 75 pixels
    long](../_static/test1Alt3.png)]{#question3_2_5_opt_c}
-   This code would turn the turtle to the south before drawing
-   [![right turn of 270 degrees before drawing, draw a line 150 pixels
    long, turn right 90, and draw a line 75 pixels
    long](../_static/test1Alt4v2.png)]{#question3_2_5_opt_d}
-   This code is almost correct, but the short end would be facing east
    instead of west.
-   [![left turn of 90 degrees before drawing, draw a line 150 pixels
    long, turn left 90, and draw a line 75 pixels
    long](../_static/test1correct.png)]{#question3_2_5_opt_e}
-   Yes, the turtle starts facing east, so to turn it north you can turn
    left 90 or right 270 degrees.
:::

**Mixed up programs**

::: {.runestone .parsons-container}
::: {#pp3_3_4 .parsons component="parsons"}
::: {.parsons_question .parsons-text}
The following program uses a turtle to draw a capital L in white on a
blue background as shown to the left,

[![image of a navigational compass and a letter L drawn by
Turtle.](../_images/BlueTurtleL.png){.align-left}](../_images/BlueTurtleL.png){.reference
.internal .image-reference}

But the lines are mixed up. The program should do all necessary set-up
and create the turtle and set the pen size to 10. The turtle should then
turn to face south, draw a line that is 150 pixels long, turn to face
east, and draw a line that is 75 pixels long. Finally, set the window to
close when the user clicks in it.

Drag the blocks of statements from the left column to the right column
and put them in the right order. Then click on *Check Me* to see if you
are right. You will be told if any of the lines are in the wrong order.
:::

``` {.parsonsblocks question_label="5.2.11" style="visibility: hidden;"}
        import turtle
wn = turtle.Screen()
---
wn.bgcolor("blue")
jamal = turtle.Turtle()
---
jamal.color("white")
jamal.pensize(10)
---
jamal.right(90)
jamal.forward(150)
---
jamal.left(90)
jamal.forward(75)
wn.exitonclick()
        
```
:::
:::

::: {.runestone .parsons-container}
::: {#pp3_2_5 .parsons component="parsons"}
::: {.parsons_question .parsons-text}
The following program uses a turtle to draw a capital T in white on a
green background as shown to the left,

[![image of a letter T drawn by
Turtle.](../_images/TurtleT.png){.align-left}](../_images/TurtleT.png){.reference
.internal .image-reference}

But the lines are mixed up. The program should do all necessary set-up,
create the turtle, and set the pen size to 10. After that the turtle
should turn to face north, draw a line that is 150 pixels long, turn to
face west, and draw a line that is 50 pixels long. Next, the turtle
should turn 180 degrees and draw a line that is 100 pixels long.
Finally, set the window to close when the user clicks in it.

Drag the blocks of statements from the left column to the right column
and put them in the right order. Then click on *Check Me* to see if you
are right. You will be told if any of the lines are in the wrong order.
:::

``` {.parsonsblocks question_label="5.2.12" style="visibility: hidden;"}
        import turtle
wn = turtle.Screen()
wn.bgcolor("green")
jamal = turtle.Turtle()
jamal.color("white")
jamal.pensize(10)
---
jamal.left(90)
jamal.forward(150)
---
jamal.left(90)
jamal.forward(50)
---
jamal.right(180)
jamal.forward(100)
---
wn.exitonclick()
        
```
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

-   [[](intro-HelloLittleTurtles.html)]{#relations-prev}
-   [[](InstancesAHerdofTurtles.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
