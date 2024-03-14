#!/usr/bin/env python
# coding: utf-8

# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')

from pathlib import Path
import os
from io import BytesIO

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import seaborn as sns
import numpy as np
from scipy.signal import butter

from IPython.display import display, Audio


# In[2]:


from ipywebrtc import AudioRecorder, CameraStream
camera = CameraStream(constraints={'audio': True,'video':False})
recorder = AudioRecorder(stream=camera)
recorder


# In[3]:


import torch
import torchaudio
from speechbrain.dataio.dataio import read_audio_info, read_audio
import speechbrain.processing.features as spf
from speechbrain.augment.time_domain import Resample

import opensmile


# In[8]:


recorder.save('test-rtc.wav')


# In[10]:


signal = read_audio('test-rtc.wav')


# In[ ]:


filename = 'test_audio.wav'
tmpdir = Path(os.path.abspath('model_dir'))
signal =read_audio(filename)
signal = signal[:, [0]]
signal = signal.unsqueeze(0)

meta  = read_audio_info(filename)
display(Audio(data=signal.squeeze(), rate=meta.sample_rate))

b, a = butter(9, 7000/(meta.sample_rate/2))
filtered = torchaudio.functional.filtfilt(signal.squeeze(), 
                                          a_coeffs=torch.tensor(a.astype(np.float32)), 
                                          b_coeffs=torch.tensor(b.astype(np.float32)))

resampler = Resample(orig_freq=meta.sample_rate, new_freq=16000)
resampled = resampler(filtered.unsqueeze(0))
signal.shape, resampled.shape
display(Audio(data=resampled.squeeze(), rate=16000))
signal = resampled
fs = 16000
torchaudio.save('test_audio_16k_single.wav', signal.squeeze().unsqueeze(0), fs) 
plt.plot(resampled.squeeze())


# In[2]:


smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.ComParE_2016,
    feature_level=opensmile.FeatureLevel.Functionals,
)
y = smile.process_file('test_audio_16k_single.wav')
y.shape


# In[3]:


compute_STFT = spf.STFT(
    sample_rate=fs, win_length=25, hop_length=10, n_fft=1200
)
features = compute_STFT(signal)
print(features.shape)
features = spf.spectral_magnitude(features.squeeze())
print(features.shape)
ax = plt.matshow(features.T, origin='lower', aspect=0.5, norm=LogNorm(vmin=0, vmax=10))
ax.axes.xaxis.set_ticks_position('bottom')


# In[4]:


compute_fbanks = spf.Filterbank(n_mels=20, n_fft=1200)
features = compute_fbanks(features.unsqueeze(0))
ax = plt.matshow(features.squeeze().T, origin='lower', aspect=1)
ax.axes.xaxis.set_ticks_position('bottom')


# In[5]:


compute_mfccs = spf.DCT(input_size=features.shape[-1], n_out=20)
features = compute_mfccs(features)
ax = plt.matshow(features.squeeze().T, origin='lower', aspect=1)
ax.axes.xaxis.set_ticks_position('bottom')


# In[6]:


compute_deltas = spf.Deltas(input_size=features.shape[-1])
delta1 = compute_deltas(features)
delta2 = compute_deltas(delta1)
features = torch.cat([features, delta1, delta2], dim=2)
ax = plt.matshow(features.squeeze().T, origin='lower', aspect=1)
ax.axes.xaxis.set_ticks_position('bottom')


# In[7]:


compute_cw = spf.ContextWindow(left_frames=5, right_frames=5)
features  = compute_cw(features)
norm = spf.InputNormalization()
features = norm(features, torch.tensor([1]).float())
ax = plt.matshow(features.squeeze().T, origin='lower', aspect=0.5)
ax.axes.xaxis.set_ticks_position('bottom')


# ### Speaker embeddings and verification

# In[8]:


from speechbrain.inference.speaker import EncoderClassifier
classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", 
                                            savedir=tmpdir / 'spkrec-ecapa-voxceleb',
                                            run_opts={"device": "mps"})
signal, fs = torchaudio.load('test_audio.wav')
embeddings = classifier.encode_batch(signal)


# In[9]:


embeddings.shape


# In[10]:


from speechbrain.inference.speaker import SpeakerRecognition
verification = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir=tmpdir / 'spkrec-ecapa-voxceleb',
    run_opts={"device": "mps"}
)

signal, fs = torchaudio.load("test_audio.wav")
signal2, fs = torchaudio.load("test_audio2.wav")
score, prediction = verification.verify_batch(signal, signal2)
score, prediction


# In[11]:


verification.verify_files('test_audio.wav', 'test_audio_16k_single.wav')


# In[12]:


import torchaudio
from speechbrain.inference.encoders import MelSpectrogramEncoder

spk_emb_encoder = MelSpectrogramEncoder.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb-mel-spec",
                                                     savedir=tmpdir / 'spkrec-ecapa-voxceleb-mel-spec'
                                                    )

signal, fs = torchaudio.load("test_audio_16k_single.wav")
spk_embedding = spk_emb_encoder.encode_waveform(signal)
spk_embedding.shape


# In[13]:


import torchaudio
from speechbrain.inference.TTS import MSTacotron2
from speechbrain.inference.vocoders import HIFIGAN

# Intialize TTS (mstacotron2) and Vocoder (HiFIGAN)
ms_tacotron2 = MSTacotron2.from_hparams(source="speechbrain/tts-mstacotron2-libritts", 
                                        savedir=tmpdir / 'tts-mstacotron2-libritts')
hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-libritts-22050Hz", 
                                savedir=tmpdir / 'tts-hifigan-libritts-22050Hz', 
                                run_opts={"device": "mps"}
                               )

# Required input
REFERENCE_SPEECH = "test_audio_16k_single.wav"
INPUT_TEXT = "Mary had a little lamb"

# Running the Zero-Shot Multi-Speaker Tacotron2 model to generate mel-spectrogram
mel_outputs, mel_lengths, alignments = ms_tacotron2.clone_voice(INPUT_TEXT, REFERENCE_SPEECH)
#.generate_random_voice

# Running Vocoder (spectrogram-to-waveform)
waveforms = hifi_gan.decode_batch(mel_outputs)

display(Audio(data=waveforms.squeeze(1).cpu(), rate=22050))

# Save the waverform
#torchaudio.save("synthesized_sample.wav", waveforms.squeeze(1).cpu(), 22050)


# In[14]:


from speechbrain.inference.ASR import EncoderASR

asr_model = EncoderASR.from_hparams(source="speechbrain/asr-wav2vec2-commonvoice-14-en", 
                                    savedir=tmpdir / "asr-wav2vec2-commonvoice-14-en",
                                   run_opts={"device": "mps"})
asr_model.transcribe_file("test_audio_16k_single.wav")


# In[15]:


from speechbrain.inference.ASR import EncoderDecoderASR

asr_model = EncoderDecoderASR.from_hparams(source="speechbrain/asr-wav2vec2-commonvoice-en", 
                                           savedir=tmpdir / "asr-wav2vec2-commonvoice-en",
                                          run_opts={"device": "mps"})
asr_model.transcribe_file("test_audio_16k_single.wav")


# In[16]:


from speechbrain.inference.ASR import WhisperASR

asr_model = WhisperASR.from_hparams(source="speechbrain/rescuespeech_whisper", 
                                    savedir=tmpdir / "rescuespeech_whisper")
asr_model.transcribe_file("test_audio_16k_single.wav")


# ### Aliasing demo

# In[17]:


fs = 48000
y = np.sin(2*np.pi*15000*np.arange(2000)/fs).astype(np.float32)
plt.plot(np.linspace(-fs/2, fs/2, len(y)), np.fft.fftshift(np.abs(np.fft.fft(y))))
display(Audio(data=y, rate=fs))


# In[18]:


#resampler = Resample(orig_freq=fs, new_freq=16000, lowpass_filter_width=10, rolloff=0.8)
#resampled = resampler(torch.tensor(y).unsqueeze(0))
resampled = torch.tensor(y[::3]).unsqueeze(0)
plt.plot(np.linspace(-8000, 8000, resampled.shape[1]), np.fft.fftshift(np.abs(np.fft.fft(resampled.squeeze()))))
display(Audio(data=resampled.squeeze()[100:-100], rate=16000))


# In[25]:


resampler = Resample(orig_freq=fs, new_freq=16000) #, lowpass_filter_width=10, rolloff=0.8)
resampled = resampler(torch.tensor(y).unsqueeze(0))
plt.plot(np.linspace(-8000, 8000, resampled.shape[1]), np.fft.fftshift(np.abs(np.fft.fft(resampled.squeeze()))))
display(Audio(data=resampled.squeeze()[100:-100], rate=16000))


# In[26]:


plt.plot(resampled.squeeze()[100:-100])


# In[27]:


from scipy import signal
b, a = signal.butter(9, 1/4)
filtered = torchaudio.functional.filtfilt(torch.tensor(y).unsqueeze(0), 
                                          a_coeffs=torch.tensor(a.astype(np.float32)), 
                                          b_coeffs=torch.tensor(b.astype(np.float32)))


# In[28]:


resampler = Resample(orig_freq=fs, new_freq=16000)
resampled = resampler(filtered)
plt.plot(np.linspace(-8000, 8000, resampled.shape[1]), np.fft.fftshift(np.abs(np.fft.fft(resampled.squeeze()))))
display(Audio(data=resampled.squeeze()[100:-100], rate=16000))


# In[29]:


plt.plot(resampled.squeeze()[100:-100])


# In[ ]:




