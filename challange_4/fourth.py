import copy

def read_file():
  data = open('input', 'r').read().split('\n')
  return data[:-1]

def load_board(data, index):
  boards = []
  for i in range(0, 5):    
    bingo_board = data[i + index].split(' ')
    bingo_board = [x.strip() for x in bingo_board if x]
    boards.append(bingo_board)

  return boards

zero_board = [
  [0,0,0,0,0],
  [0,0,0,0,0],
  [0,0,0,0,0],
  [0,0,0,0,0],
  [0,0,0,0,0]
]

def print_boards(boards):
  board_len = len(boards)
  for board_idx in range(board_len):
    for i in range(5):
      for j in range(5):
        print(f'{boards[board_idx][i][j]}\t ', end = '')
      print('')
    print('\n')
  print('---')

def build_boards(data):
  boards = []
  scores = []
  for i in range(2, data_len - 1, 6):
    boards.append(load_board(data, i))
    scores.append(copy.deepcopy(zero_board))

  return boards, scores

def calc_score(board, score):
  sum = 0
  for i in range(5):
    for j in range(5):
      if score[i][j] == 0:
        sum += int(board[i][j])
  return sum

def mark(scores, boards, index, expected_number):
  for i in range(5):
    for j in range(5):
      if boards[index][i][j] == expected_number:
        scores[index][i][j] = 1
    
def check_score(scores, boards, index):
  for i in range(5):
    sum_row = 0
    sum_col = 0
    for j in range(5):
      sum_row += scores[index][i][j]
      sum_col += scores[index][j][i]
    if sum_row == 5 or sum_col == 5:
      return True

  return False

def game_loop(scores, boards, input):
  winner_counter = {}
  boards_len = len(boards)

  for number in input:
    print(f'Current number {number}')
    number = number.strip()

    for index in range(boards_len):
      mark(scores, boards, index, number)

    for index in range(boards_len):
      winner = check_score(scores, boards, index)

      if winner:
        winner_counter[index] = 1
        score = calc_score(boards[index], scores[index])        

        print(f'==== Winner score {score}, number {number}, index {index}, result {int(score) * int(number)} ====')
      
        if len(winner_counter) == len(boards):
          print(f'It was last board')
          return (score, number)

data = read_file()
data_len = len(data)

input = data[0].split(',')
print(f'Input {input}\n')

boards, scores = build_boards(data)
game_loop(scores, boards, input)
