-module(day7).
-export([main/0]).

read_challange_input() ->
  {ok, Data} = file:read_file("input"),
  DataSplit = binary:split(Data, [<<",">>], [global]),
  lists:map(fun(Str) -> binary_to_integer(string:trim(Str)) end, DataSplit).

fuel_1([], _, Sum) -> Sum;
fuel_1([Number|Rest], Med, Sum) ->
  Val = abs(Number - Med),
  fuel_1(Rest, Med, Sum + Val).

fuel_2([], _, Sum) -> Sum;
fuel_2([Number|Rest], Avg, Sum) ->
  Val = abs(Number - Avg),
  Folded = lists:foldl(fun(X, FoldSum) -> X + FoldSum end, 0, lists:seq(1, Val)),
  fuel_2(Rest, Avg, Sum + Folded).

main() ->
  Numbers = read_challange_input(),
  Sorted = lists:sort(Numbers),
  Length = length(Numbers),
  Med = lists:nth(Length div 2, Sorted),
  Avg = round(lists:sum(Numbers) / Length),
  F1 = fuel_1(Numbers, Med, 0),
  F2 = fuel_2(Numbers, Avg, 0),
  io:format('~p ~p~n', [F1, F2]).
