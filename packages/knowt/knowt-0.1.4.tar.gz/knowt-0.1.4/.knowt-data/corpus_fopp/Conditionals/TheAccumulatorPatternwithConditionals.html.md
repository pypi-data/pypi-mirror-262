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
        Problem](/runestone/default/reportabug?course=fopp&page=TheAccumulatorPatternwithConditionals)
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
::: {#the-accumulator-pattern-with-conditionals .section}
[8.10. ]{.section-number}The Accumulator Pattern with Conditionals[¶](#the-accumulator-pattern-with-conditionals "Permalink to this heading"){.headerlink}
==========================================================================================================================================================

Sometimes when we're accumulating, we don't want to add to our
accumulator every time we iterate. Consider, for example, the following
program which counts the number of letters in a phrase.

::: {.runestone .explainer .ac_section}
::: {#ac7_10_1 component="activecode" question_label="8.10.1"}
::: {#ac7_10_1_question .ac_question}
:::
:::
:::

Here, we **initialize** the accumulator variable to be zero on line two.

We **iterate** through the sequence (line 3).

The **update** step happens in two parts. First, we check to see if the
value of `char`{.docutils .literal .notranslate} is not a space. If it
is not a space, then we update the value of our accumulator variable
`tot`{.docutils .literal .notranslate} (on line 6) by adding one to it.
If that conditional proves to be False, which means that char *is* a
space, then we don't update `tot`{.docutils .literal .notranslate} and
continue the for loop. We could have written `tot = tot + 1`{.docutils
.literal .notranslate} or `tot += 1`{.docutils .literal .notranslate},
either is fine.

At the end, we have accumulated a the total number of letters in the
phrase. Without using the conditional, we would have only been able to
count how many characters there are in the string and not been able to
differentiate between spaces and non-spaces.

We can use conditionals to also count if particular items are in a
string or list. The following code finds all occurrences of vowels in
the following string.

::: {.runestone .explainer .ac_section}
::: {#ac7_10_2 component="activecode" question_label="8.10.2"}
::: {#ac7_10_2_question .ac_question}
:::
:::
:::

We can also use `==`{.docutils .literal .notranslate} to execute a
similar operation. Here, we'll check to see if the character we are
iterating over is an "o". If it is an "o" then we will update our
counter.

![a gif that shows code to check that \"o\" is in the phrase
\"onomatopoeia\".](../_images/accum_o.gif)

::: {#accumulating-the-max-value .section}
[8.10.1. ]{.section-number}Accumulating the Max Value[¶](#accumulating-the-max-value "Permalink to this heading"){.headerlink}
------------------------------------------------------------------------------------------------------------------------------

We can also use the accumulation pattern with conditionals to find the
maximum or minimum value. Instead of continuing to build up the
accumulator value like we have when counting or finding a sum, we can
reassign the accumulator variable to a different value.

The following example shows how we can get the maximum value from a list
of integers.

::: {.runestone .explainer .ac_section}
::: {#ac7_10_3 component="activecode" question_label="8.10.1.1"}
::: {#ac7_10_3_question .ac_question}
:::
:::
:::

Here, we initialize best\_num to zero, assuming that there are no
negative numbers in the list.

In the for loop, we check to see if the current value of n is greater
than the current value of `best_num`{.docutils .literal .notranslate}.
If it is, then we want to **update** `best_num`{.docutils .literal
.notranslate} so that it now is assigned the higher number. Otherwise,
we do nothing and continue the for loop.

You may notice that the current structure could be a problem. If the
numbers were all negative what would happen to our code? What if we were
looking for the smallest number but we initialized `best_num`{.docutils
.literal .notranslate} with zero? To get around this issue, we can
initialize the accumulator variable using one of the numbers in the
list.

::: {.runestone .explainer .ac_section}
::: {#ac7_10_4 component="activecode" question_label="8.10.1.2"}
::: {#ac7_10_4_question .ac_question}
:::
:::
:::

The only thing we changed was the value of `best_num`{.docutils .literal
.notranslate} on line 2 so that the value of `best_num`{.docutils
.literal .notranslate} is the first element in `nums`{.docutils .literal
.notranslate}, but the result is still the same!

**Check your understanding**

::: {.runestone}
-   [2]{#question7_10_1_opt_a}
-   Though only two of the letters in the list are found, we count them
    each time they appear.
-   [5]{#question7_10_1_opt_b}
-   Yes, we add to x each time we come across a letter in the list.
-   [0]{#question7_10_1_opt_c}
-   Check again what the conditional is evaluating. The value of i will
    be a character in the string s, so what will happen in the if
    statement?
-   [There is an error in the code so it cannot
    run.]{#question7_10_1_opt_d}
-   There are no errors in this code.
:::

::: {.runestone}
-   [10]{#question7_10_2_opt_a}
-   Not quite. What is the conditional checking?
-   [1]{#question7_10_2_opt_b}
-   min\_value was set to a number that was smaller than any of the
    numbers in the list, so it was never updated in the for loop.
-   [0]{#question7_10_2_opt_c}
-   Yes, min\_value was set to a number that was smaller than any of the
    numbers in the list, so it was never updated in the for loop.
-   [There is an error in the code so it cannot
    run.]{#question7_10_2_opt_d}
-   The code does not have an error that would prevent it from running.
:::

::: {.runestone .explainer .ac_section}
::: {#ac7_10_5 component="activecode" question_label="8.10.1.5"}
::: {#ac7_10_5_question .ac_question}
For each string in the list `words`{.docutils .literal .notranslate},
find the number of characters in the string. If the number of characters
in the string is greater than 3, add 1 to the variable
`num_words`{.docutils .literal .notranslate} so that
`num_words`{.docutils .literal .notranslate} should end up with the
total number of words with more than 3 characters.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac7_10_7 component="activecode" question_label="8.10.1.6"}
::: {#ac7_10_7_question .ac_question}
**Challenge** For each word in `words`{.docutils .literal .notranslate},
add 'd' to the end of the word if the word ends in "e" to make it past
tense. Otherwise, add 'ed' to make it past tense. Save these past tense
words to a list called `past_tense`{.docutils .literal .notranslate}.
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

-   [[](Chainedconditionals.html)]{#relations-prev}
-   [[](WPSettingUpConditionals.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
