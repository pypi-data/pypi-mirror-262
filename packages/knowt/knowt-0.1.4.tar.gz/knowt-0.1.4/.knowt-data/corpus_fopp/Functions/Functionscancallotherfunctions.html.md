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
        Problem](/runestone/default/reportabug?course=fopp&page=Functionscancallotherfunctions)
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

::: {#functions-can-call-other-functions-composition .section}
[]{#index-0}

[12.11. ]{.section-number}Functions can call other functions (Composition)[¶](#functions-can-call-other-functions-composition "Permalink to this heading"){.headerlink}
=======================================================================================================================================================================

It is important to understand that each of the functions we write can be
used and called from other functions we write. This is one of the most
important ways that computer programmers take a large problem and break
it down into a group of smaller problems. This process of breaking a
problem into smaller subproblems is called **functional decomposition**.

Here's a simple example of functional decomposition using two functions.
The first function called `square`{.docutils .literal .notranslate}
simply computes the square of a given number. The second function called
`sum_of_squares`{.docutils .literal .notranslate} makes use of square to
compute the sum of three numbers that have been squared.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="12.11.1"}
::: {#clens11_9_1_question .ac_question}
:::

::: {#clens11_9_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 12.11.1 (clens11\_9\_1)]{.runestone_caption_text}
:::
:::

Even though this is a pretty simple idea, in practice this example
illustrates many very important Python concepts, including local and
global variables along with parameter passing. Note that the body of
`square`{.docutils .literal .notranslate} is not executed until it is
called from inside the `sum_of_squares`{.docutils .literal .notranslate}
function for the first time on line 6.

Also notice that when `square`{.docutils .literal .notranslate} is
called (at Step 8, for example), there are two groups of local
variables, one for `square`{.docutils .literal .notranslate} and one for
`sum_of_squares`{.docutils .literal .notranslate}. Each group of local
variables is called a **stack frame**. The variables `x`{.docutils
.literal .notranslate}, and `y`{.docutils .literal .notranslate} are
local variables in both functions. These are completely different
variables, even though they have the same name. Each function invocation
creates a new frame, and variables are looked up in that frame. Notice
that at step 11 of the execution, y has the value 25 in one frame and 2
in the other.

What happens when you to refer to variable y on line 3? Python looks up
the value of y in the stack frame for the `square`{.docutils .literal
.notranslate} function. If it didn't find it there, it would go look in
the global frame.

Let's use composition to build up a little more useful function. Recall
from the dictionaries chapter that we had a two-step process for finding
the letter that appears most frequently in a text string:

1.  Accumulate a dictionary with letters as keys and counts as values.
    See [[example]{.std
    .std-ref}](../Dictionaries/intro-AccumulatingMultipleResultsInaDictionary.html#accumulating-counts){.reference
    .internal}.

2.  Find the best key from that dictionary. See [[example]{.std
    .std-ref}](../Dictionaries/AccumulatingtheBestKey.html#accumulating-best-key){.reference
    .internal}.

We can make functions for each of those and then compose them into a
single function that finds the most common letter.

::: {.runestone .explainer .ac_section}
::: {#ac_11_9_1 component="activecode" question_label="12.11.2"}
::: {#ac_11_9_1_question .ac_question}
:::
:::
:::

**Check your Understanding**

::: {.runestone .explainer .ac_section}
::: {#ac11_9_1 component="activecode" question_label="12.11.3"}
::: {#ac11_9_1_question .ac_question}
**1.** Write two functions, one called `addit`{.docutils .literal
.notranslate} and one called `mult`{.docutils .literal .notranslate}.
`addit`{.docutils .literal .notranslate} takes one number as an input
and adds 5. `mult`{.docutils .literal .notranslate} takes one number as
an input, and multiplies that input by whatever is returned by
`addit`{.docutils .literal .notranslate}, and then returns the result.
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

-   [[](GlobalVariables.html)]{#relations-prev}
-   [[](FlowofExecutionSummary.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
