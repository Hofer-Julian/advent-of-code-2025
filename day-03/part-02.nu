use std


def find-digit [bank: string, last_index: int, max_index: int] {
    9..0
        | each { |digit|
            let search_range = $bank | str substring ($last_index + 1)..($max_index - 1)
            let idx = $search_range | str index-of ($digit | into string)
            if $idx >= 0 {
                { digit: $digit, index: ($last_index + 1 + $idx) }
            } else {
                null
            }
        }
        | compact
        | first
}


def extract-bank-value [bank: string] {
    let length = $bank | str length
    11..0
        | reduce --fold { value: 0, last_index: -1 } { |exponent, acc|
            let max_index = $length - $exponent
            let result = find-digit $bank $acc.last_index $max_index
            {
                value: ($acc.value + $result.digit * (10 ** $exponent))
                last_index: $result.index
            }
        }
        | get value
}


def solve [] {
    $in
        | str trim
        | lines
        | each { |bank| extract-bank-value $bank }
        | math sum
}


let result = open day-03/example.txt | solve
std assert equal $result 3121910778619

open day-03/input.txt | solve
