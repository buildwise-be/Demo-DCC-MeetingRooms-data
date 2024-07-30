from datetime import datetime
from typing_extensions import TypedDict

class EntityType(TypedDict, total=False):
    PartitionKey: str
    RowKey: str
    room: int
    start_time: datetime
    organizer: str
    title: str