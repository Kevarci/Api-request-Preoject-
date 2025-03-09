from dotenv import load_dotenv
load_dotenv()
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
 
auth_manager = SpotifyClientCredentials(client_id=client_id, 
                                       client_secret=client_secret)
spotify = spotipy.Spotify(auth_manager=auth_manager)

results = spotify.search(q='artist:Coldplay', type='track', limit=5)


tracks_data = []
for track in results['tracks']['items']:
    track_info = {
        'name': track['name'],
        'popularity': track['popularity'],
        'duration_ms': track['duration_ms'] / 1000,  
        'album': track['album']['name'],
        'release_date': track['album']['release_date']
    }
    tracks_data.append(track_info)


df_tracks = pd.DataFrame(tracks_data)


plt.figure(figsize=(10, 6))
sns.scatterplot(x='duration_ms', y='popularity', data=df_tracks, alpha=0.7)
plt.title('Relación entre Duración y Popularidad de Canciones de Coldplay')
plt.xlabel('Duración (segundos)')
plt.ylabel('Popularidad')


sns.regplot(x='duration_ms', y='popularity', data=df_tracks, scatter=False, color='red')


correlation = df_tracks['duration_ms'].corr(df_tracks['popularity'])
plt.annotate(f'Correlación: {correlation:.2f}', xy=(0.05, 0.95), xycoords='axes fraction')


plt.savefig(r'c:\Users\stick\Desktop\4Geeks Academy Projects\Api-request-Preoject-\duracion_vs_popularidad.png')
plt.show()


print("Estadísticas descriptivas:")
print(df_tracks[['duration_ms', 'popularity']].describe())
print(f"\nCorrelación entre duración y popularidad: {correlation:.4f}")


df_tracks['duration_range'] = pd.cut(df_tracks['duration_ms'], 
                                    bins=[0, 180, 240, 300, 600],
                                    labels=['< 3 min', '3-4 min', '4-5 min', '> 5 min'])


popularity_by_duration = df_tracks.groupby('duration_range')['popularity'].mean().reset_index()
print("\nPopularidad promedio por rango de duración:")
print(popularity_by_duration)


plt.figure(figsize=(10, 6))
sns.barplot(x='duration_range', y='popularity', data=popularity_by_duration)
plt.title('Popularidad Promedio por Rango de Duración')
plt.xlabel('Rango de Duración')
plt.ylabel('Popularidad Promedio')
plt.savefig(r'c:\Users\stick\Desktop\4Geeks Academy Projects\Api-request-Preoject-\popularidad_por_duracion.png')
plt.show()

#La respuesta del scatter esta en el archivo figure_1 y figure_2 en la raiz del proyecto, como se corrio en local se crearon y guardaron. 