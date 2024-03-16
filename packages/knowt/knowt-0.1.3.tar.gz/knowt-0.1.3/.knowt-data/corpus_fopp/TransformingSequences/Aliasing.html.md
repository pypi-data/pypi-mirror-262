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
        Problem](/runestone/default/reportabug?course=fopp&page=Aliasing)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [9.1 Introduction: Transforming
        Sequences](intro-SequenceMutation.html){.reference .internal}
    -   [9.2 Mutability](Mutability.html){.reference .internal}
    -   [9.3 List Element Deletion](ListDeletion.html){.reference
        .internal}
    -   [9.4 Objects and
        References](ObjectsandReferences.html){.reference .internal}
    -   [9.5 Aliasing](Aliasing.html){.reference .internal}
    -   [9.6 Cloning Lists](CloningLists.html){.reference .internal}
    -   [9.7 Mutating Methods](MutatingMethods.html){.reference
        .internal}
    -   [9.8 Append versus
        Concatenate](AppendversusConcatenate.html){.reference .internal}
    -   [9.9 Non-mutating Methods on
        Strings](NonmutatingMethodsonStrings.html){.reference .internal}
    -   [9.10 String Format Method](StringFormatting.html){.reference
        .internal}
    -   [9.11 f-Strings](FStrings.html){.reference .internal}
    -   [9.12 The Accumulator Pattern with
        Lists](TheAccumulatorPatternwithLists.html){.reference
        .internal}
    -   [9.13 The Accumulator Pattern with
        Strings](TheAccumulatorPatternwithStrings.html){.reference
        .internal}
    -   [9.14 👩‍💻 Accumulator Pattern
        Strategies](WPAccumulatorPatternStrategies.html){.reference
        .internal}
    -   [9.15 👩‍💻 Don't Mutate A List That You Are Iterating
        Through](WPDontMutateAListYouIterateThrough.html){.reference
        .internal}
    -   [9.16 Summary](Glossary.html){.reference .internal}
    -   [9.17 Exercises](Exercises.html){.reference .internal}
    -   [9.18 Chapter Assessment - List
        Methods](week4a1.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#aliasing .section}
[9.5. ]{.section-number}Aliasing[¶](#aliasing "Permalink to this heading"){.headerlink}
=======================================================================================

Since variables refer to objects, if we assign one variable to another,
both variables refer to the same object:

::: {.runestone .explainer .ac_section}
::: {#ac8_4_1 component="activecode" question_label="9.5.1"}
::: {#ac8_4_1_question .ac_question}
:::
:::
:::

In this case, the reference diagram looks like this:

![State snapshot for multiple references (aliases) to a
list](../_images/refdiag4.png)

Because the same list has two different names, `a`{.docutils .literal
.notranslate} and `b`{.docutils .literal .notranslate}, we say that it
is **aliased**. Changes made with one alias affect the other. In the
codelens example below, you can see that `a`{.docutils .literal
.notranslate} and `b`{.docutils .literal .notranslate} refer to the same
list after executing the assignment statement `b = a`{.docutils .literal
.notranslate}.

::: {.runestone .explainer .ac_section}
::: {#ac8_4_2 component="activecode" question_label="9.5.2"}
::: {#ac8_4_2_question .ac_question}
:::
:::
:::

Although this behavior can be useful, it is sometimes unexpected or
undesirable. In general, it is safer to avoid aliasing when you are
working with mutable objects. Of course, for immutable objects, there's
no problem. That's why Python is free to alias strings and integers when
it sees an opportunity to economize.

**Check your understanding**

::: {.runestone}
-   [\[\'Jamboree\', \'get-together\',
    \'party\'\]]{#question8_1_3_opt_a}
-   Yes, the value of y has been reassigned to the value of w.
-   [\[\'celebration\'\]]{#question8_1_3_opt_b}
-   No, that was the inital value of y, but y has changed.
-   [\[\'celebration\', \'Jamboree\', \'get-together\',
    \'party\'\]]{#question8_1_3_opt_c}
-   No, when we assign a list to another list it does not concatenate
    the lists together.
-   [\[\'Jamboree\', \'get-together\', \'party\',
    \'celebration\'\]]{#question8_1_3_opt_d}
-   No, when we assign a list to another list it does not concatenate
    the lists together.
:::

::: {.runestone}
-   [\[4,2,8,6,5\]]{#question8_4_1_opt_a}
-   blist is not a copy of alist, it is a reference to the list alist
    refers to.
-   [\[4,2,8,999,5\]]{#question8_4_1_opt_b}
-   Yes, since alist and blist both reference the same list, changes to
    one also change the other.
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

-   [[](ObjectsandReferences.html)]{#relations-prev}
-   [[](CloningLists.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
