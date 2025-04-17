accio "Choose a character to cast repeatedly to put Fluffy to sleep:" -> repeat_char
accio "How many times do you think you need to cast the spell? " -> snooze_count

creo i = 0
creo output = ""

/* Build the repeated string */
locus i < snooze_count @[
  creo output = output + repeat_char
  creo i = i + 1
]@

/* Print all the characters so the user can get a visual representation */
revelio output

/* Determines whether Fluffy sleeps depending on snooze_count using branching */
ramus snooze_count > 20 <~ fluffy_sleeps
ramus snooze_count <= 20 <~ fluffy_awake

@[fluffy_sleeps]@
revelio "Success! Fluffy is now peacefully sleeping."
salto done

@[fluffy_awake]@
revelio "Fluffy is still awake and is guarding the Philosopher's Stone!"

@[done]@




