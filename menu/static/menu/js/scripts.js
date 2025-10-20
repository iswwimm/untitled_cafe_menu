document.addEventListener('DOMContentLoaded', () => {
    // Анімація кнопок на головній сторінці
    const buttons = document.querySelectorAll('.home .buttons a');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', () => {
            button.style.transform = 'scale(1.05)';
        });
        button.addEventListener('mouseleave', () => {
            button.style.transform = 'scale(1)';
        });
    });

    // Анімація карточок меню
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            if (!item.classList.contains('dragging')) {
                item.style.transform = 'translateY(-5px)';
                item.style.boxShadow = '0 8px 16px rgba(0,0,0,0.3)';
            }
        });
        item.addEventListener('mouseleave', () => {
            if (!item.classList.contains('dragging')) {
                item.style.transform = 'translateY(0)';
                item.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
            }
        });
    });

    // Плавне скролювання для внутрішніх посилань
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

    // Drag and Drop функціональність тільки для dashboard
    if (window.location.pathname.includes('/modifiers/dashboard/')) {
        initDragAndDrop();
    }
    
    // Coffee Information Modal функціональність
    if (window.location.pathname.includes('/coffee/') || document.querySelector('.coffee-page')) {
        initCoffeeModal();
    }
});

// Drag and Drop функціональність
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

// Анімація кнопок Staff Dashboard
const dashboardButtons = document.querySelectorAll('.dashboard-btn');
dashboardButtons.forEach(btn => {
    btn.addEventListener('mouseenter', () => {
        btn.style.transform = 'scale(1.05)';
    });
    btn.addEventListener('mouseleave', () => {
        btn.style.transform = 'scale(1)';
    });
});

// Coffee Information Modal функціональність
function initCoffeeModal() {
    const modal = document.getElementById('coffeeModal');
    const closeBtn = document.querySelector('.close');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    
    // Перевіряємо, чи існують необхідні елементи
    if (!modal || !closeBtn || !modalTitle || !modalBody) {
        return;
    }
    
    // Отримуємо всі елементи кави з описом
    const coffeeItems = document.querySelectorAll('.menu-item[data-description]');
    
    coffeeItems.forEach(item => {
        item.style.cursor = 'pointer';
        
        // Клік — відкриває модалку
        item.addEventListener('click', function() {
            const description = this.dataset.description;
            const coffeeName = this.querySelector('h3').textContent;
            
            if (description) {
                // Скидаємо hover-ефект лише на час кліку
                this.style.backgroundColor = '';
                this.style.transform = '';
                this.classList.add('clicked');

                setTimeout(() => {
                    this.classList.remove('clicked');
                }, 300);

                modalTitle.textContent = coffeeName;
                modalBody.textContent = description;
                modal.style.display = 'block';

                // Додаємо плавну появу
                setTimeout(() => {
                    modal.style.opacity = '1';
                }, 10);
            }
        });

        // Hover ефект
        item.addEventListener('mouseenter', function() {
            if (
                this.dataset.description &&
                modal.style.display !== 'block' &&
                !this.classList.contains('clicked')
            ) {
                this.style.backgroundColor = 'rgba(41, 51, 120, 0.1)';
                this.style.transform = 'translateY(-2px)';
            }
        });

        item.addEventListener('mouseleave', function() {
            if (this.dataset.description && modal.style.display !== 'block') {
                this.style.backgroundColor = '';
                this.style.transform = '';
            }
        });
    });
    
    function resetAllCoffeeItems() {
        coffeeItems.forEach(item => {
            item.style.backgroundColor = '';
            item.style.transform = '';
        });
    }
    
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
        resetAllCoffeeItems();
    });
    
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
            resetAllCoffeeItems();
        }
    });
    
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal.style.display === 'block') {
            modal.style.display = 'none';
            resetAllCoffeeItems();
        }
    });
}
