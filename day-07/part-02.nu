use std

def solve [] {
    let rows = lines
    let r_len = ($rows | length)
    let c_len = ($rows | first | str length)

    # Build initial matrix
    mut matrix = []
    for row in $rows {
        mut matrix_row = []
        for char in ($row | split chars) {
            let value = if $char == "." {
                0
            } else if $char == "S" {
                1
            } else if $char == "^" {
                -1
            } else {
                0
            }
            $matrix_row = ($matrix_row | append $value)
        }
        $matrix = ($matrix | append [$matrix_row])
    }

    # Process the matrix row by row
    for r in 1..<$r_len {
        let prev_row = ($matrix | get ($r - 1))
        mut current_row = ($matrix | get $r)

        for c in 0..<$c_len {
            let value_above = ($prev_row | get $c)
            let current_value = ($current_row | get $c)

            if $value_above >= 1 {
                if $current_value == -1 {
                    # Splitter - distribute to left and right neighbors
                    if $c > 0 {
                        let left_idx = $c - 1
                        let left = ($current_row | get $left_idx)
                        if $left != -1 {
                            $current_row = ($current_row | update $left_idx ($left + $value_above))
                        }
                    }
                    if $c < ($c_len - 1) {
                        let right_idx = $c + 1
                        let right = ($current_row | get $right_idx)
                        if $right != -1 {
                            $current_row = ($current_row | update $right_idx ($right + $value_above))
                        }
                    }
                } else {
                    # Regular cell - add value from above
                    $current_row = ($current_row | update $c ($current_value + $value_above))
                }
            }
        }

        $matrix = ($matrix | update $r $current_row)
    }

    # Sum the last row
    $matrix | last | math sum
}

let result = open day-07/example.txt | solve
std assert equal $result 40

open day-07/input.txt | solve