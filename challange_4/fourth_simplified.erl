-module(fourth_simplified).
-export([main/0]).
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
  [IntegerInput, AllData].

% Solution
is_none_list(List) ->
  lists:any(fun(Chunk) -> Chunk == [none, none, none, none, none] end, List).

is_row_winning(Board) ->
  Row = [lists:nth(X + Y, Board) || X <- [0, 5, 10, 15, 20], Y <- [1, 2, 3, 4, 5]],
  RowInChunks = n_length_chunks(Row, 5),
  is_none_list(RowInChunks).

is_col_winning(Board) ->
  Col = [lists:nth(X + Y, Board) || X <- [1, 2, 3, 4, 5], Y <- [0, 5, 10, 15, 20]],
  ColInChunks = n_length_chunks(Col, 5),
  is_none_list(ColInChunks).

get_winner_score(Board) ->
  Values = [lists:nth(X, Board) || X <- lists:seq(1, 25)],
  WithoutNone = lists:filter(fun(X) -> X /= none end, Values),
  lists:sum(WithoutNone).

is_winning(Data) ->
  Boards = n_length_chunks(Data, 25),
  is_winning(Boards, 0).

is_winning([], _) -> [no_winner, -1, -1];
is_winning([Board | Boards], Index) ->
  RowWinning = is_row_winning(Board),
  ColWinning = is_col_winning(Board),
  Winning = RowWinning or ColWinning,
  if
    Winning ->
      Score = get_winner_score(Board),
      [won, Index, Score];
    true ->
      is_winning(Boards, Index + 1)
  end.

index_of(Item, List) -> index_of(Item, List, 1).

index_of(_, [], _)  -> not_found;
index_of(Item, [Item|_], Index) -> Index;
index_of(Item, [_|Tl], Index) -> index_of(Item, Tl, Index+1).

nullify_at(List, Pos) ->
  {L, R} = lists:split(Pos, List),
  lists:droplast(L) ++ [none] ++ R.

remove_all(ValueToRemove, From) ->
  Index = index_of(ValueToRemove, From),
  if
    Index == not_found ->
      From;
    true ->
      NewList = nullify_at(From, Index),
      remove_all(ValueToRemove, NewList)
  end.

play([Input | InputTail ], Data) ->
  UpdatedData = remove_all(Input, Data),
  [Msg, Index, Score] = is_winning(UpdatedData),
  if
    Msg == won ->
      io:format("Board: ~p, Input: ~p, Score: ~p~n", [Index, Input, Score * Input]);
    true ->
      play(InputTail, UpdatedData)
  end.

% Only Part 1
main() ->
  [Input, Data] = read_challange_input(),
  play(Input, Data).