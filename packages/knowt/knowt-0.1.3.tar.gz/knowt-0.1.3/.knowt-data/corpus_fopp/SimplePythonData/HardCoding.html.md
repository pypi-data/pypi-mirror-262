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
        Problem](/runestone/default/reportabug?course=fopp&page=HardCoding)
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

::: {#hard-coding .section}
[2.14. ]{.section-number}👩‍💻 Hard-Coding[¶](#hard-coding "Permalink to this heading"){.headerlink}
==================================================================================================

As you begin programming, you'll see that there are many ways to solve
problems. You'll also find that one of the thrills of programming is how
easily you can do things correctly that humans could easily make errors
on. For example, you'll learn how to write just a very small bit of code
to find the 1047th character in a sentence that might be thousands of
letters long, and you'll learn how to do the exact same computation on
many different pieces of data.

We'll often tell you in this textbook *not to hard-code* answers. What
does that mean?

Some things in programming you can only do by typing them out. As you've
seen, when you have to assign a value to a variable, you simply type
something like `xyz = 6`{.docutils .literal .notranslate}. No other way.

But in most cases, it's best not to do computation in your head or write
complete answers to programming problems out by hand. That's where
**hard-coding** comes in. "Don't hard code" basically means, you should
rely on your code, your logic, your program, and you should *not* write
things out by hand or do computation in your head -- even if you can do
so easily.

When you are writing code or working on the answer to a programming
exercise, you should ask yourself: *Would my answer be correct even if
the provided variables had different values?* If the answer to that
question is no, you're probably hard- coding, which you should avoid --
and there's probably at least a slightly more concise way to construct
your answer!

For example, in this following code, if you're asked in an exercise to
create a variable `zx`{.docutils .literal .notranslate} and assign it
the value of the sum of the value of `y`{.docutils .literal
.notranslate} and the value of `x`{.docutils .literal .notranslate},
writing `zx = 55`{.docutils .literal .notranslate} is *hard-coding*.

::: {.runestone .explainer .ac_section}
::: {#hard_coding_example component="activecode" question_label="2.14.1"}
::: {#hard_coding_example_question .ac_question}
:::
:::
:::

The operation `20 + 35`{.docutils .literal .notranslate} may be easy
math to do in your head or with a calculator, but when you learn to
program, you want to train yourself to notice useful patterns of how to
solve problems, which will make your life easier (perhaps beyond
programming, even).

The correct way to answer that sort of exercise would be to write:
`zx = y + x`{.docutils .literal .notranslate} (or `zx = x + y`{.docutils
.literal .notranslate}, as you were just reminded of the order of
operations). That is not hard-coding, and it will be correct no matter
what the values of `x`{.docutils .literal .notranslate} and
`y`{.docutils .literal .notranslate} are.

In the code above, if the value of `x`{.docutils .literal .notranslate}
were `40`{.docutils .literal .notranslate}, `55`{.docutils .literal
.notranslate} would not be the correct value for `zx`{.docutils .literal
.notranslate} to have. But `zx = y + x`{.docutils .literal .notranslate}
would still be absolutely correct.

Try as much as you can not to rely on your brilliant but fallible human
brain to do *computation* when you program -- use your brain to
determine how to write the correct code to solve the problem for you!
That's why we require you to avoid hard -coding for most exercises in
this book.
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

-   [[](UpdatingVariables.html)]{#relations-prev}
-   [[](Input.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
