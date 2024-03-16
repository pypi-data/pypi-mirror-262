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
        Problem](/runestone/default/reportabug?course=fopp&page=WPWhenToUseLambdaVsFunction)
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

::: {#when-to-use-a-lambda-expression .section}
[16.6. ]{.section-number}👩‍💻 When to use a Lambda Expression[¶](#when-to-use-a-lambda-expression "Permalink to this heading"){.headerlink}
==========================================================================================================================================

Though you can often use a lambda expression or a named function
interchangeably when sorting, it's generally best to use lambda
expressions until the process is too complicated, and then a function
should be used. For example, in the following examples, we'll be sorting
a dictionary's keys by properties of its values. Each key is a state
name and each value is a list of city names.

For our first sort order, we want to sort the states in order by the
length of the first city name. Here, it's pretty easy to compute that
property. `states[state]`{.docutils .literal .notranslate} is the list
of cities associated with a particular state. So If `state`{.docutils
.literal .notranslate} is a list of city strings,
`len(states[state][0])`{.docutils .literal .notranslate} is the length
of the first city name. Thus, we can use a lambda expression:

::: {.runestone .explainer .ac_section}
::: {#ac18_6_1 component="activecode" question_label="16.6.1"}
::: {#ac18_6_1_question .ac_question}
:::
:::
:::

That's already pushing the limits of complex a lambda expression can be
before it's reall hard to read (or debug).

For our second sort order, the property we want to sort by is the number
of cities that begin with the letter 'S'. The function defining this
property is harder to express, requiring a filter and count accumulation
pattern. So we are better off defining a separate, named function. Here,
we've chosen to make a lambda expression that looks up the value
associated with the particular state and pass that value to the named
function s\_cities\_count. We could have passed just the key, but then
the function would have to look up the value, and it would be a little
confusing, from the code, to figure out what dictionary the key is
supposed to be looked up in. Here, we've done the lookup right in the
lambda expression, which makes it a little bit clearer that we're just
sorting the keys of the states dictionary based on a property of their
values. It also makes it easier to reuse the counting function on other
city lists, even if they aren't embedded in that particular states
dictionary.

::: {.runestone .explainer .ac_section}
::: {#ac18_6_2 component="activecode" question_label="16.6.2"}
::: {#ac18_6_2_question .ac_question}
:::
:::
:::

At this point in the course, we don't even know how to do such a filter
and accumulation as part of a lambda expression. There is a way, using
something called list comprehensions, but we haven't covered that yet.

There will be other situations that are even more complicated than this.
In some cases, they may be too complicated to solve with a lambda
expression at all! You can always fall back on writing a named function
when a lambda expression will be too complicated.
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

-   [[](SecondarySortOrder.html)]{#relations-prev}
-   [[](Glossary.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
