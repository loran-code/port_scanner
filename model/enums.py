from enum import Enum


class PortState(Enum):
    CLOSED = 0
    OPEN = 1
    FILTERED = 2
    """
    The filtering could be from a dedicated firewall device,
     router rules, or host-based firewall software.
    """
