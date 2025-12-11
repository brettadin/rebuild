from typing import List

DEFAULT_COLORS = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'
]


class ColorManager:
    def __init__(self, palette: List[str] = None):
        self.palette = palette or DEFAULT_COLORS.copy()
        self.index = 0

    def next_color(self) -> str:
        color = self.palette[self.index % len(self.palette)]
        self.index += 1
        return color

    def reset(self):
        self.index = 0
