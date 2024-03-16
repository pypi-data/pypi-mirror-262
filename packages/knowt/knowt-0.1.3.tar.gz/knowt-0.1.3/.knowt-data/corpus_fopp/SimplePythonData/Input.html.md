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
        Problem](/runestone/default/reportabug?course=fopp&page=Input)
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

::: {#input .section}
[]{#index-0}

[2.15. ]{.section-number}Input[¶](#input "Permalink to this heading"){.headerlink}
==================================================================================

Our programs get more interesting if they don't do exactly the same
thing every time they run. One way to make them more interesting is to
get **input** from the user. Luckily, in Python there is a built-in
function to accomplish this task. It is called `input`{.docutils
.literal .notranslate}.

::: {.highlight-python .notranslate}
::: {.highlight}
    n = input("Please enter your name: ")
:::
:::

The input function allows the programmer to provide a **prompt string**.
In the example above, it is "Please enter your name: ". When the
function is evaluated, the prompt is shown (in the browser, look for a
popup window). The user of the program can type some text and press
`return`{.docutils .literal .notranslate}. When this happens the text
that has been entered is returned from the `input`{.docutils .literal
.notranslate} function, and in this case assigned to the variable
`n`{.docutils .literal .notranslate}. Run this example a few times and
try some different names in the input box that appears.

::: {.runestone .explainer .ac_section}
::: {#ac2_16_1 component="activecode" question_label="2.15.1"}
::: {#ac2_16_1_question .ac_question}
:::
:::
:::

It is very important to note that the `input`{.docutils .literal
.notranslate} function returns a string value. Even if you asked the
user to enter their age, you would get back a string like
`"17"`{.docutils .literal .notranslate}. It would be your job, as the
programmer, to convert that string into an int or a float, using the
`int`{.docutils .literal .notranslate} or `float`{.docutils .literal
.notranslate} converter functions we saw earlier.

::: {.admonition .note}
Note

We often use the word "input" (or, synonymously, argument) to refer to
the values that are passed to any function. Do not confuse that with the
`input`{.docutils .literal .notranslate} function, which asks the user
of a program to type in a value. Like any function, `input`{.docutils
.literal .notranslate} itself takes an input argument and produces an
output. The input is a character string that is displayed as a prompt to
the user. The output is whatever character string the user types.

This is analogous to the potential confusion of function "outputs" with
the contents of the output window. Every function produces an output,
which is a Python value. Only the print function puts things in the
output window. Most functions take inputs, which are Python values. Only
the input function invites users to type something.
:::

Here is a program that turns a number of seconds into more human
readable counts of hours, minutes, and seconds. A call to
`input()`{.docutils .literal .notranslate} allows the user to enter the
number of seconds. Then we convert that string to an integer. From there
we use the division and modulus operators to compute the results.

::: {.runestone .explainer .ac_section}
::: {#ac2_16_2 component="activecode" question_label="2.15.2"}
::: {#ac2_16_2_question .ac_question}
:::
:::
:::

The variable `str_seconds`{.docutils .literal .notranslate} will refer
to the string that is entered by the user. As we said above, even though
this string may be `7684`{.docutils .literal .notranslate}, it is still
a string and not a number. To convert it to an integer, we use the
`int`{.docutils .literal .notranslate} function. The result is referred
to by `total_secs`{.docutils .literal .notranslate}. Now, each time you
run the program, you can enter a new value for the number of seconds to
be converted.

**Check your understanding**

::: {.runestone}
-   [\<class \'str\'\>]{#question2_16_1_opt_a}
-   All input from users is read in as a string.
-   [\<class \'int\'\>]{#question2_16_1_opt_b}
-   Even though the user typed in an integer, it does not come into the
    program as an integer.
-   [\<class 18\>]{#question2_16_1_opt_c}
-   18 is the value of what the user typed, not the type of the data.
-   [18]{#question2_16_1_opt_d}
-   18 is the value of what the user typed, not the type of the data.
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

-   [[](HardCoding.html)]{#relations-prev}
-   [[](Glossary.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
