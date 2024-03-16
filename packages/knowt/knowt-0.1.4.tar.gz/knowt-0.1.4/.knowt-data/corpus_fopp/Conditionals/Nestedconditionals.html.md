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
        Problem](/runestone/default/reportabug?course=fopp&page=Nestedconditionals)
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
::: {#nested-conditionals .section}
[]{#index-0}

[8.8. ]{.section-number}Nested conditionals[¶](#nested-conditionals "Permalink to this heading"){.headerlink}
=============================================================================================================

One conditional can also be **nested** within another. For example,
assume we have two integer variables, `x`{.docutils .literal
.notranslate} and `y`{.docutils .literal .notranslate}. The following
pattern of selection shows how we might decide how they are related to
each other.

::: {.highlight-python .notranslate}
::: {.highlight}
    if x < y:
        print("x is less than y")
    else:
        if x > y:
            print("x is greater than y")
        else:
            print("x and y must be equal")
:::
:::

The outer conditional contains two branches. The second branch (the else
from the outer) contains another `if`{.docutils .literal .notranslate}
statement, which has two branches of its own. Those two branches could
contain conditional statements as well.

The flow of control for this example can be seen in this flowchart
illustration.

![](../_images/flowchart_nested_conditional.png)

Here is a complete program that defines values for `x`{.docutils
.literal .notranslate} and `y`{.docutils .literal .notranslate}. Run the
program and see the result. Then change the values of the variables to
change the flow of control.

::: {.runestone .explainer .ac_section}
::: {#ac7_8_1 component="activecode" question_label="8.8.1"}
::: {#ac7_8_1_question .ac_question}
:::
:::
:::

::: {.admonition .note}
Note

In some programming languages, matching the if and the else is a
problem. However, in Python this is not the case. The indentation
pattern tells us exactly which else belongs to which if.
:::

If you are still a bit unsure, here is the same selection as part of a
codelens example. Step through it to see how the correct
`print`{.docutils .literal .notranslate} is chosen.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="8.8.2"}
::: {#clens7_8_1_question .ac_question}
:::

::: {#clens7_8_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 8.8.2 (clens7\_8\_1)]{.runestone_caption_text}
:::
:::

**Check your understanding**

::: {.runestone}
-   [No]{#question7_8_1_opt_a}
-   This is a legal nested if-else statement. The inner if-else
    statement is contained completely within the body of the outer
    else-block.
-   [Yes]{#question7_8_1_opt_b}
-   This is a legal nested if-else statement. The inner if-else
    statement is contained completely within the body of the outer
    else-block.
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

-   [[](OmittingtheelseClauseUnarySelection.html)]{#relations-prev}
-   [[](Chainedconditionals.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
