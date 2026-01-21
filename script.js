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
        if (userEmail) {
            // User is logged in: Show icon, hide button, show history link
            if (getStartedNavBtn) getStartedNavBtn.classList.add('hidden');
            if (userProfileIcon) userProfileIcon.classList.remove('hidden');
            if (historyLinkContainer) historyLinkContainer.classList.remove('hidden');
        } else {
            // User is logged out: Hide icon, show button, hide history link
            if (getStartedNavBtn) getStartedNavBtn.classList.remove('hidden');
            if (userProfileIcon) userProfileIcon.classList.add('hidden');
            if (historyLinkContainer) historyLinkContainer.classList.add('hidden');
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
            
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
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
            messageEl.textContent = 'Could not connect to the server. Please try again.';
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
        if (authModal) {
            authModal.classList.add('show');
            document.body.style.overflow = 'hidden';
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

    // User profile icon click (logout)
    if (userProfileIcon) {
        userProfileIcon.addEventListener('click', () => {
            if (confirm('Do you want to log out?')) {
                localStorage.removeItem('userEmail');
                updateLoginState();
                // Optionally redirect to home page
                window.location.reload();
            }
        });
    }

    // --- Initial Page Load ---
    updateLoginState();
});