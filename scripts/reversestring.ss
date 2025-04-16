/* Defines the function reverseString */
expecto reverseString <~
  creo length = len(original)
  creo index = length - 1
  creo reversed = ""

  /* Loops backward through the original string */
  locus index >= 0 @[
    creo reversed = reversed + original[index]
    creo index = index - 1
  ]@

  /* Returns the result */
  reversio reversed
~>

/* Summons User Input & Reverses the original input */
accio "Enter a word to reverse:" -> original
creo result = reverseString
revelio "Your reversed string:"
revelio result