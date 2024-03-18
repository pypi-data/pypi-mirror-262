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
        Problem](/runestone/default/reportabug?course=fopp&page=intro-TurtlesandConditionals)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [8.1 Intro: What we can do with Turtles and
        Conditionals](intro-TurtlesandConditionals.html){.reference
        .internal}
    -   [8.2 Boolean Values and Boolean
        Expressions](BooleanValuesandBooleanExpressions.html){.reference
        .internal}
    -   [8.3 Logical operators](Logicaloperators.html){.reference
        .internal}
    -   [8.4 The in and not in
        operators](Theinandnotinoperators.html){.reference .internal}
    -   [8.5 Precedence of
        Operators](PrecedenceofOperators.html){.reference .internal}
    -   [8.6 Conditional Execution: Binary
        Selection](ConditionalExecutionBinarySelection.html){.reference
        .internal}
    -   [8.7 Omitting the else Clause: Unary
        Selection](OmittingtheelseClauseUnarySelection.html){.reference
        .internal}
    -   [8.8 Nested conditionals](Nestedconditionals.html){.reference
        .internal}
    -   [8.9 Chained conditionals](Chainedconditionals.html){.reference
        .internal}
    -   [8.10 The Accumulator Pattern with
        Conditionals](TheAccumulatorPatternwithConditionals.html){.reference
        .internal}
    -   [8.11 👩‍💻 Setting Up
        Conditionals](WPSettingUpConditionals.html){.reference
        .internal}
    -   [8.12 Glossary](Glossary.html){.reference .internal}
    -   [8.13 Exercises](Exercises.html){.reference .internal}
    -   [8.14 Chapter Assessment](week3a1.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#intro-what-we-can-do-with-turtles-and-conditionals .section}
[8.1. ]{.section-number}Intro: What we can do with Turtles and Conditionals[¶](#intro-what-we-can-do-with-turtles-and-conditionals "Permalink to this heading"){.headerlink}
============================================================================================================================================================================

So far, our programs have either been a series of statements which
always execute sequentially or operations that are applied to each item
in an iterable. Yet programs frequently need to be more subtle with
their behavior. For example, a messaging app might only set a message's
title bold if it has not been read by the user. Or a video game needs to
update the position of all the characters that are not asleep. This is
done with something called a **selection** or a **conditional
statement**.

In the context of turtle drawings, using this kind of statement will
allow us to check conditions and change the behavior of the program
accordingly

::: {.runestone .explainer .ac_section}
::: {#ac7_1_1 component="activecode" question_label="8.1.1"}
::: {#ac7_1_1_question .ac_question}
:::
:::
:::

In the above code, we first set amy's pen color to be "Pink" and then
move her forward. Next we want one of two actions to happen, either amy
should move right and then forward, or left and then forward. The
direction that we want her to go in depends on her pen color. If her pen
color is set to pink - which is determined by writing
`amy.pencolor() == "Pink"`{.docutils .literal .notranslate} which checks
to see if the value returned by `amy.pencolor()`{.docutils .literal
.notranslate} is the equivalent to the string "Pink" - then we should
have her move right and forward. Else (or otherwise) she should move
left and forward. Both things can't happen though. She can't move right,
forward *and* left, forward. We then do the same thing for kenji, though
in this case, we didn't change kenji's pen color.

It might seem a bit odd to add the conditionals in this example.
Wouldn't we already know that we set up amy and kenji's colors, so why
would we need a conditional? While it's true that this isn't the *best*
place to use a conditional, we can combine conditional statements with
for loops to make something pretty cool!

::: {.runestone .explainer .ac_section}
::: {#ac7_1_2 component="activecode" question_label="8.1.2"}
::: {#ac7_1_2_question .ac_question}
:::
:::
:::

The above example combines a for loop with a set of conditional
statements. Here, we loop through a list of colors and each iteration
checks to see what amy's pen color is. Depending on the pen color, the
turtle will move in a certain direction, for a certain distance. Before
the for loop iterates, amy's pen color is changed to whatever
`color`{.docutils .literal .notranslate} is in the for loop and it
continues. Note how the color doesn't change until the end, so that we
can start using whatever color amy is set to initally. This means that
the last color in the list `colors`{.docutils .literal .notranslate}
will not be used, though you can see how the icon changes to the
appropriate color.

This chapter will further detail how to use conditional statements.

::: {#learning-goals .section}
[8.1.1. ]{.section-number}Learning Goals[¶](#learning-goals "Permalink to this heading"){.headerlink}
-----------------------------------------------------------------------------------------------------

-   To understand boolean expressions and logical operators

-   To understand conditional execution

-   To be able to write a boolean function

-   To know when to use binary, unary, chained and nested conditional
    statements
:::

::: {#objectives .section}
[8.1.2. ]{.section-number}Objectives[¶](#objectives "Permalink to this heading"){.headerlink}
---------------------------------------------------------------------------------------------

-   To properly evaluate a (compound) boolean expression

-   To use parenthesis to properly demonstrate operator precedence

-   To use conditional statements to properly branch code
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
-   [[](BooleanValuesandBooleanExpressions.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
