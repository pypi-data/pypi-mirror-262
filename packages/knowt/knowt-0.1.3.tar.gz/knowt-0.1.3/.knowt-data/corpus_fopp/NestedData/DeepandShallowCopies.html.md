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
        Problem](/runestone/default/reportabug?course=fopp&page=DeepandShallowCopies)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [17.1 Introduction: Nested Data and Nested
        Iteration](ListswithComplexItems.html){.reference .internal}
    -   [17.2 Nested Dictionaries](NestedDictionaries.html){.reference
        .internal}
    -   [17.3 Processing JSON results](jsonlib.html){.reference
        .internal}
    -   [17.4 Nested Iteration](NestedIteration.html){.reference
        .internal}
    -   [17.5 👩‍💻 Structuring Nested
        Data](WPStructuringNestedData.html){.reference .internal}
    -   [17.6 Deep and Shallow
        Copies](DeepandShallowCopies.html){.reference .internal}
    -   [17.7 👩‍💻 Extracting from Nested
        Data](WPExtractFromNestedData.html){.reference .internal}
    -   [17.8 Exercises](Exercises.html){.reference .internal}
    -   [17.9 Chapter Assessment](ChapterAssessment.html){.reference
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

::: {#deep-and-shallow-copies .section}
[17.6. ]{.section-number}Deep and Shallow Copies[¶](#deep-and-shallow-copies "Permalink to this heading"){.headerlink}
======================================================================================================================

Earlier when we discussed cloning and aliasing lists we had mentioned
that simply cloning a list using \[:\] would take care of any issues
with having two lists unintentionally connected to each other. That was
definitely true for making shallow copies (copying a list at the highest
level), but as we get into nested data, and nested lists in particular,
the rules become a bit more complicated. We can have second-level
aliasing in these cases, which means we need to make deep copies.

When you copy a nested list, you do not also get copies of the internal
lists. This means that if you perform a mutation operation on one of the
original sublists, the copied version will also change. We can see this
happen in the following nested list, which only has two levels.

::: {.runestone .explainer .ac_section}
::: {#ac17_100_1 component="activecode" question_label="17.6.1"}
::: {#ac17_100_1_question .ac_question}
:::
:::
:::

Assuming that you don't want to have aliased lists inside of your nested
list, then you'll need to perform nested iteration.

::: {.runestone .explainer .ac_section}
::: {#ac17_100_2 component="activecode" question_label="17.6.2"}
::: {#ac17_100_2_question .ac_question}
:::
:::
:::

Or, equivalently, you could take advantage of the slice operator to do
the copying of the inner list.

::: {.runestone .explainer .ac_section}
::: {#ac17_100_2a component="activecode" question_label="17.6.3"}
::: {#ac17_100_2a_question .ac_question}
:::
:::
:::

This process above works fine when there are only two layers or levels
in a nested list. However, if we want to make a copy of a nested list
that has *more* than two levels, then we recommend using the
`copy`{.docutils .literal .notranslate} module. In the `copy`{.docutils
.literal .notranslate} module there is a method called
`deepcopy`{.docutils .literal .notranslate} that will take care of the
operation for you.

::: {.runestone .explainer .ac_section}
::: {#ac17_100_3 component="activecode" question_label="17.6.4"}
::: {#ac17_100_3_question .ac_question}
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

-   [[](WPStructuringNestedData.html)]{#relations-prev}
-   [[](WPExtractFromNestedData.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
