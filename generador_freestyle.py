import random
import re

class GeneradorFreestyle:
    def __init__(self, agresividad=0.9):
        self.agresividad = agresividad
        
        # Lexico avanzado basado en la esencia de Teorema (Técnica, Agresividad, Métrica)
        self.vocab = {
            "sujetos": ["novato", "fantasma", "copia", "estatua", "eco", "sombra", "figurante"],
            "conceptos": ["flow", "metrica", "estilo", "punchline", "escena", "trono", "leyenda", "maestria", "patron", "codigo"],
            "ataques": ["quemado", "obsoleto", "vacío", "genérico", "frágil", "silenciado", "enterrado", "borrado"],
            "poder": ["motor", "rayo", "fuego", "trueno", "imperio", "corona", "dictador", "cima", "volcan", "tsunami"],
            "verbos_ataque": ["rompo", "quemo", "borro", "aplasto", "estrujo", "aniquilo", "humillo", "desmonto"],
            "conectores": ["mientras", "porque", "entonces", "aunque", "y ahora"]
        }
        
        # Plantillas de estructura de batalla (Métrica de Teorema: Construcción -> Punchline)
        self.plantillas = [
            # Tipo 1: Comparación destructiva
            "Dices que tienes {conceptos}, pero en realidad eres un {sujetos} {ataques}.",
            "Tú hablas de {poder}, pero yo soy el {poder} que te deja {ataque}.",
            "Intentas imitar mi {conceptos}, pero tu {conceptos} es solo {ataques}.",
            "Tu rap es {ataques}, el mío es {poder} puro, ¡estás {ataques}!",
            # Tipo 2: Ataque técnico (estilo Teorema)
            "No aguantas mi {metrica}, porque mi {poder} es tu {ataque} final.",
            "Analizo tu {conceptos}, veo que es {ataques}, y yo {verbos_ataque} tu {poder}.",
            "Vienes con {conceptos} falso, yo traigo el {poder} y el {lexico['conceptos'][0]} real.",
            "Tú eres un {sujetos} en la pista, yo soy el {poder} que te deja en el {ataque}."
        ]

    def _get(self, cat):
        return random.choice(self.vocab.get(cat, ["flow"]))

    def generar_cuarteta(self, input_usuario):
        # Análisis simple del input para personalizar la respuesta
        tema = input_usuario.split()[-1] if input_usuario else "estilo"
        
        # Construcción de la cuarteta (Métrica AABB simulada)
        # Verso 1: Establece la premisa
        v1 = f"Dices que sabes de {tema}, pero tu {self._get('conceptos')} es {self._get('ataques')}."
        
        # Verso 2: Refuerza la rima A con ataque
        v2 = f"Yo {self._get('verbos_ataque')} tu {self._get('conceptos')}, dejándote {self._get('ataques')} en el suelo."
        
        # Verso 3: Sube la tensión (B)
        v3 = f"En esta batalla, tú eres solo un {self._get('sujetos')} que no aguanta el {self._get('poder')}."
        
        # Verso 4: EL PUNCHLINE FINAL (B) - El golpe de gracia
        v4 = f"¡Soy el Teorema, la ley del rap, y tú el {self._get('sujetos')} que no puede crecer!"
        
        # Ajuste de agresividad final
        if self.agresividad > 0.8:
            v4 = f"¡Cierra la boca, {self._get('sujetos')}, que el Teorema llegó para {self._get('verbos_ataque')} tu {self._get('poder')}!"

        return f"🎤 [ESTILO: TEOREMA-PUNCHLINE]\n\n{v1}\n{v2}\n{v3}\n{v4}"
