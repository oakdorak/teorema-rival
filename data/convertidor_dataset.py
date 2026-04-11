import json
import re

def validar_dataset(data):
    """Valida que la entrada tenga el esquema correcto."""
    required_keys = ['Instruction', 'Input', 'Output', 'Metadata']
    required_meta = ['esquema_rima', 'tecnica', 'silabas_promedio', 'terminacion_fonetica']
    
    for key in required_keys:
        if key not in data: return False
    for m_key in required_meta:
        if m_key not in data['Metadata']: return False
    return True

def convertir_a_jsonl(versos, output_file='dataset_teorema.jsonl'):
    """
    Toma una lista de versos y contexto y los convierte a formato dataset de fine-tuning.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in versos:
            if validar_dataset(item):
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
            else:
                print(f"Error en validación para entrada: {item.get('Input', 'Unknown')}")

# Ejemplo de estructura
data_example = [{
    "Instruction": "Batalla de ingenio sobre el tiempo.",
    "Input": "Tu tiempo se acaba, ya no queda nada.",
    "Output": "El tiempo es relativo y yo lo tengo en la mirada.",
    "Metadata": {
        "esquema_rima": "AABB",
        "tecnica": "Punchline",
        "silabas_promedio": 12,
        "terminacion_fonetica": "-ada"
    }
}]

# convertir_a_jsonl(data_example)
