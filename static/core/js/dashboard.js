document.addEventListener('DOMContentLoaded', function() {
    const lessons = {
        week1: {
            day1: 'Introduction to HTML',
            day2: 'HTML Elements',
            day3: 'Forms and Inputs',
            day4: 'HTML5 Semantic Elements',
            day5: 'Project: Basic Webpage',
        },
        week2: {
            day1: 'Introduction to CSS',
            day2: 'Selectors and Properties',
            day3: 'Box Model and Flexbox',
            day4: 'CSS Grid',
            day5: 'Project: Styling a Webpage',
        },
        week3: {
            day1: 'Introduction to JavaScript',
            day2: 'Variables and Data Types',
            day3: 'Functions and Control Flow',
            day4: 'DOM Manipulation',
            day5: 'Project: Interactive Webpage',
        }
    };

    const assignments = [
        'Week 1 Assignment: Create a personal bio webpage using HTML.',
        'Week 2 Assignment: Style the personal bio webpage with CSS.',
        'Week 3 Assignment: Add interactivity to the bio webpage using JavaScript.'
    ];

    const tasks = [
        'Task 1: Create a simple contact form with HTML and CSS.',
        'Task 2: Design a blog post layout using CSS Grid.',
        'Task 3: Build a small interactive game using JavaScript.'
    ];

    const lessonWeeks = document.getElementById('lesson-weeks');
    const assignmentList = document.getElementById('assignment-list');
    const taskList = document.getElementById('task-list');

    for (const [week, days] of Object.entries(lessons)) {
        const weekDiv = document.createElement('div');
        weekDiv.classList.add('week');
        weekDiv.innerHTML = `<h4>${week}</h4>`;
        
        for (const [day, lesson] of Object.entries(days)) {
            const lessonItem = document.createElement('div');
            lessonItem.classList.add('day');
            lessonItem.innerText = `${day}: ${lesson}`;
            weekDiv.appendChild(lessonItem);
        }

        lessonWeeks.appendChild(weekDiv);
    }

    assignments.forEach(assignment => {
        const listItem = document.createElement('li');
        listItem.innerText = assignment;
        assignmentList.appendChild(listItem);
    });

    tasks.forEach(task => {
        const listItem = document.createElement('li');
        listItem.innerText = task;
        taskList.appendChild(listItem);
    });

    // Fetch and display user progress 
    async function fetchUserProgress() { 
        try { 
            const response = await fetch('http://localhost:8000/api/progress/', { 
                method: 'GET', 
                headers: { 
                    'Content-Type': 'application/json',
                 }, 
                 credentials: 'include' // Include cookies to send the sessionid 
                 }); 
                 if (response.ok) { 
                    const data = await response.json(); 
                    const progressBar = document.getElementById('progress-bar').children[0]; 
                    progressBar.style.width = `${data.progress_percentage}%`; 
                } else { 
                    console.error('Failed to fetch user progress'); 
                } 
            } catch (error) { 
                console.error('Error:', error); 
            } 
        } 
        
        fetchUserProgress(); 
});
