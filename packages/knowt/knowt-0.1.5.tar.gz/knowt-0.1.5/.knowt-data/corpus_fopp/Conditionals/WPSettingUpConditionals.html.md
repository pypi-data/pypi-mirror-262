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
        Problem](/runestone/default/reportabug?course=fopp&page=WPSettingUpConditionals)
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
::: {#setting-up-conditionals .section}
[8.11. ]{.section-number}👩‍💻 Setting Up Conditionals[¶](#setting-up-conditionals "Permalink to this heading"){.headerlink}
==========================================================================================================================

Before writing your conditionals, it can be helpful to make your own
flowchart that will plot out the flow of each condition. By writing out
the flow, you can better determine how complex the set of conditionals
will be as well as check to see if any condition is not taken care of
before you begin writing it out.

To make sure that your code covers all of the conditions that you intend
for it to cover, you should add comments for each clause that explains
what that clause is meant to do. Then, you should add tests for each
possible path that the program could go though. What leads to certain
conditional statements being executed? Is that what you intended?

::: {#choosing-your-type-of-conditional .section}
[8.11.1. ]{.section-number}Choosing your type of Conditional[¶](#choosing-your-type-of-conditional "Permalink to this heading"){.headerlink}
--------------------------------------------------------------------------------------------------------------------------------------------

When adding conditionals to your program, you should also consider the
kinds of conditionals that are at your disposal and what would fit best.

![](../_images/valid_conditionals.png)

Though you'll use them often, remember that conditional statements don't
always need an else clause. When deciding the flow, ask yourself what
you want to have happen under a certain condition. For example, if you
wanted to find all of the words that have the letter 'n' in them. If
there's nothing that needs to happen when a word does not contain the
letter 'n' then you won't need an else clause. The program should just
continue onward!

::: {.runestone}
-   [If statement - Else statement]{#question7_11_1_opt_a}
-   Using if/else either uses an unnecessary else statement or would
    improperly keep track of one of the accumulator variables.
-   [If statement - Elif statement]{#question7_11_1_opt_b}
-   Using if/elif means that words that have both a \"t\" and a \"z\"
    would not be propperly counted by the two variables.
-   [If statement - If statement]{#question7_11_1_opt_c}
-   Yes, two if statements will keep track of - and properly update -
    the two different accumulator variables.
-   [If statement - Elif statemenet - Else
    statement]{#question7_11_1_opt_d}
-   Using if/elif/else here will provide an unnecessary else statement
    and improperly update one of the accumulator variables in the case
    where a word has both a \"t\" and a \"z\".
:::

::: {.runestone}
-   [If statement - Elif statemenet - Else
    statement]{#question7_11_2_opt_a}
-   The elif and else statements are both unnecessary.
-   [If statement - Else statement]{#question7_11_2_opt_b}
-   The else statement is unnecessary.
-   [If statement - Nested If statement]{#question7_11_2_opt_c}
-   Though you could write a set of conditional statements like this and
    answer the prompt, there is a more concise way.
-   [If statement]{#question7_11_2_opt_d}
-   Yes, this is the most concise way of writing a conditional for that
    prompt.
-   [If statement - Nested If statement - Else
    statement]{#question7_11_2_opt_e}
-   The else statement is unnecessary.
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

-   [[](TheAccumulatorPatternwithConditionals.html)]{#relations-prev}
-   [[](Glossary.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
