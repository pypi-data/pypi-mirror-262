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
        Problem](/runestone/default/reportabug?course=fopp&page=WPCodeSectionataTime)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [21.1 Building A Program: A
        Strategy](TheStrategy.html){.reference .internal}
    -   [21.2 👩‍💻 Sketch an Outline](WPSketchanOutline.html){.reference
        .internal}
    -   [21.3 👩‍💻 Code one section at a
        time](WPCodeSectionataTime.html){.reference .internal}
    -   [21.4 👩‍💻 Clean Up](WPCleanCode.html){.reference .internal}
    -   [21.5 Exercises](Exercises.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#code-one-section-at-a-time .section}
[21.3. ]{.section-number}👩‍💻 Code one section at a time[¶](#code-one-section-at-a-time "Permalink to this heading"){.headerlink}
================================================================================================================================

As a reminder, this is our prompt:

*Build a program that replicates a physical dictionary that you might
use. The program should that take five different input from the user.
Each input will have two words and we will build a dictionary where the
words are the keys and values*.

We'll start to build up the sections one at a time now! First, we need
to pick a name for the dictionary. We'll try to pick a clear name for
each of these variables

::: {.runestone .explainer .ac_section}
::: {#ac500_3_1 component="activecode" question_label="21.3.1"}
::: {#ac500_3_1_question .ac_question}
:::
:::
:::

We picked the variable name `user_dictionary`{.docutils .literal
.notranslate} because it will be a dictionary that is created by a user.
Other names could be appropriate as well! Though it may seem
unnecessary, we'll add a print statement to remind ourself that
`user_dictionary`{.docutils .literal .notranslate} is empty.

Next we'll build up the for loop!

::: {.runestone .explainer .ac_section}
::: {#ac500_3_2 component="activecode" question_label="21.3.2"}
::: {#ac500_3_2_question .ac_question}
:::
:::
:::

If we want to make sure that the for loop is iterating five times then
we can add these print statements to execute so that we can track the
progress of the program.

Next, we'lll get the input from the user!

::: {.runestone .explainer .ac_section}
::: {#ac500_3_3 component="activecode" question_label="21.3.3"}
::: {#ac500_3_3_question .ac_question}
:::
:::
:::

Now we'll want to print out the response. We're expecting that it should
be as string, so we should be able to add it to the print statement with
other strings without any issue. If there is an issue, then something
could be going wrong with how we are getting input from the user.

Now, we can separate the words so that we have our key and value to add
to the dictionary!

::: {.runestone .explainer .ac_section}
::: {#ac500_3_4 component="activecode" question_label="21.3.4"}
::: {#ac500_3_4_question .ac_question}
:::
:::
:::

Here we know that `response`{.docutils .literal .notranslate} is a
string that contains two words. We can use the split method to separate
the words, which will give us a list. The first word will be the key and
the second word will be the value, so we can use indexing to access that
information.

::: {.runestone .explainer .ac_section}
::: {#ac500_3_5 component="activecode" question_label="21.3.5"}
::: {#ac500_3_5_question .ac_question}
:::
:::
:::

Finally, we add code to add the key and value pair into a dictionary. We
can print out the final result of the dictionary once the for loop is
over so that we can determine if it has been done correctly.
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

-   [[](WPSketchanOutline.html)]{#relations-prev}
-   [[](WPCleanCode.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
