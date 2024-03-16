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
        Problem](/runestone/default/reportabug?course=fopp&page=DecodingaFunction)
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

::: {#decoding-a-function .section}
[12.6. ]{.section-number}👩‍💻 Decoding a Function[¶](#decoding-a-function "Permalink to this heading"){.headerlink}
==================================================================================================================

In general, when you see a function definition you will try figure out
what the function does, but, unless you are writing the function, you
won't care *how it does it*.

For example, here is a summary of some functions we have seen already.

-   `input`{.docutils .literal .notranslate} takes one parameter, a
    string. It is displayed to the user. Whatever the user types is
    returned, as a string.

-   `int`{.docutils .literal .notranslate} takes one parameter. It can
    be of any type that can be converted into an integer, such as a
    floating point number or a string whose characters are all digits.

Sometimes, you will be presented with a function definition whose
operation is not so neatly summarized as above. Sometimes you will need
to look at the code, either the function definition or code that invokes
the function, in order to figure out what it does.

To build your understanding of any function, you should aim to answer
the following questions:

1.  How many parameters does it have?

2.  What is the type of values that will be passed when the function is
    invoked?

3.  What is the type of the return value that the function produces when
    it executes?

If you try to make use of functions, ones you write or that others
write, without being able to answer these questions, you will find that
your debugging sessions are long and painful.

The first question is always easy to answer. Look at the line with the
function definition, look inside the parentheses, and count how many
variable names there are.

The second and third questions are not always so easy to answer. In
Python, unlike some other programming languages, variables are not
declared to have fixed types, and the same holds true for the variable
names that appear as formal parameters of functions. You have to figure
it out from context.

To figure out the types of values that a function expects to receive as
parameters, you can look at the function invocations or you can look at
the operations that are performed on the parameters inside the function.

Here are some clues that can help you determine the type of object
associated with any variable, including a function parameter. If you
see...

-   `len(x)`{.docutils .literal .notranslate}, then x must be a string
    or a list. (Actually, it can also be a dictionary, in which case it
    is equivalent to the expression `len(x.keys())`{.docutils .literal
    .notranslate}. Later in the course, we will also see some other
    sequence types that it could be). x can't be a number or a Boolean.

-   `x - y`{.docutils .literal .notranslate}, x and y must be numbers
    (integer or float)

-   `x + y`{.docutils .literal .notranslate}, x and y must both be
    numbers, both be strings, or both be lists

-   `x[3]`{.docutils .literal .notranslate}, x must be a string or a
    list containing at least four items, or x must be a dictionary that
    includes 3 as a key.

-   `x['3']`{.docutils .literal .notranslate}, x must be a dictionary,
    with '3' as a key.

-   `x[y:z]`{.docutils .literal .notranslate}, x must be a sequence
    (string or list), and y and z must be integers

-   `x and y`{.docutils .literal .notranslate}, x and y must be Boolean

-   `for x in y`{.docutils .literal .notranslate}, y must be a sequence
    (string or list) or a dictionary (in which case it's really the
    dictionary's keys); x must be a character if y is a string; if y is
    a list, x could be of any type.

**Check your understanding: decode this function definition**

::: {.runestone}
-   [0]{#question200_1_1_opt_a}
-   Count the number of variable names inside the parenetheses on
    line 1.
-   [1]{#question200_1_1_opt_b}
-   Count the number of variable names inside the parenetheses on
    line 1.
-   [2]{#question200_1_1_opt_c}
-   Count the number of variable names inside the parenetheses on
    line 1.
-   [3]{#question200_1_1_opt_d}
-   x, y, and z.
-   [Can\'t tell]{#question200_1_1_opt_e}
-   You can tell by looking inside the parentheses on line 1. Each
    variable name is separated by a comma.
:::

::: {.runestone}
-   [integer]{#question200_1_2_opt_a}
-   x - y, y-2, and x+3 can all be performed on integers.
-   [float]{#question200_1_2_opt_b}
-   x - y, y-2, and x+3 can all be performed on floats.
-   [list]{#question200_1_2_opt_c}
-   x - y, y-2, and x+3 can\'t be performed on lists.
-   [string]{#question200_1_2_opt_d}
-   x - y and y-2 can\'t be performed on strings.
-   [Can\'t tell]{#question200_1_2_opt_e}
-   You can tell from some of the operations that are performed on them.
:::

::: {.runestone}
-   [integer]{#question200_1_3_opt_a}
-   append can\'t be performed on integers.
-   [float]{#question200_1_3_opt_b}
-   append can\'t be performed on floats.
-   [list]{#question200_1_3_opt_c}
-   append can be performed on lists.
-   [string]{#question200_1_3_opt_d}
-   append can\'t be performed on strings.
-   [Can\'t tell]{#question200_1_3_opt_e}
-   You can tell from some of the operations that are performed on it.
:::

::: {.runestone}
-   [integer]{#df_question200_1_3_opt_a}
-   y-2 or x+3 could produce an integer.
-   [float]{#df_question200_1_3_opt_b}
-   y-2 or x+3 could produce a float.
-   [list]{#df_question200_1_3_opt_c}
-   y-2 or x+3 can\'t produce a list.
-   [string]{#df_question200_1_3_opt_d}
-   neither y-2 or x+3 could produce a string.
-   [Can\'t tell]{#df_question200_1_3_opt_e}
-   You can tell from the expressions that follow the word return.
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

-   [[](Returningavaluefromafunction.html)]{#relations-prev}
-   [[](TypeAnnotations.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
