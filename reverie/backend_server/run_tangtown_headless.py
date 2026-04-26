"""
Headless Tang Dynasty simulation runner for a minimal 3-agent setup.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
from collections import defaultdict

from utils import fs_storage
from global_methods import copyanything, create_folder_if_not_there
from maze import Maze
from persona.persona import Persona


MAX_STEPS_CAP = 5000
BASE_SIM_CODE = "base_the_ville_isabella_maria_klaus"
START_TIME = datetime.datetime(742, 2, 15, 18, 0, 0)


PERSONA_SPECS = [
  {
    "template_name": "Isabella Rodriguez",
    "name": "Li Mingzhu",
    "name_local": "李明珠",
    "age": 32,
    "innate": "warm, observant, practical; careful with money but generous to regulars",
    "learned": (
      "Li Mingzhu is the owner of a tea house near the West Market of Chang'an "
      "during the Tang Dynasty in 742 AD. Merchants, students, officials, and "
      "travelers pass through her doors each day, and she is fluent in the "
      "social currents of the city through her clientele."
    ),
    "currently": (
      "Li Mingzhu is preparing a Lantern Festival evening gathering at her tea "
      "house. In this simulation, Hobbs Cafe is treated conceptually as 明珠茶馆, "
      "a tea house near Chang'an West Market."
    ),
    "lifestyle": (
      "Li Mingzhu rises early to inspect tea, cakes, and lamps, and stays active "
      "through the evening rush before resting near midnight."
    ),
    "daily_plan_req": (
      "Prepare and host a successful Lantern Festival evening gathering at the "
      "tea house by arranging extra tea, sweet cakes, lamps, seating, and drawing "
      "familiar customers in after sunset."
    ),
    "memories": [
      "Li Mingzhu;742-02-15 07:00:00;She inherited the tea house from her mother after years of helping behind the counter.",
      "Li Mingzhu;742-02-15 07:05:00;She knows which merchants bargain hard and which regulars quietly tip the servers.",
      "Li Mingzhu;742-02-15 07:10:00;She keeps careful accounts because one bad week in the market can ruin a season.",
      "Li Mingzhu;742-02-15 07:15:00;She has learned that examination candidates often bring the best gossip about officials and court moods.",
      "Li Mingzhu;742-02-15 07:20:00;She likes to send an extra cake to regular customers who have had a difficult day.",
      "Li Mingzhu;742-02-15 07:25:00;Last year's Lantern Festival crowd overflowed the doorway and left her short on hot water.",
      "Li Mingzhu;742-02-15 07:30:00;She asked a lamp seller in West Market to reserve additional lanterns for tonight.",
      "Li Mingzhu;742-02-15 07:35:00;She expects scholars to recite poems if the tea house feels lively after sunset.",
      "Li Mingzhu;742-02-15 07:40:00;She wants Chen Zian to visit tonight because educated customers attract more conversation and business.",
      "Li Mingzhu;742-02-15 07:45:00;She hopes An Lushan will bring word of foreign goods because novelty draws a paying crowd.",
      "Li Mingzhu;742-02-15 07:50:00;She worries that cakes may run short if the festival turnout is strong.",
      "Li Mingzhu;742-02-15 07:55:00;She takes pride in making tired travelers feel that her tea house is a dependable refuge."
    ],
  },
  {
    "template_name": "Maria Lopez",
    "name": "Chen Zian",
    "name_local": "陈子安",
    "age": 24,
    "innate": "ambitious, thoughtful, disciplined; prone to self-doubt about his literary elegance",
    "learned": (
      "Chen Zian is a scholar from a provincial family who has come to Chang'an "
      "to sit the imperial examination. He is steeped in Confucian classics and "
      "regulated verse, and he studies diligently for advancement."
    ),
    "currently": (
      "Chen Zian is reviewing classical texts, practicing poetry, and seeking "
      "advice on court politics and essay style before the imperial examination. "
      "In this simulation, the dormitory and cafe spaces are interpreted as a "
      "scholar's inn and tea-house circuit near West Market."
    ),
    "lifestyle": (
      "Chen Zian studies late, rises after dawn, copies passages carefully, and "
      "tries to balance ambition with calm before the examinations."
    ),
    "daily_plan_req": (
      "Pass the imperial examination by reviewing classical texts, practicing "
      "poetry, and seeking advice from educated acquaintances on court politics "
      "and essay style."
    ),
    "memories": [
      "Chen Zian;742-02-15 08:00:00;His father sold part of the family grain store to fund this journey to Chang'an.",
      "Chen Zian;742-02-15 08:05:00;He can still recite passages from the Analects that his village tutor drilled into him as a child.",
      "Chen Zian;742-02-15 08:10:00;He worries that his prose is sound but not elegant enough for metropolitan examiners.",
      "Chen Zian;742-02-15 08:15:00;He has heard that the preferences of court examiners shift with factional politics.",
      "Chen Zian;742-02-15 08:20:00;He respects Li Mingzhu because her tea house often gathers clerks, scholars, and travelers with useful news.",
      "Chen Zian;742-02-15 08:25:00;He once impressed a county magistrate by composing a neat regulated verse on short notice.",
      "Chen Zian;742-02-15 08:30:00;He envies candidates who seem naturally graceful with parallel prose.",
      "Chen Zian;742-02-15 08:35:00;He intends to ask anyone well-informed whether current examiners value moral clarity over ornament.",
      "Chen Zian;742-02-15 08:40:00;He is curious whether foreign merchants hear rumors of court priorities before local scholars do.",
      "Chen Zian;742-02-15 08:45:00;Festival distractions make concentration harder, but he also knows social encounters can yield useful advice.",
      "Chen Zian;742-02-15 08:50:00;He promised himself he would not return home without giving the examinations his best effort.",
      "Chen Zian;742-02-15 08:55:00;He feels calmer when he copies a difficult passage until the brushwork settles his thoughts."
    ],
  },
  {
    "template_name": "Klaus Mueller",
    "name": "An Lushan",
    "name_local": "安禄山",
    "age": 38,
    "innate": "shrewd, sociable, adaptive; respects Tang law while always alert to profitable opportunities",
    "learned": (
      "An Lushan is a Sogdian merchant living in Chang'an, trading in spices, "
      "glassware, horses, and textiles sourced from the Silk Road. He is "
      "multilingual and often bridges foreign traders with Chinese buyers."
    ),
    "currently": (
      "An Lushan is trying to sell a new shipment of foreign glass cups and "
      "aromatic spices at West Market while securing dependable local partners "
      "before his caravan departs. In this simulation, his lodging and social "
      "haunts are conceptually mapped onto the foreign quarter inn and tavern."
    ),
    "lifestyle": (
      "An Lushan rises early for market business, spends the day negotiating and "
      "inspecting goods, and keeps evenings free for alliances, feasts, and deals."
    ),
    "daily_plan_req": (
      "Sell a new shipment of foreign glass cups and aromatic spices at West "
      "Market, and secure reliable local partners before the caravan departs Chang'an."
    ),
    "memories": [
      "An Lushan;742-02-15 06:30:00;He has crossed many caravan routes and trusts a ledger more than a promise.",
      "An Lushan;742-02-15 06:35:00;He knows foreign glass cups attract wealthy buyers if displayed where lamplight catches them.",
      "An Lushan;742-02-15 06:40:00;He keeps cordial relations with local officials because smooth paperwork protects profit.",
      "An Lushan;742-02-15 06:45:00;He can switch between languages quickly when negotiations become delicate.",
      "An Lushan;742-02-15 06:50:00;He suspects festival crowds are ideal for introducing aromatic spices to curious customers.",
      "An Lushan;742-02-15 06:55:00;He sees Li Mingzhu's tea house as a useful social hub for meeting clerks and buyers.",
      "An Lushan;742-02-15 07:00:00;He has learned that scholars often know which households seek fashionable imports.",
      "An Lushan;742-02-15 07:05:00;He wants reliable local partners so the next caravan can sell faster and safer.",
      "An Lushan;742-02-15 07:10:00;He once lost money when a careless handler chipped a crate of fragile cups.",
      "An Lushan;742-02-15 07:15:00;He respects Tang law because public disorder scares customers and invites scrutiny.",
      "An Lushan;742-02-15 07:20:00;He enjoys lively company, especially when conversation turns into trade.",
      "An Lushan;742-02-15 07:25:00;He believes a good festival night can secure more future business than a week of ordinary hawking."
    ],
  },
]


LOCATION_REMAP = {
  "Hobbs Cafe": "明珠茶馆 (Tea House)",
  "The Rose and Crown Pub": "胡姬酒肆 (Sogdian Tavern)",
  "Dorm for Oak Hill College": "学子客舍 (Scholar's Inn)",
  "The Ville": "长安西市 (Chang'an West Market district)",
}


def _safe_slug(value):
  slug = re.sub(r"[^A-Za-z0-9_-]+", "-", value.strip())
  slug = re.sub(r"-{2,}", "-", slug).strip("-")
  return slug or "simulation"


def _extract_keywords(text):
  tokens = re.findall(r"\w+", text.lower())
  stopwords = {
    "the", "and", "with", "that", "this", "from", "into", "have", "has",
    "had", "for", "his", "her", "she", "him", "was", "were", "are", "but",
    "not", "too", "who", "will", "after", "before", "near", "their", "they",
    "them", "than", "just", "very", "also", "into", "over", "each", "more",
  }
  keywords = []
  for token in tokens:
    if len(token) <= 2 or token in stopwords:
      continue
    keywords.append(token)
  return sorted(set(keywords[:12] if len(keywords) > 12 else keywords))


def _hash_to_unit_float(seed):
  return (int(seed[:8], 16) / 0xFFFFFFFF) * 2 - 1


def _local_embedding(text):
  text = text.replace("\n", " ").strip()
  if not text:
    text = "this is blank"

  embedding = []
  for i in range(64):
    digest = hashlib.sha256(f"MiniMax-Text-01:{i}:{text}".encode("utf-8")).hexdigest()
    embedding.append(_hash_to_unit_float(digest))
  return embedding


def _build_memory_stream(records):
  nodes = {}
  embeddings = {}
  for index, record in enumerate(records, start=1):
    _, timestamp, memory = record.split(";", 2)
    date_part, time_part = timestamp.split(" ")
    y, mo, d = date_part.split("-")
    h, mi, s = time_part.split(":")
    created = datetime.datetime(int(y), int(mo), int(d), int(h), int(mi), int(s))
    keywords = _extract_keywords(memory)
    object_token = keywords[0] if keywords else "memory"
    nodes[f"node_{index}"] = {
      "node_count": index,
      "type_count": index,
      "type": "thought",
      "depth": 1,
      "created": created.strftime("%Y-%m-%d %H:%M:%S"),
      "expiration": (created + datetime.timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S"),
      "subject": "self",
      "predicate": "remembers",
      "object": object_token,
      "description": memory,
      "embedding_key": memory,
      "poignancy": min(10, max(5, len(keywords))),
      "keywords": keywords,
      "filling": None,
    }
    embeddings[memory] = _local_embedding(memory)

  kw_strength = {
    "kw_strength_event": {},
    "kw_strength_thought": defaultdict(int),
  }
  for node in nodes.values():
    for keyword in node["keywords"]:
      kw_strength["kw_strength_thought"][keyword] += 1

  kw_strength["kw_strength_thought"] = dict(kw_strength["kw_strength_thought"])
  return nodes, embeddings, kw_strength


def _write_json(path, payload):
  create_folder_if_not_there(path)
  with open(path, "w") as out:
    json.dump(payload, out, indent=2, ensure_ascii=False)


def _load_json(path):
  with open(path) as infile:
    return json.load(infile)


def _prepare_simulation(sim_code):
  base_folder = os.path.join(fs_storage, BASE_SIM_CODE)
  sim_folder = os.path.join(fs_storage, sim_code)
  if os.path.exists(sim_folder):
    raise RuntimeError(f"Simulation folder already exists: {sim_folder}")

  copyanything(base_folder, sim_folder)

  meta_path = os.path.join(sim_folder, "reverie", "meta.json")
  env0_path = os.path.join(sim_folder, "environment", "0.json")
  meta = _load_json(meta_path)
  env0 = _load_json(env0_path)

  updated_env0 = {}
  updated_names = []

  for spec in PERSONA_SPECS:
    old_name = spec["template_name"]
    new_name = spec["name"]

    old_persona_dir = os.path.join(sim_folder, "personas", old_name)
    new_persona_dir = os.path.join(sim_folder, "personas", new_name)
    os.rename(old_persona_dir, new_persona_dir)

    scratch_path = os.path.join(new_persona_dir, "bootstrap_memory", "scratch.json")
    scratch = _load_json(scratch_path)
    scratch["name"] = new_name
    first_name, last_name = new_name.split(" ", 1)
    scratch["first_name"] = first_name
    scratch["last_name"] = last_name
    scratch["age"] = spec["age"]
    scratch["innate"] = spec["innate"]
    scratch["learned"] = spec["learned"]
    scratch["currently"] = spec["currently"]
    scratch["lifestyle"] = spec["lifestyle"]
    scratch["daily_plan_req"] = spec["daily_plan_req"]
    scratch["curr_time"] = None
    scratch["curr_tile"] = None
    scratch["daily_req"] = []
    scratch["f_daily_schedule"] = []
    scratch["f_daily_schedule_hourly_org"] = []
    scratch["act_address"] = None
    scratch["act_start_time"] = None
    scratch["act_duration"] = None
    scratch["act_description"] = None
    scratch["act_pronunciatio"] = None
    scratch["act_event"] = [new_name, None, None]
    scratch["act_obj_description"] = None
    scratch["act_obj_pronunciatio"] = None
    scratch["act_obj_event"] = [None, None, None]
    scratch["chatting_with"] = None
    scratch["chat"] = None
    scratch["chatting_with_buffer"] = {}
    scratch["chatting_end_time"] = None
    scratch["act_path_set"] = False
    scratch["planned_path"] = []
    _write_json(scratch_path, scratch)

    a_mem_dir = os.path.join(new_persona_dir, "bootstrap_memory", "associative_memory")
    nodes, embeddings, kw_strength = _build_memory_stream(spec["memories"])
    _write_json(os.path.join(a_mem_dir, "nodes.json"), nodes)
    _write_json(os.path.join(a_mem_dir, "embeddings.json"), embeddings)
    _write_json(os.path.join(a_mem_dir, "kw_strength.json"), kw_strength)

    updated_env0[new_name] = env0[old_name]
    updated_names.append(new_name)

  meta["fork_sim_code"] = BASE_SIM_CODE
  meta["start_date"] = START_TIME.strftime("%B %d, %Y")
  meta["curr_time"] = START_TIME.strftime("%B %d, %Y, %H:%M:%S")
  meta["step"] = 0
  meta["persona_names"] = updated_names
  _write_json(meta_path, meta)
  _write_json(env0_path, updated_env0)

  create_folder_if_not_there(os.path.join(sim_folder, "movement", "0.json"))
  create_folder_if_not_there(os.path.join(sim_folder, "outputs", "placeholder.json"))

  return sim_folder, meta, updated_env0


def _serialize_memory_node(node):
  return {
    "node_id": node.node_id,
    "type": node.type,
    "created": node.created.strftime("%Y-%m-%d %H:%M:%S"),
    "expiration": node.expiration.strftime("%Y-%m-%d %H:%M:%S") if node.expiration else None,
    "subject": node.subject,
    "predicate": node.predicate,
    "object": node.object,
    "description": node.description,
    "poignancy": node.poignancy,
    "keywords": sorted(node.keywords),
    "filling": node.filling,
  }


def _serialize_persona_state(persona, position):
  return {
    "tile": [position[0], position[1]],
    "current_action": persona.scratch.act_description,
    "action_address": persona.scratch.act_address,
    "chatting_with": persona.scratch.chatting_with,
  }


def _write_outputs(sim_folder,
                   sim_code,
                   steps_run,
                   curr_time,
                   positions,
                   personas,
                   environment_snapshots,
                   movement_logs,
                   conversation_logs,
                   timeline_lines):
  outputs_dir = os.path.join(sim_folder, "outputs")
  create_folder_if_not_there(os.path.join(outputs_dir, "dummy.txt"))

  environment_payload = {
    "simulation_code": sim_code,
    "base_simulation": BASE_SIM_CODE,
    "time_period": "February 15, 742 AD — Lantern Festival night",
    "location": "Chang'an West Market district (长安西市), Tang Dynasty imperial capital",
    "model": "MiniMax-Text-01",
    "base_url": "https://api.minimaxi.com/v1",
    "max_steps_cap": MAX_STEPS_CAP,
    "steps_run": steps_run,
    "start_time": START_TIME.strftime("%Y-%m-%d %H:%M:%S"),
    "end_time": curr_time.strftime("%Y-%m-%d %H:%M:%S"),
    "location_remap": LOCATION_REMAP,
    "agents": [
      {
        "name": spec["name"],
        "name_local": spec["name_local"],
        "state": _serialize_persona_state(personas[spec["name"]], positions[spec["name"]]),
      }
      for spec in PERSONA_SPECS
    ],
    "snapshots": environment_snapshots,
  }
  _write_json(os.path.join(outputs_dir, "environment.json"), environment_payload)
  _write_json(os.path.join(outputs_dir, "movement_logs.json"), movement_logs)
  _write_json(os.path.join(outputs_dir, "conversation_logs.json"), conversation_logs)

  personas_dir = os.path.join(outputs_dir, "personas")
  for name, persona in personas.items():
    persona_dir = os.path.join(personas_dir, name)
    create_folder_if_not_there(os.path.join(persona_dir, "memory_stream.json"))
    memory_stream = {
      "events": [_serialize_memory_node(node) for node in persona.a_mem.seq_event],
      "thoughts": [_serialize_memory_node(node) for node in persona.a_mem.seq_thought],
      "chats": [_serialize_memory_node(node) for node in persona.a_mem.seq_chat],
    }
    _write_json(os.path.join(persona_dir, "memory_stream.json"), memory_stream)

  with open(os.path.join(outputs_dir, "simulation_log.txt"), "w") as outfile:
    outfile.write("\n".join(timeline_lines) + "\n")


def run_simulation(sim_code, requested_steps):
  steps = min(requested_steps, MAX_STEPS_CAP)
  sim_folder, meta, env0 = _prepare_simulation(sim_code)

  maze = Maze(meta["maze_name"])
  personas = {}
  positions = {}
  for persona_name in meta["persona_names"]:
    persona_folder = os.path.join(sim_folder, "personas", persona_name)
    persona = Persona(persona_name, persona_folder)
    x = env0[persona_name]["x"]
    y = env0[persona_name]["y"]
    personas[persona_name] = persona
    positions[persona_name] = (x, y)
    maze.tiles[y][x]["events"].add(persona.scratch.get_curr_event_and_desc())

  curr_time = START_TIME
  step = 0
  game_obj_cleanup = {}
  conversation_seen = set()
  movement_logs = []
  conversation_logs = []
  timeline_lines = []
  environment_snapshots = [
    {
      "step": 0,
      "time": curr_time.strftime("%Y-%m-%d %H:%M:%S"),
      "positions": {name: {"x": pos[0], "y": pos[1]} for name, pos in positions.items()},
    }
  ]

  for _ in range(steps):
    print(f"Step {step}/{steps}  [{curr_time.strftime('%Y-%m-%d %H:%M:%S')}]", flush=True)
    for key, val in game_obj_cleanup.items():
      maze.turn_event_from_tile_idle(key, val)
    game_obj_cleanup = {}

    for persona_name, persona in personas.items():
      if not persona.scratch.planned_path and persona.scratch.act_address and persona.scratch.act_obj_event[0]:
        curr_obj_event = persona.scratch.get_curr_obj_event_and_desc()
        game_obj_cleanup[curr_obj_event] = positions[persona_name]
        maze.add_event_from_tile(curr_obj_event, positions[persona_name])
        blank = (curr_obj_event[0], None, None, None)
        maze.remove_event_from_tile(blank, positions[persona_name])

    movements = {"persona": {}, "meta": {"curr_time": curr_time.strftime("%B %d, %Y, %H:%M:%S")}}
    next_positions = {}
    for persona_name, persona in personas.items():
      next_tile, pronunciatio, description = persona.move(
        maze,
        personas,
        positions[persona_name],
        curr_time,
      )
      next_tile = tuple(next_tile)
      next_positions[persona_name] = next_tile
      movements["persona"][persona_name] = {
        "movement": [next_tile[0], next_tile[1]],
        "pronunciatio": pronunciatio,
        "description": description,
        "chat": persona.scratch.chat,
      }

      if persona.scratch.chat and persona.scratch.chatting_with:
        signature = (
          tuple(sorted([persona_name, persona.scratch.chatting_with])),
          tuple(tuple(row) for row in persona.scratch.chat),
        )
        if signature not in conversation_seen:
          conversation_seen.add(signature)
          conversation_logs.append({
            "step": step,
            "time": curr_time.strftime("%Y-%m-%d %H:%M:%S"),
            "participants": list(signature[0]),
            "transcript": [{"speaker": row[0], "utterance": row[1]} for row in persona.scratch.chat],
          })
          timeline_lines.append(
            f"[{curr_time.strftime('%Y-%m-%d %H:%M:%S')}] Conversation: "
            f"{' & '.join(signature[0])}"
          )

    for persona_name, persona in personas.items():
      old_tile = positions[persona_name]
      new_tile = next_positions[persona_name]
      positions[persona_name] = new_tile
      maze.remove_subject_events_from_tile(persona.name, old_tile)
      maze.add_event_from_tile(persona.scratch.get_curr_event_and_desc(), new_tile)

    movement_logs.append({
      "step": step,
      "time": curr_time.strftime("%Y-%m-%d %H:%M:%S"),
      "movements": movements["persona"],
    })
    _write_json(os.path.join(sim_folder, "movement", f"{step}.json"), movements)

    timeline_lines.append(f"[{curr_time.strftime('%Y-%m-%d %H:%M:%S')}] Step {step}")
    for persona_name, details in movements["persona"].items():
      timeline_lines.append(
        f"  - {persona_name} -> {details['description']} at {details['movement']}"
      )

    step += 1
    curr_time += datetime.timedelta(seconds=meta["sec_per_step"])

    env_snapshot = {
      name: {"maze": meta["maze_name"], "x": pos[0], "y": pos[1]}
      for name, pos in positions.items()
    }
    _write_json(os.path.join(sim_folder, "environment", f"{step}.json"), env_snapshot)
    environment_snapshots.append({
      "step": step,
      "time": curr_time.strftime("%Y-%m-%d %H:%M:%S"),
      "positions": {name: {"x": pos[0], "y": pos[1]} for name, pos in positions.items()},
    })

  meta["curr_time"] = curr_time.strftime("%B %d, %Y, %H:%M:%S")
  meta["step"] = step
  _write_json(os.path.join(sim_folder, "reverie", "meta.json"), meta)

  for persona_name, persona in personas.items():
    save_folder = os.path.join(sim_folder, "personas", persona_name, "bootstrap_memory")
    persona.save(save_folder)

  _write_outputs(
    sim_folder,
    sim_code,
    step,
    curr_time,
    positions,
    personas,
    environment_snapshots,
    movement_logs,
    conversation_logs,
    timeline_lines,
  )

  return sim_folder


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--steps", type=int, default=120)
  parser.add_argument("--sim-code", default=None)
  args = parser.parse_args()

  sim_code = args.sim_code or f"tang_lantern_minimal_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
  sim_code = _safe_slug(sim_code)
  sim_folder = run_simulation(sim_code, args.steps)
  print(json.dumps({
    "simulation_code": sim_code,
    "simulation_folder": sim_folder,
    "steps_requested": args.steps,
    "steps_capped_at": MAX_STEPS_CAP,
    "outputs": {
      "environment": os.path.join(sim_folder, "outputs", "environment.json"),
      "movements": os.path.join(sim_folder, "outputs", "movement_logs.json"),
      "conversations": os.path.join(sim_folder, "outputs", "conversation_logs.json"),
      "timeline": os.path.join(sim_folder, "outputs", "simulation_log.txt"),
    },
  }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
  main()
