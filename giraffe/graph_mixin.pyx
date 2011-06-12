from itertools import izip

from giraffe.exceptions import NoSuchVertex, NoSuchEdge

def _from_adjacency_map(cls, adj=None, **kwadj):
    if adj is None:
        adj = {}

    g = cls()

    for k, vs in dict(adj, **kwadj).iteritems():
        for v in vs:
            g.add_edge(k, v)

    return g

def _from_graph(cls, g):
    # TODO: this is gonna be broken as-is if we go from undirected to directed
    return cls(vertices=g.vertices, edges=g.edges)

cdef class GraphMixin(object):

    def __init__(self, vertices=(), edges=(), name=""):
        super(GraphMixin, self).__init__()

        self._adj = {}
        self._size = 0

        self.name = name

        self.add_vertices(vertices)
        self.add_edges(edges)

    def __contains__(self, v):
        return self.has_vertex(v)

    def __getitem__(self, v):
        try:
            return self._adj[v]
        except KeyError:
            raise NoSuchVertex(v)

    def __delitem__(self, v):
        try:
            del self._adj[v]
        except KeyError:
            raise NoSuchVertex(v)

    def __iter__(self):
        return iter(self._adj)

    def __richcmp__(self, other, int op):
        s, o = self.vertices, other.vertices

        if op == 0:
            return s < o or (s == o and self.edges < other.edges)
        elif op == 1:
            return s <= o and self.edges <= other.edges
        elif op == 2:
            return s == o and self.edges == other.edges
        elif op == 3:
            return not self == other
        elif op == 4:
            return s > o or (s == o and self.edges > other.edges)
        elif op == 5:
            return s >= o and self.edges >= other.edges

    def __len__(self):
        return self.order

    def __and__(self, other):
        return self.intersection(other)

    def __or__(self, other):
        return self.union(other)

    def __sub__(self, other):
        return self.difference(other)

    def __str__(self):
        return self.name

    from_adjacency_map = classmethod(_from_adjacency_map)
    from_graph = classmethod(_from_graph)

    property order:

        def __get__(self):
            return len(self._adj)

    property size:

        def __get__(self):
            return self._size

    property adjacency_map:

        def __get__(self):
            pass

    property vertices:

        def __get__(self):
            return self._adj.viewkeys()

    def add_vertex(self, v):
        self._adj.setdefault(v, set())

    def add_vertices(self, vs):
        for v in vs:
            self.add_vertex(v)

    def add_edges(self, es):
        for u, v in es:
            self.add_edge(u, v)

    def add_path(self, vs):
        self.add_edges(izip(vs, vs[1:]))

    def copy(self):
        return self.__class__.from_graph(self)

    def degree(self, v):
        return len(self[v])

    def has_vertex(self, v):
        # allowing non-hashable to propagate for now
        return v in self._adj

    def has_edge(self, u, v):
        return v in self[u]

    def neighbors(self, vs=()):
        if not vs:
            return self._adj
        return {k : self[k] for k in vs}

    def remove_vertices(self, vs):
        for v in vs:
            if v not in self:
                raise NoSuchVertex(v)

        for v in vs:
            self.remove_vertex(v)

    def remove_edges(self, es):
        for u, v in es:
            if not self.has_edge(u, v):
                raise NoSuchEdge((u, v))

        for u, v in es:
            self.remove_edge(u, v)

    # 2.x's viewkeys objects lack .union / .intersection methods... :/
    def union(self, *others):
        v = set(self.vertices)
        e = set(self.edges)

        for g in others:
            v |= g.vertices
            e |= g.edges

        return self.__class__(vertices=v, edges=e)

    def intersection(self, *others):
        v = set(self.vertices)
        e = set(self.edges)

        for g in others:
            v &= g.vertices
            e &= g.edges

        return self.__class__(vertices=v, edges=e)

    def difference(self, *others):
        v = set(self.vertices).difference(*others)
        e = {edge for edge in self.edges if set(edge) <= v}
        return self.__class__(vertices=v, edges=e)

    def get_subgraph_on(self, vertices):
        v = set(vertices)
        e = {e for e in self.edges if set(e) <= v}
        return self.__class__(vertices=v, edges=e)
