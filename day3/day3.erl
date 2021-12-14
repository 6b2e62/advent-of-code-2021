-module(day3).
-export([main/0]).
-import(lists, [last/1, droplast/1, nth/2]).

% Helpers
read_challange_input() ->
  {ok, Data} = file:read_file("input"),
  droplast(binary:split(Data, [<<"\n">>], [global])).

bool_to_string(Bool) ->
  if 
    Bool == true -> "1";
    true -> "0"
  end.

% Task 2
most_common_value(Sum, Length) ->
  (Sum / Length) >= 0.5.

least_common_value(Sum, Length) ->
  (Sum / Length) < 0.5.

filter_data([], _, ReturnData, _) -> ReturnData;
filter_data([Line | Rest], FilterValue, ReturnData, Index) ->
  Value = binary:bin_to_list(Line, { Index, 1 }),
  if
    Value == FilterValue ->
      filter_data(Rest, FilterValue, ReturnData, Index);
    true ->
      NewData = lists:append([Line], ReturnData),
      filter_data(Rest, FilterValue, NewData, Index)
  end.

oxygen_rating([OnlyOne], _, _) -> OnlyOne;
oxygen_rating(Data, DataLength, Index) ->
  LeftSum = check_once(Data, 0, Index),
  One_is_mcv = most_common_value(LeftSum, DataLength),
  if 
    One_is_mcv ->
      FilteredData = filter_data(Data, "0", [], Index),
      oxygen_rating(FilteredData, length(FilteredData), Index + 1);
    true ->
      FilteredData = filter_data(Data, "1", [], Index),
      oxygen_rating(FilteredData, length(FilteredData), Index + 1)
  end.

scrubber_rating([OnlyOne], _, _) -> OnlyOne;
scrubber_rating(Data, DataLength, Index) ->
  RightSum = check_once(Data, 0, Index),
  One_is_lsv = least_common_value(RightSum, DataLength),
  if
    One_is_lsv == true ->
      FilteredData = filter_data(Data, "0", [], Index),
      scrubber_rating(FilteredData, length(FilteredData), Index + 1);
    true ->
      FilteredData = filter_data(Data, "1", [], Index),
      scrubber_rating(FilteredData, length(FilteredData), Index + 1)
  end.
  
life_support_rating(Data) ->
  DataLength = length(Data),

  Oxygen_rating_int = binary_to_integer(oxygen_rating(Data, DataLength, 0), 2),
  Scrubber_rating_int = binary_to_integer(scrubber_rating(Data, DataLength, 0), 2),

  Oxygen_rating_int * Scrubber_rating_int. 

check_once([], Counter, _) -> Counter;
check_once([Bin | Rest], Counter, Index) ->
  BitStr = binary:bin_to_list(Bin, { Index, 1 }),
  case BitStr of
    "1" -> check_once(Rest, Counter + 1, Index);
    _ -> check_once(Rest, Counter, Index)
  end.

% Task 1
get_rating_msb(Map, TotalLength) ->
  BitList = [bool_to_string(X > TotalLength div 2) || X <- maps:values(Map)],
  binary_to_integer(list_to_binary(BitList), 2).

get_rating_lsb(Map, TotalLength) ->
  BitList = [bool_to_string(X < TotalLength div 2) || X <- maps:values(Map)],
  binary_to_integer(list_to_binary(BitList), 2).

power_consumption(Data) ->
  Map = initialize_map(Data),
  Indexes = maps:keys(Map),
  DataLength = length(Data),
  Indexes = maps:keys(Map),
  UpdatedMap = calc_gamma_rate(Data, Map, Indexes),
  GammaRate = get_rating_msb(UpdatedMap, DataLength),
  EpsilonRate = get_rating_lsb(UpdatedMap, DataLength),
  GammaRate * EpsilonRate.

calc_gamma_rate([], Map, _) -> Map;
calc_gamma_rate([Bin | Rest ], Map, Indexes) ->
  NewMap = check_line(Bin, Map, Indexes),
  calc_gamma_rate(Rest, NewMap, Indexes).

check_line(_, Map, []) -> Map;
check_line(Bin, Map, [Index | Rest]) ->
  BitStr = binary:bin_to_list(Bin, { Index, 1 }),
  case BitStr of
    "1" ->
      Counter = maps:get(Index, Map),
      NewMap = maps:update(Index, Counter + 1, Map),
      check_line(Bin, NewMap, Rest);
    _ ->
      check_line(Bin, Map, Rest)
  end.
  
initialize_map([FirstLine | _]) ->
  StrLen = length(bitstring_to_list(FirstLine)),
  Indexes = [{X, 0 } || X <- lists:seq(0, StrLen - 1, 1)],
  maps:from_list(Indexes).

main() ->
  Data = read_challange_input(),
  Power = power_consumption(Data),
  Oxygen = life_support_rating(Data),
  io:format("Power: ~p, Oxygen: ~p~n", [Power, Oxygen]).
