import enum
from typing import List


class ResourceType(enum.Enum):
    element = 0
    profile = 1
    metadata = 2
    data = 3
    range = 4

    def __str__(self) -> str:
        return self.name

    @classmethod
    def from_string(cls, value: str) -> 'ResourceType':
        return cls.__members__[value]

    @classmethod
    @property
    def semantic_resources(cls) -> List[str]:
        return [str(ResourceType.profile), str(ResourceType.metadata), str(ResourceType.data), str(ResourceType.range)]

    def is_semantic(self) -> bool:
        return self.value in range(1, 5)
