document.addEventListener('DOMContentLoaded', () => {
    // Animation for buttons on home page
    const buttons = document.querySelectorAll('.home .buttons a');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', () => {
            button.style.transform = 'scale(1.05)';
        });
        button.addEventListener('mouseleave', () => {
            button.style.transform = 'scale(1)';
        });
    });

    // Animation for menu cards removed

    // Smooth scrolling for internal links
    const smoothLinks = document.querySelectorAll('a[href^="#"]');
    smoothLinks.forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Drag and Drop functionality only for dashboard
    if (window.location.pathname.includes('/modifiers/dashboard/')) {
        initDragAndDrop();
    }
    
    // Coffee Information Modal functionality
    if (window.location.pathname.includes('/coffee/') || document.querySelector('.coffee-page')) {
        initCoffeeModal();
    }
    
    // Toast Information Modal functionality
    if (window.location.pathname.includes('/toasts/') || document.querySelector('.toasts-page')) {
        initToastModal();
    }
    
    // Sweet Information Modal functionality
    if (window.location.pathname.includes('/sweets/') || document.querySelector('.sweets-page')) {
        initSweetModal();
    }
});

// Drag and Drop functionality
function initDragAndDrop() {
    let draggedElement = null;
    let draggedGroup = null;
    
    // Desktop drag events
    const draggableItems = document.querySelectorAll('.menu-item[draggable="true"]');
    
    draggableItems.forEach(item => {
        item.addEventListener('dragstart', handleDragStart);
        item.addEventListener('dragend', handleDragEnd);
    });
    
    const dropZones = document.querySelectorAll('.menu-list');
    dropZones.forEach(zone => {
        zone.addEventListener('dragover', handleDragOver);
        zone.addEventListener('drop', handleDrop);
        zone.addEventListener('dragenter', handleDragEnter);
        zone.addEventListener('dragleave', handleDragLeave);
    });
    
    // Mobile touch events
    draggableItems.forEach(item => {
        let touchStartY = 0;
        let touchCurrentY = 0;
        let isDragging = false;
        let originalPosition = null;
        
        item.addEventListener('touchstart', (e) => {
            touchStartY = e.touches[0].clientY;
            originalPosition = item.getBoundingClientRect();
            item.classList.add('touch-dragging');
            isDragging = false;
        }, { passive: true });
        
        item.addEventListener('touchmove', (e) => {
            if (!isDragging && Math.abs(e.touches[0].clientY - touchStartY) > 10) {
                isDragging = true;
                item.classList.add('dragging');
            }
            
            if (isDragging) {
                e.preventDefault();
                touchCurrentY = e.touches[0].clientY;
                const deltaY = touchCurrentY - touchStartY;
                item.style.transform = `translateY(${deltaY}px)`;
                
                // Find drop target
                const targetElement = document.elementFromPoint(e.touches[0].clientX, e.touches[0].clientY);
                const targetItem = targetElement ? targetElement.closest('.menu-item') : null;
                
                if (targetItem && targetItem !== item) {
                    highlightDropTarget(item, targetItem);
                }
            }
        }, { passive: false });
        
        item.addEventListener('touchend', (e) => {
            if (isDragging) {
                const targetElement = document.elementFromPoint(e.changedTouches[0].clientX, e.changedTouches[0].clientY);
                const targetItem = targetElement ? targetElement.closest('.menu-item') : null;
                
                if (targetItem && targetItem !== item) {
                    const targetGroup = targetItem.closest('.menu-list');
                    const sourceGroup = item.closest('.menu-list');
                    
                    if (targetGroup === sourceGroup) {
                        targetGroup.insertBefore(item, targetItem);
                        updateOrder(sourceGroup);
                    }
                }
            }
            
            item.classList.remove('dragging', 'touch-dragging');
            item.style.transform = '';
            clearDropHighlights();
        });
    });
    
    function handleDragStart(e) {
        draggedElement = e.target;
        draggedGroup = e.target.closest('.menu-list');
        e.target.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
    }
    
    function handleDragEnd(e) {
        e.target.classList.remove('dragging');
        clearDropHighlights();
        draggedElement = null;
        draggedGroup = null;
    }
    
    function handleDragOver(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
    }
    
    function handleDragEnter(e) {
        e.preventDefault();
        const targetItem = e.target.closest('.menu-item');
        if (targetItem && targetItem !== draggedElement) {
            highlightDropTarget(draggedElement, targetItem);
        }
    }
    
    function handleDragLeave(e) {
        // Only clear highlights if we're leaving the drop zone entirely
        if (!e.currentTarget.contains(e.relatedTarget)) {
            clearDropHighlights();
        }
    }
    
    function handleDrop(e) {
        e.preventDefault();
        const targetItem = e.target.closest('.menu-item');
        
        if (targetItem && targetItem !== draggedElement) {
            const targetGroup = targetItem.closest('.menu-list');
            
            if (targetGroup === draggedGroup) {
                targetGroup.insertBefore(draggedElement, targetItem);
                updateOrder(targetGroup);
            }
        }
        
        clearDropHighlights();
    }
    
    function highlightDropTarget(dragged, target) {
        clearDropHighlights();
        target.classList.add('drop-target');
    }
    
    function clearDropHighlights() {
        document.querySelectorAll('.drop-target').forEach(item => {
            item.classList.remove('drop-target');
        });
    }
    
    function updateOrder(menuList) {
        const items = menuList.querySelectorAll('.menu-item[draggable="true"]');
        const itemIds = Array.from(items).map(item => item.dataset.id);
        
        // Determine model type from current page
        let modelType = 'coffee'; // default
        if (window.location.pathname.includes('/toasts/')) {
            modelType = 'toast';
        } else if (window.location.pathname.includes('/sweets/')) {
            modelType = 'sweet';
        }
        
        // Send AJAX request to update order
        fetch(`/menu/update-order/${modelType}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                items: itemIds
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Order updated successfully');
            } else {
                console.error('Error updating order:', data.error);
            }
        })
        .catch(error => {
            console.error('Error updating order:', error);
        });
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
}

// Staff Dashboard button animation
const dashboardButtons = document.querySelectorAll('.dashboard-btn');
dashboardButtons.forEach(btn => {
    btn.addEventListener('mouseenter', () => {
        btn.style.transform = 'scale(1.05)';
    });
    btn.addEventListener('mouseleave', () => {
        btn.style.transform = 'scale(1)';
    });
});

// Coffee Information Modal functionality
function initCoffeeModal() {
    const modal = document.getElementById('coffeeModal');
    const imageModal = document.getElementById('imageModal');
    const closeBtn = document.querySelector('.close');
    // Image close button removed
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    const modalImage = document.getElementById('modalImage');
    
    // Check if required elements exist
    if (!imageModal || !modalImage) {
        return;
    }
    
    // Get all coffee items with description or image
    const coffeeItems = document.querySelectorAll('.menu-item[data-description], .menu-item[data-image]');
    
    coffeeItems.forEach(item => {
        item.style.cursor = 'pointer';
        
        // Click — opens modal
        item.addEventListener('click', function() {
            const description = this.dataset.description;
            const image = this.dataset.image;
            const coffeeName = this.querySelector('h3').textContent;
            
            
            // Reset hover effect only for click duration
            this.style.backgroundColor = '';
            this.style.transform = '';
            this.classList.add('clicked');

            setTimeout(() => {
                this.classList.remove('clicked');
            }, 300);

            // If there is an image, show it
            if (image) {
                modalImage.src = image;
                modalImage.alt = coffeeName;
                imageModal.style.display = 'block';
                
                // Add smooth appearance
                setTimeout(() => {
                    imageModal.style.opacity = '1';
                }, 10);
            }
            // If there is only description, show text modal (if available)
            else if (description && modal && modalTitle && modalBody) {
                modalTitle.textContent = coffeeName;
                modalBody.textContent = description;
                modal.style.display = 'block';

                // Add smooth appearance
                setTimeout(() => {
                    modal.style.opacity = '1';
                }, 10);
            }
        });

        // Hover effect removed
    });
    
    function resetAllCoffeeItems() {
        coffeeItems.forEach(item => {
            item.style.backgroundColor = '';
            item.style.transform = '';
            item.classList.remove('clicked');
        });
    }
    
    // Close text modal
    if (closeBtn && modal) {
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
            resetAllCoffeeItems();
        });
    }
    
    // Close image modal button removed
    
    // Close on overlay click
    window.addEventListener('click', function(event) {
        if (modal && event.target === modal) {
            modal.style.display = 'none';
            resetAllCoffeeItems();
        }
        // Close image modal when clicking on overlay, modal itself, or modal-inner (but not on the image)
        if (event.target === imageModal || 
            event.target.classList.contains('modal-overlay') || 
            (event.target.classList.contains('modal-inner') && event.target !== modalImage)) {
            imageModal.style.display = 'none';
            resetAllCoffeeItems();
        }
    });
    
    // Close on Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            if (modal && modal.style.display === 'block') {
                modal.style.display = 'none';
                resetAllCoffeeItems();
            }
            if (imageModal.style.display === 'block') {
                imageModal.style.display = 'none';
                resetAllCoffeeItems();
            }
        }
    });
}

// Toast Information Modal functionality
function initToastModal() {
    const modal = document.getElementById('toastModal');
    const imageModal = document.getElementById('imageModal');
    const allergensModal = document.getElementById('allergensModal');
    const closeBtn = document.querySelector('.close');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    const modalImage = document.getElementById('modalImage');
    const allergensList = document.getElementById('allergensList');
    
    // Check if required elements exist
    if (!imageModal || !modalImage) {
        return;
    }
    
    // Get all toast items with description or image
    const toastItems = document.querySelectorAll('.menu-item[data-description], .menu-item[data-image]');
    
    toastItems.forEach(item => {
        item.style.cursor = 'pointer';
        
        // Click — opens modal
        item.addEventListener('click', function() {
            const description = this.dataset.description;
            const image = this.dataset.image;
            const toastName = this.querySelector('h3').textContent;
            
            // If there is an image, show it
            if (image) {
                modalImage.src = image;
                modalImage.alt = toastName;
                imageModal.style.display = 'block';
                
                // Add smooth appearance
                setTimeout(() => {
                    imageModal.style.opacity = '1';
                }, 10);
            }
            // If there is only description, show text modal (if available)
            else if (description && modal && modalTitle && modalBody) {
                modalTitle.textContent = toastName;
                modalBody.textContent = description;
                modal.style.display = 'block';

                // Add smooth appearance
                setTimeout(() => {
                    modal.style.opacity = '1';
                }, 10);
            }
        });
    });
    
    // Handle allergens section
    const allergensItem = document.querySelector('.allergens-item');
    if (allergensItem) {
        allergensItem.style.cursor = 'pointer';
        allergensItem.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            // Populate allergens list
            allergensList.innerHTML = `
                <p><strong>Common Allergens:</strong></p>
                <ul>
                    <li>1 - Gluten</li>
                    <li>2 - Dairy</li>
                    <li>3 - Nuts</li>
                    <li>4 - Eggs</li>
                    <li>5 - Soy</li>
                    <li>6 - Sesame</li>
                </ul>
            `;
            allergensModal.style.display = 'block';
        });
    }
    
    function resetAllToastItems() {
        toastItems.forEach(item => {
            item.style.backgroundColor = '';
            item.style.transform = '';
            item.classList.remove('clicked');
        });
    }
    
    // Close text modal
    if (closeBtn && modal) {
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
            resetAllToastItems();
        });
    }
    
    // Close on overlay click
    window.addEventListener('click', function(event) {
        if (modal && event.target === modal) {
            modal.style.display = 'none';
            resetAllToastItems();
        }
        // Close image modal when clicking on overlay, modal itself, or modal-inner (but not on the image)
        if (event.target === imageModal || 
            event.target.classList.contains('modal-overlay') || 
            (event.target.classList.contains('modal-inner') && event.target !== modalImage)) {
            imageModal.style.display = 'none';
            resetAllToastItems();
        }
        // Close allergens modal
        if (event.target === allergensModal) {
            allergensModal.style.display = 'none';
            resetAllToastItems();
        }
    });
    
    // Close on Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            if (modal && modal.style.display === 'block') {
                modal.style.display = 'none';
                resetAllToastItems();
            }
            if (imageModal.style.display === 'block') {
                imageModal.style.display = 'none';
                resetAllToastItems();
            }
            if (allergensModal.style.display === 'block') {
                allergensModal.style.display = 'none';
                resetAllToastItems();
            }
        }
    });
}

// Sweet Information Modal functionality
function initSweetModal() {
    const modal = document.getElementById('sweetModal');
    const imageModal = document.getElementById('imageModal');
    const allergensModal = document.getElementById('allergensModal');
    const closeBtn = document.querySelector('.close');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    const modalImage = document.getElementById('modalImage');
    const allergensList = document.getElementById('allergensList');
    
    // Check if required elements exist
    if (!imageModal || !modalImage) {
        return;
    }
    
    // Get all sweet items with description or image
    const sweetItems = document.querySelectorAll('.menu-item[data-description], .menu-item[data-image]');
    
    sweetItems.forEach(item => {
        item.style.cursor = 'pointer';
        
        // Click — opens modal
        item.addEventListener('click', function() {
            const description = this.dataset.description;
            const image = this.dataset.image;
            const sweetName = this.querySelector('h3').textContent;
            
            // If there is an image, show it
            if (image) {
                modalImage.src = image;
                modalImage.alt = sweetName;
                imageModal.style.display = 'block';
                
                // Add smooth appearance
                setTimeout(() => {
                    imageModal.style.opacity = '1';
                }, 10);
            }
            // If there is only description, show text modal (if available)
            else if (description && modal && modalTitle && modalBody) {
                modalTitle.textContent = sweetName;
                modalBody.textContent = description;
                modal.style.display = 'block';

                // Add smooth appearance
                setTimeout(() => {
                    modal.style.opacity = '1';
                }, 10);
            }
        });
    });
    
    // Handle allergens section
    const allergensItem = document.querySelector('.allergens-item');
    if (allergensItem) {
        allergensItem.style.cursor = 'pointer';
        allergensItem.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            // Populate allergens list
            allergensList.innerHTML = `
                <p><strong>Common Allergens:</strong></p>
                <ul>
                    <li>1 - Gluten</li>
                    <li>2 - Dairy</li>
                    <li>3 - Nuts</li>
                    <li>4 - Eggs</li>
                    <li>5 - Soy</li>
                    <li>6 - Sesame</li>
                </ul>
            `;
            allergensModal.style.display = 'block';
        });
    }
    
    function resetAllSweetItems() {
        sweetItems.forEach(item => {
            item.style.backgroundColor = '';
            item.style.transform = '';
            item.classList.remove('clicked');
        });
    }
    
    // Close text modal
    if (closeBtn && modal) {
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
            resetAllSweetItems();
        });
    }
    
    // Close on overlay click
    window.addEventListener('click', function(event) {
        if (modal && event.target === modal) {
            modal.style.display = 'none';
            resetAllSweetItems();
        }
        // Close image modal when clicking on overlay, modal itself, or modal-inner (but not on the image)
        if (event.target === imageModal || 
            event.target.classList.contains('modal-overlay') || 
            (event.target.classList.contains('modal-inner') && event.target !== modalImage)) {
            imageModal.style.display = 'none';
            resetAllSweetItems();
        }
        // Close allergens modal
        if (event.target === allergensModal) {
            allergensModal.style.display = 'none';
            resetAllSweetItems();
        }
    });
    
    // Close on Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            if (modal && modal.style.display === 'block') {
                modal.style.display = 'none';
                resetAllSweetItems();
            }
            if (imageModal.style.display === 'block') {
                imageModal.style.display = 'none';
                resetAllSweetItems();
            }
            if (allergensModal.style.display === 'block') {
                allergensModal.style.display = 'none';
                resetAllSweetItems();
            }
        }
    });
}
