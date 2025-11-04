document.addEventListener('DOMContentLoaded', () => {
    initDashboardDragAndDrop();
    initAllergensSelection();
});

function initDashboardDragAndDrop() {
    let draggedElement = null;
    let draggedGroup = null;
    
    // Desktop drag events
    const draggableItems = document.querySelectorAll('.draggable-item[draggable="true"]');
    
    draggableItems.forEach(item => {
        item.addEventListener('dragstart', handleDragStart);
        item.addEventListener('dragend', handleDragEnd);
    });
    
    const dropZones = document.querySelectorAll('.draggable-list');
    dropZones.forEach(zone => {
        zone.addEventListener('dragover', handleDragOver);
        zone.addEventListener('drop', handleDrop);
        zone.addEventListener('dragenter', handleDragEnter);
        zone.addEventListener('dragleave', handleDragLeave);
    });
    
    // Mobile touch events
    let globalIsDragging = false;
    let scrollPosition = 0;
    let activeDragItem = null;
    let dragStartTime = 0;
    
    // Prevent body scroll during drag
    function preventBodyScroll(e) {
        if (globalIsDragging) {
            e.preventDefault();
            return false;
        }
    }
    
    // Prevent touch actions on draggable items during drag
    function preventTouchAction(e) {
        if (globalIsDragging) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        }
    }
    
    draggableItems.forEach(item => {
        let touchStartY = 0;
        let touchStartX = 0;
        let touchCurrentY = 0;
        let isDragging = false;
        let touchIdentifier = null;
        let initialTransform = '';
        
        item.addEventListener('touchstart', (e) => {
            // Only handle first touch
            if (e.touches.length !== 1) return;
            
            // Don't start drag if clicking on a button or link
            const clickTarget = e.target.closest('a, button, input');
            if (clickTarget) {
                return;
            }
            
            touchIdentifier = e.touches[0].identifier;
            touchStartY = e.touches[0].clientY;
            touchStartX = e.touches[0].clientX;
            dragStartTime = Date.now();
            item.classList.add('touch-dragging');
            isDragging = false;
            activeDragItem = item;
            initialTransform = item.style.transform || '';
        }, { passive: true });
        
        item.addEventListener('touchmove', (e) => {
            // Only handle the touch we started with
            if (!touchIdentifier || e.touches.length !== 1) return;
            if (e.touches[0].identifier !== touchIdentifier) return;
            
            const touch = e.touches[0];
            const deltaY = Math.abs(touch.clientY - touchStartY);
            const deltaX = Math.abs(touch.clientX - touchStartX);
            
            // Start dragging if moved more than 10px vertically (and not horizontally scrolling)
            if (!isDragging && deltaY > 10 && deltaY > deltaX) {
                isDragging = true;
                globalIsDragging = true;
                activeDragItem = item;
                item.classList.add('dragging');
                
                // Save current scroll position and prevent body scroll
                scrollPosition = window.pageYOffset || document.documentElement.scrollTop;
                document.body.style.overflow = 'hidden';
                document.body.style.position = 'fixed';
                document.body.style.top = `-${scrollPosition}px`;
                document.body.style.width = '100%';
                document.body.style.height = '100%';
                
                // Prevent default to stop scrolling
                e.preventDefault();
            }
            
            if (isDragging) {
                e.preventDefault();
                e.stopPropagation();
                touchCurrentY = touch.clientY;
                const deltaY = touchCurrentY - touchStartY;
                item.style.transform = `translateY(${deltaY}px)`;
                
                // Find drop target
                const targetElement = document.elementFromPoint(touch.clientX, touch.clientY);
                const targetItem = targetElement ? targetElement.closest('.draggable-item') : null;
                
                if (targetItem && targetItem !== item) {
                    highlightDropTarget(item, targetItem);
                } else {
                    clearDropHighlights();
                }
            }
        }, { passive: false });
        
        item.addEventListener('touchend', (e) => {
            // Only handle the touch we started with
            if (!touchIdentifier) return;
            const touch = e.changedTouches[0];
            if (touch && touch.identifier !== touchIdentifier) return;
            
            const wasDragging = isDragging;
            const dragDuration = Date.now() - dragStartTime;
            
            // Check if we ended on a button/link
            const targetElement = document.elementFromPoint(touch.clientX, touch.clientY);
            const clickTarget = targetElement ? targetElement.closest('a, button, input') : null;
            
            if (isDragging) {
                const targetItem = targetElement ? targetElement.closest('.draggable-item') : null;
                
                // Only process drop if not clicking on a button/link
                if (targetItem && targetItem !== item && !clickTarget) {
                    const targetGroup = targetItem.closest('.draggable-list');
                    const sourceGroup = item.closest('.draggable-list');
                    
                    if (targetGroup === sourceGroup) {
                        targetGroup.insertBefore(item, targetItem);
                        updateOrder(sourceGroup);
                    }
                }
            }
            
            // Always clean up FIRST to restore normal click behavior
            cleanupDrag(item, wasDragging);
            
            // After cleanup, allow normal click behavior for buttons/links
            // The browser's native click will fire after touchend if we didn't prevent default
            if (clickTarget && !wasDragging) {
                // Don't prevent default - let the click happen naturally
                // The cleanup already happened, so buttons should work now
            }
        }, { passive: false });
        
        item.addEventListener('touchcancel', (e) => {
            cleanupDrag(item, isDragging);
        }, { passive: false });
        
        function cleanupDrag(item, wasDragging) {
            // Clean up item styles first
            item.classList.remove('dragging', 'touch-dragging');
            item.style.transform = initialTransform || '';
            clearDropHighlights();
            
            // Reset dragging state IMMEDIATELY to allow button clicks
            isDragging = false;
            globalIsDragging = false;
            activeDragItem = null;
            
            // Restore body scroll and position
            document.body.style.overflow = '';
            document.body.style.position = '';
            document.body.style.top = '';
            document.body.style.width = '';
            document.body.style.height = '';
            
            // Restore scroll position after body styles are reset
            if (wasDragging) {
                // Use requestAnimationFrame to ensure styles are applied first
                requestAnimationFrame(() => {
                    window.scrollTo(0, scrollPosition);
                });
            }
            
            // Reset touch identifier after a tiny delay to ensure event propagation completes
            setTimeout(() => {
                touchIdentifier = null;
            }, 0);
            
            // Force a repaint to ensure browser resets touch state
            void item.offsetHeight;
        }
    });
    
    // Prevent any touch events from propagating during drag
    document.addEventListener('touchmove', (e) => {
        if (globalIsDragging) {
            // Only prevent if not on a button/link
            const isButtonOrLink = e.target.closest('a, button, input');
            if (!isButtonOrLink) {
                e.preventDefault();
            }
        }
    }, { passive: false, capture: true });
    
    function handleDragStart(e) {
        draggedElement = e.target;
        draggedGroup = e.target.closest('.draggable-list');
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
        const targetItem = e.target.closest('.draggable-item');
        if (targetItem && targetItem !== draggedElement) {
            highlightDropTarget(draggedElement, targetItem);
        }
    }
    
    function handleDragLeave(e) {
        if (!e.currentTarget.contains(e.relatedTarget)) {
            clearDropHighlights();
        }
    }
    
    function handleDrop(e) {
        e.preventDefault();
        const targetItem = e.target.closest('.draggable-item');
        
        if (targetItem && targetItem !== draggedElement) {
            const targetGroup = targetItem.closest('.draggable-list');
            
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
    
    function updateOrder(draggableList) {
        const items = draggableList.querySelectorAll('.draggable-item[draggable="true"]');
        const itemIds = Array.from(items).map(item => item.dataset.id);
        
        const modelType = draggableList.dataset.model;
        const group = draggableList.dataset.group;
        
        console.log('Updating order for:', modelType, 'group:', group, 'items:', itemIds);
        
        // Send AJAX request to update order
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        console.log('Using CSRF token:', csrfToken);
        
        const url = `/update-order/${modelType}/`;
        console.log('Using URL:', url);
        
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                items: itemIds,
                group: group
            })
        })
        .then(response => {
            console.log('Response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Response data:', data);
            if (data.success) {
                console.log('Order updated successfully');
                showNotification('Order updated successfully!', 'success');
            } else {
                console.error('Error updating order:', data.error);
                showNotification('Error updating order', 'error');
            }
        })
        .catch(error => {
            console.error('Error updating order:', error);
            showNotification('Error updating order', 'error');
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
        console.log('CSRF Token:', cookieValue);
        return cookieValue;
    }
    
    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 5px;
            color: white;
            font-weight: bold;
            z-index: 10000;
            transition: opacity 0.3s ease;
            ${type === 'success' ? 'background-color: #27ae60;' : 'background-color: #e74c3c;'}
        `;
        
        document.body.appendChild(notification);
        
        // Remove notification after 3 seconds
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// Allergens selection functionality
function initAllergensSelection() {
    const allergensContainers = document.querySelectorAll('.allergens-checkboxes');
    
    allergensContainers.forEach(container => {
        // Initialize selected checkboxes
        initializeSelectedCheckboxes(container);
        
        // Add click event listeners to list items
        const listItems = container.querySelectorAll('li');
        listItems.forEach(li => {
            li.addEventListener('click', (e) => {
                e.preventDefault();
                const checkbox = li.querySelector('input[type="checkbox"]');
                if (checkbox) {
                    checkbox.checked = !checkbox.checked;
                    updateListItemStyle(li, checkbox.checked);
                }
            });
        });
        
        // Add change event listeners to checkboxes
        const checkboxes = container.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const li = e.target.closest('li');
                updateListItemStyle(li, e.target.checked);
            });
        });
    });
}

function initializeSelectedCheckboxes(container) {
    const checkboxes = container.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        const li = checkbox.closest('li');
        updateListItemStyle(li, checkbox.checked);
    });
}

function updateListItemStyle(li, isChecked) {
    if (isChecked) {
        li.classList.add('selected');
    } else {
        li.classList.remove('selected');
    }
}
