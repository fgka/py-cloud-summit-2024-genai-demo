# The branch diffs you should see

## Adding the logo

<details>
<summary>Click me</summary>

```bash
git diff steps/0_starting_point steps/1_logo_created
```

Expected:

```text
diff --git a/src/frontend/static/gemini_logo.jpeg b/src/frontend/static/gemini_logo.jpeg
new file mode 100644
index 0000000..3e3ea61
Binary files /dev/null and b/src/frontend/static/gemini_logo.jpeg differ
```
</details>

## Refactoring

<details>
<summary>Click me</summary>

```bash
git diff steps/1_logo_created steps/2_refactoring
```

Expected:

```text
diff --git a/src/backend/back.py b/src/backend/back.py
index 4092daf..c05c2a5 100644
--- a/src/backend/back.py
+++ b/src/backend/back.py
@@ -7,6 +7,7 @@ from flask import Flask, jsonify, request
 from flask_pymongo import PyMongo
 import bleach

+# Configuration
 DEFAULT_GUESTBOOK_DB_ADDR = "127.0.0.1:27017"
 GUESTBOOK_DB_ADDR = os.environ.get('GUESTBOOK_DB_ADDR', DEFAULT_GUESTBOOK_DB_ADDR)
 DEFAULT_PORT = 8321
@@ -14,27 +15,40 @@ PORT = os.environ.get('PORT', DEFAULT_PORT)
 DEFAULT_HOST = "127.0.0.1"
 HOST = os.environ.get('HOST', DEFAULT_HOST)

+# Initialize Flask app
 app = Flask(__name__)
 app.config["MONGO_URI"] = f'mongodb://{GUESTBOOK_DB_ADDR}/guestbook'
 mongo = PyMongo(app)

+# Define helper functions
+def clean_message(message):
+    """Sanitizes the message content using bleach.clean to prevent XSS attacks."""
+    return bleach.clean(message)
+
+def create_message_data(author, message):
+    """Creates a dictionary with the author, message, and timestamp."""
+    return {'author': clean_message(author),
+            'message': clean_message(message),
+            'date': time.time()}
+
+# Define routes
 @app.route('/messages', methods=['GET'])
 def get_messages():
-    """ retrieve and return the list of messages on GET request """
+    """Retrieves and returns a list of messages from the database."""
     field_mask = {'author':1, 'message':1, 'date':1, '_id':0}
     msg_list = list(mongo.db.messages.find({}, field_mask).sort("_id", -1))
     return jsonify(msg_list), 201

 @app.route('/messages', methods=['POST'])
 def add_message():
-    """ save a new message on POST request """
+    """Saves a new message to the database."""
     raw_data = request.get_json()
-    msg_data = {'author':bleach.clean(raw_data['author']),
-                'message':bleach.clean(raw_data['message']),
-                'date':time.time()}
+    msg_data = create_message_data(raw_data['author'], raw_data['message'])
     mongo.db.messages.insert_one(msg_data)
-    return  jsonify({}), 201
+    return jsonify({}), 201

+# Main execution
 if __name__ == '__main__':
-    # start Flask server
+    # Start Flask server
+    # Flask's debug mode is unrelated to ptvsd debugger used by Cloud Code
     app.run(debug=False, port=PORT, host=HOST)
```
</details>

## Added logo to web page

<details>
<summary>Click me</summary>

```bash
git diff steps/2_refactoring steps/3_logo_added
```

Expected:

```text
diff --git a/src/frontend/templates/home.html b/src/frontend/templates/home.html
index a46f3d6..235b95f 100644
--- a/src/frontend/templates/home.html
+++ b/src/frontend/templates/home.html
@@ -15,8 +15,9 @@
         <div class="container">
             <h1>
                 <a href="/">
-                    My Guestbook
+                    <img src="static/gemini_logo.jpeg" alt="My Guestbook Logo" height="50">
                 </a>
+                My new Guestbook
             </h1>
             <a href="#" class="text-muted">View on GitHub</a>
         </div>
```
</details>

## Fixing CSRF vulnerability

<details>
<summary>Click me</summary>

```bash
git diff steps/3_logo_added steps/4_csrf_fixed
```

Expected:

```text
diff --git a/src/frontend/front.py b/src/frontend/front.py
index 9a79869..120751f 100644
--- a/src/frontend/front.py
+++ b/src/frontend/front.py
@@ -6,6 +6,7 @@ import os
 import datetime
 import time
 from flask import Flask, render_template, redirect, url_for, request, jsonify
+from flask_wtf import FlaskForm, CSRFProtect
 import requests
 import dateutil.relativedelta

@@ -15,28 +16,38 @@ DEFAULT_PORT = 8123
 PORT = os.environ.get('PORT', DEFAULT_PORT)
 DEFAULT_HOST = "127.0.0.1"
 HOST = os.environ.get('HOST', DEFAULT_HOST)
+SECRET_KEY = os.urandom(32)

 app = Flask(__name__)
+app.config['SECRET_KEY'] = SECRET_KEY
 app.config["BACKEND_URI"] = f'http://{GUESTBOOK_API_ADDR}/messages'
+app.config['WTF_CSRF_ENABLED'] = True
+csrf = CSRFProtect(app)
+
+class MyForm(FlaskForm):
+    pass


 @app.route('/')
 def main():
     """ Retrieve a list of messages from the backend, and use them to render the HTML template """
+    form = MyForm()
     response = requests.get(app.config["BACKEND_URI"], timeout=3)
     json_response = json.loads(response.text)
-    return render_template('home.html', messages=json_response)
+    return render_template('home.html', form=form, messages=json_response)

 @app.route('/post', methods=['POST'])
 def post():
     """ Send the new message to the backend and redirect to the homepage """
-    new_message = {'author': request.form['name'],
-                'message':  request.form['message']}
-    requests.post(url=app.config["BACKEND_URI"],
-                data=jsonify(new_message).data,
-                headers={'content-type': 'application/json'},
-                timeout=3)
-    return redirect(url_for('main'))
+    form = MyForm()
+    if form.validate_on_submit():
+        new_message = {'author': request.form['name'],
+                    'message':  request.form['message']}
+        requests.post(url=app.config["BACKEND_URI"],
+                    data=jsonify(new_message).data,
+                    headers={'content-type': 'application/json'},
+                    timeout=3)
+        return redirect(url_for('main'))

 def format_duration(timestamp):
     """ Format the time since the input timestamp in a human readable way """
diff --git a/src/frontend/requirements.txt b/src/frontend/requirements.txt
index ad750f9..0444557 100644
--- a/src/frontend/requirements.txt
+++ b/src/frontend/requirements.txt
@@ -1,4 +1,5 @@
 Flask==2.3.3
+flask_wtf=1.2.1
 requests==2.32.0
 python-dateutil==2.8.2
 debugpy # Required for debugging
diff --git a/src/frontend/templates/home.html b/src/frontend/templates/home.html
index 235b95f..3ccbd11 100644
--- a/src/frontend/templates/home.html
+++ b/src/frontend/templates/home.html
@@ -24,7 +24,9 @@
     </div>

     <div class="container posts mt-0">
+<!-- ok: django-no-csrf-token -->
             <form class="form-inline" method="POST" action="/post">
+            {{ form.hidden_tag() }}
             <label class="sr-only" for="name">Name</label>
             <div class="input-group mb-2 mr-sm-2">
                 <div class="input-group-prepend">
                 
```
</details>
