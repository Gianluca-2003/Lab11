import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = [2015,2016,2017,2018]
        self._listColor = []
        self._prod = None

    def fillDD(self):
        ddAnni = self._view._ddyear
        for anno in self._listYear:
            ddAnni.options.append(ft.dropdown.Option(str(anno)))

        self._listColor = self._model.getAllColors()
        for color in self._listColor:
            self._view._ddcolor.options.append(ft.dropdown.Option(color))

        self._view.update_page()




    def handle_graph(self, e):
        #creo il grafo
        color = self._view._ddcolor.value
        if color == "":
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append(ft.Text("Seleziona un colore per procedere", color="red"))
            self._view.update_page()
            return
        yearInput = self._view._ddyear.value
        if yearInput == "":
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append(ft.Text("Seleziona un anno per procedere", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph( color, int(yearInput))
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text("Grafo correttamnte creato", color="blue"))
        self._view.txtOut.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodes} "
                                                  f"Numero di archi: {self._model.getNumEdges}", color="blue"))

        bestArchi = self._model.getSortArchiByPeso()
        for arco in bestArchi:
            self._view.txtOut.controls.append(ft.Text(f"Arco da {arco.p1} a {arco.p2}, peso: {arco.peso}", color="blue"))

        nodi_ripetuti = self._model.getNodi_ripetuti()
        if(len(nodi_ripetuti) == 0):
            self._view.txtOut.controls.append(ft.Text("Non ci sono nodi ripetuti", color="blue"))
        else:
            self._view.txtOut.controls.append(ft.Text("Nodi ripetuti: ", color="blue"))
            for nodo in nodi_ripetuti:
                self._view.txtOut.controls.append(ft.Text(f"{nodo}", color="blue"))


        self.fillDDProduct()



        self._view.update_page()




    def fillDDProduct(self):
        nodes = self._model.getAllNodes()
        for node in nodes:
            self._view._ddnode.options.append(ft.dropdown.Option(key=node.Product_number,
                                                                 data=node,
                                                                 on_click=self.readProduct))

    def readProduct(self,e):
        self._prod = e.control.data
        print(self._prod)



    def handle_search(self, e):
        pass
