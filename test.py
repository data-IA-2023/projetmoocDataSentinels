from pymongo import MongoClient
import dotenv
import os

dotenv.load_dotenv()

# Connexion à la base de données MongoDB
client = MongoClient(os.environ['MOGO_URL'], 27017)
db = client['demo']
iris_collection = db['iris']

# Mise à jour pour "setosa"
result_setosa = iris_collection.update_many(
    { 'species': 'setosa' },
    { '$set': { 'name': 'Iris de Hollande' } }
)

# Mise à jour pour "versicolor"
result_versicolor = iris_collection.update_many(
    { 'species': 'versicolor' },
    { '$set': { 'name': 'clajeux' } }
)

# Mise à jour pour "virginica"
result_virginica = iris_collection.update_many(
    { 'species': 'virginica' },
    { '$set': { 'name': 'Iris de virginie' } }
)

# Afficher les résultats
print("Nombre de documents mis à jour pour setosa:", result_setosa.modified_count)
print("Nombre de documents mis à jour pour versicolor:", result_versicolor.modified_count)
print("Nombre de documents mis à jour pour virginica:", result_virginica.modified_count)

# result = iris_collection.find(
#     { 'species': 'virginica' }
# )

# for doc in result:
#     # print(doc['sepalLength'])
#     print(doc)
    
    
    
results = iris_collection.find().sort('species', 1).skip(2)

# Afficher les résultats
for result in results:
    print(result)