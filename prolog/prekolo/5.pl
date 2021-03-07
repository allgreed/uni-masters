p(X, Y) :- q(X, Y).
p(X, Y) :- r(X, Y).
q(X, Y) :- s(X), !, t(Y).
r(c,d).
s(a).
s(b).
t(a).
t(b).

%p(X, Y)
% 1. q(X, Y) fail
% 2. s(X); X = a
% 3. t(Y) -> t(a) 
% X = a Y =a 

erase_pairs([], []).
erase_pairs([X, X|L1], L2) :- erase_pairs(L1, L2).
erase_pairs([X|L1], [X|L2]) :- erase_pairs(L1, L2).
