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
        Problem](/runestone/default/reportabug?course=fopp&page=WPExtractFromNestedData)
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
::: {#extracting-from-nested-data .section}
[]{#debug-nested-chap}

[17.7. ]{.section-number}👩‍💻 Extracting from Nested Data[¶](#extracting-from-nested-data "Permalink to this heading"){.headerlink}
==================================================================================================================================

A common problem, especially when dealing with data returned from a web
site, is to extract certain elements from deep inside a nested data
structure. In principle, there's nothing more difficult about pulling
something out from deep inside a nested data structure: with lists, you
use \[\] to index or a for loop to get them them all; with dictionaries,
you get the value associated with a particular key using \[\] or iterate
through all the keys, accessing the value for each. But it's easy to get
lost in the process and think you've extracted something different than
you really have. Because of this, we have created a usable technique to
help you during the debugging process.

Follow the system described below and you will have success with
extracting nested data. The process involves the following steps:

1.  Understand the nested data object.

2.  Extract one object at the next level down.

3.  Repeat the process with the extracted object

Understand. Extract. Repeat.

To illustrate this, we will walk through extracting information from
data formatted in a way that it's return by the Twitter API. This nested
dictionary results from querying Twitter, asking for three tweets
matching "University of Michigan". As you'll see, it's quite a daunting
data structure, even when printed with nice indentation as it's shown
below.

::: {.runestone .explainer .ac_section}
::: {#ac300_1_1 component="activecode" question_label="17.7.1"}
::: {#ac300_1_1_question .ac_question}
:::
:::
:::

::: {#understand .section}
[17.7.1. ]{.section-number}Understand[¶](#understand "Permalink to this heading"){.headerlink}
----------------------------------------------------------------------------------------------

At any level of the extraction process, the first task is to make sure
you understand the current object you have extracted. There are few
options here.

1.  Print the entire object. If it's small enough, you may be able to
    make sense of the printout directly. If it's a little bit larger,
    you may find it helpful to "pretty-print" it, with indentation
    showing the level of nesting of the data. We don't have a way to
    pretty-print in our online browser-based environment, but if you're
    running code with a full Python interpreter, you can use the dumps
    function in the json module. For example:

::: {.highlight-python .notranslate}
::: {.highlight}
    import json
    print(json.dumps(res, indent=2))
:::
:::

2.  If printing the entire object gives you something that's too
    unwieldy, you have other options for making sense of it.

    -   Copy and paste it to a site like <https://jsoneditoronline.org/>
        which will let you explore and collapse levels

    -   Print the type of the object.

    -   

        If it's a dictionary:

        :   -   print the keys

    -   

        If it's a list:

        :   -   print its length

            -   print the type of the first item

            -   print the first item if it's of manageable size

::: {.runestone .explainer .ac_section}
::: {#ac300_1_2 component="activecode" question_label="17.7.1.1"}
::: {#ac300_1_2_question .ac_question}
:::
:::
:::
:::

::: {#extract .section}
[17.7.2. ]{.section-number}Extract[¶](#extract "Permalink to this heading"){.headerlink}
----------------------------------------------------------------------------------------

In the extraction phase, you will be diving one level deeper into the
nested data.

1.  If it's a dictionary, figure out which key has the value you're
    looking for, and get its value. For example:
    `res2 = res['statuses']`{.docutils .literal .notranslate}

2.  If it's a list, you will typically be wanting to do something with
    each of the items (e.g., extracting something from each, and
    accumulating them in a list). For that you'll want a for loop, such
    as `for res2 in res`{.docutils .literal .notranslate}. During your
    exploration phase, however, it will be easier to debug things if you
    work with just one item. One trick for doing that is to iterate over
    a slice of the list containing just one item. For example,
    `for res2 in res[:1]`{.docutils .literal .notranslate}.

::: {.runestone .explainer .ac_section}
::: {#ac300_1_3 component="activecode" question_label="17.7.2.1"}
::: {#ac300_1_3_question .ac_question}
:::
:::
:::
:::

::: {#repeat .section}
[17.7.3. ]{.section-number}Repeat[¶](#repeat "Permalink to this heading"){.headerlink}
--------------------------------------------------------------------------------------

Now you'll repeat the Understand and Extract processes at the next
level.

::: {#level-2 .section}
### [17.7.3.1. ]{.section-number}Level 2[¶](#level-2 "Permalink to this heading"){.headerlink}

First understand.

::: {.runestone .explainer .ac_section}
::: {#ac300_1_4 component="activecode" question_label="17.7.3.1.1"}
::: {#ac300_1_4_question .ac_question}
:::
:::
:::

It's a list, with three items, so it's a good guess that each item
represents one tweet.

Now extract. Since it's a list, we'll want to work with each item, but
to keep things manageable for now, let's use the trick for just looking
at the first item. Later we'll switch to processing all the items.

::: {.runestone .explainer .ac_section}
::: {#ac300_1_5 component="activecode" question_label="17.7.3.1.2"}
::: {#ac300_1_5_question .ac_question}
:::
:::
:::
:::

::: {#level-3 .section}
### [17.7.3.2. ]{.section-number}Level 3[¶](#level-3 "Permalink to this heading"){.headerlink}

First understand.

::: {.runestone .explainer .ac_section}
::: {#ac300_1_6 component="activecode" question_label="17.7.3.2.1"}
::: {#ac300_1_6_question .ac_question}
:::
:::
:::

Then extract. Let's pull out the information about who sent each of the
tweets. Probably that's the value associated with the 'user' key.

::: {.runestone .explainer .ac_section}
::: {#ac300_1_7 component="activecode" question_label="17.7.3.2.2"}
::: {#ac300_1_7_question .ac_question}
:::
:::
:::

Now repeat.
:::

::: {#level-4 .section}
### [17.7.3.3. ]{.section-number}Level 4[¶](#level-4 "Permalink to this heading"){.headerlink}

Understand.

::: {.runestone .explainer .ac_section}
::: {#ac300_1_8 component="activecode" question_label="17.7.3.3.1"}
::: {#ac300_1_8_question .ac_question}
:::
:::
:::

Extract. Let's print out the user's screen name and when their account
was created.

::: {.runestone .explainer .ac_section}
::: {#ac300_1_9 component="activecode" question_label="17.7.3.3.2"}
::: {#ac300_1_9_question .ac_question}
:::
:::
:::

Now, we may want to go back and have it extract for all the items rather
than only the first item in res2.

::: {.runestone .explainer .ac_section}
::: {#ac300_1_10 component="activecode" question_label="17.7.3.3.3"}
::: {#ac300_1_10_question .ac_question}
:::
:::
:::
:::

::: {#reflections .section}
### [17.7.3.4. ]{.section-number}Reflections[¶](#reflections "Permalink to this heading"){.headerlink}

Notice that each time we descend a level in a dictionary, we have a \[\]
picking out a key. Each time we look inside a list, we will have a for
loop. If there are lists at multiple levels, we will have nested for
loops.

Once you've figured out how to extract everything you want, you *may*
choose to collapse things with multiple extractions in a single
expression. For example, we could have this shorter version.

::: {.runestone .explainer .ac_section}
::: {#ac300_1_11 component="activecode" question_label="17.7.3.4.1"}
::: {#ac300_1_11_question .ac_question}
:::
:::
:::

Even with this compact code, we can still count off how many levels of
nesting we have extracted from, in this case four. res\['statuses'\]
says we have descended one level (in a dictionary). for res3 in... says
we have descended another level (in a list). \['user'\] is descending
one more level, and \['screen\_name'\] is descending one more level.
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

-   [[](DeepandShallowCopies.html)]{#relations-prev}
-   [[](Exercises.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
