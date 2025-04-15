accio "How many zzz's do you need to print? " -> snooze_count

creo i = 0
creo z = "z"
creo output = ""

/* Build a string with the right number of z's */
locus i < snooze_count @[
  creo output = output + z
  creo i = i + 1
]@

/* Print all z's at once */
revelio output

/* Branch depending on snooze_count */
ramus snooze_count > 20 <~ fluffy_sleeps
ramus snooze_count <= 20 <~ fluffy_awake

@[fluffy_sleeps]@
revelio "Success! Fluffy is now peacefully sleeping."
salto done

@[fluffy_awake]@
revelio "Fluffy is still awake and is guarding the Philosopher's Stone!"

@[done]@




