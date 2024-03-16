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
        Problem](/runestone/default/reportabug?course=fopp&page=standard-exceptions)
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
::: {#standard-exceptions .section}
[]{#index-0}

[19.4. ]{.section-number}Standard Exceptions[¶](#standard-exceptions "Permalink to this heading"){.headerlink}
==============================================================================================================

Most of the standard *exceptions* built into Python are listed below.
They are organized into related groups based on the types of issues they
deal with.

  Language Exceptions   Description
  --------------------- -------------------------------------------------------------------------------------------------------------------------------------
  StandardError         Base class for all built-in exceptions except StopIteration and SystemExit.
  ImportError           Raised when an import statement fails.
  SyntaxError           Raised when there is an error in Python syntax.
  IndentationError      Raised when indentation is not specified properly.
  NameError             Raised when an identifier is not found in the local or global namespace.
  UnboundLocalError     Raised when trying to access a local variable in a function or method but no value has been assigned to it.
  TypeError             Raised when an operation or function is attempted that is invalid for the specified data type.
  LookupError           Base class for all lookup errors.
  IndexError            Raised when an index is not found in a sequence.
  KeyError              Raised when the specified key is not found in the dictionary.
  ValueError            Raised when the built-in function for a data type has the valid type of arguments, but the arguments have invalid values specified.
  RuntimeError          Raised when a generated error does not fall into any category.
  MemoryError           Raised when a operation runs out of memory.
  RecursionError        Raised when the maximum recursion depth has been exceeded.
  SystemError           Raised when the interpreter finds an internal problem, but when this error is encountered the Python interpreter does not exit.

  Math Exceptions      Description
  -------------------- --------------------------------------------------------------------------------------------------------------------------------------
  ArithmeticError      Base class for all errors that occur for numeric calculation. You know a math error occurred, but you don't know the specific error.
  OverflowError        Raised when a calculation exceeds maximum limit for a numeric type.
  FloatingPointError   Raised when a floating point calculation fails.
  ZeroDivisonError     Raised when division or modulo by zero takes place for all numeric types.

  I/O Exceptions      Description
  ------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  FileNotFoundError   Raised when a file or directory is requested but doesn't exist.
  IOError             Raised when an input/ output operation fails, such as the print statement or the open() function when trying to open a file that does not exist. Also raised for operating system-related errors.
  PermissionError     Raised when trying to run an operation without the adequate access rights.
  EOFError            Raised when there is no input from either the raw\_input() or input() function and the end of file is reached.
  KeyboardInterrupt   Raised when the user interrupts program execution, usually by pressing Ctrl+c.

  Other Exceptions      Description
  --------------------- -----------------------------------------------------------------------------------------------------------------------------------------
  Exception             Base class for all exceptions. This catches most exception messages.
  StopIteration         Raised when the next() method of an iterator does not point to any object.
  AssertionError        Raised in case of failure of the Assert statement.
  SystemExit            Raised when Python interpreter is quit by using the sys.exit() function. If not handled in the code, it causes the interpreter to exit.
  OSError               Raises for operating system related errors.
  EnvironmentError      Base class for all exceptions that occur outside the Python environment.
  AttributeError        Raised in case of failure of an attribute reference or assignment.
  NotImplementedError   Raised when an abstract method that needs to be implemented in an inherited class is not actually implemented.

All exceptions are objects. The classes that define the objects are
organized in a hierarchy, which is shown below. This is important
because the parent class of a set of related exceptions will catch all
exception messages for itself and its child exceptions. For example, an
`ArithmeticError`{.docutils .literal .notranslate} exception will catch
itself and all `FloatingPointError`{.docutils .literal .notranslate},
`OverflowError`{.docutils .literal .notranslate}, and
`ZeroDivisionError`{.docutils .literal .notranslate} exceptions.

::: {.highlight-Python .notranslate}
::: {.highlight}
    BaseException
     +-- SystemExit
     +-- KeyboardInterrupt
     +-- GeneratorExit
     +-- Exception
          +-- StopIteration
          +-- StopAsyncIteration
          +-- ArithmeticError
          |    +-- FloatingPointError
          |    +-- OverflowError
          |    +-- ZeroDivisionError
          +-- AssertionError
          +-- AttributeError
          +-- BufferError
          +-- EOFError
          +-- ImportError
          +-- LookupError
          |    +-- IndexError
          |    +-- KeyError
          +-- MemoryError
          +-- NameError
          |    +-- UnboundLocalError
          +-- OSError
          |    +-- BlockingIOError
          |    +-- ChildProcessError
          |    +-- ConnectionError
          |    |    +-- BrokenPipeError
          |    |    +-- ConnectionAbortedError
          |    |    +-- ConnectionRefusedError
          |    |    +-- ConnectionResetError
          |    +-- FileExistsError
          |    +-- FileNotFoundError
          |    +-- InterruptedError
          |    +-- IsADirectoryError
          |    +-- NotADirectoryError
          |    +-- PermissionError
          |    +-- ProcessLookupError
          |    +-- TimeoutError
          +-- ReferenceError
          +-- RuntimeError
          |    +-- NotImplementedError
          |    +-- RecursionError
          +-- SyntaxError
          |    +-- IndentationError
          |         +-- TabError
          +-- SystemError
          +-- TypeError
          +-- ValueError
          |    +-- UnicodeError
          |         +-- UnicodeDecodeError
          |         +-- UnicodeEncodeError
          |         +-- UnicodeTranslateError
          +-- Warning
               +-- DeprecationWarning
               +-- PendingDeprecationWarning
               +-- RuntimeWarning
               +-- SyntaxWarning
               +-- UserWarning
               +-- FutureWarning
               +-- ImportWarning
               +-- UnicodeWarning
               +-- BytesWarning
               +-- ResourceWarning
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

-   [[](using-exceptions.html)]{#relations-prev}
-   [[](Exercises.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
