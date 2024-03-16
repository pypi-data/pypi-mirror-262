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
        Problem](/runestone/default/reportabug?course=fopp&page=OrderofOperations)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [2.1
        Introduction](intro-VariablesExpressionsandStatements.html){.reference
        .internal}
    -   [2.2 Values and Data Types](Values.html){.reference .internal}
    -   [2.3 Operators and Operands](Operators.html){.reference
        .internal}
    -   [2.4 Function Calls](FunctionCalls.html){.reference .internal}
    -   [2.5 Data Types](DataTypes.html){.reference .internal}
    -   [2.6 Type conversion
        functions](ConvertTypeFunctions.html){.reference .internal}
    -   [2.7 Variables](Variables.html){.reference .internal}
    -   [2.8 Variable Names and
        Keywords](VariableNamesandKeywords.html){.reference .internal}
    -   [2.9 👩‍💻 Choosing the Right Variable
        Name](WPChoosingtheRightVariableName.html){.reference .internal}
    -   [2.10 Statements and
        Expressions](StatementsandExpressions.html){.reference
        .internal}
    -   [2.11 Order of Operations](OrderofOperations.html){.reference
        .internal}
    -   [2.12 Reassignment](Reassignment.html){.reference .internal}
    -   [2.13 Updating Variables](UpdatingVariables.html){.reference
        .internal}
    -   [2.14 👩‍💻 Hard-Coding](HardCoding.html){.reference .internal}
    -   [2.15 Input](Input.html){.reference .internal}
    -   [2.16 Glossary](Glossary.html){.reference .internal}
    -   [2.17 Exercises](Exercises.html){.reference .internal}
    -   [2.18 Chapter Assessment](week1a2.html){.reference .internal}
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

::: {#order-of-operations .section}
[2.11. ]{.section-number}Order of Operations[¶](#order-of-operations "Permalink to this heading"){.headerlink}
==============================================================================================================

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#precedencevid .align-center .youtube-video component="youtube" video-height="315" question_label="2.11.1" video-width="560" video-videoid="Ezve3QJv6Aw" video-divid="precedencevid" video-start="0" video-end="-1"}
:::
:::

When more than one operator appears in an expression, the order of
evaluation depends on the **rules of precedence**. Python follows the
same precedence rules for its mathematical operators that mathematics
does.

1.  *Parentheses* have the highest precedence and can be used to force
    an expression to evaluate in the order you want. Since expressions
    in parentheses are evaluated first, `2 * (3-1)`{.docutils .literal
    .notranslate} is 4, and `(1+1)**(5-2)`{.docutils .literal
    .notranslate} is 8. You can also use parentheses to make an
    expression easier to read, as in `(minute * 100) / 60`{.docutils
    .literal .notranslate}: in this case, the parentheses don't change
    the result, but they reinforce that the expression in parentheses
    will be evaluated first.

2.  *Exponentiation* has the next highest precedence, so
    `2**1+1`{.docutils .literal .notranslate} is 3 and not 4, and
    `3*1**3`{.docutils .literal .notranslate} is 3 and not 27. Can you
    explain why?

3.  *Multiplication and both division* operators have the same
    precedence, which is higher than addition and subtraction, which
    also have the same precedence. So `2*3-1`{.docutils .literal
    .notranslate} yields 5 rather than 4, and `5-2*2`{.docutils .literal
    .notranslate} is 1, not 6.

4.  Operators with the *same* precedence are evaluated from
    left-to-right. In algebra we say they are *left-associative*. So in
    the expression `6-3+2`{.docutils .literal .notranslate}, the
    subtraction happens first, yielding 3. We then add 2 to get the
    result 5. If the operations had been evaluated from right to left,
    the result would have been `6-(3+2)`{.docutils .literal
    .notranslate}, which is 1.

::: {.admonition .note}
Note

Due to some historical quirk, an exception to the left-to-right
left-associative rule is the exponentiation operator `**`{.docutils
.literal .notranslate}. A useful hint is to always use parentheses to
force exactly the order you want when exponentiation is involved:
:::

::: {.runestone .explainer .ac_section}
::: {#ac2_11_1 component="activecode" question_label="2.11.2"}
::: {#ac2_11_1_question .ac_question}
:::
:::
:::

::: {.admonition .note}
Note

This is a second way that parentheses are used in Python. The first way
you've already seen is that () indicates a function call, with the
inputs going inside the parentheses. How can Python tell when
parentheses specify to call a function, and when they are just forcing
the order of operations for ambiguous operator expressions?

The answer is that if there's a an expression to the left of the
parentheses that evaluates to a function object, then the parentheses
indicate a function call, and otherwise not. You will have to get used
to making the same inference when you see parentheses: is this a
function call, or just specifying precedence?
:::

**Check your understanding**

::: {.runestone}
-   [14]{#question2_11_1_opt_a}
-   Using parentheses, the expression is evaluated as (2\*5) first, then
    (10 // 3), then (16-3), and then (13+1).
-   [24]{#question2_11_1_opt_b}
-   Remember that \* has precedence over -.
-   [3]{#question2_11_1_opt_c}
-   Remember that // has precedence over -.
-   [13.667]{#question2_11_1_opt_d}
-   Remember that // does integer division.
:::

Here is an animation for the above expression:

::: {#se_ac2_11_1 .runestone .explainer component="showeval" question_label="2.11.4" tracemode="true"}
Next Step

Reset

::: {.evalCont style="background-color: #FDFDFD;"}
16 - 2 \* 5 // 3 + 1\
:::

::: {.evalCont}
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

-   [[](StatementsandExpressions.html)]{#relations-prev}
-   [[](Reassignment.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
