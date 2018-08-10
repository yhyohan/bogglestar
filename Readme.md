# Boggle API

Boggle is a word game that is played on a 4x4 board with 16 letter tiles.
The goal is to find as many words as possible given a time constraint.  

## Rules

For this boggle game, once it is initiated, user will be given 300 seconds to find as many words as possible, and each word will be scored proportionally to its length.

## How-to

A game needs to be initiated first before any attempts of guessing the words.

#### Start game

To start a game:
  - endpoint: /api/game
  - method: POST
  - request parameter: N/A
  - return parameter: id (required for subsequent call to submit answers, or end the game)

#### Submit answers

User can then submit the word(s), which will be checked against valid words based on the current board arrangement (see Implementation), as long as the game is not over yet:
  - endpoint: /api/game/:id
  - method: POST
  - request parameter: action {"guess"}, answers (string or list of strings)
  - response parameter: id, score, active (false indicates the game is over)

```
{
  "action": "guess",
  "answers": ["KAROOS", "SYBO", "COT", "RAKIS"]
}
```

As part of the response json, there will be a "message" as a feedback for the words that were submitted.

Note: to manually end the game, set action as "end". The game would also end if user has reached the time limit, but the game status would only be updated upon interaction on the game (e.g. user submits an answer). There is no automatic purging for the current implementation.

## Implementation

For the current implementation, the dictionary and board have been pre-loaded on server start up, and the valid words have already been compiled, which will then be used to validate user's guesses.

To generate the list of valid words, recursion and backtracking strategy is used.

Starting at the grid on the board, inspect all its neighbors and start extending the letter in the first grid to the letter in the neighboring cell. Hence, for each grid, it would potentially have 8 branches/search paths.

For example, given this board,

```
F	R	O	O
Y	I	E	S
L	*	N	T
A	E	R	E
```

The steps taken will be as follows:
  - Starting at F (head), neighbors of F: [R, I, Y] -> R is selected to extend the search path (DFS - will only backtrack to I and Y later on)
  - The sequence FR is formed, neighbors of R: [O, E, I, Y] -> F had already been visited on this traversal, and hence is excluded
  - For each sequence formed (FR, FRO), check if it is a valid word
  - Repeat the process until there is no more unvisited neighbors, while keeping track of the valid words found along the way
  - Once the current traversal with F as the head is done, repeat the steps for all grids
  - Special handling on "*" character, on which all the letters will be inspected individually (26 branches)

To avoid wasting resources constructing invalid words (no valid words in the search paths), the sequence that is not prefix to a valid word in the dictionary should be pruned. To achieve this, we build a set of valid prefixes of all the words in the dictionary.

For example, for the word "READ", the prefixes "R", "RE", "REA" are added to the set.
At the end, the set will contain all the possible prefixes. If a sequence that is formed by the search algorithm does not match any prefix, we can be sure there will be no valid word on this search path sequence.

## Sample Response

```json
{
  "data": {
    "id": "5a4383f384334db98d917d6eee86b4fc",
    "board": "TAP* EAKS OBRS S*XD",
    "score": 0,
    "found_words": [],
    "active": true,
    "gametime": 1533826186
  },
  "message": "Good luck playing Boggle!"
}


{
  "data": {
    "id": "5a4383f384334db98d917d6eee86b4fc",
    "board": "TAP* EAKS OBRS S*XD",
    "score": 15,
    "found_words": [
      "SYBO",
      "RAKIS",
      "KAROOS"
    ],
    "active": true,
    "gametime": 1533826186
  },
  "message": "Congratulations! You guessed correctly for SYBO, RAKIS, KAROOS. Invalid answers for COT."
}
```
