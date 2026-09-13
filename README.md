
---

### 🐙 Шаг 2: Создай репозиторий на GitHub

1. Зайди на [github.com](https://github.com) и войди в аккаунт.
2. Нажми **«New repository»** (зелёная кнопка).
3. Заполни:
   - **Repository name:** `chemical-elements-explorer`
   - **Description:** «Консольное приложение для изучения таблицы Менделеева»
   - **Public** (чтобы все видели)
   - **НЕ ставь галочку** «Add a README file» (ты его уже создал)
4. Нажми **«Create repository»**.

---

### 💻 Шаг 3: Залей проект через Git

**1. Установи Git**, если ещё не установлен: [git-scm.com](https://git-scm.com)

**2. Открой терминал (cmd или PowerShell) в папке проекта.**

**3. Выполни команды:**
```bash
git init
git add .
git commit -m "Первый коммит: консольный справочник по химии"
git branch -M main
git remote add origin https://github.com/ТВОЙ_НИК/chemical-elements-explorer.git
git push -u origin main
