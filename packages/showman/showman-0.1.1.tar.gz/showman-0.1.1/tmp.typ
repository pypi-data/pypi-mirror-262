#let csv-to-table(data, n-rows: -2) = {
  let headers = data.at(0)
  let rows = data.slice(1, n-rows + 1)
  let data-dict = headers.enumerate().map(idx-header => {
    let (idx, header) = idx-header
    let col = rows.map(row => row.at(idx))
    ((header): col)
  }).sum()
  data-dict.a = data-dict.a.map(x => int(x))
  data-dict
}

#let csv-data = "
a,b,c
1,2,3
4,5,6
7,8,9
"
#csv-to-table(csv.decode(csv-data))