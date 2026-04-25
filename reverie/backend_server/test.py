"""
Sanity check for the configured MiniMax-compatible text endpoint.
"""
from persona.prompt_template.gpt_structure import ChatGPT_request


if __name__ == "__main__":
  prompt = "Respond with a short greeting."
  print(ChatGPT_request(prompt))
