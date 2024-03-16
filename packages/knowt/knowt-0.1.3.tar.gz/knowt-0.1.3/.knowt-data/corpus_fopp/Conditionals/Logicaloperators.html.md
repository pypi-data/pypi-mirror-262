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
        Problem](/runestone/default/reportabug?course=fopp&page=Logicaloperators)
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

::: {#logical-operators .section}
[8.3. ]{.section-number}Logical operators[¶](#logical-operators "Permalink to this heading"){.headerlink}
=========================================================================================================

There are three **logical operators**: `and`{.docutils .literal
.notranslate}, `or`{.docutils .literal .notranslate}, and
`not`{.docutils .literal .notranslate}. All three operators take boolean
operands and produce boolean values. The semantics (meaning) of these
operators is similar to their meaning in English:

-   `x and y`{.docutils .literal .notranslate} is `True`{.docutils
    .literal .notranslate} if both `x`{.docutils .literal .notranslate}
    and `y`{.docutils .literal .notranslate} are `True`{.docutils
    .literal .notranslate}. Otherwise, `and`{.docutils .literal
    .notranslate} produces `False`{.docutils .literal .notranslate}.

-   `x or y`{.docutils .literal .notranslate} yields `True`{.docutils
    .literal .notranslate} if either `x`{.docutils .literal
    .notranslate} or `y`{.docutils .literal .notranslate} is
    `True`{.docutils .literal .notranslate}. Only if both operands are
    `False`{.docutils .literal .notranslate} does `or`{.docutils
    .literal .notranslate} yield `False`{.docutils .literal
    .notranslate}.

-   `not x`{.docutils .literal .notranslate} yields `False`{.docutils
    .literal .notranslate} if `x`{.docutils .literal .notranslate} is
    `True`{.docutils .literal .notranslate}, and vice versa.

Look at the following example. See if you can predict the output. Then,
Run to see if your predictions were correct:

::: {.runestone .explainer .ac_section}
::: {#logop_ex1 component="activecode" question_label="8.3.1"}
::: {#logop_ex1_question .ac_question}
:::
:::
:::

Although you can use boolean operators with simple boolean literals or
variables as in the above example, they are often combined with the
comparison operators, as in this example. Again, before you run this,
see if you can predict the outcome:

::: {.runestone .explainer .ac_section}
::: {#ac7_3_1 component="activecode" question_label="8.3.2"}
::: {#ac7_3_1_question .ac_question}
:::
:::
:::

The expression `x > 0 and x < 10`{.docutils .literal .notranslate} is
`True`{.docutils .literal .notranslate} only if `x`{.docutils .literal
.notranslate} is greater than 0 *and* at the same time, x is less than
10. In other words, this expression is `True`{.docutils .literal
.notranslate} if x is between 0 and 10, not including the endpoints.

::: {.admonition-common-mistake .admonition}
Common Mistake!

There is a very common mistake that occurs when programmers try to write
boolean expressions. For example, what if we have a variable
`number`{.docutils .literal .notranslate} and we want to check to see if
its value is 5 or 6. In words we might say: "number equal to 5 or 6".
However, if we translate this into Python, `number == 5 or 6`{.docutils
.literal .notranslate}, it will not yield correct results. The
`or`{.docutils .literal .notranslate} operator must have a complete
equality check on both sides. The correct way to write this is
`number == 5 or number == 6`{.docutils .literal .notranslate}. Remember
that both operands of `or`{.docutils .literal .notranslate} must be
booleans in order to yield proper results.
:::

::: {#smart-evaluation .section}
[]{#index-0}

[8.3.1. ]{.section-number}Smart Evaluation[¶](#smart-evaluation "Permalink to this heading"){.headerlink}
---------------------------------------------------------------------------------------------------------

Python is "smart" about the way it evaluates expressions using boolean
operators. Consider the following example:

::: {.highlight-default .notranslate}
::: {.highlight}
    answer = input('Continue?')
    if answer == 'Y' or answer == 'y':
       print('Continuing!')
:::
:::

There are two operands for the `or`{.docutils .literal .notranslate}
operator here: `answer == 'Y'`{.docutils .literal .notranslate} and
`'answer == 'y'`{.docutils .literal .notranslate}. Python evaluates from
left to right, and if the first operand for `or`{.docutils .literal
.notranslate} evaluates to `True`{.docutils .literal .notranslate},
Python doesn't bother evaluating the second operand, because it knows
the result must be `True`{.docutils .literal .notranslate} (recall that
if either operand for `or`{.docutils .literal .notranslate} is
`True`{.docutils .literal .notranslate}, the result is `True`{.docutils
.literal .notranslate}). So, if the user enters `Y`{.docutils .literal
.notranslate}, Python first evaluates `answer == 'Y'`{.docutils .literal
.notranslate}, determines that it is `True`{.docutils .literal
.notranslate}, and doesn't bother to check to see if
`answer == 'y'`{.docutils .literal .notranslate} is `True`{.docutils
.literal .notranslate}; it just concludes that the entire condition is
`True`{.docutils .literal .notranslate} and executes the print
statement.

In a similar fashion, with the `and`{.docutils .literal .notranslate}
operator, if the first operand evaluates to `False`{.docutils .literal
.notranslate}, Python doesn't check the second operand's value, because
it can conclude that the result must be `False`{.docutils .literal
.notranslate}.

This behavior, in which Python in some cases skips the evaluation of the
second operand to `and`{.docutils .literal .notranslate} and
`or`{.docutils .literal .notranslate}, is called **short-circuit boolean
evaluation**. You don't have to do anything to make Python do this; it's
the way Python works. It saves a little processing time. And, as a
special bonus, you can take advantage of Python's short-circuiting
behavior to shorten your code. Consider the following example:

::: {.runestone .explainer .ac_section}
::: {#ac_logop_dangerous component="activecode" question_label="8.3.1.1"}
::: {#ac_logop_dangerous_question .ac_question}
:::
:::
:::

This code checks to see if the average weight of a given number of
pieces of luggage is greater than 50 pounds. However, there is a
potential crash situation here. If the user enters `0`{.docutils
.literal .notranslate} for `num_pieces`{.docutils .literal
.notranslate}, the program will crash with a divide by zero error. Try
it out to see it happen.

To prevent the crash, you might add an extra if statement to check for
zero:

::: {.highlight-default .notranslate}
::: {.highlight}
    if num_pieces != 0:
       if total_weight / num_pieces > 50:
          print('Average weight is greater than 50 pounds -> $100 surcharge.')
:::
:::

Now, the division will not occur if `num_pieces`{.docutils .literal
.notranslate} is zero, and a potential runtime crash has been averted.
Good job!

We can shorten this example to a single `if`{.docutils .literal
.notranslate} statement if we do it carefully. Anytime you have two
nested `if`{.docutils .literal .notranslate} statements as in the
example above, you can combine them into a single `if`{.docutils
.literal .notranslate} statement by joining the conditions using the
`and`{.docutils .literal .notranslate} operator. Consider the version
below, and think about why this `if`{.docutils .literal .notranslate}
statement is equivalent in its behavior to the previous version with two
nested `if`{.docutils .literal .notranslate} statements:

::: {.runestone .explainer .ac_section}
::: {#ac_logop_smarteval component="activecode" question_label="8.3.1.2"}
::: {#ac_logop_smarteval_question .ac_question}
:::
:::
:::

But wait a minute: is this code safe? Try running the program and
entering the value `500`{.docutils .literal .notranslate} for
`total_weight`{.docutils .literal .notranslate} and the value
`5`{.docutils .literal .notranslate} for num\_pieces. Then, try it again
using the value `0`{.docutils .literal .notranslate} for num\_pieces.
There should be no crash.

Next, try altering the code and reversing the order of the
`if`{.docutils .literal .notranslate} conditions:

::: {.highlight-default .notranslate}
::: {.highlight}
    if total_weight / num_pieces > 50 and num_pieces != 0:
       print('Average weight is greater than 50 pounds -> $100 surcharge.')
:::
:::

Run the program again, performing the same two tests. This time, you
should observe a crash when you enter `0`{.docutils .literal
.notranslate} for num\_pieces. Can you analyze why the first version did
not crash, but the second one does?

In the second version, when evaluating left-to-right, the division by
zero occurs before Python evaluates the comparison
`num_pieces != 0`{.docutils .literal .notranslate}. When joining two
`if`{.docutils .literal .notranslate} statements into a single
`if`{.docutils .literal .notranslate} statement, you must be sure to put
the condition from the first `if`{.docutils .literal .notranslate}
statement on the left-hand side of the `and`{.docutils .literal
.notranslate} operator, and the other condition on the right-hand side,
in order to get the same effect.

To summarize this discussion on smart evaluation, keep in mind that when
you are performing potentially dangerous operations in an `if`{.docutils
.literal .notranslate} statement or `while`{.docutils .literal
.notranslate} loop using boolean logic with `and`{.docutils .literal
.notranslate} or `or`{.docutils .literal .notranslate}, order matters!

**Check your understanding**

::: {.runestone}
-   [x \> 0 and \< 5]{#question7_3_1_opt_a}
-   Each comparison must be between exactly two values. In this case the
    right-hand expression \< 5 lacks a value on its left.
-   [0 \< x \< 5]{#question7_3_1_opt_b}
-   Although most other programming languages do not allow this syntax,
    in Python, this syntax is allowed. Even though it is possible to use
    this format, you should not use it all the time. Instead, make
    multiple comparisons by using and or or.
-   [x \> 0 or x \< 5]{#question7_3_1_opt_c}
-   Although this is legal Python syntax, the expression is incorrect.
    It will evaluate to true for all numbers that are either greater
    than 0 or less than 5. Because all numbers are either greater than 0
    or less than 5, this expression will always be True.
-   [x \> 0 and x \< 5]{#question7_3_1_opt_d}
-   Yes, with an \`\`and\`\` keyword both expressions must be true so
    the number must be greater than 0 an less than 5 for this expression
    to be true.
:::

::: {.runestone}
-   [Option A]{#question7_3_2_opt_a}
-   Correct! The comparison yesno\[0\] == \'Y\' will crash if yesno is
    an empty string.
-   [Option B]{#question7_3_2_opt_b}
-   Incorrect. If len(yesno) \> 0 is False, the potentially unsafe
    comparison yesno\[0\] == \'Y\' will not be evaluated.
:::

::: {.runestone}
-   [Option A]{#question7_3_3_opt_a}
-   Incorrect. The comparison yesno\[0\] == \'Y\' will crash if yesno is
    an empty string.
-   [Option B]{#question7_3_3_opt_b}
-   Correct! Use the and operator to join nested if statements into a
    single statement, with the first if condition on the left-hand side.
-   [Option C]{#question7_3_3_opt_c}
-   Incorrect. The comparison yesno\[0\] == \'Y\' will crash if yesno is
    an empty string.
-   [Option D]{#question7_3_3_opt_d}
-   Incorrect. The comparison yesno\[0\] == \'Y\' will crash if yesno is
    an empty string.
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

-   [[](BooleanValuesandBooleanExpressions.html)]{#relations-prev}
-   [[](Theinandnotinoperators.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
