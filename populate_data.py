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
lesson_duplicates = Lesson.objects.values('module', 'week', 'day').annotate(count=Count('id')).filter(count__gt=1)

for duplicate in lesson_duplicates:
    # Get all lessons for this module/week/day
    lessons = Lesson.objects.filter(
        module=duplicate['module'],
        week=duplicate['week'],
        day=duplicate['day']
    ).order_by('-id')  # Assuming the latest (highest id) is the one you just updated

    # Keep the first one, delete the rest
    lessons_to_delete = lessons[1:]
    for lesson in lessons_to_delete:
        print(f"Deleting duplicate lesson: {lesson.title} (Week {lesson.week} Day {lesson.day})")
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
    {"module": module, "title": "Introduction to Web Development and Tools Setup", "content": "Web development is the process...", "week": 1, "day": 1},
    {"module": module, "title": "HTML Structure and Semantic Elements", "content": "Learn about different HTML elements...", "week": 1, "day": 2},
    {"module": module, "title": "Links, Images, and Project Organization", "content": "Links connect pages or external sites...", "week": 1, "day": 3},
    {"module": module, "title": "Introduction to CSS and Styling Your Page", "content": "What is CSS?...", "week": 1, "day": 4},
    {"module": module, "title": "Project - Personal Webpage Assignment", "content": "Create a basic webpage using HTML...", "week": 1, "day": 5},

    # Week 2 - CSS
    {"module": module, "title": "Advanced HTML Elements", "content": "Explore more powerful HTML tools...", "week": 2, "day": 1},
    {"module": module, "title": "Advanced CSS: Pseudo-classes and Pseudo-elements", "content": "Bring life and style to your...", "week": 2, "day": 2},
    {"module": module, "title": "Responsive Design with Media Queries", "content": "Make sure your website looks...", "week": 2, "day": 3},
    {"module": module, "title": "Git Workflows, Branching, and Collaboration", "content": "Go beyond the basics...", "week": 2, "day": 4},
    {"module": module, "title": "Project: Responsive Portfolio", "content": "Create a styled webpage using CSS...", "week": 2, "day": 5},

    # Week 3 - JavaScript
    {"module": module, "title": "JavaScript Basics: Variables, Data Types, and Operators", "content": "JavaScript Basics...", "week": 3, "day": 1},
    {"module": module, "title": "JavaScript Functions, Conditionals, and Events", "content": "JavaScript Functions...", "week": 3, "day": 2},
    {"module": module, "title": "JavaScript DOM Manipulation", "content": "JavaScript + The DOM...", "week": 3, "day": 3},
    {"module": module, "title": "JavaScript Loops and Arrays","content": "JavaScript Loops + Arrays...", "week": 3, "day": 4},
    {"module": module, "title": "Project: JavaScript Interactive Feature", "content": "Build Your First Interactive Feature...", "week": 3, "day": 5},
]

# Step 3: Use get_or_create to add lessons
for lesson in lesson_data:
    Lesson.objects.update_or_create(
    module=lesson["module"],
    week=lesson["week"],
    day=lesson["day"],
    defaults={
        "title": lesson["title"],
        "content": lesson["content"],
    }
)

# Update content for lessons
# Week 1: Day 1
Lesson.objects.filter(title="Introduction to Web Development and Tools Setup").update(
    content="""
    ## 🌐 What is Web Development?

    Web development is the process of creating websites and web applications that run on the internet.

    It generally includes:
    - **Frontend** (what the user sees and interacts with)
    - **Backend** (server-side logic, databases, user management)
    - **Full-stack** (both frontend and backend)

    You will start this course focusing on **frontend**.

    ---

    ## 🛠️ Key Technologies

    - **HTML** → the skeleton of the web (structure)
    - **CSS** → the skin and clothes (styling)
    - **JavaScript** → the muscles (interactivity)
    - **Git** → tracks your code changes (version control)
    - **GitHub** → online place to store and share your code

    ---

    ## 💻 Essential Tools

    ### Code Editors

    You’ll need a **code editor** to write your code.

    We recommend:
    - **Visual Studio Code (VS Code)** → https://code.visualstudio.com/
    - Install and explore: built-in terminal, extensions, file explorer.
    - Alternatives: Sublime Text, Atom (optional).

    ### Web Browsers

    You’ll test your web pages in a browser.
    - Recommended: Google Chrome
    - Alternatives: Firefox, Edge

    ### Git & GitHub Setup

    - Install **Git** → https://git-scm.com/
    - Create a free **GitHub** account → https://github.com/

    ---

    ## 🗂️ Setting Up Your First Project

    1️⃣ Create a folder on your computer, e.g., `my-first-website`.

    2️⃣ Open this folder in VS Code.

    3️⃣ Inside the folder, set up:

        /my-first-website
        ├── index.html
        ├── /css
        ├── /images
        └── /js

    
    ---

    ## ✍️ Writing Your First HTML Page

    Create a file named `index.html` and add this code:

    ```
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My First Website</title>
    </head>
    <body>
        <h1>Welcome to Web Development!</h1>
        <p>This is your very first webpage. 🎉</p>
    </body>
    </html>
    ```

    ---

    ## 🔧 Intro to Git

    Inside your project folder, open the terminal and run:

    ```
    git init
    git add .
    git commit -m "Initial commit: set up project and index.html"
    ```

    This sets up Git to track your code.

    ---

    ## 🚀 Upload to GitHub (Optional)

    1️⃣ Go to GitHub, create a new repository (no README).  
    2️⃣ Copy the remote link.

    In your terminal, connect and push:

    ```
    git remote add origin https://github.com/yourusername/your-repo.git
    git branch -M main
    git push -u origin main
    ```

    ---

    ## 🏆 Day 1 Task

    ✅ Install VS Code and Git.  
    ✅ Set up your first project folder.  
    ✅ Create an `index.html` page with a welcome message.  
    ✅ Initialize Git and make your first commit.  
    ✅ (Optional) Push your code to GitHub.

    Great job — you are now officially a web developer in training! 🚀
    """
)

# Week 1: Day 2
Lesson.objects.filter(title="HTML Structure and Semantic Elements").update(
    content="""
    ## 📦 Understanding HTML Structure

    HTML is made up of **elements**:
    - Tags (`<h1>`, `<p>`, `<a>`)  
    - Attributes (`href`, `src`, `alt`)  
    - Content (what’s inside the tags)

    Basic structure:
    ```
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Page Title</title>
    </head>
    <body>
        <!-- Visible content goes here -->
    </body>
    </html>
    ```

    ---

    ## 🏛 Semantic HTML

    Semantic tags describe **meaning** (not just appearance).  
    Examples:
    - `<header>` → top section  
    - `<nav>` → navigation links  
    - `<main>` → main page content  
    - `<section>` → grouped content  
    - `<article>` → standalone pieces  
    - `<footer>` → bottom section

    Non-semantic tags (don’t carry meaning):
    - `<div>` → general block
    - `<span>` → inline block

    ---

    ## ✨ Formatting Text

    - Headings: `<h1>` to `<h6>`
    - Paragraphs: `<p>`
    - Bold/strong: `<strong>` or `<b>`
    - Italics/emphasis: `<em>` or `<i>`
    - Line breaks: `<br>`

    Example:
    ```
    <h1>About Me</h1>
    <p>I am learning web development. <strong>It’s fun!</strong></p>
    ```

    ---

    ## 🧩 Lists

    - **Unordered list**:
    ```
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
    ```

    - **Ordered list**:
    ```
    <ol>
        <li>First</li>
        <li>Second</li>
    </ol>
    ```

    ---

    ## 🚀 Practice

    ✅ Add a header and footer to your `index.html`.  
    ✅ Create a list (ordered or unordered) about your hobbies.  
    ✅ Use at least one `<strong>` or `<em>` tag.

    Commit and push your changes to GitHub:
    ```
    git add .
    git commit -m "Added semantic HTML elements and a list"
    git push
    ```

    """
)

# Week 1: Day 3
Lesson.objects.filter(title="Links, Images, and Project Organization").update(
    content="""
    ## 🔗 Adding Links

    Links connect pages or external sites.

    ```
    <a href="https://example.com">Visit Example</a>
    ```

    - href → the URL or file you’re linking to  
    - Internal link: `<a href="about.html">About</a>`  
    - Open in new tab: `<a href="https://example.com" target="_blank">Visit</a>`

    ---

    ## 🖼 Adding Images

    ```
    <img src="images/photo.jpg" alt="My Photo">
    ```

    - src → path to the image  
    - alt → alternative text for screen readers / when image fails to load

    Use **relative paths** (`images/photo.jpg`) or **absolute URLs** (`https://...`).

    ---

    ## 📁 Organizing Your Project

    Good folder structure keeps your project clean:
    - /index.html → main page
    - /about.html → about page
    - /images/ → image files
    - /css/ → CSS stylesheets
    - /js/ → JavaScript files (later)

    Example:
    ```
    /my-website
        index.html
        about.html
        /images
        /css
        /js
    ```

    ---

    ## 🧪 Practice Task

    ✅ Add a profile picture on your about.html.  
    ✅ Link from `index.html` to about.html and vice versa.  
    ✅ Organize your files into /images/, /css/, /js/.

    Push your updates to GitHub:
    ```
    git add .
    git commit -m "Added links, images, and reorganized project folders"
    git push
    ```

    """
)

# Week 1: Day 4
Lesson.objects.filter(title="Introduction to CSS and Styling Your Page").update(
    content="""
    ## 🎨 What is CSS?

    CSS (Cascading Style Sheets) controls how your HTML looks.

    You can:
    - Change colors, fonts, and layout.
    - Add padding, margins, and borders.
    - Make your site responsive for different devices.

    ---

    ## ✏️ Writing CSS

    1️⃣ Inline (inside HTML element):
    ```
    <p style="color: blue;">Hello</p>
    ```

    2️⃣ Internal (inside `<style>` tag in `<head>`):
    ```
    <style>
        p {
            color: blue;
        }
    </style>
    ```

    3️⃣ External (best practice, using a `.css` file):
    - Create `style.css` in `/css/` folder.
    - Link in your HTML:
    ```
    <link rel="stylesheet" href="css/style.css">
    ```

    ---

    ## 🖌 Basic Styling

    - Change background:
    ```
    body {
        background-color: #f0f0f0;
    }
    ```

    - Style headings:
    ```
    h1 {
        color: darkblue;
        font-family: Arial, sans-serif;
    }
    ```

    - Add borders and padding:
    ```
    img {
        border: 2px solid #333;
        padding: 10px;
    }
    ```

    ---

    ## 🚀 Practice Task

    ✅ Create a `style.css` file.  
    ✅ Link it to both `index.html` and `about.html`.  
    ✅ Add:
    - A background color.
    - A custom font for headings.
    - A border around your profile image.

    Push changes to GitHub:
    ```
    git add .
    git commit -m "Added CSS styling"
    git push
    ```
    """
)

# Week 1: Day 5
Lesson.objects.filter(title="Project - Personal Webpage Assignment").update(
    content="""
    ## 🎯 Task Overview

    You’ll build a simple **personal webpage** that includes:
    ✅ Homepage (`index.html`)  
    ✅ About page (`about.html`)  
    ✅ Profile image  
    ✅ Links between pages  
    ✅ CSS styling from `style.css`

    ---

    ## 🏗 Requirements

    - Organized folders: `/images/`, `/css/`, etc.
    - Use semantic HTML elements.
    - Include:
        - Headings (`<h1>`–`<h3>`)
        - Paragraphs (`<p>`)
        - Lists (`<ul>` or `<ol>`)
        - Links (`<a>`)
        - Images (`<img>`)

    ---

    ## 💡 Bonus

    - Try adding an additional page (like `contact.html`).
    - Experiment with colors and fonts in CSS.
    - Add hover effects to links.

    ---

    ## 🚀 Submission Instructions

    ✅ Upload your project to GitHub:
    ```bash
    git add .
    git commit -m "Final personal webpage project"
    git push
    ```

    ✅ Submit your GitHub link via the course portal form.

    ---

    **Well done completing Week 1!** 🌟 You now have:
    - A working multi-page website.
    - Basic HTML & CSS skills.
    - Familiarity with Git and GitHub.

    Next week, we dive into deeper CSS techniques!
    """
)


# Week 2: Day 1
Lesson.objects.filter(title="Advanced HTML Elements").update(
    content="""
    **Advanced HTML Elements**

    Today we explore more powerful HTML tools to build richer webpages.

    **1️⃣ Forms**
    Forms collect user input like names, emails, or messages.
    - `<input>`: fields like text, password, email.
    - `<label>`: connects to inputs for better accessibility.
    - `<button>`: submit or reset forms.
    Example:
    ```
    <form>
        <label for="name">Name:</label>
        <input type="text" id="name" name="name">
        <button type="submit">Submit</button>
    </form>
    ```

    **2️⃣ Tables**
    Organize data into rows + columns.
    - `<table>`: wraps all data.
    - `<tr>`: defines a row.
    - `<th>`: table header.
    - `<td>`: table cell.
    Example:
    ```
    <table>
        <tr>
            <th>Item</th>
            <th>Price</th>
        </tr>
        <tr>
            <td>Book</td>
            <td>$10</td>
        </tr>
    </table>
    ```

    **3️⃣ Semantic Elements**
    Give your page *meaning* (important for accessibility + SEO).
    - `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`

    **4️⃣ Multimedia**
    Embed videos or audio.
    ```
    <video controls>
        <source src="video.mp4" type="video/mp4">
    </video>
    <audio controls>
        <source src="sound.mp3" type="audio/mpeg">
    </audio>
    ```

    **Tasks:**
    - ✅ Build a form with **name, email, message** + submit button.
    - ✅ Create a table listing **3 favorite movies** with their genre and year.
    - ✅ Add a short **YouTube video** or audio clip to your page.

    **Key Takeaways:**
    - Master form and table structures.
    - Use semantic elements for clean, meaningful layouts.
    - Embed multimedia responsibly.
    """
)


# Week 2: Day 2
Lesson.objects.filter(title="Advanced CSS: Pseudo-classes and Pseudo-elements").update(
    content="""
    **Advanced CSS: Pseudo-classes & Pseudo-elements**

    Bring life and style to your site with advanced selectors.

    **1️⃣ Pseudo-classes**
    React to element states.
    - `:hover`: when the mouse is over.
    - `:focus`: when element is active.
    - `:nth-child(n)`: target specific items.
    Example:
    ```
    li:nth-child(odd) {
        background: #f0f0f0;
    }
    ```

    **2️⃣ Pseudo-elements**
    Style specific parts of an element.
    - `::before`: insert content before.
    - `::after`: insert after.
    - `::first-letter`: style first letter.
    Example:
    ```
    p::before {
        content: "🔥 ";
    }
    ```

    **3️⃣ Transitions + Animations**
    Smoothly animate changes.
    ```
    button {
        transition: background-color 0.3s ease;
    }
    ```

    **Tasks:**
    - ✅ Make buttons **change color on hover**.
    - ✅ Style a paragraph so its **first letter** is large and bold.
    - ✅ Create a list where every **even item** has a different background.

    **Key Takeaways:**
    - Add interactive flair with pseudo-classes.
    - Control element visuals with pseudo-elements.
    - Apply smooth transitions for a polished UI.
    """
)


# Week 2: Day 3
Lesson.objects.filter(title="Responsive Design with Media Queries").update(
    content="""
    **Responsive Design**

    Make sure your website looks great on all screens.

    **1️⃣ Viewport Meta Tag**
    Helps browsers adjust layout on mobile.
    ```
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    ```

    **2️⃣ Media Queries**
    Apply styles based on screen size.
    Example:
    ```
    @media (max-width: 600px) {
        body {
            background: lightblue;
        }
    }
    ```

    **3️⃣ Flexible Layouts**
    - Use percentages or `flex` instead of fixed widths.
    - Make images scale:
    ```
    img {
        max-width: 100%;
        height: auto;
    }
    ```

    **4️⃣ Mobile-first Design**
    Start with mobile styles, then add breakpoints for larger screens.

    **Tasks:**
    - ✅ Create a page that **changes background color** on small screens.
    - ✅ Make sure your **images scale properly** on mobile.
    - ✅ Build a **two-column layout** that stacks on narrow screens.

    **Key Takeaways:**
    - Build adaptive designs.
    - Use media queries to fine-tune appearance.
    - Always test on different devices.
    """
)


# Week 2: Day 4 - CSS Grid
Lesson.objects.filter(title="Git Workflows, Branching, and Collaboration").update(
    content="""
    **Git Workflows, Branching, and Collaboration**

    Go beyond the basics — work like a pro!

    **1️⃣ Branching**
    Work on features without breaking the main code.
    ```
    git branch feature-login
    git checkout feature-login
    git merge feature-login
    ```

    **2️⃣ Handling Merge Conflicts**
    When two branches change the same line:
    - Git marks the conflict.
    - You edit + resolve manually.
    - Then commit the resolved file.

    **3️⃣ Remote Collaboration**
    Push + pull changes:
    ```
    git push origin feature-login
    git pull origin main
    ```

    **4️⃣ Pull Requests (PRs)**
    On GitHub:
    - Submit PRs to propose changes.
    - Review + discuss before merging.

    **5️⃣ Popular Workflows**
    - **Feature Branch Workflow**: isolate new features.
    - **Fork + PR**: fork main repo, contribute via PR.
    - **Gitflow**: structured with main, develop, release branches.

    **Tasks:**
    - ✅ Create a **new branch**, make a small change, and merge it.
    - ✅ Practice resolving a **merge conflict**.
    - ✅ Push a branch to **GitHub** and open a pull request.

    **Key Takeaways:**
    - Understand branching + merging.
    - Manage collaboration with GitHub PRs.
    - Work confidently in team environments.
    """
)


# Week 2: Day 5
Lesson.objects.filter(title="Project: Responsive Portfolio").update(
    content="""
    **Project: Responsive Portfolio**

    Time to combine everything you’ve learned!

    **Goal:**
    Create a personal portfolio site that:
    - Introduces you.
    - Showcases your projects.
    - Works on all devices.

    **Suggested Sections:**
    - Header with name/logo + navigation.
    - About section with short bio.
    - Projects grid with images, titles, links.
    - Contact form with name/email/message.

    **Key Features:**
    - Responsive layout using media queries.
    - Smooth hover effects + transitions.
    - Semantic HTML for structure.
    - Mobile-first design.

    **Tasks:**
    - ✅ Build the full site and **test responsiveness**.
    - ✅ Upload it to **GitHub**.
    - ✅ Share your project link for review.

    **Stretch Goals:**
    - Add **smooth scrolling** between sections.
    - Animate elements on scroll.
    - Use **GitHub Pages** to deploy your site live.

    **Final Tip:**
    Focus on clean, clear design. Small details (like hover effects or good spacing) make a big difference!
    """
)


# Week 3: Day 1
Lesson.objects.filter(title="JavaScript Basics: Variables, Data Types, and Operators").update(
    content="""
    # JavaScript Basics: Variables, Data Types, and Operators

    Welcome to JavaScript! Today, we start building the foundation.

    **1️⃣ Variables**
    Variables store data. In JavaScript, we use:
    - `var`: old way, function-scoped.
    - `let`: modern, block-scoped.
    - `const`: block-scoped, value can’t be reassigned.

    Example:
    ```js
    var city = "Nairobi";
    let temperature = 28;
    const country = "Kenya";
    ```

    **⚠ Best Practice:** Use `let` and `const`. Avoid `var` unless you understand its quirks.

    **2️⃣ Data Types**
    JavaScript has:
    - **String** → text, e.g., `"hello"`, `'world'`
    - **Number** → integers, decimals, e.g., `42`, `3.14`
    - **Boolean** → `true` or `false`
    - **Undefined** → declared but not assigned
    - **Null** → intentional “no value”
    - **Object** → collection of key–value pairs
    - **Array** → ordered list of values
    - **Symbol** → unique identifier (advanced)

    Example:
    ```js
    let name = "Sam";
    let age = 30;
    let isStudent = false;
    let hobbies = ["reading", "coding", "hiking"];
    let person = { name: "Sam", age: 30 };
    ```

    **3️⃣ Operators**
    - **Arithmetic:** `+`, `-`, `*`, `/`, `%`
    - **Assignment:** `=`, `+=`, `-=`
    - **Comparison:** `==`, `===`, `!=`, `<`, `>`, `<=`, `>=`
    - **Logical:** `&&`, `||`, `!`

    Example:
    ```js
    let sum = 5 + 3;         // 8
    let isEqual = (5 === '5'); // false
    let result = (age > 18) && isStudent; // false
    ```

    **Tasks:**
    ✅ Declare a `const` for your favorite food.  
    ✅ Create an array with 5 items you like.  
    ✅ Make an object with keys `name`, `age`, `hobby`.

    **Deep Dive Resources:**
    - MDN JavaScript: [Variables](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types)
    """
)


# Week 3: Day 2 - Variables, Data Types, and Functions
Lesson.objects.filter(title="JavaScript Functions, Conditionals, and Events").update(
    content="""
    # JavaScript Functions, Conditionals, and Events

    Now we move into **logic** and **interactivity**.

    **1️⃣ Functions**
    A function is reusable code that performs a task.
    ```js
    function greet(name) {
        return `Hello, ${name}!`;
    }
    console.log(greet("Alice")); // Hello, Alice!
    ```

    You can also use:
    - **Function expressions**
    ```js
    const add = function(a, b) {
        return a + b;
    };
    ```

    - **Arrow functions**
    ```js
    const multiply = (a, b) => a * b;
    ```

    **2️⃣ Conditionals**
    Run code only if certain conditions are met.
    ```js
    let score = 85;
    if (score >= 90) {
        console.log("A grade");
    } else if (score >= 80) {
        console.log("B grade");
    } else {
        console.log("Try again");
    }
    ```

    **3️⃣ Events**
    Add interactivity to the webpage.
    ```js
    document.getElementById("myButton").addEventListener("click", function() {
        alert("Button clicked!");
    });
    ```

    **Common events:** `click`, `mouseover`, `keydown`, `submit`.

    **Tasks:**
    ✅ Write a function that returns the square of a number.  
    ✅ Add an event listener to a button that changes text on click.  
    ✅ Use an if–else to check if a number is even or odd.

    **Deep Dive Resources:**
    - MDN JavaScript: [Functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Functions)
    - MDN: [Event Reference](https://developer.mozilla.org/en-US/docs/Web/Events)
    """
)


# Week 3: Day 3
Lesson.objects.filter(title="JavaScript DOM Manipulation").update(
    content="""
    # JavaScript + The DOM (Document Object Model)

    **DOM = how JS interacts with HTML.**

    **1️⃣ Selecting Elements**
    ```js
    document.getElementById("title");
    document.querySelector(".item");
    document.querySelectorAll("li");
    ```

    **2️⃣ Changing Content**
    ```js
    let title = document.getElementById("title");
    title.textContent = "New Title";
    title.style.color = "blue";
    ```

    **3️⃣ Creating/Removing Elements**
    ```js
    let newItem = document.createElement("li");
    newItem.textContent = "New List Item";
    document.querySelector("ul").appendChild(newItem);
    document.querySelector("ul").removeChild(newItem);
    ```

    **4️⃣ Changing Attributes**
    ```js
    let link = document.querySelector("a");
    link.setAttribute("href", "https://example.com");
    ```

    **Tasks:**
    ✅ Change the text of an existing HTML element.  
    ✅ Add a new `<li>` to an unordered list.  
    ✅ Remove a paragraph from the page.  
    ✅ Change an image’s `src` attribute.

    **Deep Dive Resources:**
    - MDN: [DOM Manipulation](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction)
    """
)


# Week 3: Day 4
Lesson.objects.filter(title="JavaScript Loops and Arrays").update(
    content="""
    # JavaScript Loops + Arrays

    **Loops = run code repeatedly.**

    **1️⃣ For Loops**
    ```js
    for (let i = 0; i < 5; i++) {
        console.log(i);
    }
    ```

    **2️⃣ While Loops**
    ```js
    let count = 0;
    while (count < 5) {
        console.log(count);
        count++;
    }
    ```

    **3️⃣ Arrays + Iteration**
    ```js
    let fruits = ["apple", "banana", "cherry"];
    fruits.forEach(fruit => console.log(fruit));

    for (let fruit of fruits) {
        console.log(fruit);
    }
    ```

    **4️⃣ Common Array Methods**
    ```js
    fruits.push("orange");
    fruits.pop();
    fruits.shift();
    fruits.unshift("kiwi");
    fruits.includes("banana");
    fruits.indexOf("apple");
    ```

    **Tasks:**
    ✅ Loop over an array and print each item.  
    ✅ Add/remove elements using array methods.  
    ✅ Write a loop that sums numbers in an array.  
    ✅ Filter an array for items longer than 5 characters.

    **Deep Dive Resources:**
    - MDN: [Loops](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Loops_and_iteration)
    - MDN: [Array Methods](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array)
    """
)


# Week 3: Day 5
Lesson.objects.filter(title="Project: JavaScript Interactive Feature").update(
    content="""
    # Project: Build Your First Interactive Feature

    **Objective:** Apply what you’ve learned to create a small but complete project.

    **Project Ideas:**
    - A **click counter** (button increases a displayed number).
    - A **to-do list** (add/remove tasks).
    - A **quiz app** (select answers, show results).
    - A **light/dark theme switcher**.

    **Project Requirements:**
    ✅ Use **functions** to organize logic.  
    ✅ Use **DOM manipulation** to update the page.  
    ✅ Attach at least **two event listeners** (e.g., click, submit).  
    ✅ Use at least one **array** to manage data.

    **Bonus Challenges:**
    🌟 Add CSS animations or transitions.  
    🌟 Make your design responsive (looks good on mobile).  
    🌟 Validate user input (e.g., don’t allow empty to-do items).

    **Final Tips:**
    - Start simple → expand gradually.
    - Test as you build.
    - Focus on **clear code** and **good user experience**.

    **Inspiration:**  
    Check CodePen, GitHub, or JSFiddle for mini-project inspiration!

    **Submission:** Upload your code to GitHub or share a live demo link.
    """
)


