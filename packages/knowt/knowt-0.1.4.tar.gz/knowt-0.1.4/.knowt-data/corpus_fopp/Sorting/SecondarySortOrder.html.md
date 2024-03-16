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
        Problem](/runestone/default/reportabug?course=fopp&page=SecondarySortOrder)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [16.1 Introduction: Sorting with Sort and
        Sorted](intro-SortingwithSortandSorted.html){.reference
        .internal}
    -   [16.2 Optional reverse
        parameter](Optionalreverseparameter.html){.reference .internal}
    -   [16.3 Optional key
        parameter](Optionalkeyparameter.html){.reference .internal}
    -   [16.4 Sorting a Dictionary](SortingaDictionary.html){.reference
        .internal}
    -   [16.5 Breaking Ties: Second
        Sorting](SecondarySortOrder.html){.reference .internal}
    -   [16.6 👩‍💻 When to use a Lambda
        Expression](WPWhenToUseLambdaVsFunction.html){.reference
        .internal}
    -   [16.7 Glossary](Glossary.html){.reference .internal}
    -   [16.8 Exercises](Exercises.html){.reference .internal}
    -   [16.9 Chapter Assessment](ChapterAssessment.html){.reference
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

::: {#breaking-ties-second-sorting .section}
[]{#sort-stable}

[16.5. ]{.section-number}Breaking Ties: Second Sorting[¶](#breaking-ties-second-sorting "Permalink to this heading"){.headerlink}
=================================================================================================================================

What happens when two items are "tied" in the sort order? For example,
suppose we sort a list of words by their lengths. Which five letter word
will appear first?

The answer is that the python interpreter will sort the tied items in
the same order they were in before the sorting.

What if we wanted to sort them by some other property, say
alphabetically, when the words were the same length? Python allows us to
specify multiple conditions when we perform a sort by returning a tuple
from a key function.

First, let's see how python sorts tuples. We've already seen that
there's a built-in sort order, if we don't specify any key function. For
numbers, it's lowest to highest. For strings, it's alphabetic order. For
a sequence of tuples, the default sort order is based on the default
sort order for the first elements of the tuples, with ties being broken
by the second elements, and then third elements if necessary, etc. For
example,

::: {.runestone .explainer .ac_section}
::: {#ac18_5_0 component="activecode" question_label="16.5.1"}
::: {#ac18_5_0_question .ac_question}
:::
:::
:::

In the code below, we are going to sort a list of fruit words first by
their length, smallest to largest, and then alphabetically to break ties
among words of the same length. To do that, we have the key function
return a tuple whose first element is the length of the fruit's name,
and second element is the fruit name itself.

::: {.runestone .explainer .ac_section}
::: {#ac18_5_1 component="activecode" question_label="16.5.2"}
::: {#ac18_5_1_question .ac_question}
:::
:::
:::

Here, each word is evaluated first on it's length, then by its
alphabetical order. Note that we could continue to specify other
conditions by including more elements in the tuple.

What would happen though if we wanted to sort it by largest to smallest,
and then by alphabetical order?

::: {.runestone .explainer .ac_section}
::: {#ac18_5_2 component="activecode" question_label="16.5.3"}
::: {#ac18_5_2_question .ac_question}
:::
:::
:::

Do you see a problem here? Not only does it sort the words from largest
to smallest, but also in reverse alphabetical order! Can you think of
any ways you can solve this issue?

One solution is to add a negative sign in front of
`len(fruit_name)`{.docutils .literal .notranslate}, which will convert
all positive numbers to negative, and all negative numbers to positive.
As a result, the longest elements would be first and the shortest
elements would be last.

::: {.runestone .explainer .ac_section}
::: {#ac18_5_3 component="activecode" question_label="16.5.4"}
::: {#ac18_5_3_question .ac_question}
:::
:::
:::

We can use this for any numerical value that we want to sort, however
this will not work for strings.

**Check Your Understanding**

::: {.runestone}
-   [first city name (alphabetically), then temperature (lowest to
    highest)]{#question18_5_1_opt_a}
-   Correct! First we sort alphabetically by city name, then by the
    temperature, from lowest to highest.
-   [first temperature (highest to lowest), then city name
    (alphabetically)]{#question18_5_1_opt_b}
-   The order of the tuple matters. The first item in the tuple is the
    first condition used to sort.
-   [first city name (alphabetically), then temperature (highest to
    lowest)]{#question18_5_1_opt_c}
-   Not quite, remember that by default, the sorted function will sort
    by alphabetical order, or lowest to highest. Is the reverse
    parameter set to True? Has a negative sign been used in the key
    parameter?
-   [first temperature (lowest to highest), then city name
    (alphabetically)]{#question18_5_1_opt_d}
-   The order of the tuple matters. The first item in the tuple is the
    first condition used to sort.
:::

::: {.runestone}
-   [first city name (reverse alphabetically), then temperature (lowest
    to highest)]{#question18_5_2_opt_a}
-   Correct! In this case, the reverse parameter will cause the city
    name to be sorted reverse alphabetically instead of alphabetically,
    and it will also negate the negative sign in front of the
    temperature.
-   [first temperature (highest to lowest), then city name
    (alphabetically)]{#question18_5_2_opt_b}
-   The order of the tuple matters. The first item in the tuple is the
    first condition used to sort. Also, take note of the reverse
    parameter - what will it do in this instance?
-   [first city name (reverse alphabetically), then temperature (highest
    to lowest)]{#question18_5_2_opt_c}
-   Not quite - is the reverse parameter set to True? Has a negative
    sign been used in the key parameter? What happens when those are
    both used?
-   [first temperature (lowest to highest), then city name
    (alphabetically)]{#question18_5_2_opt_d}
-   The order of the tuple matters. The first item in the tuple is the
    first condition used to sort.
-   [first city name (alphabetically), then temperature (lowest to
    highest)]{#question18_5_2_opt_e}
-   Not quite, remember that by default, the sorted function will sort
    by alphabetical order, or lowest to highest. Is the reverse
    parameter set to True? Has a negative sign been used in the key
    parameter?
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

-   [[](SortingaDictionary.html)]{#relations-prev}
-   [[](WPWhenToUseLambdaVsFunction.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
