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
        Problem](/runestone/default/reportabug?course=fopp&page=filter)
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
::: {#filter .section}
[23.3. ]{.section-number}Filter[¶](#filter "Permalink to this heading"){.headerlink}
====================================================================================

Now consider another common pattern: going through a list and keeping
only those items that meet certain criteria. This is called a filter.

::: {.runestone .explainer .ac_section}
::: {#ac21_3_1 component="activecode" question_label="23.3.1"}
::: {#ac21_3_1_question .ac_question}
:::
:::
:::

Again, this pattern of computation is so common that Python offers a
more compact and general way to do it, the `filter`{.docutils .literal
.notranslate} function. `filter`{.docutils .literal .notranslate} takes
two arguments, a function and a sequence. The function takes one item
and return True if the item should. It is automatically called for each
item in the sequence. You don't have to initialize an accumulator or
iterate with a for loop.

::: {.runestone .explainer .ac_section}
::: {#ac21_3_2 component="activecode" question_label="23.3.2"}
::: {#ac21_3_2_question .ac_question}
:::
:::
:::

**Check Your Understanding**

::: {.runestone .explainer .ac_section}
::: {#ac21_3_3 component="activecode" question_label="23.3.3"}
::: {#ac21_3_3_question .ac_question}
**1.** Write code to assign to the variable `filter_testing`{.docutils
.literal .notranslate} all the elements in lst\_check that have a "w" in
them using filter.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac21_3_4 component="activecode" question_label="23.3.4"}
::: {#ac21_3_4_question .ac_question}
**2.** Using filter, filter `lst`{.docutils .literal .notranslate} so
that it only contains words containing the letter "o". Assign to
variable `lst2`{.docutils .literal .notranslate}. Do not hardcode this.
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

-   [[](map.html)]{#relations-prev}
-   [[](listcomp.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
