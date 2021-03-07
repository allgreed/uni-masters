search(drzewo(V, L, P), X) :- search(L, X); search(P, X); V = X.

%search(drzewo(1, drzewo(2, nil, nil), drzewo(5, nil, nil)), 1).

prod(nil, 1).
prod(drzewo(X, L, P), R) :-
    prod(L, LR),
    prod(P, PR),
    R is (X * LR * PR).

prod(drzewo(5, drzewo(3, nil, drzewo(1, nil, nil)), drzewo(2, nil, nil)), 30).

preorder(nil, []).
preorder(node(X, L, R), O) :- 
    preorder(L, OL),
    preorder(P, OP),
    append(OL, OP, OLP),
    append([X], OLP, O),
