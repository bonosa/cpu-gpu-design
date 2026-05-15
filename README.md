# 🍪 QA Recipe — Chocolate Chip Cookies

A small **interactive baking demo** built to demonstrate **frontend QA testing** concepts using a fun recipe interface.  
Users can adjust ingredient quantities dynamically, test version-specific logic (A/B/C), and visually follow the recipe with photos.

---

## ✨ Features

- 🧮 **Interactive servings control** — scale ingredient quantities up or down  
- 🔁 **Three version modes** for testing logic behavior:
  - 🟢 **A (Good)** — Correct scaling logic  
  - 🔴 **B (Broken)** — Intentionally incorrect math for QA validation  
  - ⚫ **C (Impossible)** — Disabled interaction (for UI/UX test handling)
- 🧑‍🍳 **Step-by-step recipe images** for visual clarity  
- ♿ **Accessible UI** with ARIA labels for screen readers  

---

## 🧩 Project Layout

```
/cookies-site
├── index.html         # Main webpage structure and recipe content  
├── app.js             # Scaling logic, version handling, and QA tests  
├── styles.css         # Layout and visual styling  
├── README.md          # This file  
└── images/            # Ingredient and step-by-step PNGs  
```

---

## 🧠 How It Works

The base recipe yields **24 cookies**.  
When you change the number of cookies using the +/– buttons or the text field, JavaScript recalculates ingredient amounts dynamically.

**Version Logic Overview:**
- 🟢 **Version A:** `base × (newServings / 24)` → correct scaling  
- 🔴 **Version B:** `base × servings` → intentionally incorrect for QA  
- ⚫ **Version C:** disables all serving interactions  

---

## 🧪 Testing Guide

1. 🍴 Open the site in your browser.  
2. 🔘 Switch versions using the toolbar:
   ```
   ?v=a  → Good version  
   ?v=b  → Broken version  
   ?v=c  → Disabled version
   ```
3. ➕➖ Adjust cookie count and observe ingredient updates.  
4. ✅ Verify:
   - The **status messages** update correctly  
   - The **input field** allows full editing/deletion (e.g. remove the “1” in “12”)  
   - The **quantities** scale properly  

---

## 🚀 Local Setup

1. Clone or download this repository.  
2. Open `index.html` in any modern browser — no build tools needed.  
3. Or serve locally:
   ```bash
   python -m http.server 8080
   ```
4. Visit 👉 [http://localhost:8080/?v=a](http://localhost:8080/?v=a)

---

## 🖼️ Credits

- 👩‍🍳 Recipe & Concept: QA Demo for Frontend Testing  
- 🧈 Imagery: AI-generated baking steps  
- 💻 Developed by: **Loge QA Team (Sample)**  

---

## 🔮 Future Enhancements

- ⚙️ Add unit conversion (metric ↔ imperial)  
- 🌙 Dark mode and mobile layout improvements  
- 🎞️ Smooth animation when ingredient amounts update  

---

🍪 **Bake, test, and enjoy debugging deliciously!**
