import random
import re

class GeneradorFreestyle:
    def __init__(self, agresividad=0.8):
        self.agresividad = agresividad
        
        # Diccionario expandido estilo "Teorema" (Battler Profesional)
        self.lexico = {
            "conceptos": ["flow", "metrica", "estilo", "punchline", "escena", "trono", "leyenda", "maestria"],
            "ataque": ["quemado", "obsoleto", "copia", "fantasma", "novato", "silencio", "suelo", "cenizas"],
            "poder": ["motor", "rayo", "fuego", "trueno", "imperio", "corona", "dictador", "cima"],
            "conectores": ["pero", "aunque", "entonces", "mientras", "porque"]
        }
        
        # Plantillas de estructura de punchline (simulando la descomposición de Teorema)
        self.estructuras = [
            "Dices que tienes {conceptos}, pero en realidad eres {ataque}.",
            "Tu rap es {ataque}, el mío es el {poder} que te deja en el {ataque}.",
            "Vienes con {conceptos} falso, yo traigo el {poder} y el {lexico['conceptos'][0]} real.",
            "Hablas de {poder}, pero tu {conceptos} es solo un {ataque} en la pista.",
            "No intentes seguir mi {metrica}, porque mi {poder} es tu {ataque}."
        ]

    def _obtener_palabra(self, categoria):
        return random.choice(self.lexico.get(categoria, ["flow"]))

    def generar_cuarteta(self, input_usuario):
        # Simulación de análisis de input
        tema = input_usuario.split()[-1] if input_usuario else "estilo"
        
        # Generar 4 versos con rima simulada (AABB o ABAB)
        # Para Teorema, usamos rimas fuertes y directas
        
        # Verso 1: Ataque directo al input
        v1 = f"Dices que sabes de {tema}, pero tu {self._obtener_palabra('conceptos')} es {self._obtener_palabra('ataque')}."
        
        # Verso 2: Rima con V1 (A)
        rima_a = v1.split()[-1].lower()
        v2 = f"Yo llego con la {self._obtener_palabra('poder')}, rompiendo tu {rima_a} con mi propia {self._obtener_palabra('maestria') if 'maestria' in self.lexico['conceptos'] else 'maestria'}."
        # (Simplificación: forzamos la rima conceptualmente)
        v2 = f"Llego con el {self._obtener_palabra('poder')}, y dejo tu {self._obtener_palabra('ataque')} en el suelo, ¡está hecho!"
        
        # Verso 3: Construcción de tensión (B)
        v3 = f"En esta batalla, tú eres solo un {self._obtener_palabra('ataque')} que no aguanta el {self._obtener_palabra('poder')}."
        
        # Verso 4: PUNCHLINE FINAL (B)
        v4 = f"¡Soy el Teorema, la ley del rap, y tú solo el {self._obtener_palabra('ataque')} que no puede crecer!"
        
        # Ajuste de estilo basado en agresividad
        if self.agresividad > 0.7:
            v4 = f"¡Cierra la boca, novato, que el Teorema llegó para dejarte en el {self._obtener_palabra('ataque')}!"

        return f"🎤 [TIPO: PUNCHLINE]\n\n{v1}\n{v2}\n{v3}\n{v4}"

    def _obtener_palabra_segura(self, cat):
        return random.choice(self.lexico.get(cat, ["flow"]))
