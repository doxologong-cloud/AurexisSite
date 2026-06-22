import os

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix input bug
new_text = text.replace(
    "document.addEventListener('keydown', (e) => {",
    "document.addEventListener('keydown', (e) => {\n    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;"
)

# Fix creepy face
face_js = """const faceContainer = document.createElement('div');
        faceContainer.className = 'creepy-face';
        faceContainer.style.width = '40vw';
        faceContainer.style.height = '30vw';
        faceContainer.style.position = 'fixed';
        faceContainer.style.top = '50%';
        faceContainer.style.left = '50%';
        faceContainer.style.transform = 'translate(-50%, -50%)';
        faceContainer.style.opacity = '0';
        faceContainer.style.transition = 'opacity 2s';
        faceContainer.style.zIndex = '1000';
        faceContainer.style.pointerEvents = 'none';
        
        const dots = [
            // Left eye (angry slant)
            [15, 20], [20, 25], [25, 30], [30, 30], [35, 25],
            // Right eye (angry slant)
            [85, 20], [80, 25], [75, 30], [70, 30], [65, 25],
            // Creepy smile (jagged/curved)
            [10, 60], [20, 75], [30, 85], [40, 90], [50, 92], [60, 90], [70, 85], [80, 75], [90, 60]
        ];
        
        dots.forEach(pos => {
            const ball = document.createElement('div');
            ball.style.position = 'absolute';
            ball.style.left = pos[0] + '%';
            ball.style.top = pos[1] + '%';
            ball.style.width = '2vw';
            ball.style.height = '2vw';
            ball.style.backgroundColor = '#ff0033';
            ball.style.borderRadius = '50%';
            ball.style.boxShadow = '0 0 15px #ff0033, 0 0 30px #ff0000';
            faceContainer.appendChild(ball);
        });
        document.body.appendChild(faceContainer);
        
        setTimeout(() => faceContainer.style.opacity = '1', 100);"""

old_face = """const face = document.createElement('div');
        face.className = 'creepy-face';
        face.innerHTML = '👁️ 👄 👁️';
        document.body.appendChild(face);
        
        setTimeout(() => face.style.opacity = '1', 100);"""

if old_face in new_text:
    new_text = new_text.replace(old_face, face_js)
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Successfully updated the script.")
else:
    print("Could not find the old face code.")
