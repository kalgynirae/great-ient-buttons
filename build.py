from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from textwrap import dedent

from colormath.color_conversions import convert_color
from colormath.color_objects import ColorBase, LabColor, LCHabColor, sRGBColor

VERSION = "0.1.0"

@dataclass(frozen=True)
class Color:
    l: float
    c: float
    h: float

    def __str__(self) -> str:
        return convert_color(
            LCHabColor(self.l, self.c, self.h), sRGBColor
        ).get_rgb_hex()

    def set(self, l: float | None = None, c: float | None = None, h: float | None = None) -> Color:
        return type(self)(
            l=self.l if l is None else max(l, 0),
            c=self.c if c is None else max(c, 0),
            h=self.h if h is None else h % 360,
        )

    def adjust(self, l: float = 0, c: float = 0, h: float = 0) -> Color:
        return self.set(l=self.l + l, c=self.c + c, h=self.h + h)


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
          .gb-{name} {{
            --gb-background: linear-gradient(to bottom, {color} 40%, {color.adjust(l=-6)} 100%);
            --gb-background-hover: linear-gradient(to bottom, {color.adjust(l=6)} 20%, {color} 100%);
            --gb-background-active: linear-gradient(to bottom, {color.adjust(l=-12)} 20%, {color.adjust(l=-8)} 100%);
            --gb-background-disabled: {color.adjust(l=-10, c=-10)};
            --gb-border-color: black;
            --gb-border-radius: 10px;
            --gb-box-shadow-color: {color.adjust(l=5, c=-5)};
            --gb-box-shadow-color-active: {color.adjust(c=5)};
            --gb-color: {color.adjust(l=50, c=-35)};
            --gb-color-disabled: {color.adjust(l=10, c=-35)};
            --gb-text-shadow-color: {color.adjust(l=-30)};
            --gb-background-label: {color.adjust(l=-5, c=-10)};
            --gb-color-label: {color.adjust(l=-30)};
            --gb-text-color1: {color.adjust(l=40, c=-10)};
            --gb-text-color2: {color.adjust(l=40, c=-10, h=90)};
            --gb-text-color3: {color.adjust(l=40, c=-10, h=-90)};
            --gb-link-color: {color.adjust(l=18)};
            --gb-link-color-hover: {color.adjust(l=23, c=5)};
          }}
        """
    )
    color_classes.append(css)

stylesheet = """\
/* Great‼-ient Buttons v<VERSION> */
/* See https://github.com/kalgynirae/great-ient-buttons for license information. */

/* Selected resets from normalize.css (https://necolas.github.io/normalize.css/) */
button {
  font-family: inherit;
  font-size: 100%;
  line-height: 1.15;
  margin: 0;
  overflow: visible;
  text-transform: none;
  -webkit-appearance: button;
}

.gb-button {
  background: var(--gb-background);
  border-radius: var(--gb-border-radius);
  border: solid 1px var(--gb-border-color);
  box-shadow: inset 0 1px 0 0 var(--gb-box-shadow-color);
  color: var(--gb-color);
  line-height: 1.8;
  padding: 0 0.5em;
  text-shadow: 1px 1px 0px var(--gb-text-shadow-color);
  text-transform: none;
  touch-action: manipulation;
  white-space: nowrap;
}
a.gb-button {
  text-decoration: none;
}
a.gb-button:hover {
  color: var(--gb-color);
}
.gb-label {
  background: var(--gb-background-label);
  border-radius: var(--gb-border-radius);
  border: solid 1px var(--gb-border-color);
  box-sizing: border-box;
  color: var(--gb-color-label);
  cursor: default;
  line-height: 1.8;
  text-align: center;
  padding: 0 0.5em;
  white-space: nowrap;
}
.gb-label > *, .gb-button > * {
  vertical-align: middle;
}
.gb-button:hover {
  background: var(--gb-background-hover);
}
.gb-button:active, .gb-button.active {
  background: var(--gb-background-active);
  box-shadow: inset 0 0 0 1px var(--gb-box-shadow-color-active);
}
.gb-button:disabled {
  background: var(--gb-background-label);
  box-shadow: none;
  color: var(--gb-color-disabled);
}
.gb-button svg path {
  fill: var(--gb-color);
}
.gb-label svg path {
  fill: var(--gb-color-label);
}
.gb-button svg {
  filter: drop-shadow(1px 1px 0 var(--gb-text-shadow-color));
}

a.gb-button {
  display: inline-block;
}

.gb-row {
  display: flex;
  align-items: center;
  justify-content center;
}
.gb-row.gb-large {
  font-size: 2em;
}
.gb-row > * {
  flex: initial;
}
.gb-row.gb-stretch > * {
  flex: 0 1 100%;
}
.gb-row > .gb-label {
  flex: none;
}

@media (min-width: 600px) {
  .gb-row > :not(:last-child) {
    border-right-width: 0;
    border-top-right-radius: 0;
    border-bottom-right-radius: 0;
  }
  .gb-row > :not(:first-child) {
    border-top-left-radius: 0;
    border-bottom-left-radius: 0;
  }
}

.gb-big {
  line-height: 2.4;
  padding: 0 1em;
}

@media (max-width: 599px) {
  .gb-row {
    align-items: stretch;
    flex-direction: column;
  }
  .gb-row > :not(:last-child) {
    border-bottom-width: 0;
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
  }
  .gb-row > :not(:first-child) {
    border-top-left-radius: 0;
    border-top-right-radius: 0;
  }
}
""".replace("<VERSION>", VERSION) + "\n".join(
    color_classes
)

print(stylesheet, end="")
