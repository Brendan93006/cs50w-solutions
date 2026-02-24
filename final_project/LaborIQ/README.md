# LaborIQ - An employee manager that allows managers to add, organize, and schedule employees.
LaborIQ lets the user add and delete employees as well as the ability to schedule them. To create an employee object the user bust provide the employees name, position, and hourly wage. To schedule the employee the user must provide the employee to schedule, along with the time and date the shift is for. It also has a main page called the hub to make the website easier to explore given links for the main pages like adding and scheduling employees. The website also lets the user see all the shifts in the current week along with all the current employees. 

### Distinctiveness and Complexity
My project satisfies the distinctiveness and complexity requirements because it is neither a social network nor an ecommerce site. It is a workforce manager intended for general managers of companies to organize their workforce. I used JavaScript in my fontend and I used more than one model in Django.

## Django
### urls.py
Defines all the URL routes for the web application and maps them to the appropriate view functions in views.py. This file determines what page or action is triggered when a user visits a specific URL. This file centralizes all routing logic, making it easy to see how URLs map to functionality and ensuring users interact with the app through a consistent URL structure.

### models.py
Defines the database schema for the application using Django models. This file structures how data is stored and related, including users, employees, and shifts. This file establishes the core data structure of the app, enabling CRUD operations for employees and shifts while maintaining relationships between users, employees, and shifts. Validation ensures data integrity.

### views.py
Contains all the logic for handling HTTP requests and rendering responses. Each function corresponds to a route in urls.py and determines how users interact with the app. This file is the core of the app’s functionality. It manages user authentication, CRUD operations for employees and shifts, input validation, and dynamic responses. By separating GET and POST logic, it ensures forms behave correctly and users experience smooth navigation. The use of login_required decorators enforces security and user-specific access.

## Templates (html)
### layout.html
The base HTML template that defines the overall structure of the web application. Other page templates extend this file to maintain a consistent layout, navigation, and styling. Serves as the template foundation for the entire web app. By centralizing layout, navigation, and scripts, it reduces repetition and enforces a consistent look and feel. Blocks (title and body) allow child templates to customize content while preserving global styles and navigation.

### index.html
The homepage template for the application, extending layout.html to maintain consistent navigation and styling. It serves as the main dashboard for users once logged in. This template gives users an immediate overview of core functionality upon logging in. By using visually distinct cards and clear calls to action, it enhances usability and guides users toward important actions efficiently. Extending layout.html ensures consistent navigation, responsive design, and access to shared scripts like delete.js.

### employees.html
Displays a list of all employees for the logged-in user. Extends layout.html to maintain consistent navigation, styling, and shared scripts. This template provides a clear, interactive interface for managing employees. Cards visually separate each employee, making it easy to scan information. Integration with delete.js allows dynamic deletion without page reload, enhancing user experience. The conditional alert ensures users receive immediate feedback when no employees exist.

### add_employee.html
Provides a form for adding a new employee. Extends layout.html to ensure consistent navigation, styling, and shared scripts across the app. This template gives users a focused and intuitive interface for adding employees. The design emphasizes clarity and simplicity, reducing input errors and improving usability. Validation and messaging provide immediate feedback to the user.

### shifts.html
Displays the weekly schedule for all employees. Extends layout.html to maintain consistent navigation, styling, and shared scripts. This template provides a clear visual representation of the weekly schedule, making it easy for users to see employee shifts at a glance. The integration with delete.js enables real-time removal of shifts without page reloads, enhancing usability and efficiency.

### add_shift.html
Provides a form for adding a new shift. Extends layout.html to ensure consistent navigation, styling, and shared scripts. This template gives users a focused interface to add shifts efficiently, minimizing errors by requiring key fields. Employee selection and date-time inputs streamline scheduling, while clear messaging ensures users understand validation errors or confirmation feedback.

### login.html
Provides the login form for existing users. Extends layout.html to maintain consistent navigation, styling, and shared scripts. This template creates a secure and straightforward interface for user authentication. Clear input fields and messaging help reduce login errors, while the registration link ensures new users can quickly create an account.

### register.html
Provides the user registration form. Extends layout.html for consistent navigation, styling, and shared scripts. This template provides a clear and secure interface for new users to create accounts. Validation messaging reduces errors, while structured input fields guide users through the registration process efficiently.

## JavaScript
### delete.js
Handles dynamic deletion of employees and shifts using AJAX, without requiring page reloads. This script improves user experience by enabling seamless, real-time deletion of employees and shifts. Users can remove items without page refreshes, making the interface faster and more intuitive. The integration of CSRF protection ensures the operations remain secure.

### How to Run
1. Install Django (if not already):  
```bash
pip3 install Django
python3 manage.py runserver