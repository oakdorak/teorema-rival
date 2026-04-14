import os
from openai import OpenAI

class GeneradorFreestyle:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        
        self.prompts = {
            "teorema": (
                "Eres Teorema, el rapero más técnico y agresivo de la escena. "
                "Tu estilo se basa en la precisión quirúrgica, métricas complejas, "
                "multisílabas y punchlines devastadores que humillan al oponente. "
                "No eres amable; buscas el dominio total de la batalla. "
                "Genera una cuarteta (exactamente 4 versos) respondiendo al input del usuario. "
                "Usa lenguaje de freestyle real, enfócate en el remate final (punchline) "
                "y mantén una actitud superior y técnica."
            ),
            "goku": (
                "Eres Goku en modo batalla. Tienes una energía desbordante, "
                "espíritu de lucha inquebrantable y haces referencias constantes "
                "a Dragon Ball (Ki, Super Saiyan, transformaciones, entrenamiento). "
                "Eres dominante, poderoso, pero mantienes ese espíritu de superación. "
                "Genera una cuarteta (exactamente 4 versos) respondiendo al input del usuario. "
                "Que se sienta el poder del Ki en cada verso."
            )
        }

    def generar_cuarteta(self, input_usuario, mode="teorema"):
        system_prompt = self.prompts.get(mode, self.prompts["teorema"])
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Responde a esto con una cuarteta de freestyle: {input_usuario}"}
                ],
                temperature=0.8,
                max_tokens=150
            )
            
            text = response.choices[0].message.content.strip()
            
            header = "🎤 [ESTILO: TEOREMA-PUNCHLINE]" if mode == "teorema" else "🎤 [MODO: GOKU - ULTRA INSTINTO]"
            return f"{header}\n\n{text}"
            
        except Exception as e:
            print(f"Error generando freestyle con LLM: {e}")
            # Fallback básico en caso de error de API
            return f"🎤 [ERROR]\n\nEl motor de rimas falló, pero mi flow sigue intacto.\nSigo aquí arriba, tú sigues abajo.\nEl sistema cae, pero yo no me muevo.\n¡Esta batalla la gano aunque el código esté nuevo!"
