# 演讲稿 — Tang Dynasty Generative Agent Simulation
**总时长：8分钟 | 10张幻灯片**

---

## 【Slide 1 — 封面】 0:00–0:30

Good morning / afternoon, everyone.

Today I'm presenting a generative agent simulation set in Tang Dynasty China — specifically, Chang'an on the night of the Lantern Festival, 742 AD. I ran this simulation using the Stanford Smallville framework with an LLM backend, and over the next eight minutes I'll walk you through what the agents did, what that tells us about history, and — perhaps more importantly — what the simulation *couldn't* do, and why that matters.

---

## 【▶ 翻到 Slide 2 — Historical Context】 0:30–1:15

**（翻页）**

Let me start with the historical setting.

742 AD, Chang'an — the largest city in the world, roughly one million people. The West Market was the eastern terminus of the Silk Road, where Sogdian, Persian, and Central Asian merchants legally operated alongside Chinese traders. The Lantern Festival was the one night each year when the nocturnal curfew was lifted — meaning everyone, from imperial officials to street laborers, was out in the same public space at the same time.

This is why I chose the Lantern Festival as the scenario. It creates a moment of maximum social fluidity — all three of my agent archetypes have a plausible reason to be in the same space simultaneously. It also requires the LLM to draw on very specific historical knowledge: the imperial examination system, Silk Road commerce, and Tang social hierarchy.

---

## 【▶ 翻到 Slide 3 — Agent Setup】 1:15–2:10

**（翻页）**

Three agents were built on the Smallville framework, each reskinned with a Tang Dynasty identity and seeded with twelve custom memory nodes.

Li Mingzhu, a thirty-two-year-old tea house proprietress — her goal: host a successful Lantern Festival gathering, greet customers, keep the tea flowing.

Chen Zian, a twenty-four-year-old provincial scholar preparing for the imperial examinations — his goal: gather intelligence on examiner preferences, review the Classics, practice regulated verse.

And An Lushan, a thirty-eight-year-old Sogdian merchant from the Silk Road — his goal: sell glass cups and aromatic spices, secure local business partners, host a trade feast before his caravan departs.

Three agents who, in historical reality, would have very different legal statuses, very different access to social space — but all plausibly present on Lantern Festival night.

---

## 【▶ 翻到 Slide 4 — Behavior Overview】 2:10–3:10

**（翻页）**

The simulation ran five thousand steps — ten seconds per step — covering approximately fourteen hours of in-world time, from six in the evening on February 15th through to just before eight the following morning.

And here's the first thing you need to know about the results: roughly ninety-one percent of all agent-steps were sleep states. That bar on the left? That's basically all dark blue. Despite the Lantern Festival context, despite Li Mingzhu's explicit goal to host an evening gathering, the scheduling system — inherited from a contemporary American college-town simulation — defaulted to long sleep blocks.

But within that ninety-one percent, there were real moments. Li Mingzhu actively hosted for the first hour. The two scholars had a sixteen-turn conversation at eighteen-oh-one. An Lushan ran his trade activities in the middle of the evening. And Chen Zian studied late into the night. So there *is* a historical arc — it's just buried under a lot of sleep.

---

## 【▶ 翻到 Slide 5 — Conversation】 3:10–4:10

**（翻页）**

The most interesting output was this conversation — the scholar meets the merchant, Step 8, six minutes into the simulation.

Chen Zian opens by asking An Lushan whether he's heard any whispers about what the current examiners value. An Lushan deflects — "that's somewhat beyond my expertise" — while simultaneously identifying Chen Zian as a potential customer: "the families of successful candidates often become my best customers."

What's striking here is what *wasn't* scripted. Both agents, independently, named Li Mingzhu's tea house as a meeting venue — without any coordination prompt. And the underlying social logic — the scholar wants intelligence, the merchant wants referrals — mirrors documented patterns of instrumental cross-class interaction in Tang urban life.

This is the simulation doing something genuinely interesting: generating historically coherent social dynamics from memory-seeded goals, without being told exactly what to say.

---

## 【▶ 翻到 Slide 6 — Behavior Analysis】 4:10–5:00

**（翻页）**

Three patterns stand out from the behavior analysis.

First, role consistency — every agent, when active, acted within their seeded identity. The goal architecture worked directionally. The problem was coverage, not coherence.

Second, emergent social convergence — that spontaneous tea house naming is the clearest evidence that seeded memory can produce historically plausible emergent behavior beyond the prompt specifications.

Third, and most critically — sleep dominance. Ninety-one percent. This isn't a historical claim. It's an architectural constraint inherited from a system built for a different world. And it tells us something important: you can't reskin a framework with historical names and expect historical behavior if the underlying scheduling logic is fundamentally incompatible with the scenario.

---

## 【▶ 翻到 Slide 7 — Historical Plausibility】 5:00–5:45

**（翻页）**

So what did the simulation actually get right, and what did it distort?

On the left — what fits. The scholar-merchant intelligence exchange reflects documented Tang exam culture. An Lushan's strategy of cultivating scholars as future customers reflects Sogdian merchant social positioning. Li Mingzhu's active hosting reflects documented female agency in Tang commercial spaces.

On the right — the distortions. The tile map is an American college town. There are no honorifics in the dialogue. The agents interact as social equals, when Tang law would have placed a foreign merchant below an examination candidate. And of course — ninety-one percent sleep during the Lantern Festival is, to put it mildly, historically implausible.

---

## 【▶ 翻到 Slide 8 — Critique】 5:45–6:30

**（翻页）**

This brings me to the critique.

The simulation makes the LLM's training corpus into the implicit historical source. MiniMax-M2's knowledge of Tang social dynamics is uneven — and students who watch Chen Zian and An Lushan have a coherent conversation might mistake fluent dialogue for historically accurate dialogue. That's a real pedagogical risk.

More fundamentally, the simulation embeds structural assumptions: that history is made by three named individuals with explicit goals; that text dialogue is the primary form of social action; that a contemporary spatial map is a neutral container for any historical context. These assumptions erase legal hierarchy, ethnic status, gendered access to commercial space — and they erase the majority of historical actors entirely.

So before using this simulation in a classroom, students would need grounding in the examination system, Silk Road commerce, critical AI literacy — and an explicit framework for reading the simulation's failures as evidence, not noise.

---

## 【▶ 翻到 Slide 9 — Strengths & Limitations】 6:30–7:20

**（翻页）**

Quickly on strengths and limitations.

The strengths are real: the emergent social logic in the conversation, Li Mingzhu's goal-aligned hosting at dusk, the fourteen-hour arc that covers distinct role-specific rhythms across the full evening and night.

The limitations are also real: ninety-one percent sleep, a spatially incompatible map, only two conversations across five thousand steps, and the complete absence of structural power, collective behavior, and material culture.

The simulation is most useful not as an exploration tool, but as a critical thinking prompt — a generative provocation for asking what historical simulation can and cannot do.

---

## 【▶ 翻到 Slide 10 — Final Reflection】 7:20–8:00

**（翻页）**

To close.

This simulation produces its most historically interesting output precisely where it fails. Li Mingzhu sleeping through most of the festival she was designed to host. The scheduling system overriding an explicit goal. Ninety-one percent dark blue. These are not historical claims — they are evidence of the framework's inherited assumptions.

When the simulation did work — the opening hour of hosting, the instrumental exchange, the spontaneous convergence on the tea house — it showed that LLM agents with seeded historical memory can produce *directionally plausible* social behavior without explicit scripting. That's genuinely interesting.

But the simulation's real value isn't what the agents got right. It's using the failures, the absences, and the distortions as a mirror — to ask what historical simulation cannot do, and why that matters for how we understand the past.

Thank you.

---

## 时间分配速查

| 幻灯片 | 内容 | 时间段 | 时长 |
|--------|------|--------|------|
| Slide 1 | 封面 · 开场 | 0:00–0:30 | 30秒 |
| Slide 2 | 历史背景 | 0:30–1:15 | 45秒 |
| Slide 3 | Agent设计 | 1:15–2:10 | 55秒 |
| Slide 4 | 行为总览 | 2:10–3:10 | 60秒 |
| Slide 5 | 重点对话 | 3:10–4:10 | 60秒 |
| Slide 6 | 行为分析 | 4:10–5:00 | 50秒 |
| Slide 7 | 历史可信度 | 5:00–5:45 | 45秒 |
| Slide 8 | 批判 | 5:45–6:30 | 45秒 |
| Slide 9 | 优势与局限 | 6:30–7:20 | 50秒 |
| Slide 10 | 结语 | 7:20–8:00 | 40秒 |
