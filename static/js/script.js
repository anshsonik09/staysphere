// StaySphere Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Smooth scrolling for anchor links
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

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Date picker initialization
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(function(input) {
        // Set minimum date to today
        const today = new Date().toISOString().split('T')[0];
        input.min = today;
    });

    // Room availability check simulation
    const checkAvailabilityBtn = document.getElementById('checkAvailability');
    if (checkAvailabilityBtn) {
        checkAvailabilityBtn.addEventListener('click', function() {
            const btn = this;
            btn.innerHTML = '<span class="loading"></span> Checking...';
            btn.disabled = true;
            
            setTimeout(function() {
                btn.innerHTML = 'Check Availability';
                btn.disabled = false;
                // Show availability results
                showAvailabilityResults();
            }, 1500);
        });
    }

    // Cart functionality
    updateCartCount();
    
    // Add to cart buttons
    document.querySelectorAll('.add-to-cart').forEach(function(button) {
        button.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            const itemName = this.dataset.itemName;
            const itemPrice = this.dataset.itemPrice;
            
            addToCart(itemId, itemName, itemPrice);
            
            // Update button state
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-check"></i> Added';
            this.disabled = true;
            
            setTimeout(function() {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 2000);
        });
    });

    // Image gallery
    initializeGallery();
});

// Cart functions
function updateCartCount() {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    const cartCount = document.getElementById('cartCount');
    if (cartCount) {
        cartCount.textContent = cart.reduce((total, item) => total + item.quantity, 0);
    }
}

function addToCart(id, name, price) {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    const existingItem = cart.find(item => item.id === id);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ id, name, price, quantity: 1 });
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    
    // Show notification
    showNotification(`${name} added to cart!`);
}

function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'alert alert-success position-fixed top-0 start-50 translate-middle-x mt-3';
    notification.style.zIndex = '9999';
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(function() {
        notification.remove();
    }, 3000);
}

function showAvailabilityResults() {
    // This would typically make an AJAX call to check availability
    const resultsDiv = document.getElementById('availabilityResults');
    if (resultsDiv) {
        resultsDiv.innerHTML = `
            <div class="alert alert-success">
                <h6><i class="fas fa-check-circle me-2"></i>Available Rooms</h6>
                <div class="row mt-3">
                    <div class="col-md-4 mb-3">
                        <div class="card">
                            <div class="card-body">
                                <h6>Deluxe Room</h6>
                                <p class="mb-0">₹3,000/night</p>
                                <button class="btn btn-sm btn-primary mt-2">Select</button>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <div class="card">
                            <div class="card-body">
                                <h6>Suite</h6>
                                <p class="mb-0">₹5,000/night</p>
                                <button class="btn btn-sm btn-primary mt-2">Select</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
}

// Gallery functions
function initializeGallery() {
    const galleryImages = document.querySelectorAll('.gallery-img');
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    
    galleryImages.forEach(function(img) {
        img.addEventListener('click', function() {
            if (modal && modalImg) {
                modal.style.display = 'block';
                modalImg.src = this.src;
                modalImg.alt = this.alt;
            }
        });
    });
    
    // Close modal
    const closeBtn = document.querySelector('.modal-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            if (modal) {
                modal.style.display = 'none';
            }
        });
    }
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Form helpers
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        return form.checkValidity();
    }
    return false;
}

function showLoading(button, text = 'Loading...') {
    const originalText = button.innerHTML;
    button.innerHTML = `<span class="loading"></span> ${text}`;
    button.disabled = true;
    return originalText;
}

function hideLoading(button, originalText) {
    button.innerHTML = originalText;
    button.disabled = false;
}

// API helpers (for future AJAX implementation)
async function makeApiCall(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        showNotification('An error occurred. Please try again.');
        throw error;
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
