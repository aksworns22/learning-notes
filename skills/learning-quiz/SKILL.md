---
name: "learning-quiz"
description: "Generate skill-building quizzes from learning notes."
---

# Learning Quiz

Use this skill when the user asks for a quiz based on study material, learning notes, recent learning, or asks to improve knowledge/skill through questions.

## Source Material

- First inspect `learning-logs/` for the relevant learning content.
- If `learning-logs/` does not exist, say that no usable learning logs were found and ask the user to provide or point to the learning material.
- If multiple plausible topics exist, choose a focused topic from the available notes.

## Quiz Purpose

The goal is skill and knowledge improvement, not trivia.

Design questions that make the learner:

- Recall important concepts from the notes.
- Distinguish similar concepts or tools.
- Explain why a choice is correct.
- Apply the idea to a small practical scenario.
- Notice common mistakes or gaps in understanding.

## Workflow

1. Read the relevant files under `learning-logs/` before making the quiz.
2. Identify one concrete learning objective.
3. Ask one concise quiz question unless the user requests more.
4. Use multiple choice, short answer, or scenario format based on the content.
5. Do not reveal the answer immediately unless the user asks for it.
6. After the user answers, give brief feedback: correct answer, why, and one improvement note.

## Default Quiz Shape

For a single quiz request, prefer:

- One question.
- Four options for concept checks, or a short-answer prompt for applied reasoning.
- A clear connection to the source learning note.
- No long lecture in the first message.

## When Notes Are Missing

If no usable learning notes are found, say that the source notes are missing and ask the user to provide or point to the learning material. Do not invent a topic and pretend it came from the notes.
