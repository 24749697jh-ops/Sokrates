from __future__ import annotations

from teacher_engine import (
    build_teacher_instructions,
    classify_task,
    infer_phase,
    topic_key_for,
)


def build_tutor_instructions(task_text: str, messages: list[dict], help_level: int = 1) -> str:
    return build_teacher_instructions(task_text, messages, help_level)


def classify_topic(task_text: str, messages: list[dict]):
    task_type = classify_task(task_text, messages)

    class TopicProfile:
        key = task_type.topic_key
        label = task_type.label

    return TopicProfile()
