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
        Problem](/runestone/default/reportabug?course=fopp&page=ChapterAssessment)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [22.1 Introduction: Class Inheritance](intro.html){.reference
        .internal}
    -   [22.2 Inheriting Variables and
        Methods](inheritVarsAndMethods.html){.reference .internal}
    -   [22.3 Overriding Methods](OverrideMethods.html){.reference
        .internal}
    -   [22.4 Invoking the Parent Class's
        Method](InvokingSuperMethods.html){.reference .internal}
    -   [22.5 Multiple inheritance](MultipleInheritance.html){.reference
        .internal}
    -   [22.6 Tamagotchi Revisited](TamagotchiRevisited.html){.reference
        .internal}
    -   [22.7 Exercises](Exercises.html){.reference .internal}
    -   [22.8 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
    -   [22.9 Project - Wheel of Python](chapterProject.html){.reference
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

::: {#chapter-assessment .section}
[22.8. ]{.section-number}Chapter Assessment[¶](#chapter-assessment "Permalink to this heading"){.headerlink}
============================================================================================================

::: {.runestone .explainer .ac_section}
::: {#ee_inheritance_01 component="activecode" question_label="22.8.1"}
::: {#ee_inheritance_01_question .ac_question}
The class, `Pokemon`{.docutils .literal .notranslate}, is provided below
and describes a Pokemon and its leveling and evolving characteristics.
An instance of the class is one pokemon that you create.

`Grass_Pokemon`{.docutils .literal .notranslate} is a subclass that
inherits from `Pokemon`{.docutils .literal .notranslate} but changes
some aspects, for instance, the boost values are different.

For the subclass `Grass_Pokemon`{.docutils .literal .notranslate}, add
another method called `action`{.docutils .literal .notranslate} that
returns the string
`"[name of pokemon] knows a lot of different moves!"`{.docutils .literal
.notranslate}. Create an instance of this class with the
`name`{.docutils .literal .notranslate} as `"Belle"`{.docutils .literal
.notranslate}. Assign this instance to the variable `p1`{.docutils
.literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ee_inheritance_02 component="activecode" question_label="22.8.2"}
::: {#ee_inheritance_02_question .ac_question}
Modify the `Grass_Pokemon`{.docutils .literal .notranslate} subclass so
that the attack strength for `Grass_Pokemon`{.docutils .literal
.notranslate} instances does not change until they reach level 10. At
level 10 and up, their attack strength should increase by the
`attack_boost`{.docutils .literal .notranslate} amount when they are
trained.

To test, create an instance of the class with the name as
`"Bulby"`{.docutils .literal .notranslate}. Assign the instance to the
variable `p2`{.docutils .literal .notranslate}. Create another instance
of the `Grass_Pokemon`{.docutils .literal .notranslate} class with the
name set to `"Pika"`{.docutils .literal .notranslate} and assign that
instance to the variable `p3`{.docutils .literal .notranslate}. Then,
use `Grass_Pokemon`{.docutils .literal .notranslate} methods to train
the `p3`{.docutils .literal .notranslate} `Grass_Pokemon`{.docutils
.literal .notranslate} instance until it reaches at least level 10.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ee_inheritance_05 component="activecode" question_label="22.8.3"}
::: {#ee_inheritance_05_question .ac_question}
Along with the `Pokemon`{.docutils .literal .notranslate} parent class,
we have also provided several subclasses. Write another method in the
parent class that will be inherited by the subclasses. Call it
`opponent`{.docutils .literal .notranslate}. It should return which type
of pokemon the current type is weak and strong against, as a tuple.

-   **Grass** is weak against *Fire* and strong against *Water*

-   **Ghost** is weak against *Dark* and strong against *Psychic*

-   **Fire** is weak against *Water* and strong against *Grass*

-   **Flying** is weak against *Electric* and strong against *Fighting*

For example, if the `p_type`{.docutils .literal .notranslate} of the
subclass is `'Grass'`{.docutils .literal .notranslate},
`.opponent()`{.docutils .literal .notranslate} should return the tuple
`('Fire', 'Water')`{.docutils .literal .notranslate}
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

-   [[](Exercises.html)]{#relations-prev}
-   [[](chapterProject.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
