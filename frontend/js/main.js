/* ===================================
   PORTFOLIO INTERACTIVE FEATURES
   JavaScript for Cloud Developer Portfolio
   =================================== */

// Wait for DOM to fully load before running scripts
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Portfolio JavaScript loaded successfully!');
    
    // Initialize all features. Set each one up only here: calling these again
    // elsewhere adds duplicate buttons and duplicate form submit handlers.
    initSmoothScrolling();
    initSkillsAnimation();
    initProjectHoverEffects();
    initMobileMenu();
    initScrollToTop();
    
    // Skills and the contact form depend on whether the Python backend is reachable
    initializeWithAPI();
    
    console.log('✅ All interactive features initialized!');
});

/* ===================================
   1. SMOOTH SCROLLING NAVIGATION
   =================================== */

function initSmoothScrolling() {
    // Select all navigation links that start with #
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault(); // Stop default jump behavior
            
            // Get target section ID from href
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                // Smooth scroll to target
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Update URL without jumping
                history.pushState(null, null, targetId);
            }
        });
    });
    
    console.log('✅ Smooth scrolling enabled');
}

/* ===================================
   2. ANIMATED PROGRESS BARS
   =================================== */

function initProgressBars() {
    const progressBars = document.querySelectorAll('.progress');
    
    if (progressBars.length === 0) {
        console.log('⚠️ No progress bars found');
        return;
    }
    
    // Skill completion percentages
const skillProgress = {
    'english': 100,
    'mathematics': 100,
    'html': 100,
    'css': 100,
    'javascript': 100,
    'python': 100,
    'git': 100,
    'linux': 100,
    'sql': 100,  // 🎉 You just mastered this!
    'kubernetes': 0
};
    
    // Create Intersection Observer to detect when progress bars are visible
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const skillName = progressBar.getAttribute('data-skill');
                
                // Only animate once
                if (!progressBar.classList.contains('animated')) {
                    progressBar.classList.add('animated');
                    animateProgressBar(progressBar, skillName, skillProgress);
                }
            }
        });
    }, {
        threshold: 0.5, // Trigger when 50% visible
        rootMargin: '0px 0px -50px 0px' // Start slightly before entering viewport
    });
    
    // Observe all progress bars
    progressBars.forEach(bar => observer.observe(bar));
    
    console.log('✅ Progress bar animations ready');

}

function animateProgressBar(progressBar, skillName, skillProgress) {
    const targetWidth = skillProgress[skillName] || 0;
    let currentWidth = 0;
    
    // Smooth animation
    const animation = setInterval(() => {
        if (currentWidth >= targetWidth) {
            clearInterval(animation);
            progressBar.style.width = targetWidth + '%';
            progressBar.textContent = targetWidth + '%';
            return;
        }
        
        // Increment by 2% each step
        currentWidth += 2;
        progressBar.style.width = currentWidth + '%';
        progressBar.textContent = currentWidth + '%';
    }, 20); // 20ms intervals = smooth 50fps animation
}

/* ===================================
   3. CONTACT FORM VALIDATION
   =================================== */

// Real-time email check for the contact form. The form's submit handler is in
// initContactFormWithAPI, so this function doesn't add another one.
function initEmailValidation() {
    const emailInput = document.querySelector('#email');
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            const email = this.value;
            if (email && !isValidEmail(email)) {
                this.style.borderColor = '#e74c3c';
                showInputError(this, 'Please enter a valid email address');
            } else {
                this.style.borderColor = '';
                removeInputError(this);
            }
        });
    }
    
    console.log('✅ Contact form validation enabled');
}

function isValidEmail(email) {
    // Regex pattern for email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showFormMessage(text, type) {
    // Remove existing messages
    const existingMessage = document.querySelector('.form-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create new message
    const message = document.createElement('div');
    message.className = `form-message ${type}`;
    message.innerHTML = text;
    
    // Style based on type
    const styles = type === 'success' 
        ? 'background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb;'
        : 'background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;';
    
    message.style.cssText = `
        padding: 15px;
        margin: 20px 0;
        border-radius: 5px;
        font-weight: 600;
        text-align: center;
        animation: slideIn 0.3s ease;
        ${styles}
    `;
    
    // Add to form
    const form = document.querySelector('form');
    form.appendChild(message);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        message.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => message.remove(), 300);
    }, 5000);
}

function showInputError(input, message) {
    removeInputError(input); // Clear existing errors
    
    const error = document.createElement('small');
    error.className = 'input-error';
    error.textContent = message;
    error.style.cssText = 'color: #e74c3c; font-size: 0.9rem; margin-top: 5px; display: block;';
    
    input.parentElement.appendChild(error);
}

function removeInputError(input) {
    const error = input.parentElement.querySelector('.input-error');
    if (error) error.remove();
}

/* ===================================
   4. SKILLS SECTION ANIMATION
   =================================== */

function initSkillsAnimation() {
    const skillItems = document.querySelectorAll('.skill-item');
    
    if (skillItems.length === 0) {
        console.log('⚠️ No skill items found');
        return;
    }
    
    // Create observer for staggered animation
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Stagger animation (each item delayed by 100ms)
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100);
                
                // Stop observing once animated
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.2
    });
    
    // Set initial state and observe
    skillItems.forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(30px)';
        item.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(item);
    });
    
    console.log('✅ Skills animation ready');
}

/* ===================================
   5. PROJECT HOVER EFFECTS
   =================================== */

function initProjectHoverEffects() {
    const projects = document.querySelectorAll('.project');
    
    projects.forEach(project => {
        project.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(10px)';
        });
        
        project.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
        });
    });
    
    console.log('✅ Project hover effects enabled');
}

/* ===================================
   6. MOBILE MENU TOGGLE
   =================================== */

function initMobileMenu() {
    // This is a placeholder for mobile menu functionality
    // We'll expand this if needed
    
    const nav = document.querySelector('nav ul');
    
    // Check if mobile view
    if (window.innerWidth <= 768) {
        console.log('📱 Mobile view detected');
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth <= 768) {
            console.log('📱 Switched to mobile view');
        } else {
            console.log('🖥️ Switched to desktop view');
        }
    });
}

/* ===================================
   7. SCROLL TO TOP BUTTON
   =================================== */

function initScrollToTop() {
    // Create scroll-to-top button
    const scrollBtn = document.createElement('button');
    scrollBtn.className = 'scroll-to-top';
    scrollBtn.innerHTML = '↑';
    scrollBtn.setAttribute('aria-label', 'Scroll to top');
    
    // Style the button
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50%;
        font-size: 24px;
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: opacity 0.3s ease, visibility 0.3s ease, transform 0.3s ease;
        z-index: 999;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    `;
    
    document.body.appendChild(scrollBtn);
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', function() {
        if (window.scrollY > 500) {
            scrollBtn.style.opacity = '1';
            scrollBtn.style.visibility = 'visible';
        } else {
            scrollBtn.style.opacity = '0';
            scrollBtn.style.visibility = 'hidden';
        }
    });
    
    // Scroll to top when clicked
    scrollBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Hover effect
    scrollBtn.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1)';
    });
    
    scrollBtn.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
    });
    
    console.log('✅ Scroll-to-top button created');
}

/* ===================================
   8. UTILITY FUNCTIONS
   =================================== */

// Debounce function (limits how often a function runs)
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function (ensures function runs at most once per interval)
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Example usage of debounce for scroll events
const handleScroll = debounce(() => {
    console.log('Scroll event (debounced)');
}, 200);

window.addEventListener('scroll', handleScroll);

/* ===================================
   9. CONSOLE BRANDING (OPTIONAL FUN)
   =================================== */

console.log('%c💼 Cloud Developer Portfolio', 'font-size: 20px; font-weight: bold; color: #667eea;');
console.log('%c Built with HTML, CSS, and JavaScript', 'font-size: 12px; color: #666;');
console.log('%c⚡ All systems operational!', 'font-size: 12px; color: #27ae60; font-weight: bold;');

// Add this new function to your main.js

async function loadSkillsFromAPI() {
    try {
        const response = await fetch(`${API_BASE_URL}/skills`);
        const result = await response.json();
        
        if (result.success) {
            console.log('✅ Skills loaded from Python backend:', result.data);
            updateSkillsDisplay(result.data);
        } else {
            console.error('❌ Error loading skills:', result.error);
        }
    } catch (error) {
        console.error('❌ Failed to connect to backend:', error);
        console.log('ℹ️ Using hardcoded data instead');
    }
}

function updateSkillsDisplay(skills) {
    skills.forEach(skill => {
        const progressBar = document.querySelector(`[data-skill="${skill.name.toLowerCase()}"]`);
        if (progressBar) {
            // Update progress bar with data from Python
            setTimeout(() => {
                progressBar.style.width = skill.level + '%';
                progressBar.textContent = skill.level + '%';
            }, 500);
        }
    });
}

// Update contact form to use Python backend
async function submitContactForm(name, email, message) {
    try {
        const response = await fetch(`${API_BASE_URL}/contact`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email, message })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showFormMessage(result.message, 'success');
        } else {
            showFormMessage(result.error, 'error');
        }
    } catch (error) {
        showFormMessage('Failed to send message. Please try again.', 'error');
        console.error('Error:', error);
    }
}

/* ===================================
   API CONFIGURATION
   =================================== */

const API_BASE_URL = ['localhost', '127.0.0.1', ''].includes(location.hostname)
    ? 'http://localhost:5000/api'
    : '/api';

// Helper function for API calls
async function apiCall(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };
    
    try {
        const response = await fetch(url, mergedOptions);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || `HTTP error: ${response.status}`);
        }
        
        return data;
    } catch (error) {
        console.error(`API Error (${endpoint}):`, error);
        throw error;
    }
}


/* ===================================
   LOAD SKILLS FROM PYTHON BACKEND
   =================================== */

async function loadSkillsFromAPI() {
    try {
        console.log('📡 Fetching skills from Python backend...');
        
        const result = await apiCall('/skills');
        
        if (result.success) {
            console.log('✅ Skills loaded:', result.data);
            updateSkillsDisplay(result.data);
            return result.data;
        } else {
            throw new Error(result.error);
        }
    } catch (error) {
        console.error('❌ Failed to load skills from backend:', error.message);
        console.log('ℹ️ Using default progress bar animation instead');
        // Fall back to existing animation
        return null;
    }
}

function updateSkillsDisplay(skills) {
    skills.forEach((skill, index) => {
        // Find progress bar by data-skill attribute
        const skillName = skill.name.toLowerCase();
        const progressBar = document.querySelector(`[data-skill="${skillName}"]`);
        
        if (progressBar) {
            // Animate progress bar with stagger
            setTimeout(() => {
                progressBar.style.width = skill.level + '%';
                progressBar.textContent = skill.level + '%';
                
                // Update status text if it exists
                const skillItem = progressBar.closest('.skill-item');
                if (skillItem) {
                    const statusElement = skillItem.querySelector('strong');
                    if (statusElement && statusElement.textContent.includes('Status')) {
                        const statusEmoji = skill.level >= 75 ? '✅' : skill.level > 0 ? '⏳' : '📅';
                        statusElement.nextSibling.textContent = ` ${statusEmoji} ${skill.status}`;
                    }
                }
            }, index * 100);
        }
    });
}


/* ===================================
   SUBMIT CONTACT FORM TO PYTHON BACKEND
   =================================== */

async function submitContactFormToAPI(formData) {
    try {
        console.log('📧 Submitting contact form to Python backend...');
        
        const result = await apiCall('/contact', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        if (result.success) {
            console.log('✅ Contact form submitted:', result);
            return result;
        } else {
            throw new Error(result.error);
        }
    } catch (error) {
        console.error('❌ Failed to submit contact form:', error.message);
        throw error;
    }
}

// The contact form's only submit handler. It's set up only when the Python backend is reachable.
function initContactFormWithAPI() {
    const form = document.querySelector('form');
    
    if (!form) {
        console.log('⚠️ No contact form found');
        return;
    }
    
    initEmailValidation();
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(form);
        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            subject: formData.get('subject') || '',
            message: formData.get('message')
        };
        
        // Client-side validation
        if (!data.name || data.name.trim().length < 2) {
            showFormMessage('Please enter your name (at least 2 characters)', 'error');
            return;
        }
        
        if (!data.email || !isValidEmail(data.email)) {
            showFormMessage('Please enter a valid email address', 'error');
            return;
        }
        
        if (!data.message || data.message.trim().length < 10) {
            showFormMessage('Please enter a message (at least 10 characters)', 'error');
            return;
        }
        
        // Disable submit button while processing
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.textContent = 'Sending...';
        
        try {
            const result = await submitContactFormToAPI(data);
            showFormMessage(result.message, 'success');
            form.reset();
        } catch (error) {
            // Try to show specific error from API, or fallback message
            const errorMessage = error.message || 'Failed to send message. Please try again.';
            showFormMessage(errorMessage, 'error');
        } finally {
            // Re-enable button
            submitButton.disabled = false;
            submitButton.textContent = originalText;
        }
    });
    
    console.log('✅ Contact form connected to Python backend');
}

// Used when there's no backend (for example on GitHub Pages). Nothing could send
// the message, so hide the form instead of showing a fake "message received".
function hideContactForm() {
    const form = document.querySelector('form');
    if (form) {
        form.style.display = 'none';
        console.log('ℹ️ Contact form hidden: no backend to send messages');
    }
}


/* ===================================
   LOAD PROGRESS ANALYTICS
   =================================== */

async function loadProgressAnalytics() {
    try {
        const result = await apiCall('/analytics/progress');
        
        if (result.success) {
            console.log('📊 Progress analytics:', result.data);
            displayProgressAnalytics(result.data);
            return result.data;
        }
    } catch (error) {
        console.error('❌ Failed to load analytics:', error.message);
    }
}

function displayProgressAnalytics(analytics) {
    // You could display this in a dashboard section
    console.log(`
📊 Portfolio Progress Report:
   Total Skills: ${analytics.total_skills}
   Completed: ${analytics.completed_skills}
   Learning: ${analytics.learning_skills}
   Upcoming: ${analytics.upcoming_skills}
   Average Progress: ${analytics.average_progress}%
   Completion Rate: ${analytics.completion_rate}%
    `);
}


/* ===================================
   AWS COST CALCULATOR
   =================================== */

async function calculateAWSCost(storageGB) {
    try {
        const result = await apiCall('/calculate-cost', {
            method: 'POST',
            body: JSON.stringify({ storageGB: parseInt(storageGB) })
        });
        
        if (result.success) {
            console.log('💰 Cost calculation:', result.data);
            return result.data;
        }
    } catch (error) {
        console.error('❌ Failed to calculate cost:', error.message);
        throw error;
    }
}


/* ===================================
   CHECK API HEALTH
   =================================== */

async function checkAPIHealth() {
    try {
        const result = await apiCall('/health');
        
        if (result.success && result.data.status === 'healthy') {
            console.log('✅ Python backend is healthy');
            return true;
        }
        return false;
    } catch (error) {
        console.log('⚠️ Python backend is not available');
        console.log('ℹ️ Start it with: cd python-backend && python app.py');
        return false;
    }
}


/* ===================================
   INITIALIZE WITH API
   =================================== */

async function initializeWithAPI() {
    // Check if backend is available
    const isHealthy = await checkAPIHealth();
    
    if (isHealthy) {
        // Connect contact form to backend first, so it's ready while skills load
        initContactFormWithAPI();
        
        // Load skills from Python backend, or animate the built-in values if that fails
        const skills = await loadSkillsFromAPI();
        if (!skills) {
            initProgressBars();
        }
        
        // Load analytics
        await loadProgressAnalytics();
        
        console.log('🚀 Frontend connected to Python backend!');
    } else {
        // No backend here (for example on GitHub Pages), so the form couldn't send
        // anything. Hide it; the email link under it still works.
        console.log('📴 Running in offline mode (no backend)');
        hideContactForm();
        initProgressBars(); // Use original animation
    }
}

// Contact form submission
const contactForm = document.getElementById('contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            subject: document.getElementById('subject').value,
            message: document.getElementById('message').value
        };
        
        try {
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                showNotification('success', result.message);
                contactForm.reset();
            } else {
                showNotification('error', result.error || 'Something went wrong');
            }
        } catch (error) {
            showNotification('error', 'Failed to send message. Please try again.');
        }
    });
}

// Track page views
async function trackPageView() {
    try {
        await fetch('/api/pageview', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                path: window.location.pathname,
                referrer: document.referrer
            })
        });
    } catch (error) {
        console.log('Analytics tracking failed:', error);
    }
}

// Track on page load
document.addEventListener('DOMContentLoaded', trackPageView);

// Notification helper
function showNotification(type, message) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}