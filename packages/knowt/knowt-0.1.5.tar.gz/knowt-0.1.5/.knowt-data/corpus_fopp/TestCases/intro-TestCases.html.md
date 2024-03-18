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
        Problem](/runestone/default/reportabug?course=fopp&page=intro-TestCases)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [18.1 Introduction: Test Cases](intro-TestCases.html){.reference
        .internal}
    -   [18.2 Checking Assumptions About Data
        Types](TestingTypes.html){.reference .internal}
    -   [18.3 Checking Other
        Assumptions](CheckingOtherAssumptions.html){.reference
        .internal}
    -   [18.4 Testing Conditionals](TestingConditionals.html){.reference
        .internal}
    -   [18.5 Testing Loops](TestingLoops.html){.reference .internal}
    -   [18.6 Writing Test Cases for
        Functions](Testingfunctions.html){.reference .internal}
    -   [18.7 Testing Optional
        Parameters](TestingOptionalParameters.html){.reference
        .internal}
    -   [18.8 👩‍💻 Test Driven
        Development](WPProgramDevelopment.html){.reference .internal}
    -   [18.9 Glossary](Glossary.html){.reference .internal}
    -   [18.10 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
    -   [18.11 Exercises](Exercises.html){.reference .internal}
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

::: {#introduction-test-cases .section}
[]{#test-cases-chap}

[18.1. ]{.section-number}Introduction: Test Cases[¶](#introduction-test-cases "Permalink to this heading"){.headerlink}
=======================================================================================================================

A **test case** expresses requirements for a program, in a way that can
be checked automatically. Specifically, a test asserts something about
the state of the program at a particular point in its execution.

We have previously suggested that it's a good idea to first write down
comments about what your code is supposed to do, before actually writing
the code. It is an even better idea to write down some test cases before
writing a program.

There are several reasons why it's a good habit to write test cases.

-   Before we write code, we have in mind what it *should* do, but those
    thoughts may be a little vague. Writing down test cases forces us to
    be more concrete about what should happen.

-   As we write the code, the test cases can provide automated feedback.
    You've actually been the beneficiary of such automated feedback via
    test cases throughout this book in some of the activecode windows
    and almost all of the exercises. We wrote the code for those test
    cases but kept it hidden, so as not to confuse you and also to avoid
    giving away the answers. You can get some of the same benefit from
    writing your own test cases.

-   In larger software projects, the set of test cases can be run every
    time a change is made to the code base. **Unit tests** check that
    small bits of code are correctly implemented. **Functional tests**
    check that larger chunks of code work correctly. Running the tests
    can help to identify situations where a change in code in one place
    breaks the correct operation of some other code. We won't see that
    advantage of test cases in this textbook, but keep in mind that this
    introduction to test cases is setting the stage for an essential
    software engineering practice if you are participating in a larger
    software development project.

Now it's time to learn how to write code for test cases.

Python provides a statement called `assert`{.docutils .literal
.notranslate}.

-   Following the word assert there will be a python expression.

-   If that expression evaluates to the Boolean `False`{.docutils
    .literal .notranslate}, then the interpreter will raise a runtime
    error.

-   If the expression evaluates to `True`{.docutils .literal
    .notranslate}, then nothing happens and the execution goes on to the
    next line of code.

Why would you ever want to write a line of code that can never compute
anything useful for you, but sometimes causes a runtime error? For all
the reasons we described above about the value of automated tests. You
want a test that will alert that you that some condition you assumed was
true is not in fact true. It's much better to be alerted to that fact
right away than to have some unexpected result much later in your
program execution, which you will have trouble tracing to the place
where you had an error in your code.

Why doesn't `assert`{.docutils .literal .notranslate} print out
something saying that the test passed? The reason is that you don't want
to clutter up your output window with the results of automated tests
that pass. You just want to know when one of your tests fails. In larger
projects, other testing harnesses are used instead of `assert`{.docutils
.literal .notranslate}, such as the python `unittest`{.docutils .literal
.notranslate} module. Those provide some output summarizing tests that
have passed as well as those that failed. In this textbook, we will just
use simple `assert`{.docutils .literal .notranslate} statements for
automated tests.

To write a test, we must know what we *expect* some value to be at a
particular point in the program's execution. In the rest of the chapter,
we'll see some examples of `assert`{.docutils .literal .notranslate}
statements and ideas for what kinds of assertions one might want to add
in one's programs.

::: {.admonition .note}
Note

A note to instructors: this chapter is deliberately structured so that
you can introduce testing early in the course if you want to. You will
need to cover chapter 8, on Conditionals, before starting this chapter,
because that chapter covers Booleans. The subchapters on testing types
and testing conditionals can be covered right after that. The subchapter
on testing functions can be delayed until after you have covered
function definition.
:::

**Check your understanding**

::: {.runestone}
-   [A runtime error will occur]{#question19_1_1_opt_a}
-   The expression \`\`x==y\`\` evaluates to \`\`False\`\`, so a runtime
    error will occur
-   [A message is printed out saying that the test
    failed.]{#question19_1_1_opt_b}
-   If the assertion fails, a runtime error will occur
-   [x will get the value that y currently has]{#question19_1_1_opt_c}
-   \`\`x==y\`\` is a Boolean expression, not an assignment statement
-   [Nothing will happen]{#question19_1_1_opt_d}
-   The expression \`\`x==y\`\` evaluates to \`\`False\`\`
-   [A message is printed out saying that the test
    passed.]{#question19_1_1_opt_e}
-   When an assertion test passes, no message is printed. In this case,
    the assertion test fails.
:::

::: {.runestone}
-   [A runtime error will occur]{#question19_1_1b_opt_a}
-   The expression \`\`x==y\`\` evaluates to \`\`True\`\`
-   [A message is printed out saying that the test
    failed.]{#question19_1_1b_opt_b}
-   The expression \`\`x==y\`\` evaluates to \`\`True\`\`
-   [x will get the value that y currently has]{#question19_1_1b_opt_c}
-   \`\`x==y\`\` is a Boolean expression, not an assignment statement
-   [Nothing will happen]{#question19_1_1b_opt_d}
-   The expression \`\`x==y\`\` evaluates to \`\`True\`\`
-   [A message is printed out saying that the test
    passed.]{#question19_1_1b_opt_e}
-   When an assertion test passes, no message is printed.
:::

::: {.runestone}
-   [True]{#question19_1_2_opt_a}
-   You might not notice the error, if the code just produces a wrong
    output rather generating an error. And it may be difficult to figure
    out the original cause of an error when you do get one.
-   [False]{#question19_1_2_opt_b}
-   Test cases let you test some pieces of code as you write them,
    rather than waiting for problems to show themselves later.
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

-   [[](toctree.html)]{#relations-prev}
-   [[](TestingTypes.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
