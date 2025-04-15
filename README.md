# SpellScriptum: A Harry Potter-Inspired Interpreted Language

SpellScriptum is an interpreted, esoteric programming language inspired by the Harry Potter book series. It allows users to write scripts using spell-like commands derived from Latin. To "cast" your first script, open `run_programs.py` in an IDE that supports Python, such as PyCharm, and run the script.

## 📌 Features Overview
- **Input/Output**: Use `accio` to retrieve user input and `revelio` to reveal output.
- **Control Flow**: Includes loops (`locus`), conditionals (`si`), and branching (`ramus`).
- **Functions**: Define reusable blocks of code with `expecto`.
- **Return Statements**: Use `reversio` to return values from functions.
- **Jump Statements**: Navigate code with `salto`.

---

## ✨ SpellScriptum Guide
| **Spell**   | **Pronunciation (Latin)** | **Meaning**                              |
|-------------|---------------------------|------------------------------------------|
| `accio`     | AHK-ee-oh                 | Get user input                           |
| `creo`      | KRAY-oh                   | Create a variable                        |
| `expecto`   | eks-PEK-toh               | Define a function                        |
| `locus`     | LOH-koos                  | While loop                               |
| `ramus`     | RAH-moos                  | Branch                                   |
| `revelio`   | reh-VEL-ee-oh             | Print output to the screen               |
| `reversio`  | reh-VER-see-oh            | Return a value from a function           |
| `salto`     | SAHL-toh                  | Jump to a specific label in the code     |
| `si`        | see                       | If condition                             |

## 🧙‍♂️ Special Syntax
| **Symbol** | **Usage**                     | **Meaning**                                               |
|------------|-------------------------------|-----------------------------------------------------------|
| `<~`       | After `expecto`               | Marks the start of a function definition                  |
| `~>`       | End of a function definition  | Closes the function body                                  |
| `@[ ... ]@`| Around control flow blocks    | Denotes the start and end of blocks (loops, conditionals) |

---

## 🗂️ Project Structure
```text
spell-scriptum/
├── interpreter.py       # Core interpreter logic
├── run_programs.py      # Start here to execute all the spells
├── programs/            # SpellScriptum scripts
│   ├── helloworld.ss
│   ├── reversestring.ss
│   ├── multiply.ss
│   ├── repeater.ss
│   └── cat.ss
└── README.md            # The file you are reading now
```

---

## 📜 Example Scripts

### Hello World
```text
revelio "Hello Wizarding World!"
```
### Multiply two Numbers
```text
accio "How many shelves are there?: " -> numOfShelves
accio "How many books per shelf?: " -> numOfBooks
creo totalBooks = numOfShelves * numOfBooks
revelio "There are a total of " + totalBooks + " books to read."
```

### Reverse a String
```text
/* Define a function to reverse a string */
expecto reverseString <~
  creo length = len(original)
  creo index = length - 1
  creo reversed = ""

  /* Loop backward through the original string */
  locus index >= 0 @[
    creo reversed = reversed + original[index]
    creo index = index - 1
  ]@

  /* Return the result */
  reversio reversed
~>

/* Main program */
accio "Enter a word to reverse:" -> original
creo result = reverseString
revelio "Your reversed string:"
revelio result
```
