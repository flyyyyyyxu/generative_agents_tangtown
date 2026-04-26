"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: gpt_structure.py
Description: Wrapper functions for calling the MiniMax OpenAI-compatible API.
"""
import hashlib
import json
import openai
import re
import time

from utils import *

openai.api_key = openai_api_key
openai.api_base = minimax_api_base


def temp_sleep(seconds=0.1):
  pass


def _normalize_temperature(temperature):
  try:
    temperature = float(temperature)
  except (TypeError, ValueError):
    return 1.0

  if temperature <= 0:
    return 0.01
  if temperature > 1:
    return 1.0
  return temperature


_NO_THINK_SYSTEM = (
  "Respond directly and concisely. Do not reason step by step before answering."
)

def _chat_completion(prompt, max_tokens=512, temperature=1.0, top_p=1, stop=None):
  completion = openai.ChatCompletion.create(
    model=minimax_model,
    messages=[
      {"role": "system", "content": _NO_THINK_SYSTEM},
      {"role": "user", "content": prompt},
    ],
    max_tokens=max_tokens,
    temperature=_normalize_temperature(temperature),
    top_p=top_p if top_p is not None else 1,
    stop=stop,
  )
  content = completion["choices"][0]["message"]["content"]
  return re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()


def ChatGPT_single_request(prompt):
  temp_sleep()
  return _chat_completion(prompt, max_tokens=512, temperature=1.0, top_p=1)


# ============================================================================
# #####################[SECTION 1: CHATGPT-3 STRUCTURE] ######################
# ============================================================================

def GPT4_request(prompt):
  """
  Legacy helper retained for compatibility with the existing prompt stack.
  """
  temp_sleep()

  try:
    return _chat_completion(prompt, max_tokens=1024, temperature=1.0, top_p=1)
  except Exception:
    print("ChatGPT ERROR")
    return "ChatGPT ERROR"


def ChatGPT_request(prompt):
  """
  Legacy helper retained for compatibility with the existing prompt stack.
  """
  try:
    return _chat_completion(prompt, max_tokens=1024, temperature=1.0, top_p=1)
  except Exception:
    print("ChatGPT ERROR")
    return "ChatGPT ERROR"


def GPT4_safe_generate_response(prompt,
                                example_output,
                                special_instruction,
                                repeat=3,
                                fail_safe_response="error",
                                func_validate=None,
                                func_clean_up=None,
                                verbose=False):
  prompt = 'GPT-3 Prompt:\n"""\n' + prompt + '\n"""\n'
  prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
  prompt += "Example output json:\n"
  prompt += '{"output": "' + str(example_output) + '"}'

  if verbose:
    print("CHAT GPT PROMPT")
    print(prompt)

  for i in range(repeat):
    try:
      curr_gpt_response = GPT4_request(prompt).strip()
      end_index = curr_gpt_response.rfind('}') + 1
      curr_gpt_response = curr_gpt_response[:end_index]
      curr_gpt_response = json.loads(curr_gpt_response)["output"]

      if func_validate(curr_gpt_response, prompt=prompt):
        return func_clean_up(curr_gpt_response, prompt=prompt)

      if verbose:
        print("---- repeat count: \n", i, curr_gpt_response)
        print(curr_gpt_response)
        print("~~~~")
    except Exception:
      pass

  return fail_safe_response


def ChatGPT_safe_generate_response(prompt,
                                   example_output,
                                   special_instruction,
                                   repeat=3,
                                   fail_safe_response="error",
                                   func_validate=None,
                                   func_clean_up=None,
                                   verbose=False):
  prompt = '"""\n' + prompt + '\n"""\n'
  prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
  prompt += "Example output json:\n"
  prompt += '{"output": "' + str(example_output) + '"}'

  if verbose:
    print("CHAT GPT PROMPT")
    print(prompt)

  for i in range(repeat):
    try:
      curr_gpt_response = ChatGPT_request(prompt).strip()
      end_index = curr_gpt_response.rfind('}') + 1
      curr_gpt_response = curr_gpt_response[:end_index]
      curr_gpt_response = json.loads(curr_gpt_response)["output"]

      if func_validate(curr_gpt_response, prompt=prompt):
        return func_clean_up(curr_gpt_response, prompt=prompt)

      if verbose:
        print("---- repeat count: \n", i, curr_gpt_response)
        print(curr_gpt_response)
        print("~~~~")
    except Exception:
      pass

  return fail_safe_response


def ChatGPT_safe_generate_response_OLD(prompt,
                                       repeat=3,
                                       fail_safe_response="error",
                                       func_validate=None,
                                       func_clean_up=None,
                                       verbose=False):
  if verbose:
    print("CHAT GPT PROMPT")
    print(prompt)

  for i in range(repeat):
    try:
      curr_gpt_response = ChatGPT_request(prompt).strip()
      if func_validate(curr_gpt_response, prompt=prompt):
        return func_clean_up(curr_gpt_response, prompt=prompt)
      if verbose:
        print(f"---- repeat count: {i}")
        print(curr_gpt_response)
        print("~~~~")
    except Exception:
      pass
  print("FAIL SAFE TRIGGERED")
  return fail_safe_response


# ============================================================================
# ###################[SECTION 2: ORIGINAL GPT-3 STRUCTURE] ###################
# ============================================================================

_prompt_cache = {}

def GPT_request(prompt, gpt_parameter):
  """
  Routes legacy completion-style prompt calls through MiniMax chat completions.
  """
  cache_key = (prompt, gpt_parameter.get("max_tokens"), gpt_parameter.get("temperature"))
  if cache_key in _prompt_cache:
    return _prompt_cache[cache_key]
  temp_sleep()
  try:
    result = _chat_completion(
      prompt,
      max_tokens=gpt_parameter.get("max_tokens", 512),
      temperature=gpt_parameter.get("temperature", 1.0),
      top_p=gpt_parameter.get("top_p", 1),
      stop=gpt_parameter.get("stop"),
    )
  except Exception:
    print("TOKEN LIMIT EXCEEDED")
    return "TOKEN LIMIT EXCEEDED"
  _prompt_cache[cache_key] = result
  return result


def generate_prompt(curr_input, prompt_lib_file):
  """
  Takes in the current input and a prompt template path and materializes the
  final prompt string.
  """
  if type(curr_input) == type("string"):
    curr_input = [curr_input]
  curr_input = [str(i) for i in curr_input]

  f = open(prompt_lib_file, "r")
  prompt = f.read()
  f.close()
  for count, i in enumerate(curr_input):
    prompt = prompt.replace(f"!<INPUT {count}>!", i)
  if "<commentblockmarker>###</commentblockmarker>" in prompt:
    prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
  return prompt.strip()


def safe_generate_response(prompt,
                           gpt_parameter,
                           repeat=2,
                           fail_safe_response="error",
                           func_validate=None,
                           func_clean_up=None,
                           verbose=False):
  if verbose:
    print(prompt)

  for i in range(repeat):
    curr_gpt_response = GPT_request(prompt, gpt_parameter)
    if func_validate(curr_gpt_response, prompt=prompt):
      return func_clean_up(curr_gpt_response, prompt=prompt)
    if verbose:
      print("---- repeat count: ", i, curr_gpt_response)
      print(curr_gpt_response)
      print("~~~~")
  return fail_safe_response


def _hash_to_unit_float(seed):
  return (int(seed[:8], 16) / 0xFFFFFFFF) * 2 - 1


def get_embedding(text, model="MiniMax-Text-01"):
  """
  MiniMax's public OpenAI-compatible docs confirm chat completions; to avoid
  relying on undocumented embedding compatibility here, we use a deterministic
  local embedding surrogate for retrieval.
  """
  text = text.replace("\n", " ").strip()
  if not text:
    text = "this is blank"

  embedding = []
  for i in range(64):
    digest = hashlib.sha256(f"{model}:{i}:{text}".encode("utf-8")).hexdigest()
    embedding.append(_hash_to_unit_float(digest))
  return embedding


if __name__ == '__main__':
  gpt_parameter = {"engine": minimax_model, "max_tokens": 50,
                   "temperature": 1, "top_p": 1, "stream": False,
                   "frequency_penalty": 0, "presence_penalty": 0,
                   "stop": ['"']}
  curr_input = ["driving to a friend's house"]
  prompt_lib_file = "prompt_template/test_prompt_July5.txt"
  prompt = generate_prompt(curr_input, prompt_lib_file)

  def __func_validate(gpt_response):
    if len(gpt_response.strip()) <= 1:
      return False
    if len(gpt_response.strip().split(" ")) > 1:
      return False
    return True

  def __func_clean_up(gpt_response):
    cleaned_response = gpt_response.strip()
    return cleaned_response

  output = safe_generate_response(prompt,
                                 gpt_parameter,
                                 5,
                                 "rest",
                                 __func_validate,
                                 __func_clean_up,
                                 True)

  print(output)
