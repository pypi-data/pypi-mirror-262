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
        Problem](/runestone/default/reportabug?course=fopp&page=ObjectsandReferences)
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

::: {#objects-and-references .section}
[]{#index-0}

[9.4. ]{.section-number}Objects and References[¶](#objects-and-references "Permalink to this heading"){.headerlink}
===================================================================================================================

If we execute these assignment statements,

::: {.highlight-python .notranslate}
::: {.highlight}
    a = "banana"
    b = "banana"
:::
:::

we know that `a`{.docutils .literal .notranslate} and `b`{.docutils
.literal .notranslate} will refer to a string with the letters
`"banana"`{.docutils .literal .notranslate}. But we don't know yet
whether they point to the *same* string.

There are two possible ways the Python interpreter could arrange its
internal states:

![List illustration](../_images/refdiag1.png)

or

![List illustration](../_images/refdiag2.png)

In one case, `a`{.docutils .literal .notranslate} and `b`{.docutils
.literal .notranslate} refer to two different string objects that have
the same value. In the second case, they refer to the same object.
Remember that an object is something a variable can refer to.

We can test whether two names refer to the same object using the *is*
operator. The *is* operator will return true if the two references are
to the same object. In other words, the references are the same. Try our
example from above.

::: {.runestone .explainer .ac_section}
::: {#ac8_3_1 component="activecode" question_label="9.4.1"}
::: {#ac8_3_1_question .ac_question}
:::
:::
:::

The answer is `True`{.docutils .literal .notranslate}. This tells us
that both `a`{.docutils .literal .notranslate} and `b`{.docutils
.literal .notranslate} refer to the same object, and that it is the
second of the two reference diagrams that describes the relationship.
Python assigns every object a unique id and when we ask
`a is b`{.docutils .literal .notranslate} what python is really doing is
checking to see if id(a) == id(b).

::: {.runestone .explainer .ac_section}
::: {#ac8_3_2 component="activecode" question_label="9.4.2"}
::: {#ac8_3_2_question .ac_question}
:::
:::
:::

Since strings are *immutable*, the Python interpreter often optimizes
resources by making two names that refer to the same string value refer
to the same object. You shouldn't count on this (that is, use
`==`{.docutils .literal .notranslate} to compare strings, not
`is`{.docutils .literal .notranslate}), but don't be surprised if you
find that two variables,each bound to the string "banana", have the same
id..

This is not the case with lists, which never share an id just because
they have the same contents. Consider the following example. Here,
`a`{.docutils .literal .notranslate} and `b`{.docutils .literal
.notranslate} refer to two different lists, each of which happens to
have the same element values. They need to have different ids so that
mutations of list `a`{.docutils .literal .notranslate} do not affect
list `b`{.docutils .literal .notranslate}.

::: {.runestone .explainer .ac_section}
::: {#ac8_3_3 component="activecode" question_label="9.4.3"}
::: {#ac8_3_3_question .ac_question}
:::
:::
:::

The reference diagram for this example looks like this:

![Reference diagram for equal different lists](../_images/refdiag3.png)

`a`{.docutils .literal .notranslate} and `b`{.docutils .literal
.notranslate} have equivalent values but do not refer to the same
object. Because their contents are equivalent, a==b evaluates to True;
because they are not the same object, a is b evaluates to False.
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

-   [[](ListDeletion.html)]{#relations-prev}
-   [[](Aliasing.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
