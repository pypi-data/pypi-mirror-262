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
        Problem](/runestone/default/reportabug?course=fopp&page=ConcatenationandRepetition)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [6.1 Introduction: Sequences](intro-Sequences.html){.reference
        .internal}
    -   [6.2 Strings, Lists, and
        Tuples](StringsandLists.html){.reference .internal}
    -   [6.3 Index Operator: Working with the Characters of a
        String](IndexOperatorWorkingwiththeCharactersofaString.html){.reference
        .internal}
    -   [6.4 Disambiguating \[\]: creation vs
        indexing](DisabmiguatingSquareBrackets.html){.reference
        .internal}
    -   [6.5 Length](Length.html){.reference .internal}
    -   [6.6 The Slice Operator](TheSliceOperator.html){.reference
        .internal}
    -   [6.7 Concatenation and
        Repetition](ConcatenationandRepetition.html){.reference
        .internal}
    -   [6.8 Count and Index](CountandIndex.html){.reference .internal}
    -   [6.9 Splitting and Joining
        Strings](SplitandJoin.html){.reference .internal}
    -   [6.10 Exercises](Exercises.html){.reference .internal}
    -   [6.11 Chapter Assessment](week2a1.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#concatenation-and-repetition .section}
[]{#index-0}

[6.7. ]{.section-number}Concatenation and Repetition[¶](#concatenation-and-repetition "Permalink to this heading"){.headerlink}
===============================================================================================================================

Again, as with strings, the `+`{.docutils .literal .notranslate}
operator concatenates lists. Similarly, the `*`{.docutils .literal
.notranslate} operator repeats the items in a list a given number of
times.

::: {.runestone .explainer .ac_section}
::: {#ac5_7_1 component="activecode" question_label="6.7.1"}
::: {#ac5_7_1_question .ac_question}
:::
:::
:::

It is important to see that these operators create new lists from the
elements of the operand lists. If you concatenate a list with 2 items
and a list with 4 items, you will get a new list with 6 items (not a
list with two sublists). Similarly, repetition of a list of 2 items 4
times will give a list with 8 items.

One way for us to make this more clear is to run a part of this example
in codelens. As you step through the code, you will see the variables
being created and the lists that they refer to. Pay particular attention
to the fact that when `newlist`{.docutils .literal .notranslate} is
created by the statement `newlist = fruit + numlist`{.docutils .literal
.notranslate}, it refers to a completely new list formed by making
copies of the items from `fruit`{.docutils .literal .notranslate} and
`numlist`{.docutils .literal .notranslate}. You can see this very
clearly in the codelens object diagram. The objects are different.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="6.7.2"}
::: {#clens5_7_1_question .ac_question}
:::

::: {#clens5_7_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 6.7.2 (clens5\_7\_1)]{.runestone_caption_text}
:::
:::

::: {.admonition .note}
Note

WP: Adding types together

Beware when adding different types together! Python doesn't understand
how to concatenate different types together. Thus, if we try to add a
string to a list with `['first'] + "second"`{.docutils .literal
.notranslate} then the interpreter will return an error. To do this
you'll need to make the two objects the same type. In this case, it
means putting the string into its own list and then adding the two
together like so: `['first'] + ["second"]`{.docutils .literal
.notranslate}. This process will look different for other types though.
Remember that there are functions to convert types!
:::

**Check your understanding**

::: {.runestone}
-   [6]{#question5_7_1_opt_a}
-   Concatenation does not add the lengths of the lists.
-   [\[1,2,3,4,5,6\]]{#question5_7_1_opt_b}
-   Concatenation does not reorder the items.
-   [\[1,3,5,2,4,6\]]{#question5_7_1_opt_c}
-   Yes, a new list with all the items of the first list followed by all
    those from the second.
-   [\[3,7,11\]]{#question5_7_1_opt_d}
-   Concatenation does not add the individual items.
:::

::: {.runestone}
-   [9]{#question5_7_2_opt_a}
-   Repetition does not multiply the lengths of the lists. It repeats
    the items.
-   [\[1,1,1,3,3,3,5,5,5\]]{#question5_7_2_opt_b}
-   Repetition does not repeat each item individually.
-   [\[1,3,5,1,3,5,1,3,5\]]{#question5_7_2_opt_c}
-   Yes, the items of the list are repeated 3 times, one after another.
-   [\[3,9,15\]]{#question5_7_2_opt_d}
-   Repetition does not multiply the individual items.
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

-   [[](TheSliceOperator.html)]{#relations-prev}
-   [[](CountandIndex.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
