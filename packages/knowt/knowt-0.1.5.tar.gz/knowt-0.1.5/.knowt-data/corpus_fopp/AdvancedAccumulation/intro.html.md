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
        Problem](/runestone/default/reportabug?course=fopp&page=intro)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [23.1 Introduction: Map, Filter, List Comprehensions, and
        Zip](intro.html){.reference .internal}
    -   [23.2 Map](map.html){.reference .internal}
    -   [23.3 Filter](filter.html){.reference .internal}
    -   [23.4 List Comprehensions](listcomp.html){.reference .internal}
    -   [23.5 Zip](zip.html){.reference .internal}
    -   [23.6 Exercises](Exercises.html){.reference .internal}
    -   [23.7 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#introduction-map-filter-list-comprehensions-and-zip .section}
[]{#list-comp-chap}

[23.1. ]{.section-number}Introduction: Map, Filter, List Comprehensions, and Zip[¶](#introduction-map-filter-list-comprehensions-and-zip "Permalink to this heading"){.headerlink}
==================================================================================================================================================================================

Let's revisit the [[accumulator pattern]{.std
.std-ref}](../Iteration/TheAccumulatorPattern.html#accum-pattern){.reference
.internal}. We have frequently taken a list and produced another list
from it that contains either a subset of the items or a transformed
version of each item. When each item is transformed we say that the
operation is a **mapping, or just a map** of the original list. When
some items are omitted, we call it a **filter**.

Python provides built-in functions `map`{.docutils .literal
.notranslate} and `filter`{.docutils .literal .notranslate}. Python also
provides a new syntax, called **list comprehensions**, that lets you
express a mapping and/or filtering operation. Just as with named
functions and lambda expressions, some students seem to find it easier
to think in terms of the map and filter functions, while other students
find it easier to read and write list comprehensions. You'll learn both
ways; one may even help you understand the other. Most python
programmers use list comprehensions, so make sure you learn to read
those. In this course, you can choose to learn to write list
comprehensions or to use map and filter, whichever you prefer. You
should learn to read both list comprehensions and map/filter.

Other common accumulator patterns on lists aggregate all the values into
a single value.

Map, and filter are commands that you would use in high-performance
computing on big datasets. See [MapReduce on
Wikipedia](http://en.wikipedia.org/wiki/MapReduce){.reference
.external}.
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
-   [[](map.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
