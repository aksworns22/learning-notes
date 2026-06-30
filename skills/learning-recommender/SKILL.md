---
name: "learning-recommender"
description: "Recommend the next study topic from learning-logs."
---

# Learning Recommender

Use this skill when the user asks what to study next, asks for a learning recommendation, wants a study path, or asks to continue from existing learning history.

## Sources

- First inspect `learning-logs/` and treat it as the source of truth for study history.
- If the workspace contains nested learning logs such as `learning-logs/learning-logs/`, inspect the nested content too.
- Prefer recent handoff, recap, summary, and dated files before reading large raw notes.
- Use raw notes when recaps are missing, stale, or too vague.
- Do not load private long-term memory in shared or group chats unless explicitly permitted by current workspace rules.

## Workflow

1. List available learning-log files and identify likely topics, recency, and formats.
2. Read enough relevant files to determine:
   - what the learner has recently studied,
   - what appears unfinished,
   - what prerequisite gaps are visible,
   - what would compound best with recent work.
3. Recommend one primary next learning item.
4. Include a short reason tied to the observed logs.
5. Offer one concrete next action, such as a reading target, implementation exercise, recap task, or quiz request.
6. If useful, include one alternative path for a different goal, but keep the default recommendation clear.

## Recommendation Heuristics

Prioritize recommendations that:

- Continue an active thread from the most recent logs.
- Close a prerequisite gap before moving to a harder topic.
- Convert passive reading into implementation practice.
- Revisit weak or partially completed notes when the learner has jumped ahead.
- Connect adjacent topics already present in the logs, such as LLM fundamentals, LangChain/LangGraph, agents, evals, and Python internals.

Avoid recommendations that:

- Pretend to know progress that is not visible in the logs.
- Jump to trendy topics without a connection to the learner's notes.
- Produce a long syllabus when the user asked for the next step.
- Expose private details from unrelated memory or personal files in a group chat.

## Default Output

For a normal request, answer in Korean with:

- `추천:` one specific next topic or resource from the logs.
- `이유:` 1-2 sentences grounded in the learning history.
- `바로 할 일:` one practical task for the next study session.
- `대안:` optional, only if there is a clearly different useful route.

Keep the answer concise enough for chat. Use longer plans only when the user asks for a curriculum, roadmap, or schedule.

## Missing Or Thin Logs

If no usable learning logs are found, say that the learning logs are missing or too thin and ask the user to add notes or point to source material. Do not invent a study history.
