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
        Problem](/runestone/default/reportabug?course=fopp&page=ObjectInstances)
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
::: {#object-oriented-concepts .section}
[5.4. ]{.section-number}Object Oriented Concepts[¶](#object-oriented-concepts "Permalink to this heading"){.headerlink}
=======================================================================================================================

It's been fun drawing things with the turtles. In the process, we've
slipped in some new concepts and terms. Let's pull them out and examine
them a little more carefully.

::: {#user-defined-classes .section}
[5.4.1. ]{.section-number}User-defined Classes[¶](#user-defined-classes "Permalink to this heading"){.headerlink}
-----------------------------------------------------------------------------------------------------------------

First, just as Python provides a way to define new functions in your
programs, it also provides a way to define new classes of objects. Later
in the book you will learn how to define functions, and much later, new
classes of objects. For now, you just need to understand how to use
them.
:::

::: {#instances .section}
[5.4.2. ]{.section-number}Instances[¶](#instances "Permalink to this heading"){.headerlink}
-------------------------------------------------------------------------------------------

Given a class like `Turtle`{.docutils .literal .notranslate} or
`Screen`{.docutils .literal .notranslate}, we create a new instance with
a syntax that looks like a function call, `Turtle()`{.docutils .literal
.notranslate}. The Python interpreter figures out that Turtle is a class
rather than a function, and so it creates a new instance of the class
and returns it. Since the Turtle class was defined in a separate module,
(confusingly, also named turtle), we had to refer to the class as
turtle.Turtle. Thus, in the programs we wrote
`turtle.Turtle()`{.docutils .literal .notranslate} to make a new turtle.
We could also write `turtle.Screen()`{.docutils .literal .notranslate}
to make a new window for our turtles to paint in.
:::

::: {#attributes .section}
[5.4.3. ]{.section-number}Attributes[¶](#attributes "Permalink to this heading"){.headerlink}
---------------------------------------------------------------------------------------------

Each instance can have attributes, sometimes called **instance
variables**. These are just like other variables in Python. We use
assignment statements, with an =, to assign values to them. Thus, if
alex and tess are variables bound to two instances of the class Turtle,
we can assign values to an attribute, and we can look up those
attributes. For example, the following code would print out 1100.

::: {.highlight-python .notranslate}
::: {.highlight}
    alex.price = 500
    tess.price = 600
    print(alex.price + tess.price)
:::
:::
:::

::: {#methods .section}
[5.4.4. ]{.section-number}Methods[¶](#methods "Permalink to this heading"){.headerlink}
---------------------------------------------------------------------------------------

Classes have associated **methods**, which are just a special kind of
function. Consider the expression `alex.forward(50)`{.docutils .literal
.notranslate} The interpreter first looks up alex and finds that it is
an instance of the class Turtle. Then it looks up the attribute forward
and finds that it is a method. Since there is a left parenthesis
directly following, the interpreter invokes the method, passing 50 as a
parameter.

The only difference between a method invocation and other function calls
is that the object instance itself is also passed as a parameter. Thus
`alex.forward(50)`{.docutils .literal .notranslate} moves alex, while
`tess.forward(50)`{.docutils .literal .notranslate} moves tess.

Some of the methods of the Turtle class set attributes that affect the
actions of other methods. For example, the method pensize changes the
width of the drawing pen, and the color method changes the pen's color.

Methods return values, just as functions do. However, none of the
methods of the Turtle class that you have used return useful values the
way the `len`{.docutils .literal .notranslate} function does. Thus, it
would not make sense to build a complex expression like
`tess.forward(50) + 75`{.docutils .literal .notranslate}. It could make
sense, however to put a complex expression inside the parentheses:
`tess.forward(x + y)`{.docutils .literal .notranslate}
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

-   [[](InstancesAHerdofTurtles.html)]{#relations-prev}
-   [[](RepetitionwithaForLoop.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
