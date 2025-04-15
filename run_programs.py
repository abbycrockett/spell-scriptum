import interpreter
import os

def run_spell_file(filename):
    # Construct path to file in the programs folder
    file_path = os.path.join("programs", filename)

    print(f"\n✨ Running {filename}...\n{'-' * 47}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
            interpreter.run_spellscript(code)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"❌ Error running {filename}: {e}")


if __name__ == "__main__":
    spell_files = [
        "helloworld.ss",
        "cat.ss",
        "multiply.ss",
        "repeater.ss",
        "reversestring.ss"
    ]

    for spell_file in spell_files:
        run_spell_file(spell_file)