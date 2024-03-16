#import "@preview/showman:0.1.0": runner, formatter
#import "term.typ": term

#let cache = json("/.coderunner.json").at("examples/code2.typ", default: (:))
#let container(direction: auto, input, output) = {
  term(ps1: "$", input: input.text, output: output)
}
#let show-rule = runner.external-code.with(
  result-cache: cache,
  container: container
)
#show raw: formatter.format-raw.with(width: 100%)
// #show <example-output>: container
#show raw.where(lang: "bash"): show-rule
#show raw.where(lang: "r"): show-rule

```r
suppressPackageStartupMessages(library(tidyverse))
```

Test

```r
mtcars |> glimpse()
```

Another test

```r
x <- 5
print(x)
```