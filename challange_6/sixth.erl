-module(sixth).
-export([main/0]).

read_challange_input() ->
  {ok, Data} = file:read_file("input"),
  DataSplit = binary:split(Data, [<<",">>], [global]),
  lists:map(fun(Str) -> binary_to_integer(string:trim(Str)) end, DataSplit).

load_estimates([], Estimates) -> Estimates;
load_estimates([InputValue|Rest], Estimates) ->
	Val = maps:get(InputValue, Estimates),
  NewEstimates = maps:update(InputValue, Val + 1, Estimates),
	load_estimates(Rest, NewEstimates).

new_estimate(Key, Estimates, EstimatesCopy) ->
	Value = maps:get(Key, EstimatesCopy),
	if
		Key == 0 ->
			CurrentValue = maps:get(6, Estimates),
			UpdatedEstimates = maps:update(6, CurrentValue + Value, Estimates),
			maps:update(8, Value, UpdatedEstimates);
		true ->
			maps:update(Key - 1, Value, Estimates)
	end.

new_estimate_by_key([], _, Estimates, _) -> Estimates;
new_estimate_by_key([Key|Rest], Day, Estimates, EstimatesCopy) ->
	NewEstimates = new_estimate(Key, Estimates, EstimatesCopy),
	new_estimate_by_key(Rest, Day, NewEstimates, EstimatesCopy).	

run_estimator([], Estimates, _) -> Estimates;
run_estimator([Day|Rest], Estimates, Keys) ->
	NewEstimates = new_estimate_by_key(Keys, Day, Estimates, Estimates),
	% io:format("~p~n", [maps:values(NewEstimates)]),
	run_estimator(Rest, NewEstimates, Keys).

main() ->
  Input = read_challange_input(),
  EmptyEstimates = #{ 8 => 0, 7 => 0, 6 => 0, 5 => 0, 4 => 0, 3 => 0, 2 => 0, 1 => 0, 0 => 0},
  Keys = lists:reverse(maps:keys(EmptyEstimates)),
  Days = 256,
  DaysList = lists:seq(1, Days, 1),	
	Estimates = load_estimates(Input, EmptyEstimates),
	% io:format("~p~n", [maps:values(Estimates)]),
	NewEstimates = run_estimator(DaysList, Estimates, Keys),	
	Values = maps:values(NewEstimates),
	io:format("Res: ~p~n", [lists:sum(Values)]).
