import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._mapNodiRipeuti = {}
        self._nodes = []
        self._edges = []
        self._graph = nx.Graph()
        self._IdMapProd = {}



    def getAllNodes(self):
       return self._nodes




    def getAllColors(self):
        return DAO.getAllColors()




    def buildGraph(self,color, year):
        #pulisco tutto
        self._nodes = []
        self._edges = []
        self._graph.clear()
        #riempio i nodi dato il colore
        self._nodes = DAO.getAllNodes(color)
        self.fillIdMapProduct()
        self._graph.add_nodes_from(self._nodes)
        self._edges = DAO.getAllEdges(color,year, self._IdMapProd)
        for arco in self._edges:
            if arco.p1 in self._graph and arco.p2 in self._graph:
                self._graph.add_edge(arco.p1, arco.p2, width=arco.peso)

    def getSortArchiByPeso(self):
        self._edges = sorted(self._edges, key=lambda x: x.peso, reverse=True)
        #for arco in self._edges[:3]:
            #print(arco.p1, arco.p2, arco.peso)
        return self._edges[:3]


    def getNodi_ripetuti(self):
        best_archi = self.getSortArchiByPeso()
        self._mapNodiRipeuti = {}
        for arco in best_archi:
            if arco.p1.Product_number in self._mapNodiRipeuti:
                self._mapNodiRipeuti[arco.p1.Product_number] +=1
            else:
                self._mapNodiRipeuti[arco.p1.Product_number] = 1

            if arco.p2.Product_number in self._mapNodiRipeuti:
                self._mapNodiRipeuti[arco.p2.Product_number] +=1
            else:
                self._mapNodiRipeuti[arco.p2.Product_number] = 1

        #print(self._mapNodiRipeuti)
        nodi_rip = []
        for nodo in self._mapNodiRipeuti:
            if self._mapNodiRipeuti[nodo] >1:
                nodi_rip.append(self._IdMapProd[nodo])
        #print(nodi_rip)
        #for nodo in nodi_rip:
            #print(str(nodo))
        return nodi_rip












    def fillIdMapProduct(self):
        for p in self._nodes:
            self._IdMapProd[p.Product_number] = p



    @property
    def getNumNodes(self):
        return len(self._graph.nodes)

    @property
    def getNumEdges(self):
        return len(self._graph.edges)
