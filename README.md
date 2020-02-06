# comp0034_flask_db

The starter code in this repository is based on the previous lecture "Flask basics, Jinja2 and Forms".

### Exercise 1: Configure the app to create the database and add sample data
1. Open `models.py` and make sure you understand the structure of the classes. Do you know what the backref is used for?
2. Open `app/__init__.py` and add a line to populate data in the database after the database tables have been created i.e. after `db.create_all()`. Do you remember where to place `import populate_db from populate_db`?
3. Run the Flask app using `run.py`

### Exercise 2: Create a page that displays all courses and the teacher
1. Create a Jinja2 template. You can create your own or use `courses.html` in the templates folder.
2. Add a route to `main/routes.py` that creates a variable which is the result of a database query of all courses and then passes the resulting data to the courses template to be rendered e.g.
    ```python
    @bp_main.route('/courses', methods=['GET'])
    def courses():
       course_list = Course.query.all()
       return render_template("courses.html", courses=course_list)
    ```
3. Add a 'Courses' link to the nav bar in `base.html`. You should be able to follow the syntax of the other links to create this.
4. Restart the Flask app and check the courses page.
5. Modify the route so that the query generates the teacher's name rather than their id and modify the courses template to display the teacher name instead of the id.
### Exercise 3: Create a basic search function
You could do this a number of ways. You could create a form class as you did for sign up. However, since the search form is on the base template and appears on every page that inherits the base then it would mean passing a form parameter to each of those pages. You may be able to find a neat solution to this, the following avoids it by reverting to an HTML form instead. 
1. Add a search results template to present the results (or use `search_results.html` in the templates folder)
2. Add a search form to the navbar in the `base.html` template e.g.
    ```html
    <form class="form-inline ml-auto" action="search" method="post">     
            <input class="form-control" type="search" name="search_term" placeholder="Enter student name" aria-label="Search">
            <button type=submit class='btn btn-primary btn-outline-light'>Search</button>   
    </form>
    ```
3. Create a route that takes the search term from the posted search form, queries the database, and renders the results to the user using the search results template
    ```python
   @bp_main.route('/search', methods=['POST', 'GET'])
   def search():
       if request.method == 'POST':
           term = request.form['search_term']
           if term == "":
               flash("Enter a name to search for")
               return redirect('/')
           results = Student.query.filter(Student.name.like('%' + term + '%')).all()
           if not results:
               flash("No students found with that name.")
               return redirect('/')
           return render_template('search_results.html', results=results)
       else:
           return redirect(url_for('main.index')) 
   ```
### Exercise 4: Modify the signup form to save to the database
1. Create methods to add and retrieve a hash of the password to the Student class in models.py
    ```python
   def set_password(self, password):
       self.password_hash = generate_password_hash(password)

   def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    ```
2. Modify the route to save the new student to the database.
SQLAlchemy will throw an error if we try to signup a student with the same email address. To handle this gracefully use try / except when registering a new user.
    ```python
    
    ```
3. Create a new user, check that the user is in the database.
4. Try to create another new user with the same details, you should get an error message
### Exercise 5: Create custom error messages
1. In the templates folder you can see a parent template `base_errors.html` that doesn't have a nav bar, and two child templates for `404.html` and `500.html`.
2. Register the 500 errors with the Blueprint in routes.py, e.g.
    ```python
   @bp_main.errorhandler(500)
   def page_not_found(e):
       return render_template("500.html"), 500
    ```
5. Register the 400 error when you create the app, e.g. in app/__init__py. 
    1. Before the start of the create_app() function add the following:
        ```python
        def page_not_found(e): 
           return render_template('404.html'), 404
        ```
    2. Within the `create_app()` function, e.g. just before registering the blueprints, register the error handlers:
        ```python
        # Register error handlers    
           app.register_error_handler(404, page_not_found)
        ```
Note: you would usually apply the same method for both errors, this exercise is just so that you can see the alternative methods!