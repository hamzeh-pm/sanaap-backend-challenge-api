from dataclasses import dataclass


@dataclass
class TaskResponse:
    task_id: str
    title: str
