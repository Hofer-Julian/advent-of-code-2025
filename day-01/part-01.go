package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func solve(lines []string) int {
	position := 50
	count := 0

	for _, line := range lines {
		if len(line) == 0 {
			continue
		}

		direction := line[0]
		value, _ := strconv.Atoi(line[1:])

		if direction == 'L' {
			position -= value
		} else {
			position += value
		}

		for position < 0 {
			position += 100
		}
		for position >= 100 {
			position -= 100
		}

		if position == 0 {
			count++
		}
	}

	return count
}

func readLines(filename string) ([]string, error) {
	content, err := os.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	text := strings.TrimSpace(string(content))
	return strings.Split(text, "\n"), nil
}

func main() {
	// Test with example
	exampleLines, _ := readLines("day-01/example.txt")
	exampleResult := solve(exampleLines)
	if exampleResult != 3 {
		fmt.Printf("Example failed: expected 3, got %d\n", exampleResult)
		os.Exit(1)
	}

	// Solve with input
	inputLines, _ := readLines("day-01/input.txt")
	result := solve(inputLines)
	fmt.Println(result)
}
