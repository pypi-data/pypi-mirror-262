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
        Problem](/runestone/default/reportabug?course=fopp&page=AFewMoreturtleMethodsandObservations)
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

::: {#a-few-more-turtle-methods-and-observations .section}
[5.6. ]{.section-number}A Few More `turtle`{.docutils .literal .notranslate} Methods and Observations[¶](#a-few-more-turtle-methods-and-observations "Permalink to this heading"){.headerlink}
==============================================================================================================================================================================================

Here are a few more things that you might find useful as you write
programs that use turtles.

-   Turtle methods can use negative angles or distances. So
    `tess.forward(-100)`{.docutils .literal .notranslate} will move tess
    backwards, and `tess.left(-30)`{.docutils .literal .notranslate}
    turns her to the right. Additionally, because there are 360 degrees
    in a circle, turning 30 to the left will leave you facing in the
    same direction as turning 330 to the right! (The on-screen animation
    will differ, though --- you will be able to tell if tess is turning
    clockwise or counter-clockwise!)

    This suggests that we don't need both a left and a right turn method
    --- we could be minimalists, and just have one method. There is also
    a *backward* method. (If you are very nerdy, you might enjoy saying
    `alex.backward(-100)`{.docutils .literal .notranslate} to move alex
    forward!)

    Reviewing a few basic facts about geometry and number lines, like
    we've done here is a good start if we're going to play with turtles.

-   A turtle's pen can be picked up or put down. This allows us to move
    a turtle to a different place without drawing a line. The methods
    are `up`{.docutils .literal .notranslate} and `down`{.docutils
    .literal .notranslate}. Note that the methods `penup`{.docutils
    .literal .notranslate} and `pendown`{.docutils .literal
    .notranslate} do the same thing.

    ::: {.highlight-python .notranslate}
    ::: {.highlight}
        alex.up()
        alex.forward(100)     # this moves alex, but no line is drawn
        alex.down()
    :::
    :::

-   Every turtle can have its own shape. The ones available "out of the
    box" are `arrow`{.docutils .literal .notranslate}, `blank`{.docutils
    .literal .notranslate}, `circle`{.docutils .literal .notranslate},
    `classic`{.docutils .literal .notranslate}, `square`{.docutils
    .literal .notranslate}, `triangle`{.docutils .literal .notranslate},
    `turtle`{.docutils .literal .notranslate}.

    ::: {.highlight-python .notranslate}
    ::: {.highlight}
        ...
        alex.shape("turtle")
        ...
    :::
    :::

-   You can speed up or slow down the turtle's animation speed.
    (Animation controls how quickly the turtle turns and moves forward).
    Speed settings can be set between 1 (slowest) to 10 (fastest). But
    if you set the speed to 0, it has a special meaning --- turn off
    animation and go as fast as possible.

    ::: {.highlight-python .notranslate}
    ::: {.highlight}
        alex.speed(10)
    :::
    :::

-   A turtle can "stamp" its footprint onto the canvas, and this will
    remain after the turtle has moved somewhere else. Stamping works
    even when the pen is up.

Let's do an example that shows off some of these new features.

::: {.runestone .explainer .ac_section}
::: {#ac3_7_1 component="activecode" question_label="5.6.1"}
::: {#ac3_7_1_question .ac_question}
:::
:::
:::

If you are curious about how far the turtle is traveling each time the
for loop iterates, you can add a print statement inside of the for loop
to print out the value of `dist`{.docutils .literal .notranslate}.

One more thing to be careful about. All except one of the shapes you see
on the screen here are footprints created by `stamp`{.docutils .literal
.notranslate}. But the program still only has *one* turtle instance ---
can you figure out which one is the real tess? (Hint: if you're not
sure, write a new line of code after the `for`{.docutils .literal
.notranslate} loop to change tess' color, or to put her pen down and
draw a line, or to change her shape, etc.)

**Mixed up program**

::: {.runestone .parsons-container}
::: {#pp3_7_1 .parsons component="parsons"}
::: {.parsons_question .parsons-text}
The following program uses the stamp method to create a circle of turtle
shapes as shown to the left:

[![image of a circle of turtle
shapes](../_images/TurtleCircle.png){.align-left}](../_images/TurtleCircle.png){.reference
.internal .image-reference}

But the lines are mixed up. The program should do all necessary set-up,
create the turtle, set the shape to "turtle", and pick up the pen. Then
the turtle should repeat the following ten times: go forward 50 pixels,
leave a copy of the turtle at the current position, reverse for 50
pixels, and then turn right 36 degrees. After the loop, set the window
to close when the user clicks in it.

Drag the blocks of statements from the left column to the right column
and put them in the right order with the correct indention. Click on
*Check Me* to see if you are right. You will be told if any of the lines
are in the wrong order or are incorrectly indented.
:::

``` {.parsonsblocks question_label="5.6.2" style="visibility: hidden;"}
        import turtle
wn = turtle.Screen()
jose = turtle.Turtle()
jose.shape("turtle")
jose.penup()
---
for size in range(10):
---
  jose.forward(50)
---
  jose.stamp()
---
  jose.forward(-50)
---
  jose.right(36)
---
wn.exitonclick()
        
```
:::
:::

**Mixed up program**

::: {.runestone .parsons-container}
::: {#pp3_7_2 .parsons component="parsons"}
::: {.parsons_question .parsons-text}
The following program uses the stamp method to create a line of turtle
shapes as shown to the left:

[![image of a line of turtle
shapes](../_images/Turtle3Stamp.png){.align-left}](../_images/Turtle3Stamp.png){.reference
.internal .image-reference}

But the lines are mixed up. The program should do all necessary set-up,
create the turtle, set the shape to "turtle", and pick up the pen. Then
the turtle should repeat the following three times: go forward 50 pixels
and leave a copy of the turtle at the current position. After the loop,
set the window to close when the user clicks in it.

Drag the blocks of statements from the left column to the right column
and put them in the right order with the correct indention. Click on
*Check Me* to see if you are right. You will be told if any of the lines
are in the wrong order or are incorrectly indented.
:::

``` {.parsonsblocks question_label="5.6.3" style="visibility: hidden;"}
        import turtle
wn = turtle.Screen()
---
nikea = turtle.Turtle()
---
nikea.shape("turtle")
---
nikea.penup()
---
for size in range(3):
---
  nikea.forward(50)
---
  nikea.stamp()
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

-   [[](RepetitionwithaForLoop.html)]{#relations-prev}
-   [[](SummaryOfTurtleMethods.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
