"""
Astro-Valley - Módulo de Áudio Procedural
Gera efeitos sonoros retrô 8-bit em tempo real sem depender de arquivos externos.
"""

import pygame
import numpy as np

_initialized = False
_sounds = {}

def init_audio():
    global _initialized, _sounds
    if _initialized:
        return
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        # 1. Som de Passo / Movimento
        _sounds["step"] = _synth_tone(freq=180, duration=0.04, wave_type="noise", volume=0.15)
        
        # 2. Som de Regar / Água
        _sounds["water"] = _synth_tone(freq=400, duration=0.15, wave_type="sine", freq_end=200, volume=0.25)
        
        # 3. Som de Arar / Plantar
        _sounds["plant"] = _synth_tone(freq=260, duration=0.08, wave_type="triangle", volume=0.25)
        
        # 4. Som de Colheita / Sucesso
        _sounds["harvest"] = _synth_arpeggio([523, 659, 784, 1046], note_duration=0.06, volume=0.35)
        
        # 5. Som de Energia / Limpar Painel
        _sounds["zap"] = _synth_tone(freq=800, duration=0.12, wave_type="sawtooth", freq_end=1200, volume=0.25)
        
        # 6. Som de Mineração / Impacto
        _sounds["mine"] = _synth_tone(freq=120, duration=0.1, wave_type="square", volume=0.3)
        
        # 7. Som de Novo Sol (Fanfarra da Manhã)
        _sounds["new_sol"] = _synth_arpeggio([440, 554, 659, 880], note_duration=0.1, volume=0.4)
        
        _initialized = True
    except Exception as e:
        print(f"Aviso de áudio: {e}")

def play_sound(name: str):
    if not _initialized:
        init_audio()
    snd = _sounds.get(name)
    if snd:
        try:
            snd.play()
        except Exception:
            pass

def _synth_tone(freq=440, duration=0.1, wave_type="sine", freq_end=None, volume=0.3):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    
    if freq_end is not None:
        freq_array = np.linspace(freq, freq_end, n_samples)
        phase = 2 * np.pi * np.cumsum(freq_array) / sample_rate
    else:
        phase = 2 * np.pi * freq * t
        
    if wave_type == "sine":
        wave = np.sin(phase)
    elif wave_type == "square":
        wave = np.sign(np.sin(phase))
    elif wave_type == "triangle":
        wave = 2 * np.abs(2 * (phase / (2 * np.pi) - np.floor(phase / (2 * np.pi) + 0.5))) - 1
    elif wave_type == "sawtooth":
        wave = 2 * (phase / (2 * np.pi) - np.floor(phase / (2 * np.pi) + 0.5))
    else: # noise
        wave = np.random.uniform(-1, 1, n_samples)
        
    # Envelope de volume ADSR simples (suave no final)
    envelope = np.exp(-3 * t / duration)
    audio = wave * envelope * volume * 32767
    audio = audio.astype(np.int16)
    stereo = np.column_stack((audio, audio))
    
    return pygame.sndarray.make_sound(stereo)

def _synth_arpeggio(freqs, note_duration=0.08, volume=0.3):
    sample_rate = 44100
    total_audio = []
    
    for f in freqs:
        n_samples = int(sample_rate * note_duration)
        t = np.linspace(0, note_duration, n_samples, False)
        wave = np.sin(2 * np.pi * f * t)
        envelope = np.exp(-2.5 * t / note_duration)
        chunk = wave * envelope * volume * 32767
        total_audio.extend(chunk)
        
    audio = np.array(total_audio, dtype=np.int16)
    stereo = np.column_stack((audio, audio))
    return pygame.sndarray.make_sound(stereo)
