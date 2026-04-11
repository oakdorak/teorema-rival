import json
import spacy
import pyphen
import re

# Inicialización
nlp = spacy.load("es_core_news_sm")
dic = pyphen.Pyphen(lang='es')

def analizar_verso(verso):
    """Extrae métrica y terminación fonética."""
    palabras = re.findall(r'\w+', verso.lower())
    silabas = sum([len(dic.inserted(p).split('-')) for p in palabras])
    terminacion = verso.strip()[-4:] # Captura últimos 4 caracteres para fonética
    return silabas, terminacion

def procesar_batalla_a_dataset(archivo_txt, instruccion="Batalla freestyle de alto impacto"):
    """
    Lee un archivo .txt con formato:
    OPONENTE: ...
    TEOREMA: ...
    y genera una lista de diccionarios para el dataset.
    """
    dataset = []
    with open(archivo_txt, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
        
    for i in range(len(lineas) - 1):
        if "OPONENTE" in lineas[i] and "TEOREMA" in lineas[i+1]:
            input_text = lineas[i].split(":")[-1].strip()
            output_text = lineas[i+1].split(":")[-1].strip()
            
            silabas, term = analizar_verso(output_text)
            
            entry = {
                "Instruction": instruccion,
                "Input": input_text,
                "Output": output_text,
                "Metadata": {
                    "esquema_rima": "ABAB", # Asumido por ahora
                    "tecnica": "Punchline",
                    "silabas_promedio": silabas,
                    "terminacion_fonetica": term
                }
            }
            dataset.append(entry)
            
    return dataset

# Ejecución:
# datos = procesar_batalla_a_dataset('batalla_raw.txt')
# from convertidor_dataset import convertir_a_jsonl
# convertir_a_jsonl(datos)
