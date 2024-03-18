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
        Problem](/runestone/default/reportabug?course=fopp&page=Operators)
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

[]{#input .target}

::: {#operators-and-operands .section}
[]{#index-0}

[2.3. ]{.section-number}Operators and Operands[¶](#operators-and-operands "Permalink to this heading"){.headerlink}
===================================================================================================================

You can build complex expressions out of simpler ones using
**operators**. Operators are special tokens that represent computations
like addition, multiplication and division. The values the operator
works on are called **operands**.

The following are all legal Python expressions whose meaning is more or
less clear:

::: {.highlight-default .notranslate}
::: {.highlight}
    20 + 32
    5 ** 2
    (5 + 9) * (15 - 7)
:::
:::

The tokens `+`{.docutils .literal .notranslate}, `-`{.docutils .literal
.notranslate}, and `*`{.docutils .literal .notranslate}, and the use of
parentheses for grouping, mean in Python what they mean in mathematics.
The asterisk (`*`{.docutils .literal .notranslate}) is the token for
multiplication, and `**`{.docutils .literal .notranslate} is the token
for exponentiation. Addition, subtraction, multiplication, and
exponentiation all do what you expect.

Remember that if we want to see the results of the computation, the
program needs to specify that with the word `print`{.docutils .literal
.notranslate}. The first three computations occur, but their results are
not printed out.

::: {.runestone .explainer .ac_section}
::: {#ac2_3_1 component="activecode" question_label="2.3.1"}
::: {#ac2_3_1_question .ac_question}
:::
:::
:::

In Python 3, which we will be using, the division operator `/`{.docutils
.literal .notranslate} produces a floating point result (even if the
result is an integer; `4/2`{.docutils .literal .notranslate} is
`2.0`{.docutils .literal .notranslate}). If you want truncated division,
which ignores the remainder, you can use the `//`{.docutils .literal
.notranslate} operator (for example, `5//2`{.docutils .literal
.notranslate} is `2`{.docutils .literal .notranslate}).

::: {.runestone .explainer .ac_section}
::: {#ac2_3_2 component="activecode" question_label="2.3.2"}
::: {#ac2_3_2_question .ac_question}
:::
:::
:::

Pay particular attention to the examples above. Note that
`9//5`{.docutils .literal .notranslate} truncates rather than rounding,
so it produces the value 1 rather 2.

The truncated division operator, `//`{.docutils .literal .notranslate},
also works on floating point numbers. It truncates to the nearest
integer, but still produces a floating point result. Thus
`7.0 // 3.0`{.docutils .literal .notranslate} is `2.0`{.docutils
.literal .notranslate}.

::: {.runestone .explainer .ac_section}
::: {#ac2_3_3 component="activecode" question_label="2.3.3"}
::: {#ac2_3_3_question .ac_question}
:::
:::
:::

The **modulus operator**, sometimes also called the **remainder
operator** or **integer remainder operator** works on integers (and
integer expressions) and yields the remainder when the first operand is
divided by the second. In Python, the modulus operator is a percent sign
(`%`{.docutils .literal .notranslate}). The syntax is the same as for
other operators.

::: {.runestone .explainer .ac_section}
::: {#ac2_3_4 component="activecode" question_label="2.3.4"}
::: {#ac2_3_4_question .ac_question}
:::
:::
:::

In the above example, 7 divided by 3 is 2 when we use integer division
and there is a remainder of 1.

The modulus operator turns out to be surprisingly useful. For example,
you can check whether one number is divisible by another---if
`x % y`{.docutils .literal .notranslate} is zero, then `x`{.docutils
.literal .notranslate} is divisible by `y`{.docutils .literal
.notranslate}. Also, you can extract the right-most digit or digits from
a number. For example, `x % 10`{.docutils .literal .notranslate} yields
the right-most digit of `x`{.docutils .literal .notranslate} (in base
10). Similarly `x % 100`{.docutils .literal .notranslate} yields the
last two digits.

**Check your understanding**

::: {.runestone}
-   [4.5]{#question2_3_1_opt_a}
-   Because the result is not an integer, a floating point answer is
    produced.
-   [5]{#question2_3_1_opt_b}
-   Even if // were used, it would still truncate, not round
-   [4]{#question2_3_1_opt_c}
-   Perhaps you are thinking of the integer division operator, //
-   [4.0]{#question2_3_1_opt_d}
-   / performs exact division, without truncation
-   [2]{#question2_3_1_opt_e}
-   / does division. Perhaps you were thinking of %, which computes the
    remainder?
:::

::: {.runestone}
-   [4.5]{#question2_3_2_opt_a}
-   \- // does truncated division.
-   [5]{#question2_3_2_opt_b}
-   \- Neither / nor // leads to rounding up
-   [4]{#question2_3_2_opt_c}
-   \- Even though it truncates, it produces a floating point result
-   [4.0]{#question2_3_2_opt_d}
-   \- Yes, even though it truncates, it produces a floating point
    result because 18.0 is a float
-   [2]{#question2_3_2_opt_e}
-   \- / does division. Perhaps you were thinking of %, which computes
    the remainder?
:::

::: {.runestone}
-   [4.25]{#question2_3_3_opt_a}
-   The % operator returns the remainder after division.
-   [5]{#question2_3_3_opt_b}
-   The % operator returns the remainder after division.
-   [4]{#question2_3_3_opt_c}
-   The % operator returns the remainder after division.
-   [2]{#question2_3_3_opt_d}
-   The % operator returns the remainder after division.
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

-   [[](Values.html)]{#relations-prev}
-   [[](FunctionCalls.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
