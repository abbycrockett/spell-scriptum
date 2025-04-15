/* Define the function reverseString using expecto */
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

/* User Input & Response */
accio "Enter a word to reverse:" -> original
creo result = reverseString
revelio "Your reversed string:"
revelio result