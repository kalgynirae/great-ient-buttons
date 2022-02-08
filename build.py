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

    def set(
        self, l: int | None = None, c: int | None = None, h: int | None = None
    ) -> Color:
        return type(self)(
            l=self.l if l is None else l,
            c=self.c if c is None else c,
            h=self.h if h is None else h,
        )

    def adjust(self, l: int = 0, c: int = 0, h: int = 0) -> Color:
        return type(self)(self.l + l, self.c + c, self.h + h)


base_colors = dict(
    red=Color(45, 35, 0),
    orange=Color(45, 35, 45),
    yellow=Color(45, 35, 90),
    green=Color(45, 35, 135),
    cyan=Color(45, 35, 180),
    blue=Color(45, 35, 225),
    indigo=Color(45, 35, 270),
    purple=Color(45, 35, 315),
    gray=Color(45, 0, 0),
)
color_classes = []
for name, color in base_colors.items():
    css = dedent(
        f"""\
          .ob-{name} {{
            --ob-background-normal: linear-gradient(to bottom, {color} 30%, {color.adjust(l=-3.6)} 100%);
            --ob-background-hover: linear-gradient(to bottom, {color.adjust(l=3.6)} 20%, {color} 100%);
            --ob-background-active: linear-gradient(to bottom, {color.adjust(l=-5.4)} 20%, {color.adjust(l=-2.7)} 100%);
            --ob-background-disabled: {color.adjust(c=-18)};
            --ob-border-color: black;
            --ob-border-radius: 10px;
            --ob-border-highlight-color: {color.adjust(l=5.4)};
            --ob-text-shadow-color: {color.adjust(l=-10)};
            --ob-background-label: {color.set(c=0)};
            --ob-color-label: {color.adjust(l=-10).set(c=0)};
          }}
        """
    )
    color_classes.append(css)

stylesheet = """
.ob-button {
  background: var(--ob-background-normal);
  border-radius: var(--ob-border-radius);
  border: solid 1px var(--ob-border-color);
  box-shadow: inset 0 1px 0 0 var(--ob-border-highlight-color);
  color: inherit;
  font-size: 1.5em;
  line-height: 1.8;
  padding: 0 0.4em;
  text-shadow: 1px 1px 0px var(--ob-text-shadow-color);
  touch-action: manipulation;
}
.ob-button.ob-label {
  background: var(--ob-background-label);
  color: var(--ob-color-label);
}
.ob-button:hover {
  background: var(--ob-background-hover);
}
.ob-button:active, .ob-button.active {
  background: var(--ob-background-active);
}
.ob-button:disabled {
  background: var(--ob-background-disabled);
  box-shadow: none;
  color: gray;
}
.ob-button > svg {
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
