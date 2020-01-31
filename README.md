# comp0034_flask_db

The code in this repository is based on the previous lecture "Flask basics, Jinja2 and Forms". It builds on that code in include database interaction.


### Exercise 1: Configure the app to create the database and add sample data
1. Open `models.py` and make sure you understand the structure of the classes. Do you know what the backref is used for?
2. Open `app/__init__.py` and add a line to populate data in the database after the database tables have been created (db.create_all()). Do you remember where to place `import populate_db from populate_db`?
3. Run the Flask app using `run.py`

### Exercise 2: Create a page that displays all courses and the teacher
1. Create a Jinja2 template. You can create your own or use the code below.
    ```
    {% extends "base.html" %}
    {% block title %}Courses{% endblock %}
    {% block content %}
    {% if courses|length %}
    <table class="table">
        <thead class="thead-dark">
        <tr>
            <th scope="col">#</th>
            <th scope="col">Name</th>
            <th scope="col">Teacher</th>
        </tr>
        </thead>
        <tbody>
        {% for course in courses %}
        <tr>
            <td>{{ course.course_code }}</td>
            <td>{{ course.name }}</td>
            <td>{{ course.teacher_id }}</td>
        </tr>
        {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p>Sorry, no courses are available at this time</p>
    {% endif %}
    {% endblock %}
    ```
2. Add a route to `main/routes.py` e.g.
    ```python
    @bp_main.route('/courses', methods=['GET'])
    def courses():
       courses = Course.query.all()
       return render_template("courses.html", courses=courses)
    ```
3. Add a link to the nav bar in `base.html`. You should be able to follow the syntax of the other links to create this.
4. Restart the Flask app and check the courses page.
5. Modify the route so that the query generates the teacher's name rather than their id and modify the courses template to display the teacher name instead of the id.
### Exercise 3: Create a basic search function
1. Create a form that allows users to enter a search term
    ```python
    class UserSearchForm(FlaskForm):
       term = StringField('Search', validators=[DataRequired(), Length(min=2, max=60)])
    ```
2. Add the form to the nav bar in the base template e.g.
    ```html
    <form class="form-inline my-2 my-lg-0" action="{{ url_for('main.search_results') }}" method="post" novalidate>     
            {{ sform.hidden_tag() }}     
            {{ sform.term(class="form-control mr-sm-2", placeholder='Search for student') }}     
            <button type=submit class='btn btn-outline-success my-2 my-sm-0'>Search</button>   
    </form>
    ```

3. Add a search results template to present the results
    ```html
    {% extends ”base.html" %}
    {% block title %}Search results{% endblock %}
    {% block content %}
    {% if results|length %}
    {# Variable is not empty #}
    <table class="table">
       <thead class="thead-dark">
       <tr>
           <th scope="col">Student name</th>
           <th scope="col">Email</th>
       </tr>
       </thead>
       <tbody> {% for result in results %}
       <tr>
           <td>{{ result.name }}</td>
           <td>{{ result.email }}</td>
       </tr>
      {% endfor %}
       </tbody>
    </table>
    {% else %}
    {# Variable is empty #}
    <p>Sorry, no students found</p>
    {% endif %}
    {% endblock %}
    ```
4. Create a route that takes the search term from the posted form, queries the database, and returns the results to the user using the search results template
    ```python
    @bp_main.route('/results', methods=['POST', 'GET'])
    def search_results():   
       form = UserSearchForm()
       if form.validate_on_submit():
           term = form.term.data
           results = Student.query.filter(Student.name.like('%' + term + '%')).all()
           return render_template('search_results.html', results=results, sform=UserSearchForm())
       flash('Please enter a search term between 2 and 60 characters')
       return redirect(url_for('main.index', sform=UserSearchForm()))
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
1. Create a base template (or use base.html)
    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
       <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" 
          integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
      <title>{% block title %}{% endblock %}</title>
    </head>
    <body>
    <main role="main" class="container">
       <br>
       {% block content %}
       {% endblock %}
    </main>
    </body>
    </html>
    ```
2. Create a custom 404.html 
    ```html
   {% extends "layout_errors.html" %}
   {% block title %}Not Found{% endblock %}
   {% block content %}  
   <h1>Not Found</h1>  
   <p>What you were looking for is just not there.<p>
   <a href="{{ url_for('main.index') }}">Go back home</a>
   {% endblock %}
    ```
3. Create a custom 500.html
    ```html
   {% extends "layout_errors.html" %}
   {% block title %}Internal server error{% endblock %}
   {% block content %}  
   <h1>Not Found</h1>  
   <p>What you were looking for is just not there.</p>
   <p><a href="{{ url_for('main.index') }}">Go back home</a></p>
   {% endblock %}
    ```
4. Register the errors with the Blueprint in routes.py, e.g.
    ```python
   @bp_main.errorhandler(500)
   def page_not_found(e):
       return render_template("500.html"), 500
    ```
5. Alternatively, you can register them when you create the app, e.g. in app/__init__py
    ```python
    def page_not_found(e): 
       return render_template('404.html'), 404
   
   def create_app(config_class): 
    ...    
   # Register error handlers    
    app.register_error_handler(404, page_not_found)
    ...
    ```
