accio "Enter a word to reverse:" -> original

creo length = len(original)
creo index = length - 1
creo reversed = ""

/* Loop backward through the original string */
locus index >= 0 @[
  creo reversed = reversed + original[index]
  creo index = index - 1
]@

revelio "Your reversed string:"
revelio reversed

