-module(first).
-export([test/0, main/0]).
-export([print_list/1]).
-export([count_depths_1/2]).
-export([count_depths_2/2]).
-export([binary_to_integer_list/2]).
-import(lists,[last/1, droplast/1, reverse/1]).

% Helpers
print_list([]) -> ok;
print_list([H|T]) -> io:format("~p~n", [H]),
		     print_list(T).

binary_to_integer_list([Head|Tail], IntegerList) ->
  IntValue = binary_to_integer(Head),
  binary_to_integer_list(Tail, [IntValue|IntegerList]);

binary_to_integer_list([], IntegerList) ->
  reverse(IntegerList).

read_challange_input() ->
  {ok, Data} = file:read_file("input"),
  BinaryLines = droplast(binary:split(Data, [<<"\n">>], [global])),  
  % additional new line, thus droplast
  % io:format("~p~n", [last(BinaryLines)]),
  binary_to_integer_list(BinaryLines, []).

% Challange 1
count_depths_1([_], Times) -> Times;

count_depths_1([First, Second|Rest], Times) when [Second] > [First] ->
  count_depths_1([Second|Rest], Times + 1);

count_depths_1([_, Second|Rest], Times) ->
  count_depths_1([Second|Rest], Times).

% Challange 2
count_depths_2([_, _, _], Times) -> Times;

count_depths_2([First, Second, Third, Fourth|Rest], Times) when [First + Second + Third] < [Second + Third + Fourth] ->
  count_depths_2([Second, Third, Fourth|Rest], Times + 1);

count_depths_2([_, Second, Third, Fourth|Rest], Times) ->
  count_depths_2([Second, Third, Fourth|Rest], Times).

test() ->
  Numbers = [
    199,
    200,
    208,
    210,
    200,
    207,
    240,
    269,
    260,
    263
  ], 
  print_list(Numbers),
  Times = count_depths_1(Numbers, 0),
  io:format("Result: ~p~n", [Times]).

main() ->
  Integers = read_challange_input(),
  IncreaseCount1 = count_depths_1(Integers, 0),
  IncreaseCount2 = count_depths_2(Integers, 0),
  io:format("Result 1: ~p~n", [IncreaseCount1]),
  io:format("Result 2: ~p~n", [IncreaseCount2]).
