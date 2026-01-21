// script.js (Complete updated version for the landing page with multi-page navigation)

document.addEventListener('DOMContentLoaded', () => {

    // --- Element Selections ---
    const getStartedNavBtn = document.getElementById('getStartedNavBtn');
    const userProfileIcon = document.getElementById('userProfileIcon');
    const historyLinkContainer = document.getElementById('historyLinkContainer');
    const authModal = document.getElementById('authModal');
    const closeBtn = document.querySelector('.close-btn');

    // Buttons that open the login modal
    const openModalBtns = [
        document.getElementById('learnMoreBtn'), // The "Learn More" button in the hero section
        getStartedNavBtn // The "Log In" button in the nav
    ];

    // Buttons that navigate to the analyzer page
    const analyzeLeaseBtn = document.getElementById('analyzeLeaseBtn');
    const startFreeAnalysisBtn = document.getElementById('startFreeAnalysisBtn');

    // Form-related elements
    const showSignup = document.getElementById('showSignup');
    const showLogin = document.getElementById('showLogin');
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');

    // --- Core Functions ---

    /**
     * Checks localStorage to see if a user is logged in and updates the nav bar.
     */
    function updateLoginState() {
        const userEmail = localStorage.getItem('userEmail');
        console.log('Updating login state, user email:', userEmail); // Debug log
        
        if (userEmail) {
            // User is logged in: Show icon, hide button, show history link
            if (getStartedNavBtn) {
                getStartedNavBtn.classList.add('hidden');
                console.log('Hiding login button'); // Debug log
            }
            if (userProfileIcon) {
                userProfileIcon.classList.remove('hidden');
                userProfileIcon.title = `Logged in as ${userEmail}. Click to logout.`;
                console.log('Showing user icon'); // Debug log
            }
            if (historyLinkContainer) {
                historyLinkContainer.classList.remove('hidden');
                console.log('Showing history link'); // Debug log
            }
        } else {
            // User is logged out: Hide icon, show button, hide history link
            if (getStartedNavBtn) {
                getStartedNavBtn.classList.remove('hidden');
                console.log('Showing login button'); // Debug log
            }
            if (userProfileIcon) {
                userProfileIcon.classList.add('hidden');
                console.log('Hiding user icon'); // Debug log
            }
            if (historyLinkContainer) {
                historyLinkContainer.classList.add('hidden');
                console.log('Hiding history link'); // Debug log
            }
        }
    }

    /**
     * Handles the login/signup form submission.
     */
    const handleFormSubmit = async (form, url) => {
        const messageEl = form.querySelector('.form-message');
        const submitBtn = form.querySelector('button[type="submit"]');
        
        // Show loading state
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing...';
        }
        
        try {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            console.log('Submitting form to:', url); // Debug log
            console.log('Form data:', data); // Debug log
            
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            console.log('Response status:', response.status); // Debug log
            
            const result = await response.json();
            console.log('Response data:', result); // Debug log
            
            if (response.ok) {
                messageEl.textContent = result.message;
                messageEl.className = 'form-message success';

                if (result.email) {
                    localStorage.setItem('userEmail', result.email);
                    updateLoginState();
                }

                form.reset();
                setTimeout(closeModal, 1500);
            } else {
                messageEl.textContent = result.error || 'An error occurred.';
                messageEl.className = 'form-message error';
            }
        } catch (error) {
            console.error('Form submission error:', error);
            messageEl.textContent = 'Could not connect to the server. Please check your connection and try again.';
            messageEl.className = 'form-message error';
        } finally {
            // Reset button state
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = form.id === 'loginForm' ? 'Login' : 'Create Account';
            }
        }
    };

    /**
     * Opens the authentication modal.
     */
    function openModal() {
        console.log('openModal function called'); // Debug log
        if (authModal) {
            console.log('Modal found, showing it'); // Debug log
            authModal.classList.add('show');
            document.body.style.overflow = 'hidden';
        } else {
            console.log('Modal not found!'); // Debug log
        }
    }

    /**
     * Closes the authentication modal.
     */
    function closeModal() {
        if (authModal) {
            authModal.classList.remove('show');
            document.body.style.overflow = 'auto';
            
            // Clear any messages
            const messages = authModal.querySelectorAll('.form-message');
            messages.forEach(msg => {
                msg.textContent = '';
                msg.className = 'form-message';
            });
        }
    }

    /**
     * Navigates to the analyzer page if user is logged in, otherwise opens login modal.
     */
    function navigateToAnalyzer() {
        const userEmail = localStorage.getItem('userEmail');
        if (userEmail) {
            window.location.href = 'analyzer.html';
        } else {
            openModal();
        }
    }

    // --- Event Listeners ---

    // Open modal buttons
    openModalBtns.forEach(btn => {
        if (btn) {
            btn.addEventListener('click', openModal);
        }
    });

    // Navigate to analyzer buttons
    if (analyzeLeaseBtn) {
        analyzeLeaseBtn.addEventListener('click', navigateToAnalyzer);
    }
    if (startFreeAnalysisBtn) {
        startFreeAnalysisBtn.addEventListener('click', navigateToAnalyzer);
    }

    // Close modal
    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }

    // Close modal when clicking outside
    if (authModal) {
        authModal.addEventListener('click', (e) => {
            if (e.target === authModal) {
                closeModal();
            }
        });
    }

    // Form toggle buttons
    if (showSignup) {
        showSignup.addEventListener('click', (e) => {
            e.preventDefault();
            if (loginForm) loginForm.style.display = 'none';
            if (signupForm) signupForm.style.display = 'block';
        });
    }

    if (showLogin) {
        showLogin.addEventListener('click', (e) => {
            e.preventDefault();
            if (signupForm) signupForm.style.display = 'none';
            if (loginForm) loginForm.style.display = 'block';
        });
    }

    // Form submissions
    if (signupForm) {
        signupForm.addEventListener('submit', (e) => {
            e.preventDefault();
            handleFormSubmit(signupForm, '/api/register');
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            handleFormSubmit(loginForm, '/api/login');
        });
    }

    // User profile icon click (show login modal if not logged in, or show user menu if logged in)
    if (userProfileIcon) {
        userProfileIcon.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            console.log('User icon clicked'); // Debug log
            
            const userEmail = localStorage.getItem('userEmail');
            console.log('Current user email:', userEmail); // Debug log
            
            if (userEmail) {
                // User is logged in, show logout option
                const confirmMessage = `Logged in as: ${userEmail}\n\nDo you want to log out?`;
                if (confirm(confirmMessage)) {
                    localStorage.removeItem('userEmail');
                    updateLoginState();
                    window.location.reload();
                }
            } else {
                // User is not logged in, show login modal
                console.log('Opening login modal'); // Debug log
                openModal();
            }
        });
        
        // Add visual feedback
        userProfileIcon.style.cursor = 'pointer';
        userProfileIcon.title = 'Click to login or manage account';
    } else {
        console.log('User profile icon not found'); // Debug log
    }

    // --- Initial Page Load ---
    updateLoginState();
});