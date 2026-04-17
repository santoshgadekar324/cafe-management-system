// Add to Cart Functionality
$(document).ready(function() {
    // Handle add to cart buttons
    $('.add-to-cart').click(function() {
        const itemId = $(this).data('item-id');
        const button = $(this);
        
        // Disable button and show loading
        button.prop('disabled', true);
        button.html('<i class="fas fa-spinner fa-spin"></i> Adding...');
        
        $.ajax({
            url: `/add_to_cart/${itemId}`,
            method: 'POST',
            success: function(response) {
                if (response.success) {
                    // Update cart count
                    updateCartCount(response.cart_count);
                    
                    // Show success message
                    showNotification('Item added to cart!', 'success');
                    
                    // Reset button
                    button.prop('disabled', false);
                    button.html('<i class="fas fa-cart-plus"></i> Add');
                } else {
                    showNotification('Error adding item to cart', 'danger');
                    button.prop('disabled', false);
                    button.html('<i class="fas fa-cart-plus"></i> Add');
                }
            },
            error: function() {
                showNotification('Error adding item to cart', 'danger');
                button.prop('disabled', false);
                button.html('<i class="fas fa-cart-plus"></i> Add');
            }
        });
    });
});

// Update cart count in navbar
function updateCartCount(count) {
    const cartBadge = $('.navbar .badge');
    if (count > 0) {
        if (cartBadge.length) {
            cartBadge.text(count);
        } else {
            $('.navbar .fa-shopping-cart').parent().append(
                `<span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">${count}</span>`
            );
        }
    }
}

// Show notification
function showNotification(message, type) {
    const alert = `
        <div class="alert alert-${type} alert-dismissible fade show position-fixed" 
             style="top: 80px; right: 20px; z-index: 9999; min-width: 300px;" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    $('body').append(alert);
    
    // Auto dismiss after 3 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow', function() {
            $(this).remove();
        });
    }, 3000);
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    }
}

// Image lazy loading
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
});

// Smooth scroll
$('a[href^="#"]').on('click', function(event) {
    const target = $(this.getAttribute('href'));
    if (target.length) {
        event.preventDefault();
        $('html, body').stop().animate({
            scrollTop: target.offset().top - 70
        }, 1000);
    }
});

// Confirm delete actions
$('.delete-btn').click(function(e) {
    if (!confirm('Are you sure you want to delete this item?')) {
        e.preventDefault();
    }
});

// Auto-hide alerts
setTimeout(function() {
    $('.alert').fadeOut('slow');
}, 5000);

// Initialize tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// Initialize popovers
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
});

// Price formatting
function formatPrice(price) {
    return '₹' + parseFloat(price).toFixed(2);
}

// Date formatting
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-IN', options);
}

// Search functionality with debounce
let searchTimeout;
$('#search-input').on('input', function() {
    clearTimeout(searchTimeout);
    const query = $(this).val();
    
    searchTimeout = setTimeout(function() {
        if (query.length >= 3) {
            performSearch(query);
        }
    }, 500);
});

function performSearch(query) {
    // Implement search logic here
    console.log('Searching for:', query);
}

// Print invoice
function printInvoice() {
    window.print();
}

// Export table to CSV (for admin)
function exportTableToCSV(filename) {
    const csv = [];
    const rows = document.querySelectorAll('table tr');
    
    for (let i = 0; i < rows.length; i++) {
        const row = [];
        const cols = rows[i].querySelectorAll('td, th');
        
        for (let j = 0; j < cols.length; j++) {
            row.push(cols[j].innerText);
        }
        
        csv.push(row.join(','));
    }
    
    downloadCSV(csv.join('\n'), filename);
}

function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = 'none';
    
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

// Loading spinner
function showLoader() {
    $('body').append(`
        <div class="loader-overlay">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `);
}

function hideLoader() {
    $('.loader-overlay').remove();
}

// Add loading overlay CSS dynamically
$('<style>')
    .prop('type', 'text/css')
    .html(`
        .loader-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }
    `)
    .appendTo('head');
