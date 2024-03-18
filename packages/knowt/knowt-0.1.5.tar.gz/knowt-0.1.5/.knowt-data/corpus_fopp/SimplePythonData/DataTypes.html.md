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
        Problem](/runestone/default/reportabug?course=fopp&page=DataTypes)
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
::: {#data-types .section}
[]{#index-0}

[2.5. ]{.section-number}Data Types[¶](#data-types "Permalink to this heading"){.headerlink}
===========================================================================================

If you are not sure what class (data type) a value falls into, Python
has a function called **type** which can tell you.

::: {.runestone .explainer .ac_section}
::: {#ac2_5_1 component="activecode" question_label="2.5.1"}
::: {#ac2_5_1_question .ac_question}
:::
:::
:::

What about values like `"17"`{.docutils .literal .notranslate} and
`"3.2"`{.docutils .literal .notranslate}? They look like numbers, but
they are in quotation marks like strings.

::: {.runestone .explainer .ac_section}
::: {#ac2_5_2 component="activecode" question_label="2.5.2"}
::: {#ac2_5_2_question .ac_question}
:::
:::
:::

They're strings!

Strings in Python can be enclosed in either single quotes (`'`{.docutils
.literal .notranslate}) or double quotes (`"`{.docutils .literal
.notranslate}), or three of each (`'''`{.docutils .literal .notranslate}
or `"""`{.docutils .literal .notranslate})

::: {.runestone .explainer .ac_section}
::: {#ac2_5_3 component="activecode" question_label="2.5.3"}
::: {#ac2_5_3_question .ac_question}
:::
:::
:::

Double quoted strings can contain single quotes inside them, as in
`"Bruce's beard"`{.docutils .literal .notranslate}, and single quoted
strings can have double quotes inside them, as in
`'The knights who say "Ni!"'`{.docutils .literal .notranslate}. Strings
enclosed with three occurrences of either quote symbol are called triple
quoted strings. They can contain either single or double quotes:

::: {.runestone .explainer .ac_section}
::: {#ac2_5_4 component="activecode" question_label="2.5.4"}
::: {#ac2_5_4_question .ac_question}
:::
:::
:::

Triple quoted strings can even span multiple lines:

::: {.runestone .explainer .ac_section}
::: {#ac2_5_5 component="activecode" question_label="2.5.5"}
::: {#ac2_5_5_question .ac_question}
:::
:::
:::

Python doesn't care whether you use single or double quotes or the
three-of-a-kind quotes to surround your strings. Once it has parsed the
text of your program or command, the way it stores the value is
identical in all cases, and the surrounding quotes are not part of the
value.

::: {.runestone .explainer .ac_section}
::: {#ac2_5_6 component="activecode" question_label="2.5.6"}
::: {#ac2_5_6_question .ac_question}
:::
:::
:::

So the Python language designers usually chose to surround their strings
by single quotes. What do you think would happen if the string already
contained single quotes?

When you type a large integer, you might be tempted to use commas
between groups of three digits, as in `42,000`{.docutils .literal
.notranslate}. This is not a legal integer in Python, but it does mean
something else, which is legal:

::: {.runestone .explainer .ac_section}
::: {#ac2_5_7 component="activecode" question_label="2.5.7"}
::: {#ac2_5_7_question .ac_question}
:::
:::
:::

Well, that's not what we expected at all! Because of the comma, Python
chose to treat this as a *pair* of values. In fact, a print statement
can print any number of values as long as you separate them by commas.
Notice that the values are separated by spaces when they are displayed.

::: {.runestone .explainer .ac_section}
::: {#ac2_5_8 component="activecode" question_label="2.5.8"}
::: {#ac2_5_8_question .ac_question}
:::
:::
:::

Remember not to put commas or spaces in your integers, no matter how big
they are. Also revisit what we said in the previous chapter: formal
languages are strict, the notation is concise, and even the smallest
change might mean something quite different from what you intended.

::: {.admonition .note}
Note

The examples in this online text describe how print works in Python 3.
If you install Python 2.7 on your machine, it will work slightly
differently. One difference is that print is not called as a function,
so there are no parentheses around the values to be printed.
:::

**Check your understanding**

::: {.runestone}
-   [Print out the value and determine the data type based on the value
    printed.]{#question2_5_1_opt_a}
-   You may be able to determine the data type based on the printed
    value, but it may also be deceptive, like when a string prints,
    there are no quotes around it.
-   [Use the type function.]{#question2_5_1_opt_b}
-   The type function will tell you the class the value belongs to.
-   [Use it in a known equation and print the
    result.]{#question2_5_1_opt_c}
-   Only numeric values can be used in equations.
-   [Look at the declaration of the variable.]{#question2_5_1_opt_d}
-   In Python variables are not declared. Values, not variables, have
    types in Python. A variable can even take on values with different
    types during a program\'s execution.
:::

::: {.runestone}
-   [Character]{#question2_5_2_opt_a}
-   It is not a single character.
-   [Integer]{#question2_5_2_opt_b}
-   The data is not numeric.
-   [Float]{#question2_5_2_opt_c}
-   The value is not numeric with a decimal point.
-   [String]{#question2_5_2_opt_d}
-   Strings can be enclosed in single quotes.
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

-   [[](FunctionCalls.html)]{#relations-prev}
-   [[](ConvertTypeFunctions.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
