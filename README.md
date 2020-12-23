# Prerequisite 
Required downloads :  
- [./model_interfaces/cifar_models/model_defended/checkpoint-70000.data-00000-of-00001](https://drive.google.com/file/d/1_crLK5swgDPa-hU55ZcfwBeNjToPD3Me/view?usp=sharing)  
- [./model_interfaces/cifar_models/model_undefended/checkpoint-79000.data-00000-of-00001](https://drive.google.com/file/d/172Vy4Hcv0cAMulRal_xL6Ubb55ap7jxG/view?usp=sharing)  
- [/audios/](https://drive.google.com/drive/folders/1N5-sOO8o-82yemaRJTXKtKn6jZmBlvWM?usp=sharing)

Other dependencies:
matplotlib, tqdm, librosa, pytorch, torchvision, tensorflow=1.14
using conda, use the following commands  
1. conda create -n DeeperSearch
2. conda activate DeeperSearch
3. conda install python=3.6
4. conda install matplotlib tqdm librosa
5. conda install pytorch torchvision -c pytorch
6. conda install tensorflow=1.14 -c conda-forge
7. conda clean -a
After you finish experimenting, you may delete the environment now.
7. conda activate base
8. conda env remove -n DeeperSearch

# AISE-DeepSearch
Reproduce, improve and expand the DeepSearch paper
## References
### Original code: [Link](https://github.com/Practical-Formal-Methods/DeepSearch)
### Original paper: [Link](https://arxiv.org/pdf/1910.06296.pdf)
