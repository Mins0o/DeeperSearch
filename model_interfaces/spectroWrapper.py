# Copyright 2020 Max Planck Institute for Software Systems

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#       http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from torchvision.models import resnet50, alexnet
from torchvision import transforms
from PIL import Image
import torch
from tqdm import tqdm
import numpy as np
import time
from scipy.io.wavfile import read
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib import cm
import librosa
from os.path import exists
from os import mkdir

transform = transforms.Compose([
      # transforms.ColorJitter(0.1, 0.1, 0.1, 0.1),
      transforms.Resize((224, 224)),
      transforms.ToTensor(),
      transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
      ])

AUDDIR="./audios/"
INDICES=""
# normalize = lambda x:(x-np.array([0.485, 0.456, 0.406]))/np.array([0.229, 0.224, 0.225])
class CompatModel:
    def __init__(self):
        ############################################################
        self.model = resnet50()
        self.model.fc = torch.nn.Linear(self.model.fc.in_features, 4) 
        self.model.load_state_dict(torch.load('./model_interfaces/audio_classifier/model_librosa_resnet50.pt', map_location=torch.device('cuda')))
        ############################################################
        self.model.cuda()
        self.model.eval()
        self.calls=0
    def predict(self, sigs, **kwargs):
        j=kwargs['j']
        sigs = sigs*90 - 60
        images = sig2spec(sigs, j)
        self.calls+=1
        with torch.no_grad():
            #images = Image.fromarray(np.uint8(images[:,:,:3] * 256 - 0.5))
            images = Image.fromarray(images[:,:,:3])
            t_images = transform(images).cuda()             
            res=self.model(t_images[None, ...].float())
            res=torch.nn.functional.softmax(res,dim=1)
        model_output = res.cpu().detach().numpy()
        return model_output
        
mymodel=CompatModel()

def read_wave(wav, label):
    path = AUDDIR + label + "/" + str(wav) + ".wav"
    audio, sr =  librosa.load(path, sr = None)
    n = len(audio)
    n_fft = 204
    audio_pad = librosa.util.fix_length(audio, n + n_fft // 2)
    stft = librosa.stft(audio_pad, n_fft = n_fft)
    magnitude, phase = librosa.magphase(stft)
    magnitude_db = librosa.amplitude_to_db(magnitude)
    #print(Sxx.shape)
    #Sxx_dB = np.log10(Sxx)
    Sxx_dB = (magnitude_db+60)/90
    return Sxx_dB, phase, phase

def sig2spec(Sxx_dB, j):
    plt.imshow(np.squeeze(Sxx_dB, 0), interpolation='nearest', aspect='auto')
    if not exists('./model_interfaces/audio_classifier/intermediary/'):
        mkdir('./model_interfaces/audio_classifier/intermediary/')
    if not exists('./model_interfaces/audio_classifier/intermediary/' + label):
        mkdir('./model_interfaces/audio_classifier/intermediary/' + label)
    save_path = './model_interfaces/audio_classifier/intermediary/' + label + "/" + str(inds[j%3]) + '.png'
    plt.axis("off")
    plt.savefig(save_path, pad_inches = 0, bbox_inches = "tight")
    plt.close()
    pil_image = Image.open(save_path)   
    image = np.array(pil_image)
    return image[:,:,:3]

classes = ['cat', 'dog', 'kid', 'parrot'] # add more in the correct order of class 0, 1, ...
items_per_class= 20
inds = range(8,8+items_per_class)

x_test=[]
y_test=[]
ps = []
if INDICES=="":
  for j, label in enumerate(classes):
    x_test += [np.array(read_wave(i, label)[0]) for i in inds]
    y_test += (j*np.ones(len(inds),dtype="int32")).tolist() 
    ps += [np.array(read_wave(i, label)[1]) for i in inds]
if INDICES=="ALL":
  for j, label in enumerate(classes):
    x_test.append(np.stack([read_wave(i, label)[0] for i in tqdm(range(100))]).tolist())
    y_test.append(j*np.ones(len(x_test)).tolist())
    ps += [read_wave(i, label)[1] for i in range(100)]

print(x_test[0].shape)
