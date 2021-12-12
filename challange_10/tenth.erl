-module(tenth).
-export([main/0]).

read_challange_input() ->
  {ok, Data} = file:read_file("input"),
  DataSplit = binary:split(Data, [<<"\n">>], [global]),
  lists:droplast(DataSplit).

get(Map, MapType) ->
  maps:get(MapType, Map).

get(Map, MapType, Key) ->
  MapOfType = get(Map, MapType),
  maps:get(Key, MapOfType).

error_at(Brackets, Maps) -> error_at(Brackets, Maps, []).
error_at([],_, Stack) -> { no_error, -1,  Stack };
error_at([Bracket | Rest], Maps, Stack) ->
  IsOpening = maps:is_key([Bracket], get(Maps, "Opening")),
  case IsOpening of
    true ->
      error_at(Rest, Maps, lists:append(Stack, [Bracket]));
    false ->
      Last = [lists:last(Stack)],
      LastAsClosing = get(Maps, "Opening", Last),
      if
        LastAsClosing /= [Bracket] ->
          Points = get(Maps, "Illegal", [Bracket]),
          { error, Points, Stack };
        true ->
          error_at(Rest, Maps, lists:droplast(Stack))
      end
    end.

part_1(Data, Maps) -> part_1(Data, Maps, 0).
part_1([], _, Score) -> Score;
part_1([BinaryLine | Data], Maps, Score) ->
  { Response, Value, _} = error_at(binary_to_list(BinaryLine), Maps),
  case Response of
    error -> part_1(Data, Maps, Score + Value);
    no_error -> part_1(Data, Maps, Score)
  end.

autocomplete_score([], Score, _) -> Score;
autocomplete_score([Head | Tail], Score, Maps) ->
  MulScore = Score * 5,
  NewScore = MulScore + get(Maps, "Autocomplete", Head),
  autocomplete_score(Tail, NewScore, Maps).

autocomplete([], _, ScoreList) -> ScoreList;
autocomplete([Response | Rest], Maps, ScoreList) ->
  case Response of
    { error, _, _} -> autocomplete(Rest, Maps, ScoreList);
    { no_error, _, Stack } ->
      Reversed = lists:reverse(Stack),
      Autocompleted = lists:map(fun(R) -> get(Maps, "Opening", [R]) end, Reversed),
      NewScore = autocomplete_score(Autocompleted, 0, Maps),
      autocomplete(Rest, Maps, ScoreList ++ [NewScore])
  end.

part_2(Data, Maps) -> part_2(Data, Maps, []).
part_2(BinaryData, Maps, Score) ->
  Responses = [error_at(binary_to_list(BinaryLine), Maps) || BinaryLine <- BinaryData],
  Scores = autocomplete(Responses, Maps, Score),
  Sorted = lists:sort(Scores),
  MedianIndex = (length(Sorted) div 2) + 1,
  Median = lists:nth(MedianIndex, Sorted),
  Median.

main() ->
  Data = read_challange_input(),

  IllegalCharacterMap = #{
    ")" => 3,
    "]" => 57,
    "}" => 1197,
    ">" => 25137
  },
  AutocompleteMap = #{
    ")" => 1,
    "]" => 2,
    "}" => 3,
    ">" => 4
  },
  OpeningMap = #{
    "(" => ")",
    "[" => "]",
    "{" => "}",
    "<" => ">"
  },
  Maps = #{
    "Illegal" => IllegalCharacterMap,
    "Autocomplete" => AutocompleteMap,
    "Opening" => OpeningMap
  },
  Score1 = part_1(Data, Maps),
  Score2 = part_2(Data, Maps),
  io:format("Score1: ~p, Score2: ~p~n", [Score1, Score2]).
