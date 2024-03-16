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
        Problem](/runestone/default/reportabug?course=fopp&page=InvokingSuperMethods)
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
::: {#invoking-the-parent-class-s-method .section}
[22.4. ]{.section-number}Invoking the Parent Class's Method[¶](#invoking-the-parent-class-s-method "Permalink to this heading"){.headerlink}
============================================================================================================================================

Sometimes the parent class has a useful method, but you just need to
execute a little extra code when running the subclass's method. You can
override the parent class's method in the subclass's method with the
same name, but also invoke the parent class's method. Here's how.

Say you wanted the `Dog`{.docutils .literal .notranslate} subclass of
`Pet`{.docutils .literal .notranslate} to say "Arf! Thanks!" when the
`feed`{.docutils .literal .notranslate} method is called, as well as
executing the code in the original method.

Here's the original `Pet`{.docutils .literal .notranslate} class again.

::: {.runestone .explainer .ac_section}
::: {#inheritance_pet_class_copy component="activecode" question_label="22.4.1"}
::: {#inheritance_pet_class_copy_question .ac_question}
:::
:::
:::

And here's a subclass that overrides `feed()`{.docutils .literal
.notranslate} by invoking the the parent class's `feed()`{.docutils
.literal .notranslate} method; it then also executes an extra line of
code. It does this by calling the built-in function `super()`{.docutils
.literal .notranslate}. The `super()`{.docutils .literal .notranslate}
function returns a special object that allows you to invoke the method
of the parent class. So to call the parent class's `feed()`{.docutils
.literal .notranslate} method (`Pet.feed()`{.docutils .literal
.notranslate}), we say `super().feed()`{.docutils .literal
.notranslate}.

::: {.runestone .explainer .ac_section}
::: {#feed_me_example component="activecode" question_label="22.4.2"}
::: {#feed_me_example_question .ac_question}
:::
:::
:::

::: {.admonition .note}
Note

Another way to invoke the parent's method is to explicitly refer to the
parent class' method and invoke it on the instance. So, in this case, we
could say `Pet.feed(self)`{.docutils .literal .notranslate}. This is a
little more explicit, but it's also a little less flexible. If we later
change the name of the parent class, we'd have to change it in all the
subclasses. Also, if we later change the class hierarchy, so that
`Dog`{.docutils .literal .notranslate} is a subclass of some other
class, we'd have to change the code in all the subclasses. So, it's
better to use `super()`{.docutils .literal .notranslate}.
:::

This technique is very often used with the `__init__`{.docutils .literal
.notranslate} method for a subclass. Suppose that some extra instance
variables are defined for the subclass. When you invoke the constructor,
you pass all the regular parameters for the parent class, plus the extra
ones for the subclass. The subclass' `__init__`{.docutils .literal
.notranslate} method then stores the extra parameters in instance
variables and calls the parent class' `__init__`{.docutils .literal
.notranslate} method to store the common parameters in instance
variables and do any other initialization that it normally does.

Let's say we want to create a subclass of `Pet`{.docutils .literal
.notranslate}, called `Bird`{.docutils .literal .notranslate}, and we
want it to take an extra parameter, `chirp_number`{.docutils .literal
.notranslate}, with a default value of `2`{.docutils .literal
.notranslate}, and have an extra instance variable,
`self.chirp_number`{.docutils .literal .notranslate}. Then, we'll use
this in the `hi`{.docutils .literal .notranslate} method to make more
than one sound.

::: {.runestone .explainer .ac_section}
::: {#super_methods_1 component="activecode" question_label="22.4.3"}
::: {#super_methods_1_question .ac_question}
:::
:::
:::

**Check your understanding**

::: {.runestone}
-   [7]{#question_inheritance_4_opt_a}
-   This would print if the code was print(b2.chirp\_number).
-   [\[\"Mrrp\"\]]{#question_inheritance_4_opt_b}
-   We set b2 to be Bird(\'Sunny\', 7) above. Bird is a subclass of Pet,
    which has \[\"Mrrp\"\] for sounds, but Bird has a different value
    for that class variable. The interpreter looks in the subclass
    first.
-   [\[\"chirp\"\]]{#question_inheritance_4_opt_c}
-   The interpeter finds the value in the class variable for the class
    Bird.
-   [Error]{#question_inheritance_4_opt_d}
-   We ran set b2 to be Bird(\'Sunny\', 7) above. Bird has a value set
    for the attribute sounds.
:::

::: {.runestone}
-   [Error when invoked]{#question_inheritance_5_opt_a}
-   Since we are no longer calling the parent method in the subclass
    method definition, the actions defined in the parent method feed
    will not happen, and only Arf! Thanks! will be printed.
-   [The string \"Arf! Thanks!\" would not print out but d1 would still
    have its hunger reduced.]{#question_inheritance_5_opt_b}
-   Remember that the Python interpreter checks for the existence of
    feed in the Dog class and looks for feed in Pet only if it isn\'t
    found in Dog.
-   [The string \"Arf! Thanks!\" would still print out but d1 would not
    have its hunger reduced.]{#question_inheritance_5_opt_c}
-   Since we are no longer calling the parent Pet class\'s method in the
    Dog subclass\'s method definition, the class definition will
    override the parent method.
-   [Nothing would be different. It is the same as the current
    code.]{#question_inheritance_5_opt_d}
-   Remember that the Python interpreter checks for the existence of
    feed in the Dog class and looks for feed in Pet only if it isn\'t
    found in Dog.
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

-   [[](OverrideMethods.html)]{#relations-prev}
-   [[](MultipleInheritance.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
