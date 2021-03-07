suffix(X, [_|T]) :- X = T; suffix(X, T).

%suffix([1,2,3],[1,2,3,4,5,6]).
%suffix([1,2,3],[3,4,5,1,2,3]).

palindrom(L) :- reverse(L, L).
