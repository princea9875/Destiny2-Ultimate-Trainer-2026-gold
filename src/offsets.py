from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Offsets:
    GOD_MODE: int = 0x2a4b502
    UNLIMITED_AMMO: int = 0x2a4b4ad
    ESP_ENABLED: int = 0x2a4b68a
    SPEED_HACK: int = 0x2a4b726
    NO_RECOIL: int = 0x2a4b6f4
    LOOT_UNLOCKER: int = 0x2a4b81e
    BOUNTY_COMPLETE: int = 0x2a4b8bc
    AIMBOT_FOV: int = 0x2a4b9ac
    PLAYER_BASE: int = 0x1e8a4c5
    PLAYER_OFFSETS: list = field(default_factory=lambda: [0x0, 0x30, 0x8, 0x20])
    VERSION_OFFSETS: Dict[str, Dict[str,int]] = field(default_factory=lambda: {
        "2026.06.28-280": {
            "GOD_MODE": 0x2a4b502,
            "UNLIMITED_AMMO": 0x2a4b4ad,
        }
    })
    def get_for_version(self, ver): return self.VERSION_OFFSETS.get(ver, {})

offsets = Offsets()
