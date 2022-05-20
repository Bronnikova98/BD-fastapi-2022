from .base_models import *
from typing import List

# Схемы включают в себя ссылки на другие сущности для вложеного вывода
# их нужно выносить отдельно, чтобы избежать рекурсии в импорте
class ClimberSchema(ClimberBase):
    climbings: List[ClimbingBase]

class ClimbingSchema(ClimbingBase):
    climbers: List[ClimberBase]
    
