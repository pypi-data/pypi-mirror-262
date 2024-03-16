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
        Problem](/runestone/default/reportabug?course=fopp&page=using-exceptions)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [19.1 What is an exception?](intro-exceptions.html){.reference
        .internal}
    -   [19.3 👩‍💻 When to use
        try/except](using-exceptions.html){.reference .internal}
    -   [19.4 Standard Exceptions](standard-exceptions.html){.reference
        .internal}
    -   [19.5 Exercises](Exercises.html){.reference .internal}
    -   [19.6 Chapter Assessment](ChapterAssessment.html){.reference
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

::: {#when-to-use-try-except .section}
[19.3. ]{.section-number}👩‍💻 When to use try/except[¶](#when-to-use-try-except "Permalink to this heading"){.headerlink}
========================================================================================================================

The reason to use try/except is when you have a code block to execute
that will sometimes run correctly and sometimes not, depending on
conditions you can't foresee at the time you're writing the code.

For example, when you are running code that fetches data from a website,
you may run the code when you don't have a network connection or when
the external website is temporarily not responding. If your program can
still do something useful in those situations, you would like to handle
the exception and have the rest of your code execute.

As another example, suppose you have fetched some nested data from a
website into a dictionary d. When you try to extract specific elements,
some may be missing: d may not include a particular key, for example. If
you anticipate a particular key potentially not being present, you could
write an if..else check to take care of it.

::: {.highlight-python .notranslate}
::: {.highlight}
    if somekey in d:
        # it's there; extract the data
        extract_data(d)
    else:
        skip_this_one(d)
:::
:::

However, if you're extracting lots of different data, it can get tedious
to check for all of them. You can wrap all the data extraction in a
try/except.

::: {.highlight-python .notranslate}
::: {.highlight}
    try:
        extract_data(d)
    except:
        skip_this_one(d)
:::
:::

It's considered poor practice to catch all exceptions this way. Instead,
python provides a mechanism to specify just certain kinds of exceptions
that you'll catch (for example, just catching exceptions of type
KeyError, which happens when a key is missing from a dictionary.

::: {.highlight-python .notranslate}
::: {.highlight}
    try:
        extract_data(d)
    except KeyError:
        skip_this_one(d)
:::
:::

We won't go into more details of exception handling in this introductory
course. Check out the official [python tutorial section on error
handling](https://docs.python.org/3/tutorial/errors.html){.reference
.external} if you're interested.
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

-   [[](intro-exceptions.html)]{#relations-prev}
-   [[](standard-exceptions.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
