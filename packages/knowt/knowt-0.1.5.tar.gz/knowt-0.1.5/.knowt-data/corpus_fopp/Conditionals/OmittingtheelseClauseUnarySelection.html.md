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
        Problem](/runestone/default/reportabug?course=fopp&page=OmittingtheelseClauseUnarySelection)
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
::: {#omitting-the-else-clause-unary-selection .section}
[]{#index-0}

[8.7. ]{.section-number}Omitting the `else`{.docutils .literal .notranslate} Clause: Unary Selection[¶](#omitting-the-else-clause-unary-selection "Permalink to this heading"){.headerlink}
===========================================================================================================================================================================================

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#unaryselection .align-left .youtube-video component="youtube" video-height="315" question_label="8.7.1" video-width="560" video-videoid="Fd4a8ktQURc" video-divid="unaryselection" video-start="0" video-end="-1"}
:::
:::

Flowchart of an **if** with no **else**

![](../_images/flowchart_if_only.png)

Another form of the `if`{.docutils .literal .notranslate} statement is
one in which the `else`{.docutils .literal .notranslate} clause is
omitted entirely. This creates what is sometimes called **unary
selection**. In this case, when the condition evaluates to
`True`{.docutils .literal .notranslate}, the statements are executed.
Otherwise the flow of execution continues to the statement after the
body of the `if`{.docutils .literal .notranslate}.

::: {.runestone .explainer .ac_section}
::: {#ac7_7_1 component="activecode" question_label="8.7.2"}
::: {#ac7_7_1_question .ac_question}
:::
:::
:::

What would be printed if the value of `x`{.docutils .literal
.notranslate} is negative? Try it.

**Check your understanding**

::: {.runestone}
-   [Output a]{#question7_7_1_opt_a}
-   Because -10 is less than 0, Python will execute the body of the
    if-statement here.
-   [Output b]{#question7_7_1_opt_b}
-   Python executes the body of the if-block as well as the statement
    that follows the if-block.
-   [Output c]{#question7_7_1_opt_c}
-   Python will also execute the statement that follows the if-block
    (because it is not enclosed in an else-block, but rather just a
    normal statement).
-   [It will cause an error because every if must have an else
    clause.]{#question7_7_1_opt_d}
-   It is valid to have an if-block without a corresponding else-block
    (though you cannot have an else-block without a corresponding
    if-block).
:::

::: {.runestone}
-   [No]{#question7_7_2_opt_a}
-   Every else-block must have exactly one corresponding if-block. If
    you want to chain if-else statements together, you must use the else
    if construct, described in the chained conditionals section.
-   [Yes]{#question7_7_2_opt_b}
-   This will cause an error because the second else-block is not
    attached to a corresponding if-block.
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

-   [[](ConditionalExecutionBinarySelection.html)]{#relations-prev}
-   [[](Nestedconditionals.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
