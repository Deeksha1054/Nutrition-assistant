// Mobile menu toggle
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');

mobileMenuBtn.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
});

const mobileLinks = mobileMenu.querySelectorAll('a');
mobileLinks.forEach(link => {
    link.addEventListener('click', () => {
        mobileMenu.classList.add('hidden');
    });
});

// AI Assistant functionality
const submitBtn = document.getElementById('submit-btn');
const queryInput = document.getElementById('query-input');
const responseText = document.getElementById('response-text');
const loading = document.getElementById('loading');

// Configure backend URL (replace with your deployed URL, e.g., 'https://your-app.onrender.com')
const BACKEND_URL = window.location.hostname.includes('localhost') 
    ? 'http://localhost:5000' 
    : 'https://your-app.onrender.com'; // Replace with your actual deployed URL

submitBtn.addEventListener('click', async () => {
    const query = queryInput.value.trim();
    
    if (!query) {
        alert('Please enter a nutrition question!');
        return;
    }

    // Show loading
    loading.classList.remove('hidden');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span>Processing...</span>';

    try {
        const response = await fetch(`${BACKEND_URL}/ask`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });

        const data = await response.json();
        
        if (response.ok) {
            responseText.innerHTML = data.response.replace(/\n/g, '<br>');
            console.log('Success:', data);
        } else {
            const errorMsg = data.error || data.response || 'Failed to process query.';
            responseText.innerHTML = `❌ Error: ${errorMsg}`;
            console.error('API Error:', { status: response.status, data });
        }
    } catch (error) {
        responseText.innerHTML = '❌ Sorry, there was an error connecting to the server. Please check your connection and try again.';
        console.error('Fetch Error:', error);
    } finally {
        loading.classList.add('hidden');
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<span>Get AI Response</span><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path></svg>';
    }
});

// Enter key support for textarea
queryInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
        submitBtn.click();
    }
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});