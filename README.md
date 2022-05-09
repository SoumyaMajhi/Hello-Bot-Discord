# Hello-Bot-Discord
Commands | Bot Responds  
--- | --- 
"$hello" | "Hello!"
"$quote" | Display a random quote using the API - https://zenquotes.io/api/random
"$responding" {space} "true" or "false" | Responding to commands ON or OFF
(When Responding is ON) If any of the words within the list of sad_words is typed in the chat \ sad_words = "sad", "hopeless", "depressed", "unhappy", "angry", "depressing", "mournful", "despair", "misery", "miserable", "downcast", "gloomy", "heartbroken", "sorrowful", "glum", "dispirited", "dejected", "defeated", "woeful", "disheartened", "crushed", "crestfallen", "dismayed", "dismal", "dreary", "lose", "lost", "broke", "breakup" | Bot responds with a random message from starter_encouragements \ starter_encouragements = "Cheer up!", "Hang in there.", "You are a great person!", "You are great.", "I can't even do that, as I'm a Bot."
"$add" {space} "Your Message" | Adds "Your Message" to the list of starter_encouragements
"$remove" {space} "index of Your Message",  e.g. -1 is index for the last added item in the list | Removes "Your Message" from the list of starter_encouragements
"$list" | Shows the list of starter_encouragements
