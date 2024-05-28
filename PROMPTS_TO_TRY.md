# Some Gemini prompts to try

## Not *really* code assist, but still

Let us create a new logo for the application.
For that we are going to use [Gemini Advanced](https://gemini.google.com/)

### Basic instructions

```text
Please create a logo for a guestbook web application
```

### Ask for some tuning

```text
Make the logo clean and simple, yet recognisable
```

### Ask to add a branding/cooperation

Note: you should change it to your brand.

```text
This applicaiton should also evoke the Google brand and identify the applicaiton as a guestbook
```

We've got this:

![gemini_logo](./src/frontend/static/gemini_logo.jpeg)

### Try your own fine tuning

Try to get closer by giving specific instructions.


## Now code assist itself

Below are a couple of prompts to try out on this code base.

### Explain code

To explain a particular code, just select the file and ask for it. For example:

Select the file ``src/backend/back.py`` and type

```text
Please give me a high-level explaination of what this code does
```

### Refactoring

Let us ask for Gemini to improve maintainability. Select the ``src/backend/back.py`` or ``src/frontend/front.py`` file and ask:

```text
Could you please refactor the code to be better organized
```

### Let us add the new logo

We generate a brand new logo up there. 
Now is time to incorporate it.
We assume you saved the logo as ``src/frontend/static/gemini_logo.jpeg`` for this example.
Select the file ``src/frontend/templates/home.html`` and ask the following:

```text
Please add the logo src/frontend/static/gemini_logo.jpeg to the title
```

Oops, it ate the title out, let us put it back:

```text
Please add the title (left to the logo): "My new Guestbook"
```

### How about the outer loop?

Let us assume that your code got submitted and your CI/CD ran [Semgrep](https://semgrep.dev/) for static security analysis.

#### Run Semgrep

```bash
semgrep ci
```

You will find a violation that is a bit cryptic about ``csrf_token``.
It does not, however, give you a good recipe to fix it. 
Let us try Gemini.

#### Let us fix it

Select the file ``src/frontend/front.py`` and ask:

```text
Please add CSRF protection
```

It should generate snippets for the Python code as well as the HTML code.

#### Is it there at all?

Re-run the frontend (see instructions in [LOCAL_RUN.md](./LOCAL_RUN.md)) and open your browser at [http://localhost:8080](http://localhost:8080).

Ask for to view the source page and you should see the following snippet:

```html
    <div class="container posts mt-0">
<!-- ok: django-no-csrf-token -->
            <form class="form-inline" method="POST" action="/post">
            <input id="csrf_token" name="csrf_token" type="hidden" value="IjMwNWI0NzIxZmU2MTRiOWMyMGY1NTE4YWQzNmRmNzhmM2FmNzE5YTki.ZlXAsA.uIenYsnVxq7KGzBCnZlguZYtFHw">
            <label class="sr-only" for="name">Name</label>
            <div class="input-group mb-2 mr-sm-2">
```

#### Run Semgrep again

Let us check the fix:

```bash
semgrep ci
```

Q: Oops, is still being flagged, but why? 
A: Because, in this case, you need to tell Semgrep that you fixed it.
Q: How?
A: Just add the following comment before the open `<form>` tag, like below:

```html
    <div class="container posts mt-0">
<!-- ok: django-no-csrf-token -->
            <form class="form-inline" method="POST" action="/post">
            {{ form.hidden_tag() }}
            <label class="sr-only" for="name">Name</label>

```

Re-run Semgrep and it should have been marked as fixed.
