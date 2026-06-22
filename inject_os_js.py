import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

window_os_js = """
// ==========================================
// WEB-OS WINDOW MANAGER
// ==========================================
let zIndexCounter = 100;
let draggedWindow = null;
let offsetX = 0;
let offsetY = 0;

function bringToFront(windowId) {
    const win = document.getElementById(windowId);
    if (win) {
        zIndexCounter++;
        win.style.zIndex = zIndexCounter;
    }
}

function startDrag(e, windowId) {
    if (e.target.closest('.window-controls')) return; // Don't drag if clicking buttons
    
    draggedWindow = document.getElementById(windowId);
    if (!draggedWindow) return;
    
    bringToFront(windowId);
    
    const rect = draggedWindow.getBoundingClientRect();
    offsetX = e.clientX - rect.left;
    offsetY = e.clientY - rect.top;
    
    document.addEventListener('mousemove', dragWindow);
    document.addEventListener('mouseup', stopDrag);
}

function dragWindow(e) {
    if (!draggedWindow) return;
    
    // Convert to top/left positioning instead of transform translate for easier dragging
    draggedWindow.style.transform = 'none';
    draggedWindow.style.left = (e.clientX - offsetX) + 'px';
    draggedWindow.style.top = (e.clientY - offsetY) + 'px';
}

function stopDrag() {
    draggedWindow = null;
    document.removeEventListener('mousemove', dragWindow);
    document.removeEventListener('mouseup', stopDrag);
}

function closeWindow(windowId) {
    const win = document.getElementById(windowId);
    if (win) {
        win.classList.remove('active');
        // If it's messenger, clean up intervals if needed
    }
}

function minimizeWindow(windowId) {
    const win = document.getElementById(windowId);
    if (win) {
        const content = win.querySelector('.window-content');
        if (content.style.display === 'none') {
            content.style.display = '';
            win.style.minHeight = '200px';
        } else {
            content.style.display = 'none';
            win.style.minHeight = '40px';
            win.style.height = '40px';
        }
    }
}

function maximizeWindow(windowId) {
    const win = document.getElementById(windowId);
    if (win) {
        if (win.classList.contains('maximized')) {
            win.classList.remove('maximized');
            win.style.width = win.dataset.oldWidth || '';
            win.style.height = win.dataset.oldHeight || '';
            win.style.left = win.dataset.oldLeft || '50%';
            win.style.top = win.dataset.oldTop || '50%';
            if(win.dataset.oldLeft === undefined) {
                win.style.transform = 'translate(-50%, -50%)';
            }
        } else {
            win.dataset.oldWidth = win.style.width;
            win.dataset.oldHeight = win.style.height;
            win.dataset.oldLeft = win.style.left;
            win.dataset.oldTop = win.style.top;
            
            win.classList.add('maximized');
            win.style.transform = 'none';
            win.style.left = '0';
            win.style.top = '70px'; // Below navbar
            win.style.width = '100vw';
            win.style.height = 'calc(100vh - 70px)';
        }
    }
}

// Override switchView to open windows instead of hiding others
window.switchView = function(viewId) {
    const targetView = document.getElementById(viewId);
    if (targetView) {
        targetView.classList.add('active');
        bringToFront(viewId);
    }
};

// Make windows focusable by clicking anywhere on them
document.addEventListener('mousedown', (e) => {
    const win = e.target.closest('.window');
    if (win) {
        bringToFront(win.id);
    }
});
"""

if 'WEB-OS WINDOW MANAGER' not in js_text:
    js_text += "\n" + window_os_js
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(js_text)
    print("Injected WindowManager JS.")
else:
    print("WindowManager JS already exists.")
