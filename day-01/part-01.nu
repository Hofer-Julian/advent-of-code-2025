use std


def part-one [] {
    let input = lines
        | reduce --fold [50, 0] { |l, acc|
            let sign = if ($l | str substring 0..0) == "L" {
                -1
            } else {
                +1
            }
            let value = $l | str substring 1.. | into int
            mut result = $acc.0 + $sign * $value
            loop {
                if $result > 0 {
                    break
                }
                $result = $result + 100
            }
            loop {
                if $result < 100 {
                    break
                }
                $result = $result - 100
            }
            let count = $acc.1 + if $result == 0 { 1 } else { 0 }
            [$result, $count]
        }
    $input.1
}

let result = open day-01/example.txt | part-one
std assert equal $result 3

open day-01/input.txt | part-one
