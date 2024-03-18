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
        Problem](/runestone/default/reportabug?course=fopp&page=map)
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
::: {#map .section}
[]{#map-chap}

[23.2. ]{.section-number}Map[¶](#map "Permalink to this heading"){.headerlink}
==============================================================================

You previously were introduced to accumulating a list by transforming
each of the elements. Here we revisit that pattern.

The following function produces a new list with each item in the
original list doubled. It is an example of a mapping, from the original
list to a new list of the same length, where each element is doubled.

::: {.runestone .explainer .ac_section}
::: {#ac21_2_1 component="activecode" question_label="23.2.1"}
::: {#ac21_2_1_question .ac_question}
:::
:::
:::

The doubleStuff function is an example of the accumulator pattern, in
particular the mapping pattern. On line 3, `new_list`{.docutils .literal
.notranslate} is initialized. On line 5, the doubled value for the
current item is produced and on line 6 it is appended to the list we're
accumulating. Line 7 executes after we've processed all the items in the
original list: it returns the `new_list`{.docutils .literal
.notranslate}. Once again, codelens helps us to see the actual
references and objects as they are passed and returned.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="23.2.2"}
::: {#clens21_2_1_question .ac_question}
:::

::: {#clens21_2_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 23.2.2 (clens21\_2\_1)]{.runestone_caption_text}
:::
:::

This pattern of computation is so common that python offers a more
general way to do mappings, the `map`{.docutils .literal .notranslate}
function, that makes it more clear what the overall structure of the
computation is. `map`{.docutils .literal .notranslate} takes two
arguments, a function and a sequence. The function is the mapper that
transforms items. It is automatically applied to each item in the
sequence. You don't have to initialize an accumulator or iterate with a
for loop at all.

::: {.admonition .note}
Note

Technically, in a proper Python 3 interpreter, the `map`{.docutils
.literal .notranslate} function produces an "iterator", which is like a
list but produces the items as they are needed. Most places in Python
where you can use a list (e.g., in a for loop) you can use an "iterator"
as if it was actually a list. So you probably won't ever notice the
difference. If you ever really need a list, you can explicitly turn the
output of map into a list: `list(map(...))`{.docutils .literal
.notranslate}. In the runestone environment, `map`{.docutils .literal
.notranslate} actually returns a real list, but to make this code
compatible with a full python environment, we always convert it to a
list.
:::

As we did when passing a function as a parameter to the
`sorted`{.docutils .literal .notranslate} function, we can specify a
function to pass to `map`{.docutils .literal .notranslate} either by
referring to a function by name, or by providing a lambda expression.

::: {.runestone .explainer .ac_section}
::: {#ac21_2_2 component="activecode" question_label="23.2.3"}
::: {#ac21_2_2_question .ac_question}
:::
:::
:::

Of course, once we get used to using the `map`{.docutils .literal
.notranslate} function, it's no longer necessary to define functions
like `tripleStuff`{.docutils .literal .notranslate} and
`quadrupleStuff`{.docutils .literal .notranslate}.

::: {.runestone .explainer .ac_section}
::: {#ac21_2_3 component="activecode" question_label="23.2.4"}
::: {#ac21_2_3_question .ac_question}
:::
:::
:::

**Check Your Understanding**

::: {.runestone .explainer .ac_section}
::: {#ac21_2_4 component="activecode" question_label="23.2.5"}
::: {#ac21_2_4_question .ac_question}
**1.** Using map, create a list assigned to the variable
`greeting_doubled`{.docutils .literal .notranslate} that doubles each
element in the list `lst`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac21_2_5 component="activecode" question_label="23.2.6"}
::: {#ac21_2_5_question .ac_question}
**2.** Below, we have provided a list of strings called
`abbrevs`{.docutils .literal .notranslate}. Use map to produce a new
list called `abbrevs_upper`{.docutils .literal .notranslate} that
contains all the same strings in upper case.
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

-   [[](intro.html)]{#relations-prev}
-   [[](filter.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
