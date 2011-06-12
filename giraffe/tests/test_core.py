import unittest

import giraffe as c
import giraffe.exceptions as exc

def make_graph_tst(cls):
    class Test(unittest.TestCase):
        def test_eq_ne(self):
            g = cls()
            g2 = cls()

            self.assertEqual(g, g2)
            self.assertEqual(g2, g)

            g.add_vertex(1)
            self.assertNotEqual(g, g2)

            g2.add_vertex(1)
            self.assertEqual(g, g2)
            self.assertEqual(g2, g)

            g.add_edge(1, 2)
            self.assertNotEqual(g, g2)

            g2.add_edge(1, 2)
            self.assertEqual(g, g2)
            self.assertEqual(g2, g)

        def test_le_lt_gt_ge(self):
            g = cls()
            g2 = cls()

            self.assertLessEqual(g, g2)
            self.assertLessEqual(g2, g)
            self.assertGreaterEqual(g, g2)
            self.assertGreaterEqual(g2, g)

            g.add_vertices({1, 2, 3})
            g.add_edges({(1, 2), (2, 3)})

            self.assertLess(g2, g)
            self.assertGreater(g, g2)

            g2.add_vertices({1, 2, 3})
            g2.add_edges({(2, 3)})

            self.assertLess(g2, g)
            self.assertGreater(g, g2)

            g2.add_vertex(4)
            self.assertFalse(g <= g2)
            self.assertFalse(g >= g2)

        def test_getitem(self):
            o = object()
            g = cls(edges=[(0, o)])
            self.assertIn(o, g[0])

        def test_iter(self):
            v = {object() for _ in range(5)}
            g = cls(v)
            self.assertEqual(set(iter(g)), v)

        def test_str(self):
            g = cls()
            g.name = "Test"
            self.assertEqual(g.name, "Test")
            self.assertEqual(str(g), "Test")

        def test_from_graph(self):
            g = cls(edges={(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)})
            self.assertEqual(g, cls.from_graph(g))

        def test_copy(self):
            g = cls(edges={(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)})
            copy = g.copy()
            self.assertEqual(g, copy)
            self.assertIsNot(g, copy)

        def test_no_such_vertex(self):
            g = cls()
            self.assertRaises(exc.NoSuchVertex, g.__getitem__, 0)

        def test_add_vertex(self):
            g = cls()

            self.assertFalse(g)
            self.assertEqual(len(g), 0)
            self.assertEqual(g.order, 0)

            self.assertFalse(g.has_vertex(1))
            self.assertNotIn(1, g)

            g.add_vertex(1)

            self.assertTrue(g)
            self.assertEqual(g.order, 1)
            self.assertEqual(len(g), 1)

            self.assertTrue(g.has_vertex(1))
            self.assertIn(1, g)

        def test_add_vertices(self):
            g = cls()
            g.add_vertices(range(5))

            for i in range(5):
                self.assertIn(i, g)

        def add_vertex_existing(self):
            o, p = object(), object()
            g = cls((o, p))
            g.add_vertices([o, p])
            self.assertIn(o, g)
            self.assertIn(p, g)

        def test_union(self):
            v, e = set(range(1, 4)), {(1, 3), (2, 3)}
            v2, e2 = set(range(2, 5)), {(2, 3), (2, 4), (1, 4)}

            g = cls(v, e)
            g2 = cls(v2, e2)

            u = g | g2
            u2 = g.union(g2)
            u3 = g.union(g2, g2)
            self.assertTrue(u == u2 == u3)

            self.assertEqual(u.vertices, v | v2)
            self.assertEqual(u.edges, e | e2)

        def test_intersection(self):
            v, e = set(range(1, 4)), {(1, 3), (2, 3)}
            v2, e2 = set(range(2, 5)), {(2, 3), (2, 4), (3, 4)}

            g = cls(v, e)
            g2 = cls(v2, e2)

            u = g & g2
            u2 = g.intersection(g2)
            u3 = g.intersection(g2, g2)
            self.assertTrue(u == u2 == u3)

            self.assertEqual(u.vertices, v & v2)
            self.assertEqual(u.edges, e & e2)

        def test_difference(self):
            v, e = set(range(1, 5)), {(1, 3), (1, 4), (2, 3), (2, 4), (3, 4)}
            g = cls(v, e)

            u = g - {2, 4}
            u2 = g.difference({2, 4})
            u3 = g.difference({2}, {4})
            self.assertTrue(u == u2 == u3)

            self.assertEqual(u.vertices, {1, 3})
            self.assertEqual(u.edges, {(1, 3)})

        def test_get_induced_subgraph(self):
            v, e = set(range(1, 4)), {(1, 3), (1, 4), (2, 4), (2, 3)}
            g = cls(v, e)
            i = g.get_subgraph_on((1, 2, 4))

            self.assertEqual(i.vertices, {1, 2, 4})
            self.assertEqual(i.edges, {(1, 4), (2, 4)})

        def test_remove_vertex(self):
            e = {(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)}
            g = cls(range(6), e)

            g.remove_vertex(5)
            self.assertEqual(g.order, 5)
            self.assertEqual(g.edges, e)

            g.remove_vertex(1)
            self.assertEqual(g.order, 4)
            self.assertEqual(g.edges, {(2, 3), (3, 4)})

        def test_remove_vertices(self):
            e = {(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)}
            g = cls(range(6), e)

            g.remove_vertices((2, 3))
            self.assertEqual(g.edges, {(0, 1), (1, 4)})

        def test_remove_vertex_nonexistent(self):
            e = {(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)}
            g = cls(range(6), e)

            self.assertRaises(exc.NoSuchVertex, g.remove_vertex, 10)
            self.assertRaises(exc.NoSuchVertex, g.remove_vertices, (8, 10))

        def test_remove_vertex_atomic(self):
            e = {(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)}
            g = cls(range(6), e)

            with self.assertRaises(exc.NoSuchVertex):
                g.remove_vertices((2, 10))

            self.assertIn(2, g.vertices)
            self.assertEqual(g.edges, e)

        def test_remove_edge(self):
            e = {(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)}
            g = cls(range(6), e)

            g.remove_edge(2, 3)
            self.assertEqual(g.edges, e - {(2, 3)})
            self.assertEqual(g.size, 4)

        def test_remove_edges(self):
            e = {(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)}
            g = cls(range(6), e)

            g.remove_edges([(2, 3), (3, 4)])
            self.assertEqual(g.edges, {(0, 1), (1, 2), (1, 4)})

        def test_remove_edge_nonexistent(self):
            e = {(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)}
            g = cls(range(6), e)

            self.assertRaises(exc.NoSuchEdge, g.remove_edge, 1, 5)
            self.assertRaises(exc.NoSuchEdge, g.remove_edges, [(0, 1), (1, 3)])

        def test_remove_edge_atomic(self):
            e = {(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)}
            g = cls(range(6), e)

            with self.assertRaises(exc.NoSuchEdge):
                g.remove_edges([(0, 1), (2, 10)])

            self.assertEqual(g.edges, e)

    return Test

class TestGraph(make_graph_tst(c.Graph)):
    @unittest.expectedFailure
    def test_is_simple(self):
        g = c.Graph()
        self.assertFalse(g.is_directed)
        self.assertFalse(g.is_multigraph)

    def test_from_adjacency_map(self):
        g = c.Graph.from_adjacency_map({1 : [2, 3], 2 : [1, 4], 4 : [5]})
        self.assertEqual(g.vertices, set(range(1, 6)))

        e = g.edges
        f = e - {(1, 2), (2, 1)}
        self.assertTrue((1, 2) in e or (2, 1) in e)
        self.assertEqual(f, {(1, 3), (2, 4), (4, 5)})

    def test_add_edge(self):
        o, p = object(), object()
        g = c.Graph((o, p))

        self.assertEqual(g.size, 0)
        self.assertFalse(g.has_edge(o, p))
        self.assertFalse(g.has_edge(p, o))

        g.add_edge(o, p)
        self.assertTrue(g.has_edge(o, p))
        self.assertTrue(g.has_edge(p, o))

        self.assertEqual(g.size, 1)

        e = g.edges
        self.assertTrue((o, p) in e or (p, o) in e, "Undirected should have "
                    "edge in both directions but only appear once in .edges")

        self.assertIn(p, g[o])

    def test_add_edges(self):
        e = {(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)}
        g = c.Graph(range(6), e)

        for u, v in e:
            self.assertTrue(g.has_edge(u, v))
            self.assertTrue(g.has_edge(v, u), "Didn't add an undirected edge!")

        e = {(3, 1), (5, 3), (5, 4), (4, 2)}
        g.add_edges(e)

        for u, v in e:
            self.assertTrue(g.has_edge(u, v), "Didn't add an undirected edge!")
            self.assertTrue(g.has_edge(v, u))

    def test_add_edges_nonexisting_vertices(self):
        e = {(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)}
        g = c.Graph(edges=e)

        self.assertEqual(g.vertices, set(range(5)))

        for u, v in e:
            self.assertTrue(g.has_edge(u, v))
            self.assertTrue(g.has_edge(v, u))

    def test_add_edge_cant_add_loop(self):
        g = c.Graph({1})
        self.assertRaises(exc.EdgeCreatesLoop, g.add_edge, 1, 1)

    def test_add_path(self):
        g = c.Graph(range(6), {(1, 4)})

        e = {(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (1, 4)}
        g.add_path(range(6))
        self.assertEqual(g.edges, e)

    def test_degree(self):
        e = {(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)}
        g = c.Graph(range(6), e)

        for i, v in enumerate((1, 3, 2, 2, 2, 0)):
            self.assertEqual(g.degree(i), v)

    def test_neighbors(self):
        e = {(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)}
        g = c.Graph(range(6), e)

        self.assertEqual(g.neighbors([1]), {1 : {0, 2, 4}})
        self.assertEqual(g.neighbors([1])[1], g[1])

        self.assertEqual(g.neighbors([2, 4]), {2 : {1, 3}, 4 : {1, 3}})

    def test_edges(self):
        e = {(1, 5), (2, 5), (3, 4)}
        g = c.Graph(range(1, 6), e)
        self.assertEqual(g.edges, e)

    def test_adjacency_map(self):
        v, e = set(range(1, 4)), {(1, 3), (1, 4), (2, 4), (2, 3)}
        g = c.Graph(v, e)

        m = g.adjacency_map
        self.assertEqual(m, {1 : {3, 4}, 2 : {3, 4}, 3 : {1, 2}, 4 : {1, 2}})

        m[1].add(2)
        self.assertFalse(g.has_edge(1, 2), "Adjacency map mutated the graph.")

class TestDiGraph(make_graph_tst(c.DiGraph)):
    @unittest.expectedFailure
    def test_is_simple(self):
        g = c.DiGraph()
        self.assertFalse(g.is_directed)
        self.assertFalse(g.is_multigraph)

    def test_from_adjacency_map(self):
        g = c.DiGraph.from_adjacency_map({1 : [2, 3], 2 : [4], 4 : [2, 5]})
        self.assertEqual(g.vertices, set(range(1, 6)))
        self.assertEqual(g.edges, {(1, 2), (1, 3), (2, 4), (4, 2), (4, 5)})

    def test_add_edge(self):
        o, p = object(), object()
        g = c.DiGraph((o, p))

        self.assertEqual(g.size, 0)
        self.assertFalse(g.has_edge(o, p))
        self.assertFalse(g.has_edge(p, o))

        g.add_edge(o, p)
        self.assertTrue(g.has_edge(o, p))
        self.assertFalse(g.has_edge(p, o))

        self.assertEqual(g.size, 1)

        e = g.edges
        self.assertIn((o, p), e)
        self.assertNotIn((p, o), e)

        self.assertIn(p, g[o])
        self.assertNotIn(o, g[p])

        g.add_edge(p, o)
        self.assertTrue(g.has_edge(o, p))
        self.assertTrue(g.has_edge(p, o))

        self.assertEqual(g.size, 2)

        e = g.edges
        self.assertIn((o, p), e)
        self.assertIn((p, o), e)

        self.assertIn(p, g[o])
        self.assertIn(o, g[p])

    def test_add_edges(self):
        e = {(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)}
        g = c.DiGraph(range(6), e)

        for u, v in e:
            self.assertTrue(g.has_edge(u, v))
            self.assertFalse(g.has_edge(v, u))

        e = {(3, 1), (5, 3), (5, 4), (4, 2)}
        g.add_edges(e)

        for u, v in e:
            self.assertTrue(g.has_edge(u, v))
            self.assertFalse(g.has_edge(v, u))

    def test_add_edges_nonexisting_vertices(self):
        e = {(0, 1), (1, 2), (2, 3), (3, 4), (4, 1)}
        g = c.DiGraph(edges=e)

        self.assertEqual(g.vertices, set(range(5)))

        for u, v in e:
            self.assertTrue(g.has_edge(u, v))
            self.assertFalse(g.has_edge(v, u))

    def test_add_edge_cant_add_loop(self):
        g = c.DiGraph({1})
        self.assertRaises(exc.EdgeCreatesLoop, g.add_edge, 1, 1)

    def test_add_path(self):
        g = c.DiGraph(range(6), {(1, 4)})

        e = {(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (1, 4)}
        g.add_path(range(6))
        self.assertEqual(g.edges, e)

    def test_degree(self):
        e = {(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)}
        g = c.DiGraph(range(6), e)

        for i, v in enumerate((1, 3, 2, 2, 2, 0)):
            self.assertEqual(g.degree(i), g.in_degree(i) + g.out_degree(i))
            self.assertEqual(g.degree(i), v)

    def test_in_degree(self):
        e = {(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)}
        g = c.DiGraph(range(6), e)

        for i, v in enumerate((0, 1, 1, 1, 2, 0)):
            self.assertEqual(g.in_degree(i), v)

    def test_out_degree(self):
        e = {(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)}
        g = c.DiGraph(range(6), e)

        for i, v in enumerate((1, 2, 1, 1, 0, 0)):
            self.assertEqual(g.out_degree(i), v)

    def test_neighbors(self):
        e = {(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)}
        g = c.DiGraph(range(6), e)

        self.assertEqual(g.neighbors([1]), {1 : {2, 4}})
        self.assertEqual(g.neighbors([1])[1], g[1])

        self.assertEqual(g.neighbors([2, 4]), {2 : {3}, 4 : set()})

    def test_edges(self):
        e = {(1, 5), (2, 5), (5, 2), (5, 1), (3, 4)}
        g = c.DiGraph(range(1, 6), e)
        self.assertEqual(g.edges, e)

    def test_adjacency_map(self):
        v, e = set(range(1, 4)), {(1, 3), (1, 4), (2, 4), (3, 2)}
        g = c.DiGraph(v, e)

        m = g.adjacency_map
        self.assertEqual(m, {1 : {3, 4}, 2 : {4}, 3 : {2}, 4 : set()})

        m[1].add(2)
        self.assertFalse(g.has_edge(1, 2), "Adjacency map mutated the graph.")
