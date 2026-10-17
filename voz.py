import os
import sounddevice as sd
import soundfile as sf
import whisper
import edge_tts
import asyncio

class GestorVoz:
    def __init__(self):
        print("[VOZ] Cargando modelo Whisper 'small' (mejor precisión)...")
        self.modelo = whisper.load_model("small")

    def escuchar(self, duracion=6, sample_rate=16000):
        """Graba audio del micrófono y lo transcribe con contexto"""
        print("\nNIVY te escucha... (habla claro ahora)")
        archivo_audio = "temp_audio.wav"
        try:
            # Grabar audio
            audio = sd.rec(int(duracion * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
            sd.wait()
            
            # Guardar en wav temporal
            sf.write(archivo_audio, audio, sample_rate)
            
            # Prompt inicial: Ayuda a Whisper a entender el contexto
            contexto = "comandos del sistema experto nivel nivi: reproduce mi playlist, busca en internet, dime la hora, que fecha es, abre youtube, pon música, siguiente canción."
            
            # Transcribir forzando español
            resultado = self.modelo.transcribe(
                archivo_audio, 
                language="es", 
                fp16=False,
                initial_prompt=contexto
            )
            texto = resultado["text"].strip()
            
            print(f"Dijiste: {texto}")
            return texto
        except Exception as e:
            print(f"[VOZ] Error al procesar el audio: {e}")
            return ""
        finally:
            if os.path.exists(archivo_audio):
                try:
                    os.remove(archivo_audio)
                except:
                    pass

    def hablar(self, texto):
        """Genera voz neuronal fluida en formato WAV y la reproduce limpiamente"""
        print(f"NIVY (Voz) > {texto}")
        archivo_respuesta_wav = "respuesta.wav"
        try:
            # Seleccionamos la voz femenina neuronal de México (fluida y natural)
            voz_neuronal = "es-MX-DaliaNeural"
            
            # Usamos una función asíncrona interna para pedirle el audio a Edge-TTS
            async def generar_audio():
                comunicador = edge_tts.Communicate(texto, voz_neuronal, rate="+0%")
                # Edge-tts permite guardar directamente como webm/wav si se procesa o bien convertimos
                await comunicador.save(archivo_respuesta_wav)

            # Ejecutar la generación de la voz
            asyncio.run(generar_audio())
            
            # Leer y reproducir el archivo de audio directamente con sounddevice
            data, fs = sf.read(archivo_respuesta_wav, dtype='float32')
            sd.play(data, fs)
            sd.wait() # Esperar a que la asistente termine de hablar
            
        except Exception as e:
            print(f"[VOZ] Error al reproducir voz: {e}")
        finally:
            # Limpiar archivo temporal de voz
            if os.path.exists(archivo_respuesta_wav):
                try:
                    os.remove(archivo_respuesta_wav)
                except:
                    pass