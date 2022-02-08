from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from textwrap import dedent

from colormath.color_conversions import convert_color
from colormath.color_objects import ColorBase, LabColor, LCHabColor, sRGBColor


@dataclass(frozen=True)
class Color:
    l: float
    c: float
    h: float

    def __str__(self) -> str:
        return convert_color(
            LCHabColor(self.l, self.c, self.h), sRGBColor
        ).get_rgb_hex()

    def set(self, l: float | None = None, c: float | None = None) -> Color:
        return type(self)(
            l=self.l if l is None else max(l, 0),
            c=self.c if c is None else max(c, 0),
            h=self.h,
        )

    def adjust(self, l: float = 0, c: float = 0) -> Color:
        return self.set(l=self.l + l, c=self.c + c)


base_colors = dict(
    red=Color(35, 35, 0),
    orange=Color(35, 35, 45),
    yellow=Color(35, 35, 90),
    green=Color(35, 35, 135),
    cyan=Color(35, 35, 180),
    blue=Color(35, 35, 225),
    indigo=Color(35, 35, 270),
    purple=Color(35, 35, 315),
    gray=Color(35, 0, 0),
)
color_classes = []
for name, color in base_colors.items():
    css = dedent(
        f"""\
          .ob-{name} {{
            --ob-background: linear-gradient(to bottom, {color} 40%, {color.adjust(l=-6)} 100%);
            --ob-background-hover: linear-gradient(to bottom, {color.adjust(l=6)} 20%, {color} 100%);
            --ob-background-active: linear-gradient(to bottom, {color.adjust(l=-12)} 20%, {color.adjust(l=-8)} 100%);
            --ob-background-disabled: {color.adjust(l=-10, c=-10)};
            --ob-border-color: black;
            --ob-border-radius: 10px;
            --ob-box-shadow-color: {color.adjust(l=5, c=-5)};
            --ob-box-shadow-color-active: {color.adjust(c=5)};
            --ob-color: {color.adjust(l=50, c=-35)};
            --ob-color-disabled: {color.adjust(l=10, c=-35)};
            --ob-text-shadow-color: {color.adjust(l=-30)};
            --ob-background-label: {color.adjust(l=-5, c=-10)};
            --ob-color-label: {color.adjust(l=-30)};
          }}
        """
    )
    color_classes.append(css)

stylesheet = """
.ob-button {
  background: var(--ob-background);
  border-radius: var(--ob-border-radius);
  border: solid 1px var(--ob-border-color);
  box-shadow: inset 0 1px 0 0 var(--ob-box-shadow-color);
  color: var(--ob-color);
  font-family: inherit;
  font-size: 100%;
  line-height: 1.8;
  margin: 0;
  overflow: visible;
  padding: 0 0.4em;
  text-shadow: 1px 1px 0px var(--ob-text-shadow-color);
  text-transform: none;
  touch-action: manipulation;
}
.ob-label {
  background: var(--ob-background-label);
  border-radius: var(--ob-border-radius);
  border: solid 1px var(--ob-border-color);
  box-sizing: border-box;
  color: var(--ob-color-label);
  cursor: default;
  font-size: 100%;
  line-height: 1.8;
  padding: 0 0.4em;
}
.ob-label > *, .ob-button > * {
  vertical-align: middle;
}
.ob-button:hover {
  background: var(--ob-background-hover);
}
.ob-button:active, .ob-button.active {
  background: var(--ob-background-active);
  box-shadow: inset 0 0 0 1px var(--ob-box-shadow-color-active);
}
.ob-button:disabled {
  background: var(--ob-background-label);
  box-shadow: none;
  color: var(--ob-color-disabled);
}
.ob-button svg path {
  fill: var(--ob-color);
}
.ob-label svg path {
  fill: var(--ob-color-label);
}
.ob-button svg {
  filter: drop-shadow(1px 1px 0 var(--ob-text-shadow-color));
}

.ob-row {
  display: flex;
  align-items: center;
  justify-content center;
}
.ob-row.ob-large {
  font-size: 2em;
}
.ob-row > * {
  flex: 1 0 0;
}
.ob-row.ob-stretch > * {
  flex: 0 1 100%;
}
.ob-row > .ob-label {
  flex: 0 1 0;
}
.ob-row > :not(:last-child) {
  border-right-width: 0;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}
.ob-row > :not(:first-child) {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}

""" + "\n".join(
    color_classes
)

print(stylesheet, end="")
