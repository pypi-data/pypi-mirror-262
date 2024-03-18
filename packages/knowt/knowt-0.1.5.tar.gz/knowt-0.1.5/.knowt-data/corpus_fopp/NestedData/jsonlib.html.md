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
        Problem](/runestone/default/reportabug?course=fopp&page=jsonlib)
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
::: {#processing-json-results .section}
[17.3. ]{.section-number}Processing JSON results[¶](#processing-json-results "Permalink to this heading"){.headerlink}
======================================================================================================================

JSON stands for JavaScript Object Notation. It looks a lot like the
representation of nested dictionaries and lists in python when we write
them out as literals in a program, but with a few small differences
(e.g., the word null instead of None). When your program receives a
JSON-formatted string, generally you will want to convert it into a
python object, a list or a dictionary.

Again, python provides a module for doing this. The module is called
json. We will be using two functions in this module, `loads`{.docutils
.literal .notranslate} and `dumps`{.docutils .literal .notranslate}.

`json.loads()`{.docutils .literal .notranslate} takes a string as input
and produces a python object (a dictionary or a list) as output.

Consider, for example, some data that we might get from Apple's iTunes,
in the JSON format:

::: {.runestone .explainer .ac_section}
::: {#ac17_3_1 component="activecode" question_label="17.3.1"}
::: {#ac17_3_1_question .ac_question}
:::
:::
:::

The other function we will use is `dumps`{.docutils .literal
.notranslate}. It does the inverse of `loads`{.docutils .literal
.notranslate}. It takes a python object, typically a dictionary or a
list, and returns a string, in JSON format. It has a few other
parameters. Two useful parameters are sort\_keys and indent. When the
value True is passed for the sort\_keys parameter, the keys of
dictionaries are output in alphabetic order with their values. The
indent parameter expects an integer. When it is provided, dumps
generates a string suitable for displaying to people, with newlines and
indentation for nested lists or dictionaries. For example, the following
function uses json.dumps to make a human-readable printout of a nested
data structure.

::: {.runestone .explainer .ac_section}
::: {#ac17_3_2 component="activecode" question_label="17.3.2"}
::: {#ac17_3_2_question .ac_question}
:::
:::
:::

**Check Your Understanding**

::: {.runestone}
-   [json.loads(d)]{#question17_3_1_opt_a}
-   loads turns a json-formatted string into a list or dictionary
-   [json.dumps(d)]{#question17_3_1_opt_b}
-   dumps turns a list or dictionary into a json-formatted string
-   [d.json()]{#question17_3_1_opt_c}
-   .json() tries to invoke the json method, but that method is not
    defined for dictionaries
:::

::: {.runestone}
-   [entertainment.json()]{#question17_3_2_opt_a}
-   The .json() method is not defined for strings.
-   [json.dumps(entertainment)]{#question17_3_2_opt_b}
-   dumps (dump to string) turns a list or dictionary into a
    json-formatted string
-   [json.loads(entertainment)]{#question17_3_2_opt_c}
-   loads (load from string) turns a json-formatted string into a list
    or dictionary
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

-   [[](NestedDictionaries.html)]{#relations-prev}
-   [[](NestedIteration.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
