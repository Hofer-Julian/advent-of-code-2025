package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
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

		// Wrap position to 0-99 range (proper modulo for negative numbers)
		position = ((position % 100) + 100) % 100

		if position == 0 {
			count++
		}
	}

	return count
}

func readLines(filename string) ([]string, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines, scanner.Err()
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
