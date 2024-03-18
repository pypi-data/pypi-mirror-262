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
    -   [18.1 Introduction: Test Cases](intro-TestCases.html){.reference
        .internal}
    -   [18.2 Checking Assumptions About Data
        Types](TestingTypes.html){.reference .internal}
    -   [18.3 Checking Other
        Assumptions](CheckingOtherAssumptions.html){.reference
        .internal}
    -   [18.4 Testing Conditionals](TestingConditionals.html){.reference
        .internal}
    -   [18.5 Testing Loops](TestingLoops.html){.reference .internal}
    -   [18.6 Writing Test Cases for
        Functions](Testingfunctions.html){.reference .internal}
    -   [18.7 Testing Optional
        Parameters](TestingOptionalParameters.html){.reference
        .internal}
    -   [18.8 👩‍💻 Test Driven
        Development](WPProgramDevelopment.html){.reference .internal}
    -   [18.9 Glossary](Glossary.html){.reference .internal}
    -   [18.10 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
    -   [18.11 Exercises](Exercises.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#chapter-assessment .section}
[18.10. ]{.section-number}Chapter Assessment[¶](#chapter-assessment "Permalink to this heading"){.headerlink}
=============================================================================================================

::: {.runestone .explainer .ac_section}
::: {#ac_19_4_1 component="activecode" question_label="18.10.1"}
::: {#ac_19_4_1_question .ac_question}
The function mySum is supposed to return the sum of a list of numbers
(and 0 if that list is empty), but it has one or more errors in it. Use
this space to write test cases to determine what errors there are. You
will be using this information to answer the next set of multiple choice
questions.
:::
:::
:::

::: {.runestone}
-   [an empty list]{#mc_19_4_1_opt_a}
-   Correct, 0 is not returned if the function is given an empty list.
-   [a list with one item]{#mc_19_4_1_opt_b}
-   Incorrect, a list with one item returns the correct value.
-   [a list with more than one item]{#mc_19_4_1_opt_c}
-   Correct, a list with more than one item does not provide the correct
    response.
:::

::: {.runestone}
-   [Yes]{#mc_19_4_2_opt_a}
-   Incorrect. Though it is possible that the function could have more
    issues, we can\'t tell if other cases would fail (such as combining
    integers and floats) due to the current issues.
-   [No]{#mc_19_4_2_opt_b}
-   Correct. At the moment we can\'t tell if other cases would fail
    (such as combining integers and floats), but it is possible that the
    function could have more issues once the current issues are fixed.
:::

::: {.runestone .explainer .ac_section}
::: {#ac_19_4_2 component="activecode" question_label="18.10.4"}
::: {#ac_19_4_2_question .ac_question}

The class Student is supposed to accept two arguments in its constructor:

:   1.  A name string

    2.  An optional integer representing the number of years the student
        has been at Michigan (default:1)

Every student has three instance variables:

:   1.  self.name (set to the name provided)

    2.  self.years\_UM (set to the number of years the student has been
        at Michigan)

    3.  self.knowledge (initialized to 0)

There are three methods:

:   -   .study() should increase self.knowledge by 1 and return None

    -   .getKnowledge() should return the value of self.knowledge

    -   .year\_at\_umich() should return the value of self.years\_UM

There are one or more errors in the class. Use this space to write test
cases to determine what errors there are. You will be using this
information to answer the next set of multiple choice questions.
:::
:::
:::

::: {.runestone}
-   [the method study does not return None]{#mc_19_4_3_opt_a}
-   Incorrect, the method study does return None.
-   [the optional integer in the constructor is not
    optional]{#mc_19_4_3_opt_b}
-   Incorrect, the integer for number of years is optional.
-   [the attributes/instance variables are not correctly assigned in the
    constructor]{#mc_19_4_3_opt_c}
-   Correct! The constructor does not actually use the optional integer
    that is provided. Instead it sticks with using the default value.
-   [the method study does not increase
    self.knowledge]{#mc_19_4_3_opt_d}
-   Correct! Study does not increase the self.knowledge.
-   [the method year\_at\_umich does not return the value of
    self.years\_UM]{#mc_19_4_3_opt_e}
-   Incorrect, year\_at\_umich does return the value assigned to
    self.years\_UM.
:::

::: {.runestone}
-   [Yes]{#mc_19_4_4_opt_a}
-   Correct! There is an issue with the getKnowledge method because it
    returns None when self.knowledge is 0, even though it returns the
    correct value when self.knowledge is non-zero.
-   [No]{#mc_19_4_4_opt_b}
-   Incorrect, there are more cases that fail. Try finding those other
    cases!
:::

::: {.runestone .explainer .ac_section}
::: {#ac_19_4_3 component="activecode" question_label="18.10.7"}
::: {#ac_19_4_3_question .ac_question}
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

-   [[](Glossary.html)]{#relations-prev}
-   [[](Exercises.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
