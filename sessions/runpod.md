# Conexión a servidor virtual

Uso runpod.io como proveedor de servicios de LLM.
He dado de alta una clave pública que he generado espcíficamente con 1password

ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJmYlcq6W8/fr+00jFuPMOSBXp0dj94mvMrtDDWDpPK1
key type: Ed25519

Uso los parámetros de runpod: ssh root@205.196.17.187 -p 18161 -i ~/.ssh/id_ed25519
y autorizo el acceso con la clave pública desde 1password


Runpod te cobra si la máquina está activa, independientemente de si estás usando la máquina o no.
puedes pararla desde el dashboard de runpod, que te cobra bastante menos pero
! ojo, el puerto cambia cada vez que se reinicia el servidor

Hay que cambiarlo en el fichero ~/.ssh/config
/Users/ant/.ssh/config

root@2a84138efc9e:~# nvidia-smi
Fri Dec 27 11:43:19 2024
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 565.57.01              Driver Version: 565.57.01      CUDA Version: 12.7     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA H100 NVL                On  |   00000000:A1:00.0 Off |                    0 |
| N/A   34C    P0             62W /  310W |       1MiB /  95830MiB |      0%      Default |
|                                         |                        |             Disabled |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+

root@2a84138efc9e:~# uname -a
Linux 2a84138efc9e 6.8.0-50-generic #51~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Nov 21 12:03:03 UTC  x86_64 x86_64 x86_64 GNU/Linux


Desde Cursor me puedo conectar en remoto a la máquina

Para clonar el repo de github, desde el directorio de trabajo, hago:
git clone https://github.com/hormigo69/real-time-ml-3.git
