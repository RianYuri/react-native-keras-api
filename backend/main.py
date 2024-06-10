from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from io import StringIO
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree, DecisionTreeClassifier
from deap import base, creator, tools, algorithms
from numpy import random
import numpy

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def process_data(algorithm: str = Form(...), database: UploadFile = Form(...)):
    contents = await database.read()
    df = pd.read_csv(StringIO(contents.decode('utf-8')))

    if algorithm == 'KNN':
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]

        X = X.apply(LabelEncoder().fit_transform)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        classifier = KNeighborsClassifier(n_neighbors=5)
        classifier.fit(X_train, y_train)

        y_pred = classifier.predict(X_test)

        print(confusion_matrix(y_test, y_pred))
        print(accuracy_score(y_test, y_pred) * 100)

        return {
            "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
            "accuracy": accuracy_score(y_test, y_pred) * 100
        }

    elif algorithm == 'Árvore de decisão':
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]

        X = X.apply(LabelEncoder().fit_transform)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

        classifier = DecisionTreeClassifier()
        classifier.fit(X_train, y_train)

        y_pred = classifier.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred) * 100

        plt.figure(figsize=(20, 10))
        plot_tree(classifier, filled=True)
        plt.savefig('../frontend/assets/images/decision_tree.png')
        return {
            "accuracy": accuracy,
        }

    elif algorithm == 'Algoritmo Genético':
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]

        X = X.apply(LabelEncoder().fit_transform)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()
        toolbox.register("attr_bool", random.randint, 0, 1)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(X_train.columns))
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        def evalOneMax(individual):
            return sum(individual),

        toolbox.register("evaluate", evalOneMax)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=3)

        pop = toolbox.population(n=300)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)

        pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40, stats=stats, halloffame=hof, verbose=True)
        return {
            "Melhor indivíduo": hof[0],
            "População final": pop[0],
            "Log": log[0],
        }
        

