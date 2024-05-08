from enum import Enum

class OrderHistoryStatus(Enum):
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    CANCELLED = 'CANCELLED'
    
    
class OrderType(Enum):
    DINE_IN = 'DINE_IN'
    PACK = 'PACK'
    DELIVERY = 'DELIVERY'