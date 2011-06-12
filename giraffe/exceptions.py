class GiraffeException(Exception):
    pass

class EdgeCreatesLoop(GiraffeException):
    pass

class NoSuchVertex(GiraffeException):
    pass

class NoSuchEdge(GiraffeException):
    pass
