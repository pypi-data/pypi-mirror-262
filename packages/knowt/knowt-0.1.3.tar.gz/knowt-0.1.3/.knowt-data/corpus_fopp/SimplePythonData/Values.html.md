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
        Problem](/runestone/default/reportabug?course=fopp&page=Values)
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

::: {#values-and-data-types .section}
[2.2. ]{.section-number}Values and Data Types[¶](#values-and-data-types "Permalink to this heading"){.headerlink}
=================================================================================================================

A **value** is one of the fundamental things --- like a word or a number
--- that a program manipulates. Some values are `5`{.docutils .literal
.notranslate} (the result when we add `2 + 3`{.docutils .literal
.notranslate}), and `"Hello, World!"`{.docutils .literal .notranslate}.
These objects are classified into different classes, or data types: 4 is
an integer, and "Hello, World!" is a string, so-called because it
contains a string or sequence of letters. You (and the interpreter) can
identify strings because they are enclosed in quotation marks.

We can specify values directly in the programs we write. For example we
can specify a number as a **literal** just by (literally) typing it
directly into the program (e.g., `5`{.docutils .literal .notranslate} or
`4.32`{.docutils .literal .notranslate}). In a program, we specify a
word, or more generally a string of characters, by enclosing the
characters inside quotation marks (e.g., `"Hello, World!"`{.docutils
.literal .notranslate}).

During execution of a program, the Python interpreter creates an
internal representation of literals that are specified in a program. It
can then manipulate them, for example by multiplying two numbers. We
call the internal representations **objects** or just **values**.

You can't directly see the internal representations of values. You can,
however, use the `print`{.docutils .literal .notranslate} function to
see a printed representation in the output window.

The printed representation of a number uses the familiar decimal
representation (reading [Roman
Numerals](http://en.wikipedia.org/wiki/Roman_numerals){.reference
.external} is a fun challenge in museums, but thank goodness the Python
interpreter doesn't present the number 2014 as MMXIV in the output
window). Thus, the printed representation of a number shown in the
output window is the same as the literal that you specify in a program.

The printed representation of a character string, however, is not
exactly the same as the literal used to specify the string in a program.
For the literal in a program, you enclose the string in quotation marks.
The printed representation, in the output window, omits the quotation
marks.

::: {.runestone .explainer .ac_section}
::: {#ac2_2_1 component="activecode" question_label="2.2.1"}
::: {#ac2_2_1_question .ac_question}
:::
:::
:::

::: {.admonition .note}
Note

**Literals** appear in programs. The Python interpreter turns literals
into **values**, which have internal representations that people never
get to see directly. **Outputs** are external representations of values
that appear in the output window. When we are being careful, we will use
the terms this way. Sometimes, however, we will get a little sloppy and
refer to literals or external representations as values.
:::

Numbers with a decimal point belong to a class called **float**, because
these numbers are represented in a format called *floating-point*. At
this stage, you can treat the words *class* and *type* interchangeably.
We'll come back to a deeper understanding of what a class is in later
chapters.

You will soon encounter other types of objects as well, such as lists
and dictionaries. Each of these has its own special representation for
specifying an object as a literal in a program, and for displaying an
object when you print it. For example, list contents are enclosed in
square brackets `[ ]`{.docutils .literal .notranslate}. You will also
encounter some more complicated objects that do not have very nice
printed representations: printing those won't be very useful.

**Check your understanding**

::: {.runestone}
-   [Nothing is printed. It generates a runtime
    error.]{#question2_2_1_opt_a}
-   \"Hello World!\" has a printed representation, so there will not be
    an error.
-   [\"Hello World!\"]{#question2_2_1_opt_b}
-   The literal in the program includes the quote marks, but the printed
    representation omits them.
-   [Hello World!]{#question2_2_1_opt_c}
-   The printed representation omits the quote marks that are included
    in the string literal.
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

-   [[](intro-VariablesExpressionsandStatements.html)]{#relations-prev}
-   [[](Operators.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
