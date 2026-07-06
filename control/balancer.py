"""Балансировка нагрузки между модулями сортировщика."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ModuleLoad:
    module_id: int
    active_items: int = 0
    induction_queue: int = 0
    failed: bool = False
    degraded: bool = False


@dataclass
class InputBalancer:
    num_modules: int
    modules: dict[int, ModuleLoad] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.modules:
            self.modules = {
                i: ModuleLoad(module_id=i) for i in range(1, self.num_modules + 1)
            }

    def score(self, module_id: int) -> float:
        module = self.modules[module_id]
        if module.failed:
            return float("inf")
        penalty = 1.35 if module.degraded else 1.0
        return (module.active_items + module.induction_queue * 0.5) * penalty

    def select_module(self, preferred_module: int | None = None) -> int | None:
        available = [m for m, load in self.modules.items() if not load.failed]
        if not available:
            return None
        if preferred_module and preferred_module in available:
            preferred_score = self.score(preferred_module)
            best = min(available, key=self.score)
            if self.score(best) + 2 < preferred_score:
                return best
            return preferred_module
        return min(available, key=self.score)

    def on_induction_start(self, module_id: int) -> None:
        self.modules[module_id].induction_queue += 1

    def on_induction_end(self, module_id: int) -> None:
        module = self.modules[module_id]
        module.induction_queue = max(0, module.induction_queue - 1)
        module.active_items += 1

    def on_item_complete(self, module_id: int) -> None:
        module = self.modules[module_id]
        module.active_items = max(0, module.active_items - 1)

    def set_failed(self, module_id: int) -> None:
        self.modules[module_id].failed = True

    def set_degraded(self, module_id: int) -> None:
        self.modules[module_id].degraded = True
