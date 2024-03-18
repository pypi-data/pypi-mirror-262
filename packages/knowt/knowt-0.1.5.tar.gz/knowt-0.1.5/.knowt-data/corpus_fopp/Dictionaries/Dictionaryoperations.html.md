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
        Problem](/runestone/default/reportabug?course=fopp&page=Dictionaryoperations)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [11.1 Introduction:
        Dictionaries](intro-DictionaryGoals.html){.reference .internal}
    -   [11.2 Getting Started with
        Dictionaries](intro-Dictionaries.html){.reference .internal}
    -   [11.3 Dictionary
        operations](Dictionaryoperations.html){.reference .internal}
    -   [11.4 Dictionary methods](Dictionarymethods.html){.reference
        .internal}
    -   [11.5 Aliasing and copying](Aliasingandcopying.html){.reference
        .internal}
    -   [11.6 Introduction: Accumulating Multiple Results In a
        Dictionary](intro-AccumulatingMultipleResultsInaDictionary.html){.reference
        .internal}
    -   [11.7 Accumulating Results From a
        Dictionary](AccumulatingResultsFromaDictionary.html){.reference
        .internal}
    -   [11.8 Accumulating the Best
        Key](AccumulatingtheBestKey.html){.reference .internal}
    -   [11.9 👩‍💻 When to use a
        dictionary](WPChoosingDictionaries.html){.reference .internal}
    -   [11.10 Glossary](Glossary.html){.reference .internal}
    -   [11.11 Exercises](Exercises.html){.reference .internal}
    -   [11.12 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#dictionary-operations .section}
[]{#index-0}

[11.3. ]{.section-number}Dictionary operations[¶](#dictionary-operations "Permalink to this heading"){.headerlink}
==================================================================================================================

The `del`{.docutils .literal .notranslate} statement removes a key-value
pair from a dictionary. For example, the following dictionary contains
the names of various fruits and the number of each fruit in stock. If
someone buys all of the pears, we can remove the entry from the
dictionary.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="11.3.1"}
::: {#clens10_2_1_question .ac_question}
:::

::: {#clens10_2_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 11.3.1 (clens10\_2\_1)]{.runestone_caption_text}
:::
:::

Dictionaries are mutable, as the delete operation above indicates. As
we've seen before with lists, this means that the dictionary can be
modified by referencing an association on the left hand side of the
assignment statement. In the previous example, instead of deleting the
entry for `pears`{.docutils .literal .notranslate}, we could have set
the inventory to `0`{.docutils .literal .notranslate}.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="11.3.2"}
::: {#clens10_2_2_question .ac_question}
:::

::: {#clens10_2_2 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 11.3.2 (clens10\_2\_2)]{.runestone_caption_text}
:::
:::

::: {.admonition .note}
Note

Setting the value associated with `pears`{.docutils .literal
.notranslate} to 0 has a different effect than removing the key-value
pair entirely with `del`{.docutils .literal .notranslate}. Try printout
out the two dictionaries in the examples above.
:::

Similarily, a new shipment of 200 bananas arriving could be handled like
this. Notice that there are now 512 bananas--- the dictionary has been
modified. Note also that the `len`{.docutils .literal .notranslate}
function also works on dictionaries. It returns the number of key-value
pairs.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="11.3.3"}
::: {#clens10_2_3_question .ac_question}
:::

::: {#clens10_2_3 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 11.3.3 (clens10\_2\_3)]{.runestone_caption_text}
:::
:::

Notice that there are now 512 bananas---the dictionary has been
modified. Note also that the `len`{.docutils .literal .notranslate}
function also works on dictionaries. It returns the number of key-value
pairs.

**Check your understanding**

::: {.runestone}
-   [12]{#question10_2_1_opt_a}
-   12 is associated with the key cat.
-   [0]{#question10_2_1_opt_b}
-   The key mouse will be associated with the sum of the two values.
-   [18]{#question10_2_1_opt_c}
-   Yes, add the value for cat and the value for dog (12 + 6) and create
    a new entry for mouse.
-   [Error, there is no entry with mouse as the
    key.]{#question10_2_1_opt_d}
-   Since the new key is introduced on the left hand side of the
    assignment statement, a new key-value pair is added to the
    dictionary.
:::

::: {.runestone .explainer .ac_section}
::: {#ac10_2_1 component="activecode" question_label="11.3.5"}
::: {#ac10_2_1_question .ac_question}
**2.** Update the value for "Phelps" in the dictionary
`swimmers`{.docutils .literal .notranslate} to include his medals from
the Rio Olympics by adding 5 to the current value (Phelps will now have
28 total medals). Do not rewrite the dictionary.
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

-   [[](intro-Dictionaries.html)]{#relations-prev}
-   [[](Dictionarymethods.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
