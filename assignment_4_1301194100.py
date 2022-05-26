# -*- coding: utf-8 -*-
"""Assignment 4 - 1301194100.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TeAwNWL9eqlgldRTksLOVYT9PNTcD7D3

# Assignment 4
**NAMA : RIDHA ZALFA SALSABILA**
**NIM : 1301194100**
**KELAS : IF-42-GAB03** 

link google colab: https://colab.research.google.com/drive/1TeAwNWL9eqlgldRTksLOVYT9PNTcD7D3?usp=sharing

# Install & Imporrt library
"""

# Commented out IPython magic to ensure Python compatibility.
!pip install geoplot
!pip install geopandas
import geoplot as gplt
import geopandas as gpd
import geoplot.crs as gcrs
import imageio
import pandas as pd
from IPython.display import Image
import pathlib
import datetime
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import cm
from tqdm import tqdm
import mapclassify as mc
import numpy as np

# %matplotlib inline
import warnings
warnings.filterwarnings('ignore')

"""# Siapkan data"""

!gdown --id 1X4qTsukH2NUy1xuSQXUqVYhk9h9cuOjO
! gdown --id 1ZJG5fHK5A_m1zaqn1Uojf27slpDtavZ3

ina = gpd.read_file("indonesia_province_border.shp")
ina.head()

ina.plot(figsize=(30, 18))

#bagi beberapa provinsi berdasarkan pulau-pulau di Indonesia

sumatera = ['ACEH', 'SUMATERA UTARA', 'KEPULAUAN RIAU', 'SUMATERA BARAT', 'JAMBI', 'SUMATERA SELATAN',
            'BENGKULU', 'LAMPUNG', 'KEPULAUAN BANGKA BELITUNG', 'RIAU']

jawa = ['DKI JAKARTA', 'BANTEN', 'JAWA BARAT', 'JAWA TENGAH', 'JAWA TIMUR', 'DAERAH ISTIMEWA YOGYAKARTA',
        'BALI', 'NUSA TENGGARA BARAT', 'NUSA TENGGARA TIMUR']

kalimantan = ['KALIMANTAN BARAT', 'KALIMANTAN TIMUR', 'KALIMANTAN TENGAH', 'KALIMANTAN SELATAN', 'KALIMANTAN UTARA']

sulawesi = ['SULAWESI UTARA', 'GORONTALO', 'SULAWESI TENGAH', 'SULAWESI BARAT', 'SULAWESI SELATAN', 
            'SULAWESI TENGGARA']

papua = ['MALUKU UTARA', 'MALUKU', 'PAPUA', 'PAPUA BARAT']

df = pd.read_csv('dataset_covid_indonesia_as_05012021.csv')
df.head()

"""cari nilai minmax untuk tiap dataset sebagai batas atas dan batas bawah colorbar"""

# min max seluruh indonesia

min_ina = min(df['Daily_Case'])
max_ina = max(df['Daily_Case'])
df.describe()

# min max sumatera

df_sumatera = pd.DataFrame()
for i in range(len(sumatera)):
  df_sumatera = df_sumatera.append(df[(df['Province'] == sumatera[i])])
min_sumatera = min(df_sumatera['Daily_Case'])
max_sumatera = max(df_sumatera['Daily_Case'])

# min max jawa

df_jawa = pd.DataFrame()
for i in range(len(jawa)):
  df_jawa = df_jawa.append(df[(df['Province'] == jawa[i])])
min_jawa = min(df_jawa['Daily_Case'])
max_jawa = max(df_jawa['Daily_Case'])

# min max kalimantan

df_kalimantan = pd.DataFrame()
for i in range(len(kalimantan)):
  df_kalimantan = df_kalimantan.append(df[(df['Province'] == kalimantan[i])])
min_kalimantan = min(df_kalimantan['Daily_Case'])
max_kalimantan = max(df_kalimantan['Daily_Case'])

# min max sulawesi

df_sulawesi = pd.DataFrame()
for i in range(len(sulawesi)):
  df_sulawesi = df_sulawesi.append(df[(df['Province'] == sulawesi[i])])
min_sulawesi = min(df_sulawesi['Daily_Case'])
max_sulawesi = max(df_sulawesi['Daily_Case'])

# min max papua

df_papua = pd.DataFrame()
for i in range(len(papua)):
  df_papua = df_papua.append(df[(df['Province'] == papua[i])])
min_papua = min(df_papua['Daily_Case'])
max_papua = max(df_papua['Daily_Case'])

#penggabungan dataset supaya file .shp memiliki data dari .csv

df = ina.set_index('Provinsi').join(df.set_index('Province'))
df.head()

"""# fungsi"""

#plot daerah yang terkena covid

def plot_covid(anim_path, kolom, date, min, max, title, list_prov = [], n=10):
  if len(list_prov)!=0:
    df_covid = df.loc[list_prov]
    df_covid = df_covid.loc[df_covid['Date'] == date]
  else:
    df_covid = df.loc[df['Date'] == date]

  colormap = cm.get_cmap('RdYlGn_r', n)

  convert_scalar = plt.cm.ScalarMappable(cmap = colormap, norm = plt.Normalize(vmin=min, vmax=max))

  fig, ax = plt.subplots(1, figsize=(30, 8))
  df_covid.plot(column=kolom, ax=ax, cmap=colormap)

  cb_min = int(np.floor(min))
  cb_max = int(np.ceil(max))
  ticks = [cb_min, cb_max]
  for i in range(1, n):
    ticks.append(int(i*(cb_max - cb_min) / n + cb_min))

  colorbar = fig.colorbar(convert_scalar)
  colorbar.set_ticks(ticks)
  colorbar.set_ticklabels(ticks)

  date = datetime.datetime.strptime(date, '%d/%m/%Y')
  date = date.strftime("%d-%m-%Y")

  plt.title(f'Daily Positive Case di {title} pada Tanggal {date}', fontsize=15, pad=16)

  file_name = f'{anim_path}/{date}.png'
  plt.savefig(file_name, bbox_inches="tight", pad_inches=0.1)
  plt.close(fig)

  return file_name

"""# direktori"""

# direktori seluruh Indonesia
path = pathlib.Path("hasil/")
path.mkdir(parents=True, exist_ok=True)

# direktori untuk daerah sumatera
path_sumatera = pathlib.Path("hasil/sumatera")
path_sumatera.mkdir(parents=True, exist_ok=True)

# direktori untuk daerah jawa
path_jawa = pathlib.Path("hasil/jawa")
path_jawa.mkdir(parents=True, exist_ok=True)

# direktori untuk daerah kalimantan
path_kalimantan = pathlib.Path("hasil/kalimantan")
path_kalimantan.mkdir(parents=True, exist_ok=True)

# direktori untuk daerah sulawesi
path_sulawesi = pathlib.Path("hasil/sulawesi")
path_sulawesi.mkdir(parents=True, exist_ok=True)

# direktori untuk daerah papua
path_papua = pathlib.Path("hasil/papua")
path_papua.mkdir(parents=True, exist_ok=True)

# inisiasi range date yang diambil (dari 1 mei 2021 - 1 agustus 2021)
date_range = [x.strftime('%d/%m/%Y') for x in pd.date_range("05-01-2021", "08-01-2021")]
print(date_range)

"""# plot data ke dalam file & direktori"""

# inisiasi list

list_files_all, list_files_sumatera, list_files_jawa, = [], [], []
list_files_kalimantan, list_files_sulawesi, list_files_papua = [], [], []

# plot semua data 

for i in tqdm(range(len(date_range))):
  list_files_all.append(plot_covid(path, 'Daily_Case', date_range[i], min_ina, max_ina, 'Seluruh Indonesia'))
  list_files_sumatera.append(plot_covid(path_sumatera, 'Daily_Case', date_range[i], min_sumatera, max_sumatera, 'Daerah Pulau Sumatera', sumatera))
  list_files_jawa.append(plot_covid(path_jawa, 'Daily_Case', date_range[i], min_jawa, max_jawa, 'Daerah Pulau Jawa, Bali, dan Nusa tenggara', jawa))
  list_files_kalimantan.append(plot_covid(path_kalimantan, 'Daily_Case', date_range[i], min_kalimantan, max_kalimantan, 'Daerah Pulau Kalimantan', kalimantan))
  list_files_sulawesi.append(plot_covid(path_sulawesi, 'Daily_Case', date_range[i], min_sulawesi, max_sulawesi, 'Daerah Pulau Sulawesi', sulawesi))
  list_files_papua.append(plot_covid(path_papua, 'Daily_Case', date_range[i], min_papua, max_papua, 'Daerah Papua dan Maluku', papua))
print('\nSelesai.')

"""# membuat gif"""

#gabungkan semua file agar masing-masing list bisa menjadi gif
img_all = [imageio.imread(file_name) for file_name in list_files_all]
img_sumatera = [imageio.imread(file_name) for file_name in list_files_sumatera]
img_jawa = [imageio.imread(file_name) for file_name in list_files_jawa]
img_kalimantan = [imageio.imread(file_name) for file_name in list_files_kalimantan]
img_sulawesi = [imageio.imread(file_name) for file_name in list_files_sulawesi]
img_papua = [imageio.imread(file_name) for file_name in list_files_papua]

#simpan gif dengan rate 2 frames/second
imageio.mimsave("daily_case_ina.gif", img_all, fps=2)
imageio.mimsave("daily_case_sumatera.gif", img_sumatera, fps=2)
imageio.mimsave("daily_case_jawa.gif", img_jawa, fps=2)
imageio.mimsave("daily_case_kalimantan.gif", img_kalimantan, fps=2)
imageio.mimsave("daily_case_sulawesi.gif", img_sulawesi, fps=2)
imageio.mimsave("daily_case_papua.gif", img_papua, fps=2)

"""# output"""

# output seluruh Indonesia

Image(open('daily_case_ina.gif', 'rb').read())

# output Daerah Pulau Sumatera

Image(open('daily_case_sumatera.gif', 'rb').read())

# output Daerah Pulau Jawa, Bali, dan Nusa Tenggara

Image(open('daily_case_jawa.gif', 'rb').read())

# output Daerah Pulau Kalimantan

Image(open('daily_case_kalimantan.gif', 'rb').read())

# output Daerah Pulau Sulawesi

Image(open('daily_case_sulawesi.gif', 'rb').read())

# output Daerah Papua dan Maluku

Image(open('daily_case_papua.gif', 'rb').read())