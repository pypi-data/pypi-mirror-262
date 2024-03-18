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
    -   [8.1 Intro: What we can do with Turtles and
        Conditionals](intro-TurtlesandConditionals.html){.reference
        .internal}
    -   [8.2 Boolean Values and Boolean
        Expressions](BooleanValuesandBooleanExpressions.html){.reference
        .internal}
    -   [8.3 Logical operators](Logicaloperators.html){.reference
        .internal}
    -   [8.4 The in and not in
        operators](Theinandnotinoperators.html){.reference .internal}
    -   [8.5 Precedence of
        Operators](PrecedenceofOperators.html){.reference .internal}
    -   [8.6 Conditional Execution: Binary
        Selection](ConditionalExecutionBinarySelection.html){.reference
        .internal}
    -   [8.7 Omitting the else Clause: Unary
        Selection](OmittingtheelseClauseUnarySelection.html){.reference
        .internal}
    -   [8.8 Nested conditionals](Nestedconditionals.html){.reference
        .internal}
    -   [8.9 Chained conditionals](Chainedconditionals.html){.reference
        .internal}
    -   [8.10 The Accumulator Pattern with
        Conditionals](TheAccumulatorPatternwithConditionals.html){.reference
        .internal}
    -   [8.11 👩‍💻 Setting Up
        Conditionals](WPSettingUpConditionals.html){.reference
        .internal}
    -   [8.12 Glossary](Glossary.html){.reference .internal}
    -   [8.13 Exercises](Exercises.html){.reference .internal}
    -   [8.14 Chapter Assessment](week3a1.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#exercises .section}
[8.13. ]{.section-number}Exercises[¶](#exercises "Permalink to this heading"){.headerlink}
==========================================================================================

1.  ::: {#q1 .alert .alert-warning component="tabbedStuff"}
    ::: {component="tab" tabname="Question"}
    ::: {.runestone .explainer .ac_section}
    ::: {#ac7_14_1 component="activecode" question_label="8.13.1"}
    ::: {#ac7_14_1_question .ac_question}
    Write code that asks the user to enter a numeric score (0-100). In
    response, it should print out the score and corresponding letter
    grade, according to the table below.

      Score      Grade
      ---------- -------
      \>= 90     A
      \[80-90)   B
      \[70-80)   C
      \[60-70)   D
      \< 60      F

    The square and round brackets denote closed and open intervals. A
    closed interval includes the number, and open interval excludes it.
    So 79.99999 gets grade C , but 80 gets grade B.
    :::
    :::
    :::
    :::

    ::: {component="tab" tabname="Answer"}
    ::: {.runestone .explainer .ac_section}
    ::: {#ans7_14_1 component="activecode" question_label="8.13.2"}
    ::: {#ans7_14_1_question .ac_question}
    :::
    :::
    :::
    :::
    :::

2.  ::: {#q2 .alert .alert-warning component="tabbedStuff"}
    ::: {component="tab" tabname="Question"}
    ::: {.runestone .explainer .ac_section}
    ::: {#ac7_14_2 component="activecode" question_label="8.13.3"}
    ::: {#ac7_14_2_question .ac_question}
    A year is a **leap year** if it is divisible by 4; however, if the
    year can be evenly divided by 100, it is NOT a leap year, unless the
    year is **also** evenly divisible by 400 then it is a leap year.
    Write code that asks the user to input a year and output True if
    it's a leap year, or False otherwise. Use if statements.

      Year   Leap?
      ------ -------
      1944   True
      2011   False
      1986   False
      1800   False
      1900   False
      2000   True
      2056   True

    Above are some examples of what the output should be for various
    inputs.
    :::
    :::
    :::
    :::
    :::

3.  ::: {#q3 .alert .alert-warning component="tabbedStuff"}
    ::: {component="tab" tabname="Question"}
    ::: {.runestone .explainer .ac_section}
    ::: {#ac7_14_3 component="activecode" question_label="8.13.4"}
    ::: {#ac7_14_3_question .ac_question}
    What do these expressions evaluate to?

    1.  `3 == 3`{.docutils .literal .notranslate}

    2.  `3 != 3`{.docutils .literal .notranslate}

    3.  `3 >= 4`{.docutils .literal .notranslate}

    4.  `not (3 < 4)`{.docutils .literal .notranslate}
    :::
    :::
    :::
    :::

    ::: {component="tab" tabname="Answer"}
    1.  True

    2.  False

    3.  False

    4.  False
    :::
    :::

4.  ::: {#q4 .alert .alert-warning component="tabbedStuff"}
    ::: {component="tab" tabname="Question"}
    ::: {.runestone .explainer .ac_section}
    ::: {#ac7_14_4 component="activecode" question_label="8.13.5"}
    ::: {#ac7_14_4_question .ac_question}
    Give the **logical opposites** of these conditions, meaning an
    expression that would produce False whenever this expression
    produces True, and vice versa. You are not allowed to use the
    `not`{.docutils .literal .notranslate} operator.

    1.  `a > b`{.docutils .literal .notranslate}

    2.  `a >= b`{.docutils .literal .notranslate}

    3.  `a >= 18  and  day == 3`{.docutils .literal .notranslate}

    4.  `a >= 18  or  day != 3`{.docutils .literal .notranslate}
    :::
    :::
    :::
    :::
    :::

5.  ::: {#q5 .alert .alert-warning component="tabbedStuff"}
    ::: {component="tab" tabname="Question"}
    ::: {.runestone .explainer .ac_section}
    ::: {#ac7_14_5 component="activecode" question_label="8.13.6"}
    ::: {#ac7_14_5_question .ac_question}
    Provided are the lengths of two sides of a right-angled triangle.
    Assign the length of the hypotenuse the the variable
    `hypo_len`{.docutils .literal .notranslate}. (Hint:
    `x ** 0.5`{.docutils .literal .notranslate} will return the square
    root, or use `sqrt`{.docutils .literal .notranslate} from the math
    module)
    :::
    :::
    :::
    :::
    :::

6.  ::: {#q6 .alert .alert-warning component="tabbedStuff"}
    ::: {component="tab" tabname="Question"}
    ::: {.runestone .explainer .ac_section}
    ::: {#ac7_14_6 component="activecode" question_label="8.13.7"}
    ::: {#ac7_14_6_question .ac_question}
    Provided is a list of numbers. For each of the numbers in the list,
    determine whether they are even. If the number is even, add
    `True`{.docutils .literal .notranslate} to a new list called
    `is_even`{.docutils .literal .notranslate}. If the number is odd,
    then add `False`{.docutils .literal .notranslate}.
    :::
    :::
    :::
    :::
    :::

7.  ::: {#q7 .alert .alert-warning component="tabbedStuff"}
    ::: {component="tab" tabname="Question"}
    ::: {.runestone .explainer .ac_section}
    ::: {#ac7_14_7 component="activecode" question_label="8.13.8"}
    ::: {#ac7_14_7_question .ac_question}
    Provided is a list of numbers. For each of the numbers in the list,
    determine whether they are odd. If the number is odd, add
    `True`{.docutils .literal .notranslate} to a new list called
    `is_odd`{.docutils .literal .notranslate}. If the number is even,
    then add `False`{.docutils .literal .notranslate}.
    :::
    :::
    :::
    :::
    :::

8.  ::: {#q8 .alert .alert-warning component="tabbedStuff"}
    ::: {component="tab" tabname="Question"}
    ::: {.runestone .explainer .ac_section}
    ::: {#ac7_14_8 component="activecode" question_label="8.13.9"}
    ::: {#ac7_14_8_question .ac_question}
    Given the lengths of three sides of a triange, determine whether the
    triangle is right angled. If it is, the assign `True`{.docutils
    .literal .notranslate} to the variable `is_rightangled`{.docutils
    .literal .notranslate}. If it's not, then assign `False`{.docutils
    .literal .notranslate} to the variable `is_rightangled`{.docutils
    .literal .notranslate}.

    Hint: floating point arithmetic is not always exactly accurate, so
    it is not safe to test floating point numbers for equality. If a
    good programmer wants to know whether `x`{.docutils .literal
    .notranslate} is equal or close enough to `y`{.docutils .literal
    .notranslate}, they would probably code it up as

    ::: {.highlight-python .notranslate}
    ::: {.highlight}
        if  abs(x - y) < 0.001:      # if x is approximately equal to y
            ...
    :::
    :::
    :::
    :::
    :::
    :::
    :::

9.  ::: {#q9 .alert .alert-warning component="tabbedStuff"}
    ::: {component="tab" tabname="Question"}
    ::: {.runestone .explainer .ac_section}
    ::: {#ac7_14_9 component="activecode" question_label="8.13.10"}
    ::: {#ac7_14_9_question .ac_question}
    Implement the calculator for the date of Easter.

    The following algorithm computes the date for Easter Sunday for any
    year between 1900 to 2099.

    Ask the user to enter a year. Compute the following:

    > <div>
    >
    > 1.  a = year % 19
    >
    > 2.  b = year % 4
    >
    > 3.  c = year % 7
    >
    > 4.  d = (19 \* a + 24) % 30
    >
    > 5.  e = (2 \* b + 4 \* c + 6 \* d + 5) % 7
    >
    > 6.  dateofeaster = 22 + d + e
    >
    > </div>

    Special note: The algorithm can give a date in April. You will know
    that the date is in April if the calculation gives you an answer
    greater than 31. (You'll need to adjust) Also, if the year is one of
    four special years (1954, 1981, 2049, or 2076) then subtract 7 from
    the date.

    Your program should print an error message if the user provides a
    date that is out of range.
    :::
    :::
    :::
    :::

    ::: {component="tab" tabname="Answer"}
    ::: {.runestone .explainer .ac_section}
    ::: {#answer_ex_6_13 component="activecode" question_label="8.13.11"}
    ::: {#answer_ex_6_13_question .ac_question}
    :::
    :::
    :::
    :::

    ::: {component="tab" tabname="Discussion"}
    [Show Comments](#disqus_thread){.disqus_thread_link}
    :::
    :::

10. ::: {#q9 .alert .alert-warning component="tabbedStuff"}
    ::: {component="tab" tabname="Question"}
    ::: {.runestone .explainer .ac_section}
    ::: {#ac7_14_10 component="activecode" question_label="8.13.12"}
    ::: {#ac7_14_10_question .ac_question}
    Get the user to enter some text and print out True if it's a
    palindrome, False otherwise. (Hint: Start by reversing the input
    string, and then use the == operator to compare two values to see if
    they are the same)
    :::
    :::
    :::
    :::
    :::

11. ::: {.runestone .parsons-container}
    ::: {#pp7_14_11 .parsons component="parsons"}
    ::: {.parsons_question .parsons-text}
    Write a program that will print out a greeting to each student in
    the list. This list should also keep track of how many students have
    been greeted and note that each time a new student has been greeted.
    When only one student has entered, the program should say "The first
    student has entered!". Afterwards, the program should say "There are
    {number here} students in the classroom!".
    :::

    ``` {.parsonsblocks question_label="8.13.13" style="visibility: hidden;"}
            students = ["Jay", "Stacy", "Iman", "Trisha", "Ahmed", "Daniel", "Shadae", "Tosin", "Charlotte"]
    ---
    num_students = 0
    ---
    for student in students:
    ---
        print("Welcome to class, " + student)
        num_students += 1
    ---
        if num_students == 1:
            print("The first student has entered!")
    ---
        elif num_students > 1:
            print("There are " + str(num_students) + " students in the classroom!")
            
    ```
    :::
    :::

12. ::: {.runestone .parsons-container}
    ::: {#pp7_14_12 .parsons component="parsons"}
    ::: {.parsons_question .parsons-text}
    Piece together a program so that it can successfully print out one
    print statement, given the value of x.
    :::

    ``` {.parsonsblocks question_label="8.13.14" style="visibility: hidden;"}
            x = 16
    ---
    if x > 10:
    ---
        if x > 20:
            print("This is a large number!")
    ---
        else:
            print("This is a pretty big number.")
            
    ```
    :::
    :::

::: {#contributed-exercises .section}
[8.13.1. ]{.section-number}Contributed Exercises[¶](#contributed-exercises "Permalink to this heading"){.headerlink}
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

-   [[](Glossary.html)]{#relations-prev}
-   [[](week3a1.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
