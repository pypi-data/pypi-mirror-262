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
        Problem](/runestone/default/reportabug?course=fopp&page=RandomlyWalkingTurtles)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [14.1 Introduction](intro-indefiniteiteration.html){.reference
        .internal}
    -   [14.2 The while Statement](ThewhileStatement.html){.reference
        .internal}
    -   [14.3 The Listener Loop](listenerLoop.html){.reference
        .internal}
    -   [14.4 Randomly Walking
        Turtles](RandomlyWalkingTurtles.html){.reference .internal}
    -   [14.5 Break and Continue](BreakandContinue.html){.reference
        .internal}
    -   [14.6 👩‍💻 Infinite Loops](WPInfiniteLoops.html){.reference
        .internal}
    -   [14.7 Exercises](Exercises.html){.reference .internal}
    -   [14.8 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#randomly-walking-turtles .section}
[]{#id1}

[14.4. ]{.section-number}Randomly Walking Turtles[¶](#randomly-walking-turtles "Permalink to this heading"){.headerlink}
========================================================================================================================

Suppose we want to entertain ourselves by watching a turtle wander
around randomly inside the screen. When we run the program we want the
turtle and program to behave in the following way:

1.  The turtle begins in the center of the screen.

2.  Flip a coin. If it's heads then turn to the left 90 degrees. If it's
    tails then turn to the right 90 degrees.

3.  Take 50 steps forward.

4.  If the turtle has moved outside the screen then stop, otherwise go
    back to step 2 and repeat.

Notice that we cannot predict how many times the turtle will need to
flip the coin before it wanders out of the screen, so we can't use a for
loop in this case. In fact, although very unlikely, this program might
never end, that is why we call this indefinite iteration.

So based on the problem description above, we can outline a program as
follows:

::: {.highlight-python .notranslate}
::: {.highlight}
    create a window and a turtle

    while the turtle is still in the window:
        generate a random number between 0 and 1
        if the number == 0 (heads):
            turn left
        else:
            turn right
        move the turtle forward 50
:::
:::

Now, probably the only thing that seems a bit confusing to you is the
part about whether or not the turtle is still in the screen. But this is
the nice thing about programming, we can delay the tough stuff and get
*something* in our program working right away. The way we are going to
do this is to delegate the work of deciding whether the turtle is still
in the screen or not to a boolean function. Let's call this boolean
function `isInScreen`{.docutils .literal .notranslate} We can write a
very simple version of this boolean function by having it always return
`True`{.docutils .literal .notranslate}, or by having it decide
randomly, the point is to have it do something simple so that we can
focus on the parts we already know how to do well and get them working.
Since having it always return True would not be a good idea we will
write our version to decide randomly. Let's say that there is a 90%
chance the turtle is still in the window and 10% that the turtle has
escaped.

::: {.runestone .explainer .ac_section}
::: {#ac14_4_1 component="activecode" question_label="14.4.1"}
::: {#ac14_4_1_question .ac_question}
:::
:::
:::

Now we have a working program that draws a random walk of our turtle
that has a 90% chance of staying on the screen. We are in a good
position, because a large part of our program is working and we can
focus on the next bit of work -- deciding whether the turtle is inside
the screen boundaries or not.

We can find out the width and the height of the screen using the
`window_width`{.docutils .literal .notranslate} and
`window_height`{.docutils .literal .notranslate} methods of the screen
object. However, remember that the turtle starts at position 0,0 in the
middle of the screen. So we never want the turtle to go farther right
than width/2 or farther left than negative width/2. We never want the
turtle to go further up than height/2 or further down than negative
height/2. Once we know what the boundaries are we can use some
conditionals to check the turtle position against the boundaries and
return `False`{.docutils .literal .notranslate} if the turtle is outside
or `True`{.docutils .literal .notranslate} if the turtle is inside.

Once we have computed our boundaries we can get the current position of
the turtle and then use conditionals to decide. Here is one
implementation:

::: {.highlight-python .notranslate}
::: {.highlight}
    def isInScreen(wn,t):
        leftBound = -(wn.window_width() / 2)
        rightBound = wn.window_width() / 2
        topBound = wn.window_height() / 2
        bottomBound = -(wn.window_height() / 2)

        turtleX = t.xcor()
        turtleY = t.ycor()

        stillIn = True
        if turtleX > rightBound or turtleX < leftBound:
            stillIn = False
        if turtleY > topBound or turtleY < bottomBound:
            stillIn = False

        return stillIn
:::
:::

There are lots of ways that the conditional could be written. In this
case we have given `stillIn`{.docutils .literal .notranslate} the
default value of `True`{.docutils .literal .notranslate} and use two
`if`{.docutils .literal .notranslate} statements to possibly set the
value to `False`{.docutils .literal .notranslate}. You could rewrite
this to use nested conditionals or `elif`{.docutils .literal
.notranslate} statements and set `stillIn`{.docutils .literal
.notranslate} to `True`{.docutils .literal .notranslate} in an else
clause.

Here is the full version of our random walk program.

::: {.runestone .explainer .ac_section}
::: {#ac14_4_2 component="activecode" question_label="14.4.2"}
::: {#ac14_4_2_question .ac_question}
:::
:::
:::

We could have written this program without using a boolean function. You
might want to try to rewrite it using a complex condition on the while
statement. However, using a boolean function makes the program much more
readable and easier to understand. It also gives us another tool to use
if this was a larger program and we needed to have a check for whether
the turtle was still in the screen in another part of the program.
Another advantage is that if you ever need to write a similar program,
you can reuse this function with confidence the next time you need it.
Breaking up this program into a couple of parts is another example of
functional decomposition.

**Check your understanding**

::: {.runestone}
-   [Returns True if the turtle is still on the screen and False if the
    turtle is no longer on the screen.]{#question14_4_1_opt_a}
-   The isInScreen function computes the boolean test of whether the
    turtle is still in the window. It makes the condition of the while
    loop in the main part of the code simpler.
-   [Uses a while loop to move the turtle randomly until it goes off the
    screen.]{#question14_4_1_opt_b}
-   The isInScreen function does not contain a while-loop. That loop is
    outside the isInScreen function.
-   [Turns the turtle right or left at random and moves the turtle
    forward 50.]{#question14_4_1_opt_c}
-   The isInScreen function does not move the turtle.
-   [Calculates and returns the position of the turtle in the
    window.]{#question14_4_1_opt_d}
-   While the isInScreen function does use the size of the window and
    position of the turtle, it does not return the turtle position.
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

-   [[](listenerLoop.html)]{#relations-prev}
-   [[](BreakandContinue.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
