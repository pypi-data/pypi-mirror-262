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
        Problem](/runestone/default/reportabug?course=fopp&page=VariableNamesandKeywords)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [2.1
        Introduction](intro-VariablesExpressionsandStatements.html){.reference
        .internal}
    -   [2.2 Values and Data Types](Values.html){.reference .internal}
    -   [2.3 Operators and Operands](Operators.html){.reference
        .internal}
    -   [2.4 Function Calls](FunctionCalls.html){.reference .internal}
    -   [2.5 Data Types](DataTypes.html){.reference .internal}
    -   [2.6 Type conversion
        functions](ConvertTypeFunctions.html){.reference .internal}
    -   [2.7 Variables](Variables.html){.reference .internal}
    -   [2.8 Variable Names and
        Keywords](VariableNamesandKeywords.html){.reference .internal}
    -   [2.9 👩‍💻 Choosing the Right Variable
        Name](WPChoosingtheRightVariableName.html){.reference .internal}
    -   [2.10 Statements and
        Expressions](StatementsandExpressions.html){.reference
        .internal}
    -   [2.11 Order of Operations](OrderofOperations.html){.reference
        .internal}
    -   [2.12 Reassignment](Reassignment.html){.reference .internal}
    -   [2.13 Updating Variables](UpdatingVariables.html){.reference
        .internal}
    -   [2.14 👩‍💻 Hard-Coding](HardCoding.html){.reference .internal}
    -   [2.15 Input](Input.html){.reference .internal}
    -   [2.16 Glossary](Glossary.html){.reference .internal}
    -   [2.17 Exercises](Exercises.html){.reference .internal}
    -   [2.18 Chapter Assessment](week1a2.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#variable-names-and-keywords .section}
[2.8. ]{.section-number}Variable Names and Keywords[¶](#variable-names-and-keywords "Permalink to this heading"){.headerlink}
=============================================================================================================================

**Variable names** can be arbitrarily long. They can contain both
letters and digits, but they have to begin with a letter or an
underscore. Although it is legal to use uppercase letters, by convention
we don't. If you do, remember that case matters. `Bruce`{.docutils
.literal .notranslate} and `bruce`{.docutils .literal .notranslate} are
different variables.

::: {.admonition .caution}
Caution

Variable names can never contain spaces.
:::

The underscore character ( `_`{.docutils .literal .notranslate}) can
also appear in a name. It is often used in names with multiple words,
such as `my_name`{.docutils .literal .notranslate} or
`price_of_tea_in_china`{.docutils .literal .notranslate}. There are some
situations in which names beginning with an underscore have special
meaning, so a safe rule for beginners is to start all names with a
letter.

If you give a variable an illegal name, you get a syntax error. In the
example below, each of the variable names is illegal.

::: {.highlight-default .notranslate}
::: {.highlight}
    76trombones = "big parade"
    more$ = 1000000
    class = "Computer Science 101"
:::
:::

`76trombones`{.docutils .literal .notranslate} is illegal because it
does not begin with a letter. `more$`{.docutils .literal .notranslate}
is illegal because it contains an illegal character, the dollar sign.
But what's wrong with `class`{.docutils .literal .notranslate}?

It turns out that `class`{.docutils .literal .notranslate} is one of the
Python **keywords**. Keywords define the language's syntax rules and
structure, and they cannot be used as variable names. Python has
thirty-something keywords (and every now and again improvements to
Python introduce or eliminate one or two):

  --------- ------- -------- ---------- -------- ----------
  and       as      assert   break      class    continue
  def       del     elif     else       except   exec
  finally   for     from     global     if       import
  in        is      lambda   nonlocal   not      or
  pass      raise   return   try        while    with
  yield     True    False    None                
  --------- ------- -------- ---------- -------- ----------

You might want to keep this list handy. If the interpreter complains
about one of your variable names and you don't know why, see if it is on
this list.

**Check your understanding**

::: {.runestone}
-   [True]{#question2_8_1_opt_a}
-   \- The + character is not allowed in variable names.
-   [False]{#question2_8_1_opt_b}
-   \- The + character is not allowed in variable names (everything else
    in this name is fine).
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

-   [[](Variables.html)]{#relations-prev}
-   [[](WPChoosingtheRightVariableName.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
