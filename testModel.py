from model.model import Model

myModel = Model()




myModel.buildGraph("White",2018)

print("N nodi: ",myModel.getNumNodes, "N archi: ",myModel.getNumEdges)

bestArchi = myModel.getSortArchiByPeso()
for arco in bestArchi:
    print(f"Arco da {arco.p1} a {arco.p2}, peso: {arco.peso}")

myModel.getNodi_ripetuti()
