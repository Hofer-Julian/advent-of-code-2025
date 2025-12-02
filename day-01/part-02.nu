use std


def solve [] {
    let input = lines
        | reduce --fold [50, 0] { |l, acc|
            mut result = $acc.0
            mut final_count = $acc.1
            let sign = if ($l | str substring 0..0) == "L" {
                -1
            } else {
                +1
            }
            mut value = $l | str substring 1.. | into int

            while $value > 0 {
                $result = ($result + $sign) mod 100
                $value = $value - 1
                if $result == 0 {
                    $final_count = $final_count + 1
                }
            }
            [$result, $final_count]
        }
    $input.1
}

let result = open day-01/example.txt | solve
std assert equal $result 6

open day-01/input.txt | solve
