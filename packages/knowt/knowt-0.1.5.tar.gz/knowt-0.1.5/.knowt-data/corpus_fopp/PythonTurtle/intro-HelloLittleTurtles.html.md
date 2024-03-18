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
        Problem](/runestone/default/reportabug?course=fopp&page=intro-HelloLittleTurtles)
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

::: {#hello-little-turtles .section}
[]{#turtles-chap}[]{#index-0}

[5.1. ]{.section-number}Hello Little Turtles![¶](#hello-little-turtles "Permalink to this heading"){.headerlink}
================================================================================================================

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#vid_turtleintro .align-left .youtube-video component="youtube" video-height="315" question_label="5.1.1" video-width="560" video-videoid="Yxyx6KpKRzY" video-divid="vid_turtleintro" video-start="0" video-end="-1"}
:::
:::

There are many *modules* in Python that provide very powerful features
that we can use in our own programs. Some of these can send email or
fetch web pages. Others allow us to perform complex mathematical
calculations. In this chapter we will introduce a module that allows us
to create a data object called a **turtle** that can be used to draw
pictures.

Turtle graphics, as it is known, is based on a very simple metaphor.
Imagine that you have a turtle that understands English. You can tell
your turtle to do simple commands such as go forward and turn right. As
the turtle moves around, if its tail is down touching the ground, it
will draw a line (leave a trail behind) as it moves. If you tell your
turtle to lift up its tail it can still move around but will not leave a
trail. As you will see, you can make some pretty amazing drawings with
this simple capability.

::: {.admonition .note}
Note

The turtles are fun because they allow us to visualize what our code is
doing, but the real purpose of the chapter is to teach ourselves a
little more Python and to develop our theme of computational thinking.
You'll first draw simple geometric shapes with the turtles, and then
we'll summarize the concepts and syntax you've learned, in particular,
classes, instances, and method invocations. These concepts are the
building blocks of object-oriented programming, a paradigm for
structuring a program that is widespread in every modern programming
language.
:::

::: {#learning-goals .section}
[5.1.1. ]{.section-number}Learning Goals[¶](#learning-goals "Permalink to this heading"){.headerlink}
-----------------------------------------------------------------------------------------------------

-   To understand the use of loops as a way of repeating actions

-   To introduce the idea of looking for patterns when problem solving

-   To distinguish between instances, attributes, and methods
:::

::: {#objectives .section}
[5.1.2. ]{.section-number}Objectives[¶](#objectives "Permalink to this heading"){.headerlink}
---------------------------------------------------------------------------------------------

-   Write a multi-line program (using the turtle framework)

-   Invoke methods & set attributes using dot notation

-   Use the for loop to draw common geometric shapes with the turtle
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

-   [[](toctree.html)]{#relations-prev}
-   [[](OurFirstTurtleProgram.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
