// Colorscheme
// https://www.schemecolor.com/macos-window-ui-colors.php

#let width = 300pt
#let inset_size = 10pt
#let radius_size = 10pt

#let button_size = 10pt
#let button_spacing = 10pt

#let button_red_color = rgb("FF605C")
#let button_orange_color = rgb("FFBD44")
#let button_green_color = rgb("00CA4E")
#let toolbar_bg_color = rgb("F5F5F5")
#let stroke_color = rgb("E1DFE1")
#let main_bg_color = rgb("FFFFFF")

#let font = "Roboto Mono"

#show raw: set text(font: font)

#let button(
  color: none,
) = {
  return box(
    width: button_size,
    height: button_size,
    radius: button_size,
    fill: color,
  )
}

#let toolbar() = {
  return block(
    width: 100%,
    inset: inset_size,
    radius: (
      top: radius_size,
    ),
    fill: toolbar_bg_color,
    stroke: stroke_color,
    stack(
      dir: ltr,
      spacing: button_spacing,
      button(color: button_red_color),
      button(color: button_orange_color),
      button(color: button_green_color),
    )
  )
}

#let main(
  ps1: [],
  input: [],
  output: [],
) = {
  return block(
    width: 100%,
    inset: inset_size,
    radius: (
      bottom: radius_size,
    ),
    fill: main_bg_color,
    stroke: stroke_color,
    [
      #ps1 #input \
      #output
    ]
  )
}

#let term(
  ps1: [],
  input: [],
  output: [],
) = {
  return align(
    left, 
    box(
      width: 300pt,
      stack(
        dir: ttb,
        align(left, toolbar()),
        main(
          ps1: ps1,
          input: input,
          output: output,
        ),
      )
    )
  )
}