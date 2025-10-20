document.addEventListener('DOMContentLoaded', () => {
    initDashboardDragAndDrop();
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
    draggableItems.forEach(item => {
        let touchStartY = 0;
        let touchCurrentY = 0;
        let isDragging = false;
        
        item.addEventListener('touchstart', (e) => {
            touchStartY = e.touches[0].clientY;
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
                const targetItem = targetElement ? targetElement.closest('.draggable-item') : null;
                
                if (targetItem && targetItem !== item) {
                    highlightDropTarget(item, targetItem);
                }
            }
        }, { passive: false });
        
        item.addEventListener('touchend', (e) => {
            if (isDragging) {
                const targetElement = document.elementFromPoint(e.changedTouches[0].clientX, e.changedTouches[0].clientY);
                const targetItem = targetElement ? targetElement.closest('.draggable-item') : null;
                
                if (targetItem && targetItem !== item) {
                    const targetGroup = targetItem.closest('.draggable-list');
                    const sourceGroup = item.closest('.draggable-list');
                    
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
