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
        Problem](/runestone/default/reportabug?course=fopp&page=listcomp)
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
::: {#list-comprehensions .section}
[23.4. ]{.section-number}List Comprehensions[¶](#list-comprehensions "Permalink to this heading"){.headerlink}
==============================================================================================================

Python provides an alternative way to do `map`{.docutils .literal
.notranslate} and `filter`{.docutils .literal .notranslate} operations,
called a **list comprehension**. Many programmers find them easier to
understand and write. List comprehensions are concise ways to create
lists from other lists. The general syntax is:

::: {.highlight-default .notranslate}
::: {.highlight}
    [<transformer_expression> for <loop_var> in <sequence> if <filtration_expression>]
:::
:::

where the if clause is optional. For example,

::: {.runestone .explainer .ac_section}
::: {#ac20_4_1 component="activecode" question_label="23.4.1"}
::: {#ac20_4_1_question .ac_question}
:::
:::
:::

The transformer expression is `value * 2`{.docutils .literal
.notranslate}. The item variable is `value`{.docutils .literal
.notranslate} and the sequence is `things`{.docutils .literal
.notranslate}. This is an alternative way to perform a mapping
operation. As with `map`{.docutils .literal .notranslate}, each item in
the sequence is transformed into an item in the new list. Instead of the
iteration happening automatically, however, we have adopted the syntax
of the for loop which may make it easier to understand.

Just as in a regular for loop, the part of the statement
`for value in things`{.docutils .literal .notranslate} says to execute
some code once for each item in things. Each time that code is executed,
`value`{.docutils .literal .notranslate} is bound to one item from
`things`{.docutils .literal .notranslate}. The code that is executed
each time is the transformer expression, `value * 2`{.docutils .literal
.notranslate}, rather than a block of code indented underneath the for
statement. The other difference from a regular for loop is that each
time the expression is evaluated, the resulting value is appended to a
list. That happens automatically, without the programmer explicitly
initializing an empty list or appending each item.

The `if`{.docutils .literal .notranslate} clause of a list comprehension
can be used to do a filter operation. To perform a pure filter
operation, the expression can be simply the variable that is bound to
each item. For example, the following list comprehension will keep only
the even numbers from the original list.

::: {.runestone .explainer .ac_section}
::: {#ac20_4_2 component="activecode" question_label="23.4.2"}
::: {#ac20_4_2_question .ac_question}
:::
:::
:::

You can also combine `map`{.docutils .literal .notranslate} and
`filter`{.docutils .literal .notranslate} operations by chaining them
together, or with a single list comprehension.

::: {.runestone .explainer .ac_section}
::: {#ac20_4_3 component="activecode" question_label="23.4.3"}
::: {#ac20_4_3_question .ac_question}
:::
:::
:::

**Check your understanding**

::: {.runestone}
-   [\[4,2,8,6,5\]]{#question21_4_1_opt_a}
-   Items from alist are doubled before being placed in blist.
-   [\[8,4,16,12,10\]]{#question21_4_1_opt_b}
-   Not all the items in alist are to be included in blist. Look at the
    if clause.
-   [10]{#question21_4_1_opt_c}
-   The result needs to be a list.
-   [\[10\]]{#question21_4_1_opt_d}
-   Yes, 5 is the only odd number in alist. It is doubled before being
    placed in blist.
:::

::: {.runestone .explainer .ac_section}
::: {#ac21_4_4 component="activecode" question_label="23.4.5"}
::: {#ac21_4_4_question .ac_question}
**2.** The for loop below produces a list of numbers greater than 10.
Below the given code, use list comprehension to accomplish the same
thing. Assign it the the variable `lst2`{.docutils .literal
.notranslate}. Only one line of code is needed.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac21_4_5 component="activecode" question_label="23.4.6"}
::: {#ac21_4_5_question .ac_question}
**3.** Write code to assign to the variable `compri`{.docutils .literal
.notranslate} all the values of the key `name`{.docutils .literal
.notranslate} in any of the sub-dictionaries in the dictionary
`tester`{.docutils .literal .notranslate}. Do this using a list
comprehension.
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

-   [[](filter.html)]{#relations-prev}
-   [[](zip.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
