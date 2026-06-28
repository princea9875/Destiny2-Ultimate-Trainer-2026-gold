from __future__ import annotations
import asyncio, logging
from typing import Dict
import keyboard, discordrpc
from src.config import Config
from src.memorymanager import MemoryManager
from src.offsets import offsets

log = logging.getLogger("Destiny2-Ultimate-Trainer-2026-gold.Trainer")

class Trainer:
    def __init__(self, config: Config):
        self.config = config
        self.memory = MemoryManager(config.process_name)
        self.running = False
        self.features: Dict[str,bool] = { "god_mode": False, "unlimited_ammo": False, "esp": False, "speed_hack": False, "no_recoil": False, "loot_unlocker": False, "bounty_complete": False, "aimbot": False }
        self.lock = asyncio.Lock()
        self.discord = None
        if config.discord_rich_presence:
            try:
                discordrpc.initialize('123456789012345678')
                self.discord = True
            except:
                pass

    async def start(self):
        self.running = True
        keyboard.add_hotkey(self.config.hotkey_toggle, self.toggle_cheats)
        keyboard.add_hotkey(self.config.hotkey_exit, self.stop)
        asyncio.create_task(self._loop())

    async def _loop(self):
        while self.running:
            await asyncio.sleep(0.05)
            if not self.memory.pm:
                continue
            async with self.lock:
                if self.features["god_mode"]:
                    await self.memory.write_pointer(offsets.PLAYER_BASE, offsets.PLAYER_OFFSETS, 1, "int32")
                if self.features["unlimited_ammo"]:
                    await self.memory.write_pointer(offsets.UNLIMITED_AMMO, [], 1337, "int32")
            if self.discord:
                self._update_discord()

    def _update_discord(self):
        active = [n for n,v in self.features.items() if v]
        try:
            discordrpc.update_presence(state=", ".join(active) if active else "Idle",
                                       details="Destiny2-Ultimate-Trainer-2026-gold", large_image="logo", large_text="v2.0.0")
        except:
            pass

    async def toggle_feature(self, feature: str, value: bool):
        async with self.lock:
            if feature in self.features:
                self.features[feature] = value
                log.info(f"{feature} -> {value}")

    def toggle_cheats(self):
        asyncio.create_task(self.toggle_feature("god_mode", not self.features["god_mode"]))

    def stop(self):
        self.running = False
        if self.discord:
            try:
                discordrpc.shutdown()
            except:
                pass
        keyboard.unhook_all()
