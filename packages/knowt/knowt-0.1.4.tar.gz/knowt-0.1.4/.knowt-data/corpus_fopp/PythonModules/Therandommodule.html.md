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
        Problem](/runestone/default/reportabug?course=fopp&page=Therandommodule)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [4.1 Introduction to Python
        Modules](intro-PythonModules.html){.reference .internal}
    -   [4.2 Modules](intro-ModulesandGettingHelp.html){.reference
        .internal}
    -   [4.3 The random module](Therandommodule.html){.reference
        .internal}
    -   [4.4 Glossary](Glossary.html){.reference .internal}
    -   [4.5 Exercises](Exercises.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#the-random-module .section}
[4.3. ]{.section-number}The `random`{.docutils .literal .notranslate} module[¶](#the-random-module "Permalink to this heading"){.headerlink}
============================================================================================================================================

We often want to use **random numbers** in programs. Here are a few
typical uses:

-   To play a game of chance where the computer needs to throw some
    dice, pick a number, or flip a coin,

-   To shuffle a deck of playing cards randomly,

-   To randomly allow a new enemy spaceship to appear and shoot at you,

-   To simulate possible rainfall when we make a computerized model for
    estimating the environmental impact of building a dam,

-   For encrypting your banking session on the Internet.

Python provides a module `random`{.docutils .literal .notranslate} that
helps with tasks like this. You can take a look at it in the
documentation. Here are the key things we can do with it.

::: {.runestone .explainer .ac_section}
::: {#ac13_2_1 component="activecode" question_label="4.3.1"}
::: {#ac13_2_1_question .ac_question}
:::
:::
:::

Press the run button a number of times. Note that the values change each
time. These are random numbers.

The `randrange`{.docutils .literal .notranslate} function generates an
integer between its lower and upper argument where the lower bound is
included, but the upper bound is excluded. So,
`randrange(1,7)`{.docutils .literal .notranslate} will include numbers
from 1-6. If you omit the first parameter it is assumed to be 0 so
`randrange(10)`{.docutils .literal .notranslate} will give you numbers
from 0-9. All the values have an equal probability of occurring (i.e.
the results are *uniformly* distributed).

The `random()`{.docutils .literal .notranslate} function returns a
floating point number in the range \[0.0, 1.0) --- the square bracket
means "closed interval on the left" and the round parenthesis means
"open interval on the right". In other words, 0.0 is possible, but all
returned numbers will be strictly less than 1.0. It is usual to *scale*
the results after calling this method, to get them into a range suitable
for your application.

In the case shown below, we've converted the result of the method call
to a number in the range \[0.0, 5.0). Once more, these are uniformly
distributed numbers --- numbers close to 0 are just as likely to occur
as numbers close to 3, or numbers close to 5. If you continue to press
the run button you will see random values between 0.0 and up to but not
including 5.0.

::: {.runestone .explainer .ac_section}
::: {#ac13_2_2 component="activecode" question_label="4.3.2"}
::: {#ac13_2_2_question .ac_question}
:::
:::
:::

It is important to note that random number generators are based on a
**deterministic** algorithm --- repeatable and predictable. So they're
called **pseudo-random** generators --- they are not genuinely random.
They start with a *seed* value. Each time you ask for another random
number, you'll get one based on the current seed attribute, and the
state of the seed (which is one of the attributes of the generator) will
be updated. The good news is that each time you run your program, the
seed value is likely to be different meaning that even though the random
numbers are being created algorithmically, you will likely get random
behavior each time you execute.

**Check your understanding**

::: {.runestone}
-   [prob = random.randrange(1, 101)]{#question13_2_1_opt_a}
-   This will generate a number between 1 and 101, but does not
    include 101.
-   [prob = random.randrange(1, 100)]{#question13_2_1_opt_b}
-   This will generate a number between 1 and 100, but does not
    include 100. The highest value generated will be 99.
-   [prob = random.randrange(0, 101)]{#question13_2_1_opt_c}
-   This will generate a number between 0 and 100. The lowest value
    generated is 0. The highest value generated will be 100.
-   [prob = random.randrange(0, 100)]{#question13_2_1_opt_d}
-   This will generate a number between 0 and 100, but does not
    include 100. The lowest value generated is 0 and the highest value
    generated will be 99.
:::

::: {.runestone}
-   [There is no computer on the stage for the
    drawing.]{#question13_2_2_opt_a}
-   They could easily put one there.
-   [Because computers don't really generate random numbers, they
    generate pseudo-random numbers.]{#question13_2_2_opt_b}
-   Computers generate random numbers using a deterministic algorithm.
    This means that if anyone ever found out the algorithm they could
    accurately predict the next value to be generated and would always
    win the lottery.
-   [They would just generate the same numbers over and over
    again.]{#question13_2_2_opt_c}
-   This might happen if the same seed value was used over and over
    again, but they could make sure this was not the case.
-   [The computer can't tell what values were already selected, so it
    might generate all 5's instead of 5 unique
    numbers.]{#question13_2_2_opt_d}
-   While a programmer would need to ensure the computer did not select
    the same number more than once, it is easy to ensure this.
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

-   [[](intro-ModulesandGettingHelp.html)]{#relations-prev}
-   [[](Glossary.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
