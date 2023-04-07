import poe

session_token = ""
client = poe.Client(f"{session_token}")

poe.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

message = "Summarize the GNU GPL v3"
for chunk in client.send_message("chinchilla", message, with_chat_break=True):
  print(chunk["text_new"], end="", flush=True)