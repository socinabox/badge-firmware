#!/usr/bin/env python3
"""Create a pleasant 'boop' sound instead of harsh beep"""
import wave
import struct
import math

sample_rate = 22050
duration = 0.3  # Short 300ms

# Two-tone pleasant "boop" - descending notes
freq1 = 800  # Higher note
freq2 = 600  # Lower note
transition = 0.15  # Switch frequency at 150ms

num_samples = int(sample_rate * duration)
samples = []

for i in range(num_samples):
    t = i / sample_rate

    # Envelope: fade in and fade out for smooth sound
    if t < 0.02:  # Fast fade in
        envelope = t / 0.02
    elif t > duration - 0.1:  # Fade out
        envelope = (duration - t) / 0.1
    else:
        envelope = 1.0

    # Frequency transition
    if t < transition:
        freq = freq1
    else:
        freq = freq2

    # Generate sine wave with envelope
    sample = int(32767 * 0.3 * envelope * math.sin(2 * math.pi * freq * t))
    samples.append(sample)

# Write WAV file
with wave.open('test_beep.wav', 'w') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 2 bytes
    wav_file.setframerate(sample_rate)

    for sample in samples:
        wav_file.writeframes(struct.pack('<h', sample))

print("Created pleasant 'boop' sound (test_beep.wav)")
print("- 300ms two-tone descending sound")
print("- Smooth fade in/out envelope")
