split(X, L, L1, L2) :- pslit(X, L, [], [], L1, L2).
%split(P, L, L1, L2) :- pslit(P, L, [], [], L1, L2).
%
%pslit(_, [], L1, L2, L1, L2).
%pslit(X, [H|T], L1, L2, RL1, RL2) :-
%   #H =< X,
%   #append(L1, [H], Y),
%   #pslit(X, T, Y, L2, RL1, RL2).
%
%pslit(X, [H|T], L1, L2, RL1, RL2) :-
%   #H > X,
%   #append(L2, [H], Y),
%   #pslit(X, T, L1, Y, RL1, RL2).

%split(5,[2,7,4,8,-1,5],L1,L2)

pslit(_, [], L1, L2, L1, L2).
pslit(P, [H|T], L1, L2, RL1, RL2) :-
    call(P, H),
    append(L1, [H], Y),
    pslit(P, T, Y, L2, RL1, RL2).

pslit(P, [H|T], L1, L2, RL1, RL2) :-
    (\+ call(P, H)),
    append(L2, [H], Y),
    pslit(P, T, L1, Y, RL1, RL2).

odd(X) :- 1 is mod(X, 2).
%split(odd,[2,7,4,8,-1,5],L1,L2)

