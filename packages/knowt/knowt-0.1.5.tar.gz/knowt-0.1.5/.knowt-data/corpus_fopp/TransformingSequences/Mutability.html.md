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
        Problem](/runestone/default/reportabug?course=fopp&page=Mutability)
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
[]{#mutability .target}

::: {#index-0 .section}
[]{#id1}

[9.2. ]{.section-number}Mutability[¶](#index-0 "Permalink to this heading"){.headerlink}
========================================================================================

Some Python collection types - strings and lists so far - are able to
change and some are not. If a type is able to change, then it is said to
be mutable. If the type is not able to change then it is said to be
immutable. This will be expanded below.

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#mutabilityvid .align-left .youtube-video component="youtube" video-height="315" question_label="9.2.1" video-width="560" video-videoid="fnSijYDKz3c" video-divid="mutabilityvid" video-start="0" video-end="-1"}
:::
:::

::: {#lists-are-mutable .section}
[9.2.1. ]{.section-number}Lists are Mutable[¶](#lists-are-mutable "Permalink to this heading"){.headerlink}
-----------------------------------------------------------------------------------------------------------

Unlike strings, lists are **mutable**. This means we can change an item
in a list by accessing it directly as part of the assignment statement.
Using the indexing operator (square brackets) on the left side of an
assignment, we can update one of the list items.

::: {.runestone .explainer .ac_section}
::: {#ac8_1_4 component="activecode" question_label="9.2.1.1"}
::: {#ac8_1_4_question .ac_question}
:::
:::
:::

An assignment to an element of a list is called **item assignment**.
Item assignment does not work for strings. Recall that strings are
immutable.

Here is the same example in codelens so that you can step through the
statements and see the changes to the list elements.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="9.2.1.2"}
::: {#clens8_1_1_question .ac_question}
:::

::: {#clens8_1_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 9.2.1.2 (clens8\_1\_1)]{.runestone_caption_text}
:::
:::

By combining assignment with the slice operator we can update several
elements at once.

::: {.runestone .explainer .ac_section}
::: {#ac8_1_5 component="activecode" question_label="9.2.1.3"}
::: {#ac8_1_5_question .ac_question}
:::
:::
:::

We can also remove elements from a list by assigning the empty list to
them.

::: {.runestone .explainer .ac_section}
::: {#ac8_1_6 component="activecode" question_label="9.2.1.4"}
::: {#ac8_1_6_question .ac_question}
:::
:::
:::

We can even insert elements into a list by squeezing them into an empty
slice at the desired location.

::: {.runestone .explainer .ac_section}
::: {#ac8_1_7 component="activecode" question_label="9.2.1.5"}
::: {#ac8_1_7_question .ac_question}
:::
:::
:::
:::

::: {#strings-are-immutable .section}
[9.2.2. ]{.section-number}Strings are Immutable[¶](#strings-are-immutable "Permalink to this heading"){.headerlink}
-------------------------------------------------------------------------------------------------------------------

One final thing that makes strings different from some other Python
collection types is that you are not allowed to modify the individual
characters in the collection. It is tempting to use the `[]`{.docutils
.literal .notranslate} operator on the left side of an assignment, with
the intention of changing a character in a string. For example, in the
following code, we would like to change the first letter of
`greeting`{.docutils .literal .notranslate}.

::: {.runestone .explainer .ac_section}
::: {#ac8_1_1 component="activecode" question_label="9.2.2.1"}
::: {#ac8_1_1_question .ac_question}
:::
:::
:::

Instead of producing the output `Jello, world!`{.docutils .literal
.notranslate}, this code produces the runtime error
`TypeError: 'str' object does not support item assignment`{.docutils
.literal .notranslate}.

Strings are **immutable**, which means you cannot change an existing
string. The best you can do is create a new string that is a variation
on the original.

::: {.runestone .explainer .ac_section}
::: {#ac8_1_2 component="activecode" question_label="9.2.2.2"}
::: {#ac8_1_2_question .ac_question}
:::
:::
:::

The solution here is to concatenate a new first letter onto a slice of
`greeting`{.docutils .literal .notranslate}. This operation has no
effect on the original string.

While it's possible to make up new variable names each time we make
changes to existing values, it could become difficult to keep track of
them all.

::: {.runestone .explainer .ac_section}
::: {#ac8_1_3 component="activecode" question_label="9.2.2.3"}
::: {#ac8_1_3_question .ac_question}
:::
:::
:::

The more that you change the string, the more difficult it is to come up
with a new variable to use. It's perfectly acceptable to re-assign the
value to the same variable name in this case.
:::

::: {#tuples-are-immutable .section}
[9.2.3. ]{.section-number}Tuples are Immutable[¶](#tuples-are-immutable "Permalink to this heading"){.headerlink}
-----------------------------------------------------------------------------------------------------------------

As with strings, if we try to use item assignment to modify one of the
elements of a tuple, we get an error. In fact, that's the key difference
between lists and tuples: tuples are like immutable lists. None of the
operations on lists that mutate them are available for tuples. Once a
tuple is created, it can't be changed.

::: {.highlight-python .notranslate}
::: {.highlight}
    julia[0] = 'X'  # TypeError: 'tuple' object does not support item assignment
:::
:::

**Check your understanding**

::: {.runestone}
-   [\[4,2,True,8,6,5\]]{#question8_1_1_opt_a}
-   Item assignment does not insert the new item into the list.
-   [\[4,2,True,6,5\]]{#question8_1_1_opt_b}
-   Yes, the value True is placed in the list at index 2. It replaces 8.
-   [Error, it is illegal to assign]{#question8_1_1_opt_c}
-   Item assignment is allowed with lists. Lists are mutable.
:::

::: {.runestone}
-   [Ball]{#question8_1_2_opt_a}
-   Assignment is not allowed with strings.
-   [Call]{#question8_1_2_opt_b}
-   Assignment is not allowed with strings.
-   [Error]{#question8_1_2_opt_c}
-   Yes, strings are immutable.
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

-   [[](intro-SequenceMutation.html)]{#relations-prev}
-   [[](ListDeletion.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
