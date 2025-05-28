document.addEventListener('DOMContentLoaded', function() {
    // Configuration
    const config = {
        baseUrl: window.location.hostname === 'localhost' 
                ? 'http://localhost:8000' 
                : 'https://skill-development-and-certification.onrender.com',
        carouselInterval: 8000, // 8 seconds
        apiEndpoints: {
            lessons: '/lessons/',
            progress: '/progress/'
        }
    };

    // DOM Elements
    const elements = {
        lessonWeeks: document.getElementById('lesson-weeks'),
        assignmentList: document.getElementById('assignment-list'),
        taskList: document.getElementById('task-list'),
        progressBar: document.getElementById('progress-bar')?.children[0],
        carouselItems: document.querySelectorAll('.carousel-item')
    };

    // Sample Data (fallback if API fails)
    const sampleData = {
        assignments: [
            'Week 1 Assignment: Create a personal bio webpage using HTML.',
            'Week 2 Assignment: Style the personal bio webpage with CSS.',
            'Week 3 Assignment: Add interactivity to the bio webpage using JavaScript.'
        ],
        tasks: [
            'Task 1: Create a simple contact form with HTML and CSS.',
            'Task 2: Design a blog post layout using CSS Grid.',
            'Task 3: Build a small interactive game using JavaScript.'
        ]
    };

    // API Fetch Functions
    async function fetchData(url) {
        try {
            const response = await fetch(`${config.baseUrl}${url}`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include'
            });
            
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error(`Error fetching ${url}:`, error);
            return null;
        }
    }

    // Lesson Display
    async function displayLessons() {
        if (!elements.lessonWeeks) return;
        
        const lessons = await fetchData(config.apiEndpoints.lessons) || [];
        
        if (lessons.length === 0) {
            elements.lessonWeeks.innerHTML = '<p>No lessons available at the moment.</p>';
            return;
        }

        lessons.forEach(lesson => {
            const weekDiv = document.createElement('div');
            weekDiv.className = 'week';
            weekDiv.innerHTML = `<h4>Week ${lesson.week}</h4>`;
            
            lesson.days.forEach(day => {
                const lessonItem = document.createElement('div');
                lessonItem.className = 'day';
                lessonItem.innerHTML = `
                    <span class="day-name">${day}:</span>
                    <span class="lesson-name">${lesson.name}</span>
                `;
                weekDiv.appendChild(lessonItem);
            });

            elements.lessonWeeks.appendChild(weekDiv);
        });
    }

    // Progress Display
    async function displayProgress() {
        if (!elements.progressBar) return;
        
        const progressData = await fetchData(config.apiEndpoints.progress);
        const percentage = progressData?.progress_percentage || 0;
        
        elements.progressBar.style.width = `${percentage}%`;
        elements.progressBar.setAttribute('aria-valuenow', percentage);
        elements.progressBar.textContent = `${percentage}%`;
    }

    // Static Content Display
    function displayStaticContent() {
        // Assignments
        if (elements.assignmentList) {
            sampleData.assignments.forEach(assignment => {
                const listItem = document.createElement('li');
                listItem.className = 'assignment-item';
                listItem.innerHTML = `
                    <input type="checkbox" id="assignment-${sampleData.assignments.indexOf(assignment)}">
                    <label for="assignment-${sampleData.assignments.indexOf(assignment)}">${assignment}</label>
                `;
                elements.assignmentList.appendChild(listItem);
            });
        }

        // Tasks
        if (elements.taskList) {
            sampleData.tasks.forEach(task => {
                const listItem = document.createElement('li');
                listItem.className = 'task-item';
                listItem.innerHTML = `
                    <input type="checkbox" id="task-${sampleData.tasks.indexOf(task)}">
                    <label for="task-${sampleData.tasks.indexOf(task)}">${task}</label>
                `;
                elements.taskList.appendChild(listItem);
            });
        }
    }

    // Carousel Functionality
    function initCarousel() {
        if (elements.carouselItems.length === 0) return;
        
        let currentIndex = 0;
        const dotsContainer = document.createElement('div');
        dotsContainer.className = 'carousel-dots';
        
        // Create dots
        elements.carouselItems.forEach((_, index) => {
            const dot = document.createElement('button');
            dot.className = 'carousel-dot';
            dot.setAttribute('aria-label', `Go to slide ${index + 1}`);
            dot.addEventListener('click', () => showSlide(index));
            dotsContainer.appendChild(dot);
        });
        
        document.querySelector('.carousel').appendChild(dotsContainer);
        const dots = document.querySelectorAll('.carousel-dot');
        
        function showSlide(index) {
            // Update current index
            currentIndex = (index + elements.carouselItems.length) % elements.carouselItems.length;
            
            // Update slides
            elements.carouselItems.forEach((item, i) => {
                item.classList.toggle('active', i === currentIndex);
            });
            
            // Update dots
            dots.forEach((dot, i) => {
                dot.classList.toggle('active', i === currentIndex);
            });
        }
        
        // Auto-rotation
        let carouselInterval = setInterval(() => {
            showSlide(currentIndex + 1);
        }, config.carouselInterval);
        
        // Pause on hover
        const carousel = document.querySelector('.carousel');
        carousel.addEventListener('mouseenter', () => clearInterval(carouselInterval));
        carousel.addEventListener('mouseleave', () => {
            carouselInterval = setInterval(() => {
                showSlide(currentIndex + 1);
            }, config.carouselInterval);
        });
        
        // Keyboard navigation
        carousel.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') showSlide(currentIndex - 1);
            if (e.key === 'ArrowRight') showSlide(currentIndex + 1);
        });
        
        // Initialize first slide
        showSlide(0);
    }

    // Accessibility Enhancements
    function enhanceAccessibility() {
        // Add focus styles
        const focusableElements = document.querySelectorAll(
            'a, button, input, select, textarea, [tabindex]'
        );
        
        focusableElements.forEach(el => {
            el.addEventListener('focus', () => {
                el.style.outline = '2px solid #004466';
                el.style.outlineOffset = '3px';
            });
            
            el.addEventListener('blur', () => {
                el.style.outline = 'none';
            });
        });
        
        // Make carousel items focusable
        elements.carouselItems.forEach(item => {
            item.setAttribute('tabindex', '0');
        });
    }

    // Mobile Menu Toggle
    function initMobileMenu() {
        const menuToggle = document.createElement('button');
        menuToggle.className = 'menu-toggle';
        menuToggle.innerHTML = '☰ Menu';
        menuToggle.setAttribute('aria-label', 'Toggle navigation menu');
        
        const headerRight = document.querySelector('.header-right');
        
        if (window.innerWidth < 768 && headerRight) {
            headerRight.style.display = 'none';
            document.querySelector('.dashboard header').prepend(menuToggle);
            
            menuToggle.addEventListener('click', () => {
                const isHidden = headerRight.style.display === 'none';
                headerRight.style.display = isHidden ? 'flex' : 'none';
                menuToggle.setAttribute('aria-expanded', isHidden);
            });
            
            window.addEventListener('resize', () => {
                if (window.innerWidth >= 768) {
                    headerRight.style.display = 'flex';
                    menuToggle.remove();
                }
            });
        }
    }

    // Initialize all functionality
    function init() {
        displayLessons();
        displayProgress();
        displayStaticContent();
        initCarousel();
        enhanceAccessibility();
        initMobileMenu();
    }

    init();
});