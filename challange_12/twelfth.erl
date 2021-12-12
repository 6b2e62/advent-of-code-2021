-module(twelfth).
-export([main/0]).

read_challange_input() ->
  {ok, Data} = file:read_file("input"),
  DataSplit = binary:split(Data, [<<"\n">>], [global]),
  Paths = [binary:split(ToSplit, [<<"-">>], [global]) || ToSplit <- DataSplit],
  Paths.

find_paths(Graph) ->
  Start = << "start" >>,
  Vertices = digraph:out_neighbours(Graph, Start),
  VisitedMap = #{ Start => 1 },
  VisitedList = [Start],

  lists:foreach(fun(Vertex) ->
    traverse_graph(Graph, Vertex, VisitedMap, VisitedList) end,
    Vertices
  ).

allow_traverse(Map, Key) ->
  % Tolerance = 1 - Part 1
  % Tolerance = 2 - Part 2
  Tolerance = 2,
  IsKey = maps:is_key(Key, Map),
  if
    IsKey ->
      { ok, Value } = maps:find(Key, Map),
      Tolerable = Value < Tolerance,
      VisitedMoreThanOnce = lists:any(fun(Val) -> Val > 1 end, maps:values(Map)),
      Tolerable and not VisitedMoreThanOnce;
    true ->
      true
  end.

should_stop(Vertex) ->
  case Vertex of
    << "end" >> -> true;
    << "start" >> -> true;
    _ -> false
  end.

should_stop(VertexFrom, VertexTo, VisitedMap) ->
  case VertexFrom of
    << "end" >> -> true;
    << "start" >> -> true;
    _ -> not allow_traverse(VisitedMap, VertexTo)
  end.

is_lowercase(<< BinFirst, _/binary >>) ->
  Str = [BinFirst],
  Lower = string:to_lower(Str),
  Str == Lower.

update_or_insert_visited_map(VisitedMap, Key) ->
  IsLower = is_lowercase(Key),
  if
    IsLower ->
      IsKey = maps:is_key(Key, VisitedMap),
      if
        IsKey ->
          { ok, Value } = maps:find(Key, VisitedMap),
          maps:put(Key, Value + 1, VisitedMap);
        true ->
          maps:put(Key, 1, VisitedMap)
      end;
    true ->
      VisitedMap
  end.

traverse_graph(Graph, Vertex, VisitedMap, VisitedList) ->  
  EndNow  = should_stop(Vertex),
  NewVisitedList = VisitedList ++ [Vertex],

  if
    EndNow ->
      update_global([NewVisitedList]);
    true ->
      NewVisitedMap = update_or_insert_visited_map(VisitedMap, Vertex),
      Vertices = digraph:out_neighbours(Graph, Vertex),
      lists:foreach(fun(VertexTo) ->
        Skip = should_stop(Vertex, VertexTo, NewVisitedMap),
        if
          Skip == false ->
            traverse_graph(Graph, VertexTo, NewVisitedMap, NewVisitedList);
          true ->
            ok
        end
      end, Vertices)
  end.

add_edge(Graph, V1, V2) ->
  if
    (V1 /= << "end" >>) and (V2 /= << "start" >>) ->
      digraph:add_edge(Graph, V1, V2);
    true ->
      ok
  end.

build_graph([], Graph) -> Graph;
build_graph([Path|Paths], Graph) ->
  [From, To] = Path,
  V1 = digraph:add_vertex(Graph, From),
  V2 = digraph:add_vertex(Graph, To),
  add_edge(Graph, V1, V2),
  add_edge(Graph, V2, V1),
  build_graph(Paths, Graph).


init_global() ->
  % Global ETS table, initialization
  % ets:new(all_paths, [named_table, public, set, { keypos, 1 }]),
  % ets:insert(all_paths, { list, [] }).
  ets:new(all_paths_counter, [named_table, public, set]),
  ets:insert(all_paths_counter, { counter, 0 }).
  

update_global(_NewPath) ->
  % [{_, CurrentPaths}] = ets:lookup(all_paths, list),
  % ets:insert(all_paths, { list, CurrentPaths ++ NewPath }).
  % This insert is extremely slow!
  ets:update_counter(all_paths_counter, counter, 1).

print_global() ->
  % [{_, CurrentPaths}] = ets:lookup(all_paths, list),
  % io:format("Count ~p~n", [length(CurrentPaths)]).
  % timer:sleep(10000),
  % all_paths takes a lot of time to update, thus use it only for test_input
  [{ _, Count }] = ets:lookup(all_paths_counter, counter),
  io:format("Count ~p~n", [ Count ]).

main() ->
  init_global(),

  Paths = read_challange_input(),
  Graph = digraph:new(),
  build_graph(Paths, Graph),
  find_paths(Graph),

  spawn(fun() -> print_global() end).

