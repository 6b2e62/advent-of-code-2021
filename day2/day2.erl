-module(day2).
-export([main/0]).
-export([calc_position/2]).
-import(lists, [last/1, droplast/1]).

% Helpers
read_challange_input() ->
  {ok, Data} = file:read_file("input"),
  droplast(binary:split(Data, [<<"\n">>], [global])). 

% Core
calc_position([Head|Tail], Position) ->
  [Direction, BinVal] = binary:split(Head, <<" ">>),
  NewPosition = update_position(Direction, binary_to_integer(BinVal), Position),
  calc_position(Tail, NewPosition);

calc_position([], Position) -> Position.

% Aim based
update_position(<<"forward">>, Val, {Depth, Horizontal, Aim}) ->
  {Depth + (Aim * Val), Horizontal + Val, Aim};

update_position(<<"up">>, Val, {Depth, Horizontal, Aim}) ->
  {Depth, Horizontal, Aim - Val};

update_position(<<"down">>, Val, {Depth, Horizontal, Aim}) ->
  {Depth, Horizontal, Aim + Val};

% No aim
update_position(<<"forward">>, Val, {Depth, Horizontal}) ->
  {Depth, Horizontal + Val};

update_position(<<"up">>, Val, {Depth, Horizontal}) ->
  {Depth - Val, Horizontal};

update_position(<<"down">>, Val, {Depth, Horizontal}) ->
  {Depth + Val, Horizontal}.

main() ->
  BinaryLines = read_challange_input(),

  % 1st part
  { Depth_1, Horizontal_1 } = calc_position(BinaryLines, {0, 0}),
  io:format("~p~n", [{Depth_1, Horizontal_1}]),
  io:format("~p~n", [Depth_1 * Horizontal_1]),

  % 2nd part
  { Depth_2, Horizontal_2, _ } = calc_position(BinaryLines, {0, 0, 0}),
  io:format("~p~n", [{Depth_2, Horizontal_2}]),
  io:format("~p~n", [Depth_2 * Horizontal_2]).
 
