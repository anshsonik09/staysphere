// Enhanced JavaScript for StaySphere

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all enhanced features
    initBackToTop();
    initNavbarScroll();
    initSmoothScroll();
    initFormValidation();
    initTooltips();
    initCounters();
    initProgressBars();
    initLazyLoading();
});

// Back to Top Button
function initBackToTop() {
    const backToTopButton = document.getElementById('backToTop');
    
    if (backToTopButton) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('show');
            } else {
                backToTopButton.classList.remove('show');
            }
        });
        
        backToTopButton.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// Navbar Scroll Effect
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
}

// Smooth Scroll for Anchor Links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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
}

// Enhanced Form Validation
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            
            form.classList.add('was-validated');
            
            // Add custom validation feedback
            const invalidInputs = form.querySelectorAll(':invalid');
            invalidInputs.forEach(input => {
                input.classList.add('is-invalid');
                showValidationMessage(input);
            });
        });
        
        // Remove validation feedback on input
        form.querySelectorAll('input, select, textarea').forEach(input => {
            input.addEventListener('input', function() {
                if (this.checkValidity()) {
                    this.classList.remove('is-invalid');
                    hideValidationMessage(this);
                }
            });
        });
    });
}

// Show Validation Message
function showValidationMessage(input) {
    let message = input.getAttribute('data-validation-message') || 'This field is required';
    
    if (input.type === 'email') {
        message = 'Please enter a valid email address';
    } else if (input.type === 'tel') {
        message = 'Please enter a valid phone number';
    }
    
    const feedbackDiv = document.createElement('div');
    feedbackDiv.className = 'invalid-feedback';
    feedbackDiv.textContent = message;
    feedbackDiv.setAttribute('id', input.id + '-feedback');
    
    const existingFeedback = document.getElementById(input.id + '-feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }
    
    input.parentNode.appendChild(feedbackDiv);
}

// Hide Validation Message
function hideValidationMessage(input) {
    const feedback = document.getElementById(input.id + '-feedback');
    if (feedback) {
        feedback.remove();
    }
}

// Initialize Tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Animated Counters
function initCounters() {
    const counters = document.querySelectorAll('.counter');
    
    const countUp = (counter) => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000; // 2 seconds
        const step = target / (duration / 16); // 60fps
        let current = 0;
        
        const updateCounter = () => {
            current += step;
            if (current < target) {
                counter.textContent = Math.ceil(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        };
        
        updateCounter();
    };
    
    // Use Intersection Observer to trigger counter animation
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                countUp(entry.target);
                observer.unobserve(entry.target);
            }
        });
    });
    
    counters.forEach(counter => {
        observer.observe(counter);
    });
}

// Animated Progress Bars
function initProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar-animated');
    
    const animateProgressBar = (progressBar) => {
        const target = parseInt(progressBar.getAttribute('data-target'));
        const duration = 1500;
        const step = target / (duration / 16);
        let current = 0;
        
        const updateProgress = () => {
            current += step;
            if (current < target) {
                progressBar.style.width = current + '%';
                progressBar.setAttribute('aria-valuenow', current);
                requestAnimationFrame(updateProgress);
            } else {
                progressBar.style.width = target + '%';
                progressBar.setAttribute('aria-valuenow', target);
            }
        };
        
        updateProgress();
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateProgressBar(entry.target);
                observer.unobserve(entry.target);
            }
        });
    });
    
    progressBars.forEach(bar => {
        observer.observe(bar);
    });
}

// Lazy Loading for Images
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.getAttribute('data-src');
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => {
        imageObserver.observe(img);
    });
}

// Enhanced Cart Functionality
class EnhancedCart {
    constructor() {
        this.cart = JSON.parse(localStorage.getItem('cart') || '{}');
        this.init();
    }
    
    init() {
        this.updateCartUI();
        this.bindEvents();
    }
    
    bindEvents() {
        document.addEventListener('click', (e) => {
            if (e.target.matches('.add-to-cart-btn')) {
                this.addToCart(e.target);
            }
            if (e.target.matches('.remove-from-cart')) {
                this.removeFromCart(e.target);
            }
            if (e.target.matches('.update-quantity')) {
                this.updateQuantity(e.target);
            }
        });
    }
    
    addToCart(button) {
        const itemId = button.dataset.itemId;
        const itemName = button.dataset.itemName;
        const itemPrice = parseFloat(button.dataset.itemPrice);
        
        if (this.cart[itemId]) {
            this.cart[itemId] += 1;
        } else {
            this.cart[itemId] = 1;
        }
        
        this.saveCart();
        this.updateCartUI();
        this.showNotification(`${itemName} added to cart!`, 'success');
        
        // Button animation
        button.classList.add('added');
        button.disabled = true;
        setTimeout(() => {
            button.classList.remove('added');
            button.disabled = false;
        }, 1000);
    }
    
    removeFromCart(button) {
        const itemId = button.dataset.itemId;
        delete this.cart[itemId];
        this.saveCart();
        this.updateCartUI();
        this.showNotification('Item removed from cart', 'info');
    }
    
    updateQuantity(button) {
        const itemId = button.dataset.itemId;
        const action = button.dataset.action;
        
        if (action === 'increase') {
            this.cart[itemId] += 1;
        } else if (action === 'decrease' && this.cart[itemId] > 1) {
            this.cart[itemId] -= 1;
        } else if (action === 'decrease' && this.cart[itemId] === 1) {
            delete this.cart[itemId];
        }
        
        this.saveCart();
        this.updateCartUI();
    }
    
    saveCart() {
        localStorage.setItem('cart', JSON.stringify(this.cart));
    }
    
    updateCartUI() {
        const cartCount = Object.values(this.cart).reduce((sum, qty) => sum + qty, 0);
        const cartCountElements = document.querySelectorAll('.cart-count');
        
        cartCountElements.forEach(element => {
            element.textContent = cartCount;
        });
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
        notification.style.zIndex = '9999';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Initialize Enhanced Cart
const enhancedCart = new EnhancedCart();

// Enhanced Search Functionality
class EnhancedSearch {
    constructor() {
        this.searchInput = document.querySelector('.search-input');
        this.searchResults = document.querySelector('.search-results');
        this.init();
    }
    
    init() {
        if (this.searchInput) {
            this.searchInput.addEventListener('input', this.debounce(this.handleSearch.bind(this), 300));
            this.searchInput.addEventListener('focus', () => this.showResults());
            document.addEventListener('click', (e) => {
                if (!e.target.closest('.search-container')) {
                    this.hideResults();
                }
            });
        }
    }
    
    async handleSearch(e) {
        const query = e.target.value.trim();
        
        if (query.length < 2) {
            this.hideResults();
            return;
        }
        
        // Show loading state
        this.showLoading();
        
        try {
            // Simulate API call
            const results = await this.performSearch(query);
            this.displayResults(results);
        } catch (error) {
            this.showError('Search failed. Please try again.');
        }
    }
    
    async performSearch(query) {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 300));
        
        // Mock search results
        return [
            { id: 1, title: 'Deluxe Room', type: 'room', price: 2999 },
            { id: 2, title: 'Paneer Tikka', type: 'food', price: 299 },
            { id: 3, title: 'Swimming Pool', type: 'facility', price: 500 }
        ].filter(item => 
            item.title.toLowerCase().includes(query.toLowerCase())
        );
    }
    
    displayResults(results) {
        if (results.length === 0) {
            this.searchResults.innerHTML = '<div class="p-3 text-muted">No results found</div>';
        } else {
            const html = results.map(result => `
                <a href="#" class="search-result-item d-block p-3 text-decoration-none border-bottom">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="mb-1">${result.title}</h6>
                            <small class="text-muted">${result.type}</small>
                        </div>
                        <span class="text-primary fw-bold">₹${result.price}</span>
                    </div>
                </a>
            `).join('');
            
            this.searchResults.innerHTML = html;
        }
        
        this.showResults();
    }
    
    showLoading() {
        this.searchResults.innerHTML = '<div class="p-3 text-center"><div class="loading-spinner"></div></div>';
        this.showResults();
    }
    
    showError(message) {
        this.searchResults.innerHTML = `<div class="p-3 text-danger">${message}</div>`;
        this.showResults();
    }
    
    showResults() {
        this.searchResults.classList.add('show');
    }
    
    hideResults() {
        this.searchResults.classList.remove('show');
    }
    
    debounce(func, wait) {
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
}

// Initialize Enhanced Search
const enhancedSearch = new EnhancedSearch();

// Utility Functions
const utils = {
    // Format currency
    formatCurrency: (amount) => {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    },
    
    // Format date
    formatDate: (date, options = {}) => {
        const defaultOptions = {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        };
        return new Date(date).toLocaleDateString('en-IN', { ...defaultOptions, ...options });
    },
    
    // Debounce function
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Throttle function
    throttle: (func, limit) => {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};

// Export for global use
window.StaySphere = {
    EnhancedCart,
    EnhancedSearch,
    utils
};
