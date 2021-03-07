#delete(X, [X], []).
# it's not working yet
delete(X, [X | L1], [L1]).
delete(X, [Y | L1], [Y | L2]) :- delete(X, L1, L2).
