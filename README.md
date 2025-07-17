# ShoutLang

A fun, expressive, and beginner-friendly programming language inspired by shouting! This project includes a custom interpreter and a web playground for experimenting with ShoutLang code.

![ShoutLang Banner](playground/static/shoutlang-7-15-2025.png)

## 🚀 Features
- Simple variable assignment and arithmetic
- Print/output with `SHOUT()`
- Type checking with `AMPLIFY()`
- User input with `WHATT`
- Math operations: `ADD`, `SUB`, `MUL`, `DIV`, `DIVF`, `MOD`
- Comparison operations with YESSS/NOOO output
- Modes: ANGRY, CALM, CHAOS, NORMAL
- Comments with `!`
- Web playground for instant feedback

## 🖥️ Playground
Try ShoutLang in your browser! The playground supports all language features and provides instant output.

## 📦 Installation
```bash
# Clone the repo
https://github.com/adhyys07/ShoutLang.git
cd ShoutLang

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r playground/requirements.txt
```

## ▶️ Usage
### Run the Interpreter
```bash
python -m shoutlang.cli shoutlang/program.shout
```

### Start the Playground (Flask Web App)
```bash
cd playground
python playground.py
```
Then open [http://localhost:5000](http://localhost:5000) in your browser.

## 📝 Language Syntax & Examples
### Set Variables
```shoutlang
SET A = 10
SET NAME = "John"
SET FL  = 1.5
```

### Math Operations
```shoutlang
ADD A 3         ! A becomes 13
SUB B 2         ! B becomes 3
MUL A B         ! A becomes 39 (13*3)
DIV B 2         ! B becomes 1.5
SET C = ADD A 7 ! C is 46 (39+7)
SET D = MUL A B ! D is 58.5 (39*1.5)
```

### Printing & Output
```shoutlang
SHOUT("Hello", A)
SHOUT(A)
```

### Comparisons
```shoutlang
SHOUT(A < B)      # YESSS or NOOO
SHOUT(A >= B)
SHOUT(A == B)
```

### Type & Input
```shoutlang
AMPLIFY(A)
SET NAME = WHATT("WHAT IS YOUR NAME?")
```

### Modes
```shoutlang
MODE ANGRY   # Only uppercase code is accepted
MODE CALM    # Only lowercase code is accepted
MODE CHAOS   # All math operations have double effect
MODE NORMAL  # Regular behavior
```

### Comments
```shoutlang
! This is a comment
```

### MORE THINGS TO COME SO GET EXCITED TILL THEN SHOUTTT !!!!
---
Made with ❤️ by [adhyys07](https://github.com/adhyys07)
