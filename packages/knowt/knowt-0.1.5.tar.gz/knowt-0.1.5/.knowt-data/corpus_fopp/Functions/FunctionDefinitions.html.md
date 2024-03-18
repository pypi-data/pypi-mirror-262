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
        Problem](/runestone/default/reportabug?course=fopp&page=FunctionDefinitions)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [12.1 Introduction to
        Functions](intro-Functions.html){.reference .internal}
    -   [12.2 Function Definition](FunctionDefinitions.html){.reference
        .internal}
    -   [12.3 Function Invocation](FunctionInvocation.html){.reference
        .internal}
    -   [12.4 Function Parameters](FunctionParameters.html){.reference
        .internal}
    -   [12.5 Returning a value from a
        function](Returningavaluefromafunction.html){.reference
        .internal}
    -   [12.6 👩‍💻 Decoding a
        Function](DecodingaFunction.html){.reference .internal}
    -   [12.7 Type Annotations](TypeAnnotations.html){.reference
        .internal}
    -   [12.8 A function that
        accumulates](Afunctionthataccumulates.html){.reference
        .internal}
    -   [12.9 Variables and parameters are
        local](Variablesandparametersarelocal.html){.reference
        .internal}
    -   [12.10 Global Variables](GlobalVariables.html){.reference
        .internal}
    -   [12.11 Functions can call other functions
        (Composition)](Functionscancallotherfunctions.html){.reference
        .internal}
    -   [12.12 Flow of Execution
        Summary](FlowofExecutionSummary.html){.reference .internal}
    -   [12.13 👩‍💻 Print vs. return](Printvsreturn.html){.reference
        .internal}
    -   [12.14 Passing Mutable
        Objects](PassingMutableObjects.html){.reference .internal}
    -   [12.15 Side Effects](SideEffects.html){.reference .internal}
    -   [12.16 Glossary](Glossary.html){.reference .internal}
    -   [12.17 Exercises](Exercises.html){.reference .internal}
    -   [12.18 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#function-definition .section}
[12.2. ]{.section-number}Function Definition[¶](#function-definition "Permalink to this heading"){.headerlink}
==============================================================================================================

The syntax for creating a named function, a **function definition**, is:

::: {.highlight-python .notranslate}
::: {.highlight}
    def name( parameters ):
        statements
:::
:::

You can make up any names you want for the functions you create, except
that you can't use a name that is a Python keyword, and the names must
follow the rules for legal identifiers that were given previously. The
parameters specify what information, if any, you have to provide in
order to use the new function. Another way to say this is that the
parameters specify what the function needs to do its work.

There can be any number of statements inside the function, but they have
to be indented from the `def`{.docutils .literal .notranslate}. In the
examples in this book, we will use the standard indentation of four
spaces. Function definitions are the third of several **compound
statements** we will see, all of which have the same pattern:

1.  A header line which begins with a keyword and ends with a colon.

2.  A **body** consisting of one or more Python statements, each
    indented the same amount -- *4 spaces is the Python standard* --
    from the header line.

We've already seen the `for`{.docutils .literal .notranslate} statement
which has the same structure, with an indented block of code, and the
`if`{.docutils .literal .notranslate}, `elif`{.docutils .literal
.notranslate}, and `else`{.docutils .literal .notranslate} statements
that do so as well.

In a function definition, the keyword in the header is `def`{.docutils
.literal .notranslate}, which is followed by the name of the function
and some *parameter names* enclosed in parentheses. The parameter list
may be empty, or it may contain any number of parameters separated from
one another by commas. In either case, the parentheses are required.

We will come back to the parameters in a little while, but first let's
see what happens when a function is executed, using a function without
any parameters to illustrate.

Here's the definition of a simple function, hello.

::: {.runestone .explainer .ac_section}
::: {#ac11_1_1 component="activecode" question_label="12.2.1"}
::: {#ac11_1_1_question .ac_question}
:::
:::
:::

::: {.admonition-docstrings .admonition}
docstrings

If the first thing after the function header is a string (some tools
insist that it must be a triple-quoted string), it is called a
**docstring** and gets special treatment in Python and in some of the
programming tools.

Another way to retrieve this information is to use the interactive
interpreter, and enter the expression
`<function_name>.__doc__`{.docutils .literal .notranslate}, which will
retrieve the docstring for the function. So the string you write as
documentation at the start of a function is retrievable by python tools
*at runtime*. This is different from comments in your code, which are
completely eliminated when the program is parsed.

By convention, Python programmers use docstrings for the key
documentation of their functions.
:::

We can apply functions to the turtle drawings we've done in the past as
well.

::: {.runestone .explainer .ac_section}
::: {#ac11_1_2 component="activecode" question_label="12.2.2"}
::: {#ac11_1_2_question .ac_question}
:::
:::
:::

This function is named `drawSquare`{.docutils .literal .notranslate}. It
has two parameters --- one to tell the function which turtle to move
around and the other to tell it the size of the square we want drawn. In
the function definition they are called `t`{.docutils .literal
.notranslate} and `sz`{.docutils .literal .notranslate} respectively.
Make sure you know where the body of the function ends --- it depends on
the indentation and the blank lines don't count for this purpose!
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

-   [[](intro-Functions.html)]{#relations-prev}
-   [[](FunctionInvocation.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
