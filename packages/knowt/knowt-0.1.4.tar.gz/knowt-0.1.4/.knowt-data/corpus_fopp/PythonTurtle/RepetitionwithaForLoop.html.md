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
        Problem](/runestone/default/reportabug?course=fopp&page=RepetitionwithaForLoop)
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
::: {#repetition-with-a-for-loop .section}
[5.5. ]{.section-number}Repetition with a For Loop[¶](#repetition-with-a-for-loop "Permalink to this heading"){.headerlink}
===========================================================================================================================

Some of the programs we've seen so far are a bit tedious to type. If we
want to make a repetitive pattern in our drawings, then it can take many
lines of code. Thankfully, Python has a few ways for making this kind of
task easier. For now you'll get a brief preview of a helpful control
structure and function in Python which you will learn about later.

The control structure is called a for loop. If you've learned other
programming languages then you may be familiar with what it does but the
structure may be new. A for loop allows Python to execute a program in a
non-linear fashion. Instead of evaluating the code line by line until it
reaches the end, once the program reaches a for loop, it will tell the
program to execute a set of lines repeatedly. After doing all that, the
program will then continue to evaluate and execute whatever is below the
for loop.

In the code below, we make use of the `range`{.docutils .literal
.notranslate} function to specify how many times the code inside the for
loop will execute. In a later chapter, we will explain exactly what the
range function is doing and how it works with the for loop. For now,
just try to understand what happens when the following code executes.

::: {.runestone .explainer .ac_section}
::: {#ac3_5_1 component="activecode" question_label="5.5.1"}
::: {#ac3_5_1_question .ac_question}
:::
:::
:::

There are a few things to notice here for when you use this later on.
First, is that the two print statements on line 4 and 5 are executed
three times, but we don't print line 4 three times and then print line 5
three times. Instead, we print line 4, then line 5. Once that is done
the for loop iterates, or brings the program back to the beginning of
the for loop, and continues to print out lines 4 and 5 again until it
has printed them both a total of three times.

Second, these lines were printed the same number of times as is inside
the `range`{.docutils .literal .notranslate} function. If we wanted to
print them more or fewer times, then we would just need to change the
number inside of the parentheses on line 3.

Finally, the indentation is important here. All of the statements that
were printed out multiple times were indented under the for loop. Once
we stopped indenting those lines, then the program was outside of the
for loop and it would continue to execute linearly. If you'd like to
watch the execution, checkout the code above in codelens!

Now it's time to combine this with the Turtle module. We can do a lot of
cool stuff if we combine these two things! Below is code to do just
that. Try to predict what the program will do before running it.

::: {.runestone .explainer .ac_section}
::: {#ac3_5_2 component="activecode" question_label="5.5.2"}
::: {#ac3_5_2_question .ac_question}
:::
:::
:::

::: {.admonition .note}
Note

Try it out yourself in the space below. What can you make?

::: {.runestone .explainer .ac_section}
::: {#ac3_5_3 component="activecode" question_label="5.5.3"}
::: {#ac3_5_3_question .ac_question}
:::
:::
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

-   [[](ObjectInstances.html)]{#relations-prev}
-   [[](AFewMoreturtleMethodsandObservations.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
