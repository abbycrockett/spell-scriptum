revelio "You enter the Restricted Section of the Library."
accio "How many shelves are there?: " -> numOfShelves
accio "How many books per shelf?: " -> numOfBooks
creo totalBooks = numOfShelves * numOfBooks
revelio "There are a total of " + (numOfShelves * numOfBooks) + " to read."

