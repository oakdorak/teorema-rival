import random
import re

class GeneradorFreestyle:
    def __init__(self, agresividad=0.9):
        self.agresividad = agresividad
        
        # Lexico Teorema (Técnica y Agresividad)
        self.vocab_teorema = {
            "sujetos": ["novato", "fantasma", "copia", "estatua", "eco", "sombra", "figurante"],
            "conceptos": ["flow", "metrica", "estilo", "punchline", "escena", "trono", "leyenda", "maestria", "patron", "codigo"],
            "ataques": ["quemado", "obsoleto", "vacío", "genérico", "frágil", "silenciado", "enterrado", "borrado"],
            "poder": ["motor", "rayo", "fuego", "trueno", "imperio", "corona", "dictador", "cima", "volcan", "tsunami"],
            "verbos_ataque": ["rompo", "quemo", "borro", "aplasto", "estrujo", "aniquilo", "humillo", "desmonto"],
        }
        
        # Lexico Goku (Energía y Dragon Ball)
        self.vocab_goku = {
            "sujetos": ["guerrero", "rival", "enemigo", "villano", "terrestre", "saiyan"],
            "conceptos": ["ki", "entrenamiento", "fuerza", "voluntad", "espíritu", "batalla", "destrucción"],
            "ataques": ["derrotado", "superado", "fuera de combate", "humillado", "en el polvo"],
            "poder": ["Kamehameha", "Genkidama", "Ultra Instinto", "Super Saiyan", "Kaio Ken", "Esferas del Dragón"],
            "verbos_ataque": ["supero", "vuelo", "golpeo", "estallo", "transformo", "desintegro"],
        }

    def _get(self, cat, mode="teorema"):
        vocab = self.vocab_teorema if mode == "teorema" else self.vocab_goku
        return random.choice(vocab.get(cat, ["flow"]))

    def generar_cuarteta(self, input_usuario, mode="teorema"):
        tema = input_usuario.split()[-1] if input_usuario else "estilo"
        
        if mode == "goku":
            # Estilo Goku: Energético, optimista pero dominante
            v1 = f"Siento tu {self._get('conceptos', 'goku')} en el aire, pero mi {self._get('poder', 'goku')} es superior."
            v2 = f"Te enfrentas a un {self._get('sujetos', 'goku')} que nunca se rinde, ¡estás {self._get('ataques', 'goku')}!"
            v3 = f"Entrené en el espacio y el tiempo para {self._get('verbos_ataque', 'goku')} tu {self._get('conceptos', 'goku')}."
            v4 = f"¡Siente el poder del {self._get('poder', 'goku')}! ¡KAMEHAMEHA final para dejarte {self._get('ataques', 'goku')}!"
            header = "🎤 [MODO: GOKU - ULTRA INSTINTO]"
        else:
            # Estilo Teorema: Técnico y Agresivo
            v1 = f"Dices que sabes de {tema}, pero tu {self._get('conceptos', 'teorema')} es {self._get('ataques', 'teorema')}."
            v2 = f"Yo {self._get('verbos_ataque', 'teorema')} tu {self._get('conceptos', 'teorema')}, dejándote {self._get('ataques', 'teorema')} en el suelo."
            v3 = f"En esta batalla, tú eres solo un {self._get('sujetos', 'teorema')} que no aguanta el {self._get('poder', 'teorema')}."
            v4 = f"¡Soy el Teorema, la ley del rap, y tú el {self._get('sujetos', 'teorema')} que no puede crecer!"
            header = "🎤 [ESTILO: TEOREMA-PUNCHLINE]"

        return f"{header}\n\n{v1}\n{v2}\n{v3}\n{v4}"
