import time
import os
from algorithms import *
from data_fetch import graph_generation

if __name__ == "__main__":
    
    file_path = input("Inserisci il percorso del file del dataset (inclusa l'estensione): ")
    
    # Generiamo il grafo una sola volta, dato che la struttura non cambia
    graph_weighted = graph_generation(file_path, weighted=True)  # Per Dijkstra (grafo pesato)
    graph_unweighted = graph_generation(file_path, weighted=False)  # Per gli altri algoritmi (grafo non pesato)

    keys = list(graph_weighted.keys())  # I nodi sono gli stessi in entrambi i grafi
    elements = list()


    # Aggiungiamo i nodi dei vari archi ai nodi esistenti per ottenere tutti i nodi nel grafo
    for key in keys:
        for elem in graph_weighted[key]:
            if isinstance(elem, tuple):  # Per grafi pesati (con peso)
                elements.append(elem[0])
            else:
                elements.append(elem)
    
    all_nodes = set(keys + elements)  # Creiamo un set che contiene tutti i nodi unici

    while True: 

        # Cancelliamo il terminale all'inizio di ogni sessione di ricerca
        os.system('cls' if os.name == 'nt' else 'clear')



        print("\n\n--- ALGORITMO DI RICERCA ---")

        depth = 0  # Impostiamo il valore predefinito della profondità


        # Selezione del nodo di partenza
        while True:

            try:

                start_node = int(input("Inserisci il Nodo di Partenza: "))
                if start_node not in all_nodes:
                    raise ValueError
                break

            except ValueError:
                print("⚠ Errore: Nodo non esistente. Riprova.")


        # Selezione del nodo di arrivo
        while True:

            try:

                goal_node = int(input("Inserisci il Nodo di Arrivo: "))
                if goal_node not in all_nodes:
                    raise ValueError
                break

            except ValueError:
                print("⚠ Errore: Nodo non esistente. Riprova.")


        # Selezione dell'algoritmo
        while True:

            try:

                print("\nSeleziona l'Algoritmo di Ricerca:")
                print("0 -> Breadth-First (BFS)")
                print("1 -> Depth-First (DFS)")
                print("2 -> Depth-Limited (DLS)")
                print("3 -> Iterative Deepening (IDS)")
                print("4 -> Dijkstra")

                choice = int(input("\nScelta: "))

                match choice:

                    case 0:
                        search_type = "BFS"
                        graph = graph_unweighted  # BFS utilizza un grafo non pesato
                    case 1:
                        search_type = "DFS"
                        graph = graph_unweighted  # DFS utilizza un grafo non pesato
                    case 2:
                        depth = int(input("\nSeleziona la profondità massima di ricerca: "))
                        if depth < 0:
                            raise ValueError
                        search_type = "DLS"
                        graph = graph_unweighted  # DLS utilizza un grafo non pesato
                    case 3:
                        search_type = "IDS"
                        graph = graph_unweighted  # IDS utilizza un grafo non pesato
                    case 4:
                        search_type = "Dijkstra"
                        graph = graph_weighted  # Dijkstra utilizza un grafo pesato
                    case _:
                        raise ValueError

                break

            except ValueError:
                print("⚠ Errore: Scelta non valida. Riprova.")


        # Esecuzione della ricerca
        timer = time.time()  # Avvio del timer per calcolare il tempo di esecuzione
        search(start_node, goal_node, graph, search_type, depth, timer)


        # Chiedere se si vuole eseguire un'altra ricerca
        answer = input("Vuoi eseguire un'altra ricerca? (s/n): ").strip().lower()

        if answer != 's':  
            break  # Esce dal loop e termina il programma

    print("👋 Arrivederci! Grazie per aver usato il nostro programma.")
