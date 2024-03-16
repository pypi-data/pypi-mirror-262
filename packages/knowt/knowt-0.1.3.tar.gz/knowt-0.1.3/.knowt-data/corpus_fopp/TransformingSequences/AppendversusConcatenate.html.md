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
        Problem](/runestone/default/reportabug?course=fopp&page=AppendversusConcatenate)
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
::: {#append-versus-concatenate .section}
[9.8. ]{.section-number}Append versus Concatenate[¶](#append-versus-concatenate "Permalink to this heading"){.headerlink}
=========================================================================================================================

The `append`{.docutils .literal .notranslate} method adds a new item to
the end of a list. It is also possible to add a new item to the end of a
list by using the concatenation operator. However, you need to be
careful.

Consider the following example. The original list has 3 integers. We
want to add the word "cat" to the end of the list.

::: {.runestone .explainer .ac_section}
::: {#clens8_7_1 component="activecode" question_label="9.8.1"}
::: {#clens8_7_1_question .ac_question}
:::
:::
:::

Here we have used `append`{.docutils .literal .notranslate} which simply
modifies the list. In order to use concatenation, we need to write an
assignment statement that uses the accumulator pattern:

::: {.highlight-default .notranslate}
::: {.highlight}
    origlist = origlist + ["cat"]
:::
:::

Note that the word "cat" needs to be placed in a list since the
concatenation operator needs two lists to do its work.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="9.8.2"}
::: {#clens8_7_2_question .ac_question}
:::

::: {#clens8_7_2 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 9.8.2 (clens8\_7\_2)]{.runestone_caption_text}
:::
:::

It is also important to realize that with append, the original list is
simply modified. On the other hand, with concatenation, an entirely new
list is created. This can be seen in the following codelens example
where\`\`newlist\`\` refers to a list which is a copy of the original
list, `origlist`{.docutils .literal .notranslate}, with the new item
"cat" added to the end. `origlist`{.docutils .literal .notranslate}
still contains the three values it did before the concatenation. This is
why the assignment operation is necessary as part of the accumulator
pattern.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="9.8.3"}
::: {#clens8_7_3_question .ac_question}
:::

::: {#clens8_7_3 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 9.8.3 (clens8\_7\_3)]{.runestone_caption_text}
:::
:::

This might be difficult to understand since these two lists appear to be
the same. In Python, every object has a unique identification tag.
Likewise, there is a built-in function that can be called on any object
to return its unique id. The function is appropriately called
`id`{.docutils .literal .notranslate} and takes a single parameter, the
object that you are interested in knowing about. You can see in the
example below that a real id is usually a very large integer value
(corresponding to an address in memory). In the textbook though the
number will likely be smaller.

::: {.highlight-python .notranslate}
::: {.highlight}
    >>> alist = [4, 5, 6]
    >>> id(alist)
    4300840544
    >>>
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac8_7_1 component="activecode" question_label="9.8.4"}
::: {#ac8_7_1_question .ac_question}
:::
:::
:::

Note how even though `newlist`{.docutils .literal .notranslate} and
`origlist`{.docutils .literal .notranslate} appear the same, they have
different identifiers.

We have previously described x += 1 as a shorthand for x = x + 1. With
lists, += is actually a little different. In particular, origlist +=
\["cat"\] appends "cat" to the end of the original list object. If there
is another alias for \`origlist, this can make a difference, as in the
code below. See if you can follow (or, better yet, predict, changes in
the reference diagram).

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="9.8.5"}
::: {#clens8_7_2a_question .ac_question}
:::

::: {#clens8_7_2a .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 9.8.5 (clens8\_7\_2a)]{.runestone_caption_text}
:::
:::

We can use append or concatenate repeatedly to create new objects. If we
had a string and wanted to make a new list, where each element in the
list is a character in the string, where do you think you should start?
In both cases, you'll need to first create a variable to store the new
object.

::: {.runestone .explainer .ac_section}
::: {#ac8_72 component="activecode" question_label="9.8.6"}
::: {#ac8_72_question .ac_question}
:::
:::
:::

Then, character by character, you can add to the empty list. The process
looks different if you concatentate as compared to using append.

::: {.runestone .explainer .ac_section}
::: {#ac8_7_3 component="activecode" question_label="9.8.7"}
::: {#ac8_7_3_question .ac_question}
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac8_7_4 component="activecode" question_label="9.8.8"}
::: {#ac8_7_4_question .ac_question}
:::
:::
:::

This might become tedious though, and difficult if the length of the
string is long. Can you think of a better way to do this?

**Check your understanding**

::: {.runestone}
-   [\[4,2,8,6,5,999\]]{#question8_7_1_opt_a}
-   You cannot concatenate a list with an integer.
-   [Error, you cannot concatenate a list with an
    integer.]{#question8_7_1_opt_b}
-   Yes, in order to perform concatenation you would need to write
    alist+\[999\]. You must have two lists.
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

-   [[](MutatingMethods.html)]{#relations-prev}
-   [[](NonmutatingMethodsonStrings.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
