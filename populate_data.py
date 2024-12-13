from core.models import Course, Module, LearningResource, Lesson
from django.db.models import Count

# Step 1: Find and remove duplicate courses
duplicates = Course.objects.values('title').annotate(count=Count('id')).filter(count__gt=1)

for duplicate in duplicates:
    courses_to_delete = Course.objects.filter(title=duplicate['title'])[1:]  # Keep the first instance
    for course in courses_to_delete:
        course.delete()

# Step 2: Check if the course already exists, and create if not
course, created = Course.objects.get_or_create(
    title="Web Development Basics",
    defaults={"description": "Learn the fundamentals of web development, including HTML, CSS, and JavaScript."}
)

# Step 3: Check if the module already exists for the course, and create if not
module, created = Module.objects.get_or_create(
    title='Web Development',
    course=course,  # Link to the existing course
    defaults={
        'description': 'Learn how to build websites and web applications.',
        'image': 'modules/html-css-js.png'
    }
)

# Step 4: Find duplicate modules
module_duplicates = Module.objects.values('title', 'course').annotate(count=Count('title')).filter(count__gt=1)

for duplicate in module_duplicates:
    modules_to_delete = Module.objects.filter(title=duplicate['title'], course=duplicate['course'])[1:]
    for module in modules_to_delete:
        module.delete()
        
# Remove duplicate lessons
lesson_duplicates = Lesson.objects.values('title', 'module').annotate(count=Count('id')).filter(count__gt=1)
for duplicate in lesson_duplicates:
    lessons_to_delete = Lesson.objects.filter(title=duplicate['title'], module=duplicate['module'])[1:]
    for lesson in lessons_to_delete:
        lesson.delete()        
        
# Create learning resources
LearningResource.objects.bulk_create([
    LearningResource(
        title='Free Online Courses with Certificates & Diplomas',
        url='https://alison.com',
        description='Expand Your Knowledge In Other Fields with Alison\'s Free Courses.',
        image='learning_resources/alison.png'
    ),
    LearningResource(
        title='Free Mobile Development Courses for Power Learn Community',
        url='https://bit.ly/mobile-devt-courses',
        description='Are You Enthusiastic About Mobile Development? This is Your Chance.',
        image='learning_resources/power-learn.jpg'
    )
])

# Step 2: Create lessons for Web Development (HTML, CSS, and JavaScript)
lesson_data = [
    # Week 1 - HTML
    {"module": module, "title": "Introduction to HTML", "content": "HTML is the structure of the web...", "week": 1, "day": 1},
    {"module": module, "title": "HTML Elements", "content": "Learn about different HTML elements...", "week": 1, "day": 2},
    {"module": module, "title": "Forms and Inputs", "content": "Learn how to create forms in HTML...", "week": 1, "day": 3},
    {"module": module, "title": "HTML5 Semantic Elements", "content": "Understand the new semantic tags in HTML5...", "week": 1, "day": 4},
    {"module": module, "title": "Project: Basic Webpage", "content": "Create a basic webpage using HTML...", "week": 1, "day": 5},

    # Week 2 - CSS
    {"module": module, "title": "Introduction to CSS", "content": "CSS is used for styling the web pages...", "week": 2, "day": 1},
    {"module": module, "title": "Selectors and Properties", "content": "Learn how to select HTML elements and style them...", "week": 2, "day": 2},
    {"module": module, "title": "Box Model and Flexbox", "content": "Understanding the box model and using Flexbox...", "week": 2, "day": 3},
    {"module": module, "title": "CSS Grid", "content": "Learn how to create layouts with CSS Grid...", "week": 2, "day": 4},
    {"module": module, "title": "Project: Styling a Webpage", "content": "Create a styled webpage using CSS...", "week": 2, "day": 5},

    # Week 3 - JavaScript
    {"module": module, "title": "Introduction to JavaScript", "content": "JavaScript is used to make webpages interactive...", "week": 3, "day": 1},
    {"module": module, "title": "Variables and Data Types", "content": "Learn about variables, and different data types in JS...", "week": 3, "day": 2},
    {"module": module, "title": "Functions and Control Flow", "content": "Learn how to define functions and use control flow...", "week": 3, "day": 3},
    {"module": module, "title": "DOM Manipulation", "content": "Learn how to manipulate the DOM using JavaScript...", "week": 3, "day": 4},
    {"module": module, "title": "Project: Interactive Webpage", "content": "Create an interactive webpage with JavaScript...", "week": 3, "day": 5},
]

# Step 3: Use get_or_create to add lessons
for lesson in lesson_data:
    Lesson.objects.get_or_create(
        module=lesson["module"],
        title=lesson["title"],
        defaults={
            "content": lesson["content"],
            "week": lesson["week"],
            "day": lesson["day"],
        }
    )

# Update content for lessons
Lesson.objects.filter(title="Introduction to HTML").update(
    content="""
    HTML (HyperText Markup Language) is the backbone of every webpage. It defines the structure using tags. 
    Tags are enclosed in < >, like <html> or <body>.
    
    **Basic Structure of an HTML Document**:
    ```
    <!DOCTYPE html>
    <html>
    <head>
        <title>My First Webpage</title>
    </head>
    <body>
        <h1>Hello, World!</h1>
        <p>This is a paragraph.</p>
    </body>
    </html>
    ```

    **Key Tags**:
    - <html>: The root tag of an HTML document.
    - <head>: Contains metadata, like the page title.
    - <body>: Contains visible content like headings, paragraphs, and images.

    **Further Reading**:
    - [Introduction to HTML (MDN)](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML)
    """
)

# Week 1: Day 2
Lesson.objects.filter(title="HTML Elements").update(
    content="""
    HTML elements represent parts of a webpage. Elements have a start tag, optional content, and an end tag:
    ```
    <tagname>Content</tagname>
    ```

    **Common Elements**:
    - Headings: <h1> to <h6> (e.g., <h1>Main Heading</h1>)
    - Paragraphs: <p> (e.g., <p>This is a paragraph.</p>)
    - Links: <a href="https://example.com">Visit Example</a>
    - Images: <img src="image.jpg" alt="Description">

    **Example**:
    ```
    <h1>This is a Heading</h1>
    <p>This is a paragraph with a <a href="https://example.com">link</a>.</p>
    <img src="path/to/image.jpg" alt="Example Image">
    ```

    **Further Reading**:
    - [HTML Elements (W3Schools)](https://www.w3schools.com/html/html_elements.asp)
    """
)

# Week 1: Day 3
Lesson.objects.filter(title="Forms and Inputs").update(
    content="""
    HTML forms allow users to input data, which can then be sent to a server. 

    **Basic Form Example**:
    ```
    <form action="/submit" method="POST">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name">
        <button type="submit">Submit</button>
    </form>
    ```

    **Common Input Types**:
    - Text: <input type="text">
    - Email: <input type="email">
    - Password: <input type="password">
    - Submit Button: <button type="submit">

    **Further Reading**:
    - [HTML Forms (MDN)](https://developer.mozilla.org/en-US/docs/Learn/Forms)
    """
)

# Week 1: Day 4
Lesson.objects.filter(title="HTML5 Semantic Elements").update(
    content="""
    Semantic elements in HTML5 clearly define their purpose, improving readability for developers and browsers.

    **Examples**:
    - <header>: Defines a page header.
    - <nav>: Represents navigation links.
    - <main>: Represents the main content.
    - <article>: Represents an independent piece of content.
    - <footer>: Defines a page footer.

    **Example**:
    ```
    <header>
        <h1>Website Title</h1>
    </header>
    <main>
        <article>
            <h2>Article Title</h2>
            <p>This is the main content of the article.</p>
        </article>
    </main>
    <footer>
        <p>Copyright 2024</p>
    </footer>
    ```

    **Further Reading**:
    - [HTML5 Semantic Elements (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTML/Element)
    """
)

# Week 1: Day 5
Lesson.objects.filter(title="Project: Basic Webpage").update(
    content="""
    **Project Description**:
    Create a simple webpage using everything learned in Week 1. Your webpage should:
    1. Include a header, main content, and footer.
    2. Use semantic elements like <header>, <main>, and <footer>.
    3. Add a form with at least one input field.

    **Example Structure**:
    ```
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Basic Webpage</title>
    </head>
    <body>
        <header>
            <h1>Welcome to My Webpage</h1>
        </header>
        <main>
            <p>This is my first webpage project.</p>
            <form action="/submit" method="POST">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email">
                <button type="submit">Submit</button>
            </form>
        </main>
        <footer>
            <p>Created by [Your Name]</p>
        </footer>
    </body>
    </html>
    ```

    **Further Reading**:
    - [HTML Basics (MDN)](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML)
    """
)


# Week 2: Day 1
Lesson.objects.filter(title="Introduction to CSS").update(
    content="""
    CSS (Cascading Style Sheets) is used to control the layout and appearance of a webpage.

    **Basic Structure of CSS**:
    ```
    h1 {
        color: blue;
    }
    ```

    **Common CSS Properties**:
    - color: Sets the text color.
    - background-color: Sets the background color.
    - font-family: Specifies the font.
    - margin: Controls the space around elements.
    - padding: Controls the space inside elements.

    **Example**:
    ```
    body {
        background-color: lightblue;
    }
    h1 {
        color: red;
    }
    ```

    **Further Reading**:
    - [Introduction to CSS (MDN)](https://developer.mozilla.org/en-US/docs/Learn/CSS/Introduction_to_CSS)
    """
)

# Week 2: Day 2
Lesson.objects.filter(title="Selectors and Properties").update(
    content="""
    CSS selectors allow you to select HTML elements to apply styles to them.

    **Common Selectors**:
    - Element Selector: `h1 { color: red; }`
    - ID Selector: `#header { font-size: 20px; }`
    - Class Selector: `.intro { font-style: italic; }`
    - Universal Selector: `* { margin: 0; padding: 0; }`

    **Example**:
    ```
    #header {
        color: green;
    }
    .intro {
        font-size: 18px;
    }
    ```

    **Further Reading**:
    - [CSS Selectors (MDN)](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors)
    """
)

# Week 2: Day 3
Lesson.objects.filter(title="Box Model and Flexbox").update(
    content="""
    The CSS box model describes the rectangular boxes generated for elements, including margins, borders, padding, and content.

    **Box Model Structure**:
    - Content: The actual content of the box (e.g., text or image).
    - Padding: Space between the content and the border.
    - Border: A line surrounding the padding and content.
    - Margin: Space outside the border.

    **Example**:
    ```
    div {
        margin: 20px;
        border: 1px solid black;
        padding: 10px;
    }
    ```
    
    Flexbox is a one-dimensional layout method for distributing space along a row or column.

    **Basic Flexbox Example**:
    ```
    .container {
        display: flex;
    }
    .item {
        flex: 1;
    }
    ```

    **Key Flexbox Properties**:
    - display: flex; Makes an element a flex container.
    - justify-content: Aligns items horizontally (e.g., center, space-between).
    - align-items: Aligns items vertically (e.g., flex-start, center).

    **Further Reading**:
	- [CSS Box Model (MDN)](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/The_box_model)
    - [CSS Flexbox (MDN)](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Flexbox)
    """
)

# Week 2: Day 4 - CSS Grid
Lesson.objects.filter(title="CSS Grid").update(
    content="""
    CSS Grid is a two-dimensional layout system for the web. It lets you design web pages with complex layouts.

    **Basic CSS Grid Example**:
    ```
    <div class="grid-container">
        <div class="item1">Item 1</div>
        <div class="item2">Item 2</div>
        <div class="item3">Item 3</div>
    </div>

    <style>
        .grid-container {
            display: grid;
            grid-template-columns: auto auto auto;
        }
        .item1, .item2, .item3 {
            padding: 20px;
            border: 1px solid #ddd;
        }
    </style>
    ```
    
    **CSS Grid Properties**:
    - `grid-template-columns`: Defines the number and size of columns.
    - `grid-template-rows`: Defines the size of rows.
    - `grid-gap`: Defines the space between rows and columns.
    
    **Further Reading**:
    - [CSS Grid Layout (MDN)](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout)
    """
)

# Week 2: Day 5
Lesson.objects.filter(title="Project: Styling a Webpage").update(
    content="""
    **Project Description**:
    Create a webpage with the following elements:
    1. A header section with a navigation bar.
    2. A main content section with text and images.
    3. A footer with contact information.

    **Requirements**:
    - Use CSS to style your webpage.
    - Use the box model and flexbox to layout elements.
    - Ensure the webpage is responsive.

    **Example Structure**:
    ```
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Styled Webpage</title>
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <header>
            <nav>
                <ul>
                    <li><a href="#home">Home</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <section id="home">
                <h1>Welcome to My Webpage</h1>
                <img src="image.jpg" alt="Image">
            </section>
        </main>
        <footer>
            <p>Contact info: email@example.com</p>
        </footer>
    </body>
    </html>
    ```

    **Further Reading**:
    - [CSS Basics (MDN)](https://developer.mozilla.org/en-US/docs/Learn/CSS/First_steps)
    """
)


# Week 3: Day 1
Lesson.objects.filter(title="Introduction to JavaScript").update(
    content="""
    JavaScript is a programming language used to create interactive effects within web browsers.

    **Basic Structure of JavaScript**:
    ```
    <script>
        alert('Hello, World!');
    </script>
    ```

    **Common JavaScript Concepts**:
    - Variables: Store data (e.g., let x = 10;)
    - Functions: Reusable blocks of code.
    - Events: Handle user actions (e.g., click, mouseover).

    **Example**:
    ```
    <button onclick="alert('Hello!')">Click Me</button>
    ```

    **Further Reading**:
    - [JavaScript Basics (MDN)](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/First_steps)
    """
)

# Week 3: Day 2 - Variables, Data Types, and Functions
Lesson.objects.filter(title="Variables and Data Types").update(
    content="""
    JavaScript Variables, Data Types, and Functions are the building blocks of programming in JavaScript.

    **Variables**:
    Variables store values. In JavaScript, you can declare variables using `var`, `let`, or `const`.

    **Basic Variable Example**:
    ```
    let name = "John";
    const age = 30;
    ```

    **Data Types**:
    JavaScript has various data types such as:
    - `String`: Represents text.
    - `Number`: Represents numeric values.
    - `Boolean`: Represents true or false.

    **Basic Data Type Example**:
    ```
    let isActive = true;  // Boolean
    let price = 29.99;    // Number
    let message = "Hello!";  // String
    ```

    **Functions**:
    Functions are blocks of reusable code. You can define functions in JavaScript as follows:

    **Basic Function Example**:
    ```
    function greet(name) {
        return "Hello, " + name + "!";
    }

    console.log(greet("John"));
    ```

    **Further Reading**:
    - [JavaScript Variables (MDN)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types)
    - [JavaScript Functions (MDN)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Functions)
    """
)

# Week 3: Day 3
Lesson.objects.filter(title="DOM Manipulation").update(
    content="""
    DOM (Document Object Model) manipulation allows JavaScript to interact with HTML elements.

    **Basic DOM Example**:
    ```
    <button id="btn">Click Me</button>
    <script>
        document.getElementById('btn').onclick = function() {
            alert('Button clicked!');
        }
    </script>
    ```

    **Common DOM Methods**:
    - getElementById(): Selects an element by its ID.
    - getElementsByClassName(): Selects elements by class.
    - querySelector(): Selects elements using CSS selectors.

    **Further Reading**:
    - [DOM Manipulation (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Document_object_model)
    """
)

# Week 3: Day 4
Lesson.objects.filter(title="JavaScript Events").update(
    content="""
    Events allow JavaScript to respond to user interactions like clicks and keyboard input.

    **Event Types**:
    - click: Triggered when an element is clicked.
    - mouseover: Triggered when the mouse moves over an element.
    - keydown: Triggered when a key is pressed.

    **Example**:
    ```
    <button onclick="alert('Button clicked!')">Click Me</button>
    ```

    **Further Reading**:
    - [JavaScript Events (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Event)
    """
)

# Week 3: Day 5
Lesson.objects.filter(title="Project: Interactive Webpage").update(
    content="""
    **Project Description**:
    Create an interactive webpage with the following:
    1. A button that triggers a JavaScript event (e.g., displays an alert or changes content).
    2. An input field that reacts to user input (e.g., a button that shows entered text).
    3. An image or text element that updates when clicked.

    **Example Structure**:
    ```
    <!DOCTYPE html>
    <html>
    <head>
        <title>Interactive Webpage</title>
        <script>
            function updateContent() {
                document.getElementById('content').innerHTML = 'You clicked the button!';
            }
        </script>
    </head>
    <body>
        <button onclick="updateContent()">Click Me</button>
        <div id="content">Original Content</div>
    </body>
    </html>
    ```

    **Further Reading**:
    - [DOM Events (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Event_target)
    """
)

