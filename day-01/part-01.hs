import Control.Arrow ((>>>))
import Control.Exception (assert)

solve :: [String] -> Int
solve = foldl processLine (50, 0) >>> snd

processLine (pos, count) line =
    let (dir:rest) = line
        value = read rest :: Int
        delta = if dir == 'L' then -value else value
        newPos = (pos + delta) `mod` 100
        newCount = if newPos == 0 then count + 1 else count
    in (newPos, newCount)

main :: IO ()
main = do
  -- Test with example
  exampleContent <- readFile "day-01/example.txt"
  let exampleResult = solve (lines exampleContent)
  assert (exampleResult == 3) $ return ()

  -- Solve with input
  inputContent <- readFile "day-01/input.txt"
  let result = solve (lines inputContent)
  print result
