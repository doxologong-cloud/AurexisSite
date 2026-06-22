import os

css_code = """

/* --- TOGGLE SWITCH (PARTICLES) --- */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #333;
  transition: .4s;
  border-radius: 34px;
  border: 1px solid rgba(255,255,255,0.1);
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
  box-shadow: 0 0 5px rgba(0,0,0,0.5);
}

input:checked + .slider {
  background-color: #e5b322; /* Golden/Yellow */
  box-shadow: 0 0 15px rgba(229, 179, 34, 0.5);
  border-color: #e5b322;
}

input:checked + .slider:before {
  transform: translateX(26px);
  background-color: #fff;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
}
"""

with open('static/style.css', 'a', encoding='utf-8') as f:
    f.write(css_code)
print("CSS appended successfully.")
