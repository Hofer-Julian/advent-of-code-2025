use std


def parse-range [input: string] {
    let parts = $input | split row "-"
    { lower: ($parts.0 | into int), upper: ($parts.1 | into int) }
}


def ranges-overlap [a: record, b: record] {
    ($a.lower <= $b.lower and $b.lower <= $a.upper or
     $b.lower <= $a.lower and $a.lower <= $b.upper)
}


def merge-two-ranges [a: record, b: record] {
    { lower: ([$a.lower, $b.lower] | math min), upper: ([$a.upper, $b.upper] | math max) }
}


def merge-ranges [] {
    sort-by lower
    | reduce --fold [] { |range, acc|
        if ($acc | is-empty) {
            [$range]
        } else {
            let last = $acc | last
            if (ranges-overlap $last $range) {
                $acc | drop | append (merge-two-ranges $last $range)
            } else {
                $acc | append $range
            }
        }
    }
}


def solve [] {
    $in
        | str trim
        | split row "\n\n"
        | first
        | lines
        | each { |line| parse-range $line }
        | merge-ranges
        | each { |range| $range.upper - $range.lower + 1 }
        | math sum
}


let result = open day-05/example.txt | solve
std assert equal $result 14

open day-05/input.txt | solve
