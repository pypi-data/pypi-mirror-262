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
        Problem](/runestone/default/reportabug?course=fopp&page=week3a1)
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
::: {#chapter-assessment .section}
[8.14. ]{.section-number}Chapter Assessment[¶](#chapter-assessment "Permalink to this heading"){.headerlink}
============================================================================================================

**Check your understanding**

::: {.runestone .explainer .ac_section}
::: {#assess_ps3_1_1_1 component="activecode" question_label="8.14.1"}
::: {#assess_ps3_1_1_1_question .ac_question}
`rainfall_mi`{.docutils .literal .notranslate} is a string that contains
the average number of inches of rainfall in Michigan for every month (in
inches) with every month separated by a comma. Write code to compute the
number of months that have more than 3 inches of rainfall. Store the
result in the variable `num_rainy_months`{.docutils .literal
.notranslate}. In other words, count the number of items with values
`> 3.0`{.docutils .literal .notranslate}.

Hard-coded answers will receive no credit.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ps3_1_1_2 component="activecode" question_label="8.14.2"}
::: {#assess_ps3_1_1_2_question .ac_question}
The variable `sentence`{.docutils .literal .notranslate} stores a
string. Write code to determine how many words in `sentence`{.docutils
.literal .notranslate} start and end with the same letter, including
one-letter words. Store the result in the variable
`same_letter_count`{.docutils .literal .notranslate}.

Hard-coded answers will receive no credit.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ps3_1_1_3 component="activecode" question_label="8.14.3"}
::: {#assess_ps3_1_1_3_question .ac_question}
Write code to count the number of strings in list `items`{.docutils
.literal .notranslate} that have the character `w`{.docutils .literal
.notranslate} in it. Assign that number to the variable
`acc_num`{.docutils .literal .notranslate}.

HINT 1: Use the accumulation pattern!

HINT 2: the `in`{.docutils .literal .notranslate} operator checks
whether a substring is present in a string.

Hard-coded answers will receive no credit.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ps3_1_1_4 component="activecode" question_label="8.14.4"}
::: {#assess_ps3_1_1_4_question .ac_question}
Write code that counts the number of words in `sentence`{.docutils
.literal .notranslate} that contain *either* an "a" or an "e". Store the
result in the variable `num_a_or_e`{.docutils .literal .notranslate}.

Note 1: be sure to not double-count words that contain both an a and an
e.

HINT 1: Use the `in`{.docutils .literal .notranslate} operator.

HINT 2: You can either use `or`{.docutils .literal .notranslate} or
`elif`{.docutils .literal .notranslate}.

Hard-coded answers will receive no credit.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ps3_1_1_5 component="activecode" question_label="8.14.5"}
::: {#assess_ps3_1_1_5_question .ac_question}
Write code that will count the number of vowels in the sentence
`s`{.docutils .literal .notranslate} and assign the result to the
variable `num_vowels`{.docutils .literal .notranslate}. For this
problem, vowels are only a, e, i, o, and u. Hint: use the `in`{.docutils
.literal .notranslate} operator with `vowels`{.docutils .literal
.notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ac3_1_1_6 component="activecode" question_label="8.14.6"}
::: {#assess_ac3_1_1_6_question .ac_question}
Create one conditional so that if "Friendly" is in `w`{.docutils
.literal .notranslate}, then "Friendly is here!" should be assigned to
the variable `wrd`{.docutils .literal .notranslate}. If it's not, check
if "Friend" is in `w`{.docutils .literal .notranslate}. If so, the
string "Friend is here!" should be assigned to the variable
`wrd`{.docutils .literal .notranslate}, otherwise "No variation of
friend is in here." should be assigned to the variable `wrd`{.docutils
.literal .notranslate}. (Also consider: does the order of your
conditional statements matter for this problem? Why?)
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ac3_1_1_7 component="activecode" question_label="8.14.7"}
::: {#assess_ac3_1_1_7_question .ac_question}
We have written conditionals for you to use. Create the variable x and
assign it some integer so that at the end of the code,
`output`{.docutils .literal .notranslate} will be assigned the string
`"Consistently working"`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ac3_1_1_8 component="activecode" question_label="8.14.8"}
::: {#assess_ac3_1_1_8_question .ac_question}
Write code so that if `"STATS 250"`{.docutils .literal .notranslate} is
in the list `schedule`{.docutils .literal .notranslate}, then the string
`"You could be in Information Science!"`{.docutils .literal
.notranslate} is assigned to the variable `resp`{.docutils .literal
.notranslate}. Otherwise, the string `"That's too bad."`{.docutils
.literal .notranslate} should be assigned to the variable
`resp`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ac3_1_1_9 component="activecode" question_label="8.14.9"}
::: {#assess_ac3_1_1_9_question .ac_question}
Create the variable `z`{.docutils .literal .notranslate} whose value is
`30`{.docutils .literal .notranslate}. Write code to see if
`z`{.docutils .literal .notranslate} is greater than `y`{.docutils
.literal .notranslate}. If so, add 5 to `y`{.docutils .literal
.notranslate}'s value, otherwise do nothing. Then, multiply
`z`{.docutils .literal .notranslate} and `y`{.docutils .literal
.notranslate}, and assign the resulting value to the variable
`x`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ac3_1_1_10 component="activecode" question_label="8.14.10"}
::: {#assess_ac3_1_1_10_question .ac_question}
For each string in `wrd_lst`{.docutils .literal .notranslate}, find the
number of characters in the string. If the number of characters is less
than 6, add 1 to `accum`{.docutils .literal .notranslate} so that in the
end, `accum`{.docutils .literal .notranslate} will contain an integer
representing the total number of words in the list that have fewer than
6 characters.
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

-   [[](Exercises.html)]{#relations-prev}
-   [[](../TransformingSequences/toctree.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
