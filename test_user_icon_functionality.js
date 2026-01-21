// Test script to verify user icon functionality
// Run this in browser console on http://localhost:5000

console.log('🔍 Testing User Icon Functionality');

// Test 1: Check if user icon exists
const userIcon = document.getElementById('userProfileIcon');
if (userIcon) {
    console.log('✅ User icon found');
    
    // Test 2: Check if it's clickable
    const hasClickListener = userIcon.onclick !== null || userIcon.addEventListener;
    console.log(hasClickListener ? '✅ User icon is clickable' : '❌ User icon not clickable');
    
    // Test 3: Check visibility
    const isVisible = !userIcon.classList.contains('hidden') && userIcon.style.display !== 'none';
    console.log(isVisible ? '✅ User icon is visible' : '❌ User icon is hidden');
    
} else {
    console.log('❌ User icon not found');
}

// Test 4: Check if modal exists
const modal = document.getElementById('authModal');
if (modal) {
    console.log('✅ Auth modal found');
    
    // Test 5: Check modal CSS
    const modalStyles = window.getComputedStyle(modal);
    const hasShowClass = modal.classList.contains('show');
    console.log(`Modal display: ${modalStyles.display}, Has show class: ${hasShowClass}`);
    
} else {
    console.log('❌ Auth modal not found');
}

// Test 6: Test login state
const userEmail = localStorage.getItem('userEmail');
console.log(`Current login state: ${userEmail ? `Logged in as ${userEmail}` : 'Not logged in'}`);

// Test 7: Simulate user icon click
if (userIcon) {
    console.log('🖱️ Simulating user icon click...');
    userIcon.click();
}

console.log('🏁 User icon functionality test complete');