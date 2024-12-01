document.addEventListener('DOMContentLoaded', function () {
    const lessonWeeks = document.getElementById('lesson-weeks');
    
    // Proceed only if lessonWeeks exists
    if (lessonWeeks) {
        async function fetchLessons() {
            try {
                const response = await fetch('http://localhost:8000/api/lessons/', { 
                    method: 'GET', 
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include' // Include cookies to send the sessionid 
                });

                if (response.ok) {
                    const data = await response.json();

                    data.forEach(lesson => {
                        const weekDiv = document.createElement('div');
                        weekDiv.classList.add('week');
                        weekDiv.innerHTML = `<h4>Week ${lesson.week}</h4>`;
                        
                        lesson.days.forEach(day => {
                            const lessonItem = document.createElement('div');
                            lessonItem.classList.add('day');
                            lessonItem.innerText = `${day}: ${lesson.name}`;
                            weekDiv.appendChild(lessonItem);
                        });

                        lessonWeeks.appendChild(weekDiv);
                    });
                } else {
                    console.error('Failed to fetch lessons');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }

        fetchLessons();
    } else {
        console.error('Element with id "lesson-weeks" not found in the DOM.');
    }

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

    const assignmentList = document.getElementById('assignment-list');
    const taskList = document.getElementById('task-list');

    // Proceed only if assignmentList and taskList exist
    if (assignmentList) {
        assignments.forEach(assignment => {
            const listItem = document.createElement('li');
            listItem.innerText = assignment;
            assignmentList.appendChild(listItem);
        });
    } else {
        console.error('Element with id "assignment-list" not found in the DOM.');
    }

    if (taskList) {
        tasks.forEach(task => {
            const listItem = document.createElement('li');
            listItem.innerText = task;
            taskList.appendChild(listItem);
        });
    } else {
        console.error('Element with id "task-list" not found in the DOM.');
    }

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
                const progressBar = document.getElementById('progress-bar')?.children[0]; 
                
                if (progressBar) {
                    progressBar.style.width = `${data.progress_percentage}%`;
                } else {
                    console.error('Element with id "progress-bar" not found or has no children.');
                }
            } else { 
                console.error('Failed to fetch user progress'); 
            } 
        } catch (error) { 
            console.error('Error:', error); 
        } 
    } 

    fetchUserProgress();     
});
