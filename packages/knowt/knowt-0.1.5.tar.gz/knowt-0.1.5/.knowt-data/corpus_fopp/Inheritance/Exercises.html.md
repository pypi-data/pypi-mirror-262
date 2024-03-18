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
        Problem](/runestone/default/reportabug?course=fopp&page=Exercises)
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
::: {#exercises .section}
[22.7. ]{.section-number}Exercises[¶](#exercises "Permalink to this heading"){.headerlink}
==========================================================================================

For exercises, you can expand the Tamagotchi game even further. Try
these out.

Here's *all* the code we just saw for our new and improved game, with a
few additions. You can run this and play the game again.

1.  ::: {#q1 .alert .alert-warning component="tabbedStuff"}
    ::: {component="tab" tabname="Question"}
    ::: {.runestone .explainer .ac_section}
    ::: {#tamagotchi_exercises component="activecode" question_label="22.7.1"}
    ::: {#tamagotchi_exercises_question .ac_question}
    1.  Change the above code to allow you to adopt a Tiger pet (that
        you're about to create). HINT: look at the `whichtype`{.docutils
        .literal .notranslate} function, and think about what's
        happening in the code for that function.

    2.  Now, modify the code to define a new class, `Tiger`{.docutils
        .literal .notranslate}. The `Tiger`{.docutils .literal
        .notranslate} class should inherit from the `Cat`{.docutils
        .literal .notranslate} class, but its default meow count should
        be `5`{.docutils .literal .notranslate}, not `3`{.docutils
        .literal .notranslate}, and it should have an extra instance
        method, `roar`{.docutils .literal .notranslate}, that prints out
        the string `ROOOOOAR!`{.docutils .literal .notranslate}.

    3.  Next, modify the code so that when the `hi`{.docutils .literal
        .notranslate} method is called for the `Tiger`{.docutils
        .literal .notranslate} class, the `roar`{.docutils .literal
        .notranslate} method is called. HINT: You'll have to call one
        instance method inside another, and you'll have to redefine a
        method for the `Tiger`{.docutils .literal .notranslate} class.
        See the **overriding methods** section.

    4.  Now, modify the code to define another new class,
        `Retriever`{.docutils .literal .notranslate}. This class should
        inherit from `Lab`{.docutils .literal .notranslate}. It should
        be exactly like `Lab`{.docutils .literal .notranslate}, except
        instead of printing just `I found the tennis ball!`{.docutils
        .literal .notranslate} when the `fetch`{.docutils .literal
        .notranslate} method is called, it should say
        `I found the tennis ball! I can fetch anything!`{.docutils
        .literal .notranslate}.

    5.  Add your own new pets and modifications as you like -- remember,
        to use them in the game, you'll also have to alter the
        `whichtype`{.docutils .literal .notranslate} function so they
        can be used in game play. Otherwise, you'll have different
        classes that may work just fine, but you won't see the effects
        in the game, since the code that actually makes the game play is
        found in the second half of the provided code (look for the
        `while`{.docutils .literal .notranslate} loop!).
    :::
    :::
    :::
    :::
    :::

::: {#contributed-exercises .section}
[22.7.1. ]{.section-number}Contributed Exercises[¶](#contributed-exercises "Permalink to this heading"){.headerlink}
--------------------------------------------------------------------------------------------------------------------
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

-   [[](TamagotchiRevisited.html)]{#relations-prev}
-   [[](ChapterAssessment.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
