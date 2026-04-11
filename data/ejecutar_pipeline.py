import json
from pipeline_preprocess import procesar_batalla_a_dataset
from convertidor_dataset import convertir_a_jsonl

# 1. Procesar el archivo de texto a una lista de diccionarios
datos = procesar_batalla_a_dataset('/Users/robbit/Desktop/teorema-rival/data/batalla_raw.txt')

# 2. Convertir esa lista al formato .jsonl final
convertir_a_jsonl(datos, '/Users/robbit/Desktop/teorema-rival/data/dataset_teorema.jsonl')

print("Dataset generado con éxito en: /Users/robbit/Desktop/teorema-rival/data/dataset_teorema.jsonl")
