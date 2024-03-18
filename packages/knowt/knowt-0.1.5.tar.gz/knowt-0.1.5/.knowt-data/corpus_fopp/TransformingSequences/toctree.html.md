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
        Problem](/runestone/default/reportabug?course=fopp&page=toctree)
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
::: {#transforming-sequences .section}
[9. ]{.section-number}Transforming Sequences[¶](#transforming-sequences "Permalink to this heading"){.headerlink}
=================================================================================================================

::: {.toctree-wrapper .compound}
[Transforming Sequences]{.caption-text}

-   [9.1. Introduction: Transforming
    Sequences](intro-SequenceMutation.html){.reference .internal}
    -   [9.1.1. Learning
        Goals](intro-SequenceMutation.html#learning-goals){.reference
        .internal}
    -   [9.1.2.
        Objectives](intro-SequenceMutation.html#objectives){.reference
        .internal}
-   [9.2. Mutability](Mutability.html){.reference .internal}
    -   [9.2.1. Lists are
        Mutable](Mutability.html#lists-are-mutable){.reference
        .internal}
    -   [9.2.2. Strings are
        Immutable](Mutability.html#strings-are-immutable){.reference
        .internal}
    -   [9.2.3. Tuples are
        Immutable](Mutability.html#tuples-are-immutable){.reference
        .internal}
-   [9.3. List Element Deletion](ListDeletion.html){.reference
    .internal}
-   [9.4. Objects and References](ObjectsandReferences.html){.reference
    .internal}
-   [9.5. Aliasing](Aliasing.html){.reference .internal}
-   [9.6. Cloning Lists](CloningLists.html){.reference .internal}
-   [9.7. Mutating Methods](MutatingMethods.html){.reference .internal}
    -   [9.7.1. List
        Methods](MutatingMethods.html#list-methods){.reference
        .internal}
-   [9.8. Append versus
    Concatenate](AppendversusConcatenate.html){.reference .internal}
-   [9.9. Non-mutating Methods on
    Strings](NonmutatingMethodsonStrings.html){.reference .internal}
-   [9.10. String Format Method](StringFormatting.html){.reference
    .internal}
-   [9.11. f-Strings](FStrings.html){.reference .internal}
-   [9.12. The Accumulator Pattern with
    Lists](TheAccumulatorPatternwithLists.html){.reference .internal}
-   [9.13. The Accumulator Pattern with
    Strings](TheAccumulatorPatternwithStrings.html){.reference
    .internal}
-   [9.14. 👩‍💻 Accumulator Pattern
    Strategies](WPAccumulatorPatternStrategies.html){.reference
    .internal}
    -   [9.14.1. When to Use
        it](WPAccumulatorPatternStrategies.html#when-to-use-it){.reference
        .internal}
    -   [9.14.2. Before Writing
        it](WPAccumulatorPatternStrategies.html#before-writing-it){.reference
        .internal}
    -   [9.14.3. Choosing Good Accumulator and Iterator Variable
        Names](WPAccumulatorPatternStrategies.html#choosing-good-accumulator-and-iterator-variable-names){.reference
        .internal}
-   [9.15. 👩‍💻 Don't Mutate A List That You Are Iterating
    Through](WPDontMutateAListYouIterateThrough.html){.reference
    .internal}
-   [9.16. Summary](Glossary.html){.reference .internal}
-   [9.17. Exercises](Exercises.html){.reference .internal}
    -   [9.17.1. Contributed
        Exercises](Exercises.html#contributed-exercises){.reference
        .internal}
-   [9.18. Chapter Assessment - List Methods](week4a1.html){.reference
    .internal}
    -   [9.18.1. Chapter Assessment - Aliases and
        References](week4a1.html#chapter-assessment-aliases-and-references){.reference
        .internal}
    -   [9.18.2. Chapter Assessment - Split and
        Join](week4a1.html#chapter-assessment-split-and-join){.reference
        .internal}
    -   [9.18.3. Chapter Assessment - For Loop
        Mechanics](week4a1.html#chapter-assessment-for-loop-mechanics){.reference
        .internal}
    -   [9.18.4. Chapter Assessment - Accumulator
        Pattern](week4a1.html#chapter-assessment-accumulator-pattern){.reference
        .internal}
    -   [9.18.5. Chapter Assessment - Problem
        Solving](week4a1.html#chapter-assessment-problem-solving){.reference
        .internal}
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

-   [[](../Conditionals/week3a1.html)]{#relations-prev}
-   [[](intro-SequenceMutation.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
