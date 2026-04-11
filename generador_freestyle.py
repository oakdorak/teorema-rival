import random
import re

class GeneradorFreestyle:
    def __init__(self, agresividad=0.5):
        self.agresividad = max(0, min(1, agresividad))  # 0.0 a 1.0
        # Diccionario léxico según nivel de agresividad
        self.lexico = {
            "bajo": ["ritmo", "flow", "pista", "mente"],
            "medio": ["fuego", "destino", "camino", "brillo"],
            "alto": ["arma", "sangre", "guerra", "fuerte"]
        }
        self.esquemas = ["AABB", "ABAB"]

    def _get_vocabulario(self):
        if self.agresividad < 0.4:
            return self.lexico["bajo"]
        elif self.agresividad < 0.7:
            return self.lexico["medio"]
        else:
            return self.lexico["alto"]

    def validar_rima(self, v1, v2):
        # Validación fonética simple (comparación de sufijo de 2 letras)
        sufijo1 = v1.strip()[-2:].lower()
        sufijo2 = v2.strip()[-2:].lower()
        return sufijo1 == sufijo2

    def generar_cuarteta(self, input_usuario):
        vocab = self._get_vocabulario()
        esquema = random.choice(self.esquemas)
        
        # Generación simulada de versos basada en input
        # En una implementación real usarías un modelo generativo
        versos = [f"Hablas de {input_usuario} pero no tienes el {random.choice(vocab)}",
                  f"Yo vengo con fuerza, demostrando mi {random.choice(vocab)}",
                  f"En esta batalla, tú eres solo un {random.choice(vocab)}",
                  f"Te dejo en el suelo, perdiendo mi {random.choice(vocab)}"]
        
        # Validación de rima
        if esquema == "AABB":
            if not (self.validar_rima(versos[0], versos[1]) and self.validar_rima(versos[2], versos[3])):
                versos[1] = "Verso con rima forzada A"
                versos[3] = "Verso con rima forzada B"
        
        return f"Esquema {esquema}:\n" + "\n".join(versos)

# Ejemplo de uso:
# gen = GeneradorFreestyle(agresividad=0.8)
# print(gen.generar_cuarteta("tu estilo"))
