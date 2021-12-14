-module(day4).
-export([main/0]).
-export([test/0]).
-import(lists, [last/1, droplast/1, nth/2]).

% Helpers
load_all_boards_data([], Boards) -> Boards;
load_all_boards_data([Head | Rest], Boards) ->
  BoardRow = binary:split(Head, <<" ">>, [global]),
  BoardRowFiltered = lists:filter(fun(Str) -> bit_size(Str) /= 0 end, BoardRow),
  RowElements = lists:map(fun(Str) -> binary_to_integer(string:trim(Str)) end, BoardRowFiltered),
  AllBoards = lists:append(Boards, RowElements),
  load_all_boards_data(Rest, AllBoards).

n_length_chunks([],_) -> [];
n_length_chunks(List, Len) when Len > length(List) ->
    [List];
n_length_chunks(List,Len) ->
    {Head, Tail} = lists:split(Len, List),
    [Head | n_length_chunks(Tail, Len)].

% Data parsing
read_challange_input() ->
  {ok, Data} = file:read_file("input"),
  DataByLine = binary:split(Data, [<<"\n">>], [global]),

  [Input | Rest] = DataByLine,
  InputSplit = binary:split(Input, <<",">>, [global]),
  IntegerInput = lists:map(fun(Str) -> binary_to_integer(string:trim(Str)) end, InputSplit),

  AllData = load_all_boards_data(Rest, []),
  % 25 elements in each board
  % 5 elements in each row
  Boards1d = n_length_chunks(AllData, 25), 
  Boards2d = [n_length_chunks(Board1d, 5) || Board1d <- Boards1d],

  EmptyBoards1d = [[] || _ <- Boards1d],
  EmptyBoards2d = [
    [
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0]
    ] || _ <- EmptyBoards1d
  ],

  [IntegerInput, Boards2d, EmptyBoards2d].

% Tests
is_winner_in_rows([]) -> false;
is_winner_in_rows([Row | Rest]) ->
  ListSum = lists:sum(Row),
  if
     ListSum == 5 ->
      true;
    true ->
      is_winner_in_rows(Rest)
    end.

check_rows(Board) ->
  is_winner_in_rows(Board).

check_col(Rows, Col) ->
  Sum = sum_cols(Rows, Col, 0),
  if
    Sum == 5 ->
      true;
    true ->
      false
  end.

sum_cols([], _, Sum) -> Sum;
sum_cols([Row | Rest], Col, Sum) ->
  Val = lists:nth(Col, Row),
  sum_cols(Rest, Col, Val + Sum).

is_winner_in_cols(_, []) -> false;
is_winner_in_cols(Rows, [Now | Next]) ->
  Is_winner = check_col(Rows, Now),
  if
    Is_winner ->
      true;
    true ->
      is_winner_in_cols(Rows, Next)
  end.

check_for_winner_in_cols(Rows) ->
  Cols = lists:seq(1, 5),
  is_winner_in_cols(Rows, Cols).
  
check_cols(Board) ->
  check_for_winner_in_cols(Board).

is_winner([], _) -> [false, -1];
is_winner([Board | Boards], Index) ->
  Winner = check_cols(Board) or check_rows(Board),
  if
    Winner == true ->
      [true, Index];
    true ->
      is_winner(Boards, Index + 1)
  end.

all_winners([], [], _) -> [];
all_winners([], Winners, _) -> Winners;
all_winners([Board | Boards], Winners, Index) ->
  Winner = check_cols(Board) or check_rows(Board),
  if
    Winner == true ->
      Duplicate = lists:member(Index, Winners),
      if Duplicate == true ->
        all_winners(Boards, Winners, Index + 1);
      true ->
        NewWinners = Winners ++ [Index],
        all_winners(Boards, NewWinners, Index + 1)
      end;
    true ->
      all_winners(Boards, Winners, Index + 1)
  end.

test() ->
  io:format("~p~n~p~n", [
    check_cols(
      [
        [0, 1, 1, 1, 1],
        [1, 0, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1],
        [1, 1, 1, 1, 0]
      ]
    ),
    check_rows(
      [
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0]
      ]
    )
  ]).

find_in_row(_, [], _, _, PositionsFound) -> PositionsFound;
find_in_row(X, [Y | Yr], ToFind, Board, PositionsFound) ->
  Val = lists:nth(Y, lists:nth(X, Board)),
  if
    Val == ToFind ->
      lists:append(PositionsFound, [[X, Y]]);
    true ->
      find_in_row(X, Yr, ToFind, Board, PositionsFound)
  end.

find_xy([], _, _, _, PositionsFound) -> PositionsFound;
find_xy([X | Xr], Y, ToFind, Board, PositionsFound) ->
  NewPositionsFound = find_in_row(X, Y, ToFind, Board, PositionsFound),
  find_xy(Xr, Y, ToFind, Board, NewPositionsFound).

for_boards([], _, _, PositionsFoundByBoard, _) -> PositionsFoundByBoard;
for_boards([Board | Rest], ToFind, Size, PositionsFoundByBoard, BoardIndex) ->
  NewPositionsFound = find_xy(Size, Size, ToFind, Board, []),
  NewPositionsFoundByBoard = lists:append(PositionsFoundByBoard, [[BoardIndex, NewPositionsFound]]),
  for_boards(Rest, ToFind, Size, NewPositionsFoundByBoard, BoardIndex + 1).

update_2d_arr_element_at(Y, Value, Array) ->
  { ElemsLeft, ElemsRight } = lists:split(Y, Array),
  lists:droplast(ElemsLeft) ++ [Value] ++ ElemsRight.

update_2d_arr_at(X, Y, Value, Array2d) ->
  { RowsLeft, RowsRight } = lists:split(X, Array2d),
  RowToUpdate = lists:last(RowsLeft),
  NewRow = update_2d_arr_element_at(Y, Value, RowToUpdate),
  NewArray2d = lists:droplast(RowsLeft) ++ [NewRow] ++ RowsRight,
  NewArray2d.

update_list_at(X, NewElement, List) ->
  { ListLeft, ListRight } = lists:split(X, List),
  lists:droplast(ListLeft) ++ [NewElement] ++ ListRight.

update_points([], Board) -> Board;
update_points([Point | Points], Board) ->
  [X, Y] = Point,
  NewBoard = update_2d_arr_at(X, Y, 1, Board),
  update_points(Points, NewBoard).

update_score_board([], ScoreBoards) -> ScoreBoards;
update_score_board([Score | Rest], ScoreBoards) ->
  [BoardIndex, Points] = Score,
  ScoreBoard = lists:nth(BoardIndex, ScoreBoards),
  NewScoreBoard = update_points(Points, ScoreBoard),
  NewScoreBoards = update_list_at(BoardIndex, NewScoreBoard, ScoreBoards),
  update_score_board(Rest, NewScoreBoards).

sum_if([], [], Sum) -> Sum;
sum_if([Int | R1], [IntBin | R2], Sum) ->
  if
    IntBin == 0 ->
      NewSum = Sum + Int;
    true ->
      NewSum = Sum
  end,
  sum_if(R1, R2, NewSum).

calculate_score(ScoreBoard, Board, WinningNumber) ->
  FlatScoreBoard = lists:flatten(ScoreBoard),
  FlatBoard = lists:flatten(Board),  
  Res = WinningNumber * sum_if(FlatBoard, FlatScoreBoard, 0),
  Res.

play([], _, _, _, _) -> ok;
play([ToFind | Next], Boards, ScoreBoards, Counter, Winners) ->
  Size = lists:seq(1, 5),
  Scores = for_boards(Boards, ToFind, Size, [], 1),
  NewScoreBoards = update_score_board(Scores, ScoreBoards),
  [Winner, WinningBoardIndex] = is_winner(NewScoreBoards, 1),
  NewWinners = all_winners(NewScoreBoards, Winners, 1),
  if
    Winner == true ->
      Score = calculate_score(
        lists:nth(WinningBoardIndex, NewScoreBoards),
        lists:nth(WinningBoardIndex, Boards),
        ToFind
      ),
      io:format("Winner ~p~n", [Score]);
    true ->
      ok
  end,
  if
    length(NewWinners) == length(NewScoreBoards) ->
      LastIndex = lists:last(NewWinners),
      LastScore = calculate_score(
        lists:nth(LastIndex, NewScoreBoards),
        lists:nth(LastIndex, Boards),
        ToFind
      ),
      io:format("LastWinner ~p~n", [LastScore]);
    true ->
       play(Next, Boards, NewScoreBoards, Counter + 1, NewWinners)
  end.

% Part 1 & Part 2
main() ->
  [Input, Boards, ScoreBoards] = read_challange_input(),
  play(Input, Boards, ScoreBoards, 0, []).