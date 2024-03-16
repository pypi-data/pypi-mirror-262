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
        Problem](/runestone/default/reportabug?course=fopp&page=MultipleInheritance)
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

::: {#multiple-inheritance .section}
[22.5. ]{.section-number}Multiple inheritance[¶](#multiple-inheritance "Permalink to this heading"){.headerlink}
================================================================================================================

In Python, a class can inherit from more than one parent class. This is
called **multiple inheritance**. Multiple inheritance can be useful when
you want to create a class that is a combination of multiple classes.
For example, suppose we have a class `Swimmer`{.docutils .literal
.notranslate} (which represents all of the aspects of a character that
can swim) and a class `Flyer`{.docutils .literal .notranslate} (for all
of the aspects of a character that relate to flying). We can create a
class `Goose`{.docutils .literal .notranslate} that inherits from both
`Swimmer`{.docutils .literal .notranslate} and `Flyer`{.docutils
.literal .notranslate} by putting both these class names in parentheses:
`class Goose(Swimmer, Flyer)`{.docutils .literal .notranslate}. This
class will have all the methods and attributes of both
`Swimmer`{.docutils .literal .notranslate} and `Flyer`{.docutils
.literal .notranslate}:

::: {.runestone .explainer .ac_section}
::: {#multiple_inheritance_example component="activecode" question_label="22.5.1"}
::: {#multiple_inheritance_example_question .ac_question}
:::
:::
:::

Multiple inheritance can improve our ability to re-use code and classes.
It can be particularly useful if the classes represent "features" that
we can selectively apply to subclasses. However, **it's generally a good
rule to avoid multiple inheritance unless it provides a clear and
significant benefit**. Always consider simpler alternatives, such as
composition (using an instance of one class as an instance variable
inside of another class) or single inheritance, before turning to
multiple inheritance.
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

-   [[](InvokingSuperMethods.html)]{#relations-prev}
-   [[](TamagotchiRevisited.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
