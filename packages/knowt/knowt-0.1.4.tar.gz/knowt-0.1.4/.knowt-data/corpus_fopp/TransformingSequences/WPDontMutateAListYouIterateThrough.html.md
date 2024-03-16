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
        Problem](/runestone/default/reportabug?course=fopp&page=WPDontMutateAListYouIterateThrough)
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
::: {#dont-mutate-a-list-that-you-are-iterating-through .section}
[9.15. ]{.section-number}👩‍💻 Don't Mutate A List That You Are Iterating Through[¶](#dont-mutate-a-list-that-you-are-iterating-through "Permalink to this heading"){.headerlink}
===============================================================================================================================================================================

So far we've shown you how to iterate through a list:

::: {.runestone .explainer .ac_section}
::: {#ac8_12_1 component="activecode" question_label="9.15.1"}
::: {#ac8_12_1_question .ac_question}
:::
:::
:::

As well as accumulate a list by appending items:

::: {.runestone .explainer .ac_section}
::: {#ac8_12_2 component="activecode" question_label="9.15.2"}
::: {#ac8_12_2_question .ac_question}
:::
:::
:::

You may be tempted now to iterate through a list and accumulate some
data into it or delete data from it as you're traversing the list,
however that often becomes very confusing. In the following code we will
filter out all words that begin with P, B, or T.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="9.15.3"}
::: {#ac8_12_3_question .ac_question}
:::

::: {#ac8_12_3 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 9.15.3 (ac8\_12\_3)]{.runestone_caption_text}
:::
:::

In the code above, we iterated through the indexes, and deleted each
item that begins with a bad letter. However, we run into a problem
because as we delete content from the list, the list becomes shorter.
Eventually, we have an issue indexing on line 4. Try stepping through it
in codelens to see what's going on.

We can also try to accumulate a list that we're iterating through as
well. What do you think will happen here?

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="9.15.4"}
::: {#ac8_12_4_question .ac_question}
:::

::: {#ac8_12_4 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 9.15.4 (ac8\_12\_4)]{.runestone_caption_text}
:::
:::

Now try stepping through this code. When we come across a color that
begins with a vowel, that color is added to the end of the list. The
python interpreter doesn't make a copy of the sequence at the beginning
and iterate through that copy. It actually asks for the next item in the
sequence at the top of each iteration. But here we are adding a new item
to the end of the list before we get to the end of the list, so there's
always a next item. We would have an infinite loop.

To prevent the infinite loop, we've added a break once the list has six
strings in it. You'll learn about break and continue later in the book.

The main message here is that you should not mutate a list while you're
iterating through it! You'll get errors, infinite loops, or, worse,
semantic errors: your code may run and produce very surprising results.
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

-   [[](WPAccumulatorPatternStrategies.html)]{#relations-prev}
-   [[](Glossary.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
