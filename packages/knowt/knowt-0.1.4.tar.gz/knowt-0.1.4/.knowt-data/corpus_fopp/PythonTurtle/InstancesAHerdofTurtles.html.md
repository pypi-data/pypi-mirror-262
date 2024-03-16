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
        Problem](/runestone/default/reportabug?course=fopp&page=InstancesAHerdofTurtles)
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

::: {#instances-a-herd-of-turtles .section}
[]{#index-0}

[5.3. ]{.section-number}Instances: A Herd of Turtles[¶](#instances-a-herd-of-turtles "Permalink to this heading"){.headerlink}
==============================================================================================================================

Just like we can have many different integers in a program, we can have
many turtles. Each of them is an independent object and we call each one
an **instance** of the Turtle type (class). Each instance has its own
attributes and methods --- so alex might draw with a thin pink pen and
be at some position, while tess might be going in her own direction with
a fat black pen. So here is what happens when alex completes a square
and tess completes her triangle:

::: {.runestone .explainer .ac_section}
::: {#ac3_3_1 component="activecode" question_label="5.3.1"}
::: {#ac3_3_1_question .ac_question}
:::
:::
:::

Here are some *How to think like a computer scientist* observations:

-   There are 360 degrees in a full circle. If you add up all the turns
    that a turtle makes, *no matter what steps occurred between the
    turns*, you can easily figure out if they add up to some multiple
    of 360. This should convince you that alex is facing in exactly the
    same direction as he was when he was first created. (Geometry
    conventions have 0 degrees facing East and that is the case here
    too!)

-   We could have left out the last turn for alex, but that would not
    have been as satisfying. If you're asked to draw a closed shape like
    a square or a rectangle, it is a good idea to complete all the turns
    and to leave the turtle back where it started, facing the same
    direction as it started in. This makes reasoning about the program
    and composing chunks of code into bigger programs easier for us
    humans!

-   We did the same with tess: she drew her triangle and turned through
    a full 360 degress. Then we turned her around and moved her aside.
    Even the blank line 18 is a hint about how the programmer's *mental
    chunking* is working: in big terms, tess' movements were chunked as
    "draw the triangle" (lines 12-17) and then "move away from the
    origin" (lines 19 and 20).

-   One of the key uses for comments is to record your mental chunking,
    and big ideas. They're not always explicit in the code.

-   And, uh-huh, two turtles may not be enough for a herd, but you get
    the idea!

**Check your understanding**

::: {.runestone}
-   [True]{#question3_3_1_opt_a}
-   You can create and use as many turtles as you like. As long as they
    have different names, you can operate them independently, and make
    them move in any order you like. To convince yourself this is true,
    try interleaving the instructions for alex and tess in ActiveCode
    box 3.
-   [False]{#question3_3_1_opt_b}
-   You can create and use as many turtles as you like. As long as they
    have different names, you can operate them independently, and make
    them move in any order you like. If you are not totally convinced,
    try interleaving the instructions for alex and tess in ActiveCode
    box 3.
:::

**Mixed up programs**

::: {.runestone .parsons-container}
::: {#pp3_3_1 .parsons component="parsons"}
::: {.parsons_question .parsons-text}
The following program has one turtle, "jamal", draw a capital L in blue
and then another, "tina", draw a line to the west in orange as shown to
the left:

[![image of a capital letter L in blue color drawn by one Turtle and a
line to the west in orange color drawn by another Turtle. Both the
Turtles have same starting
point.](../_images/TwoTurtles1.png){.align-left}](../_images/TwoTurtles1.png){.reference
.internal .image-reference}

The program should do all set-up, have "jamal" draw the L, and then have
"tina" draw the line. Finally, it should set the window to close when
the user clicks in it.

Drag the blocks of statements from the left column to the right column
and put them in the right order. Then click on *Check Me* to see if you
are right. You will be told if any of the lines are in the wrong order.
:::

``` {.parsonsblocks question_label="5.3.3" style="visibility: hidden;"}
        import turtle
wn = turtle.Screen()
---
jamal = turtle.Turtle()
jamal.pensize(10)
jamal.color("blue")
jamal.right(90)
jamal.forward(150)
---
jamal.left(90)
jamal.forward(75)
---
tina = turtle.Turtle()
tina.pensize(10)
tina.color("orange")
tina.left(180)
tina.forward(75)
---
wn.exitonclick()
        
```
:::
:::

::: {.runestone .parsons-container}
::: {#pp3_3_2 .parsons component="parsons"}
::: {.parsons_question .parsons-text}
The following program has one turtle, "jamal", draw a line to the north
in blue and then another, "tina", draw a line to the east in orange as
shown to the left,

[![Image of a line to the north in blue color drawn by one Turtle and a
line to the east in orange drawn by another Turtle. Both the Turtles
have a same starting
point.](../_images/TwoTurtlesL.png){.align-left}](../_images/TwoTurtlesL.png){.reference
.internal .image-reference}

The program should import the turtle module, get the window to draw on,
create the turtle "jamal", have it draw a line to the north, then create
the turtle "tina", and have it draw a line to the east. Finally, it
should set the window to close when the user clicks in it.

Drag the blocks of statements from the left column to the right column
and put them in the right order. Then click on *Check Me* to see if you
are right. You will be told if any of the lines are in the wrong order.
:::

``` {.parsonsblocks question_label="5.3.4" style="visibility: hidden;"}
        import turtle
---
wn = turtle.Screen()
---
jamal = turtle.Turtle()
jamal.color("blue")
jamal.pensize(10)
---
jamal.left(90)
jamal.forward(150)
---
tina = turtle.Turtle()
tina.pensize(10)
tina.color("orange")
tina.forward(150)
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

-   [[](OurFirstTurtleProgram.html)]{#relations-prev}
-   [[](ObjectInstances.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
