# Compréhension des vidéos  |  Gemini API  |  Google AI for Developers
Les modèles Gemini peuvent traiter des vidéos, ce qui permet de créer de nombreux cas d'utilisation innovants qui auraient auparavant nécessité des modèles spécifiques au domaine. Voici quelques-unes des fonctionnalités de vision de Gemini:

*   Décrire, segmenter et extraire des informations à partir de vidéos
*   Répondre aux questions sur le contenu vidéo
*   Faire référence à des codes temporels sp��cifiques dans une vidéo

Gemini a été conçu dès le départ pour être multimodal, et nous continuons de repousser les limites du possible. Ce guide explique comment utiliser l'API Gemini pour générer des réponses textuelles basées sur des entrées vidéo.

Entrée vidéo
------------

Vous pouvez fournir des vidéos à Gemini de différentes manières:

*   [Importez un fichier vidéo](#upload-video) à l'aide de l'API File avant d'envoyer une requête à `generateContent`. Utilisez cette méthode pour les fichiers de plus de 20 Mo, les vidéos de plus d'une minute environ ou lorsque vous souhaitez réutiliser le fichier dans plusieurs requêtes.
*   [Transmettez des données vidéo intégrées](#inline-video) avec la requête à `generateContent`. Utilisez cette méthode pour les fichiers de petite taille (<20 Mo) et les durées plus courtes.
*   [Inclure une URL YouTube](#youtube) directement dans l'invite.

### Importer un fichier vidéo

Vous pouvez utiliser l'[API Files](https://ai.google.dev/gemini-api/docs/files?hl=fr) pour importer un fichier vidéo. Utilisez toujours l'API Files lorsque la taille totale de la requête (y compris le fichier, l'invite de texte, les instructions système, etc.) est supérieure à 20 Mo, que la durée de la vidéo est importante ou si vous prévoyez d'utiliser la même vidéo dans plusieurs invites.

L'API File accepte directement les formats de fichiers vidéo. Cet exemple utilise le court métrage de la NASA ["La Grande Tache rouge de Jupiter se rétrécit et se développe"](https://www.youtube.com/watch?v=JDi4IdtvDVE0&hl=fr). Crédit: Goddard Space Flight Center (GSFC)/David Ladd (2018).

"Jupiter's Great Red Spot Shrinks and Grows" est dans le domaine public et ne montre pas de personnes identifiables. ([Consignes d'utilisation des images et des contenus multimédias de la NASA](https://www.nasa.gov/nasa-brand-center/images-and-media/))

Le code suivant télécharge l'exemple de vidéo, l'importe à l'aide de l'API File, attend qu'il soit traité, puis utilise la référence de fichier dans une requête `generateContent`.

### Python

```
from google import genai

client = genai.Client()

myfile = client.files.upload(file="path/to/sample.mp4")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents=[myfile, "Summarize this video. Then create a quiz with an answer key based on the information in this video."]
)

print(response.text)

```


### JavaScript

```
import {
  GoogleGenAI,
  createUserContent,
  createPartFromUri,
} from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const myfile = await ai.files.upload({
    file: "path/to/sample.mp4",
    config: { mimeType: "video/mp4" },
  });

  const response = await ai.models.generateContent({
    model: "gemini-2.0-flash",
    contents: createUserContent([
      createPartFromUri(myfile.uri, myfile.mimeType),
      "Summarize this video. Then create a quiz with an answer key based on the information in this video.",
    ]),
  });
  console.log(response.text);
}

await main();

```


### Go

```
uploadedFile, _ := client.Files.UploadFromPath(ctx, "path/to/sample.mp4", nil)

parts := []*genai.Part{
    genai.NewPartFromText("Summarize this video. Then create a quiz with an answer key based on the information in this video."),
    genai.NewPartFromURI(uploadedFile.URI, uploadedFile.MIMEType),
}

contents := []*genai.Content{
    genai.NewContentFromParts(parts, genai.RoleUser),
}

result, _ := client.Models.GenerateContent(
    ctx,
    "gemini-2.0-flash",
    contents,
    nil,
)

fmt.Println(result.Text())

```


### REST

```
VIDEO_PATH="path/to/sample.mp4"
MIME_TYPE=$(file -b --mime-type "${VIDEO_PATH}")
NUM_BYTES=$(wc -c < "${VIDEO_PATH}")
DISPLAY_NAME=VIDEO

tmp_header_file=upload-header.tmp

echo "Starting file upload..."
curl "https://generativelanguage.googleapis.com/upload/v1beta/files" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -D ${tmp_header_file} \
  -H "X-Goog-Upload-Protocol: resumable" \
  -H "X-Goog-Upload-Command: start" \
  -H "X-Goog-Upload-Header-Content-Length: ${NUM_BYTES}" \
  -H "X-Goog-Upload-Header-Content-Type: ${MIME_TYPE}" \
  -H "Content-Type: application/json" \
  -d "{'file': {'display_name': '${DISPLAY_NAME}'}}" 2> /dev/null

upload_url=$(grep -i "x-goog-upload-url: " "${tmp_header_file}" | cut -d" " -f2 | tr -d "\r")
rm "${tmp_header_file}"

echo "Uploading video data..."
curl "${upload_url}" \
  -H "Content-Length: ${NUM_BYTES}" \
  -H "X-Goog-Upload-Offset: 0" \
  -H "X-Goog-Upload-Command: upload, finalize" \
  --data-binary "@${VIDEO_PATH}" 2> /dev/null > file_info.json

file_uri=$(jq -r ".file.uri" file_info.json)
echo file_uri=$file_uri

echo "File uploaded successfully. File URI: ${file_uri}"

# --- 3. Generate content using the uploaded video file ---
echo "Generating content from video..."
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[
          {"file_data":{"mime_type": "'"${MIME_TYPE}"'", "file_uri": "'"${file_uri}"'"}},
          {"text": "Summarize this video. Then create a quiz with an answer key based on the information in this video."}]
        }]
      }' 2> /dev/null > response.json

jq -r ".candidates[].content.parts[].text" response.json

```


Pour en savoir plus sur l'utilisation des fichiers multimédias, consultez la section [API Files](https://ai.google.dev/gemini-api/docs/files?hl=fr).

### Transmettre des données vidéo de manière intégrée

Au lieu d'importer un fichier vidéo à l'aide de l'API File, vous pouvez transmettre des vidéos plus petites directement dans la requête à `generateContent`. Cette méthode convient aux vidéos plus courtes dont la taille de requête totale est inférieure à 20 Mo.

Voici un exemple de données vidéo intégrées:

### Python

```
# Only for videos of size <20Mb
video_file_name = "/path/to/your/video.mp4"
video_bytes = open(video_file_name, 'rb').read()

response = client.models.generate_content(
    model='models/gemini-2.0-flash',
    contents=types.Content(
        parts=[
            types.Part(
                inline_data=types.Blob(data=video_bytes, mime_type='video/mp4')
            ),
            types.Part(text='Please summarize the video in 3 sentences.')
        ]
    )
)

```


### JavaScript

```
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

const ai = new GoogleGenAI({});
const base64VideoFile = fs.readFileSync("path/to/small-sample.mp4", {
  encoding: "base64",
});

const contents = [
  {
    inlineData: {
      mimeType: "video/mp4",
      data: base64VideoFile,
    },
  },
  { text: "Please summarize the video in 3 sentences." }
];

const response = await ai.models.generateContent({
  model: "gemini-2.0-flash",
  contents: contents,
});
console.log(response.text);

```


### REST

```
VIDEO_PATH=/path/to/your/video.mp4

if [[ "$(base64 --version 2>&1)" = *"FreeBSD"* ]]; then
  B64FLAGS="--input"
else
  B64FLAGS="-w0"
fi

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[
            {
              "inline_data": {
                "mime_type":"video/mp4",
                "data": "'$(base64 $B64FLAGS $VIDEO_PATH)'"
              }
            },
            {"text": "Please summarize the video in 3 sentences."}
        ]
      }]
    }' 2> /dev/null

```


### Inclure une URL YouTube

L'API Gemini et AI Studio acceptent les URL YouTube en tant que données de fichier `Part`. Vous pouvez inclure une URL YouTube avec une invite demandant au modèle de résumer, de traduire ou d'interagir d'une autre manière avec le contenu vidéo.

**Limites :**

*   Avec l'abonnement sans frais, vous ne pouvez pas importer plus de huit heures de vidéos YouTube par jour.
*   Pour l'abonnement payant, aucune limite n'est appliquée à la durée des vidéos.
*   Pour les modèles antérieurs à la version 2.5, vous ne pouvez importer qu'une seule vidéo par requête. Pour les modèles postérieurs à la version 2.5, vous pouvez importer jusqu'à 10 vidéos par requête.
*   Vous ne pouvez mettre en ligne que des vidéos publiques (et non privées ni non répertoriées).

L'exemple suivant montre comment inclure une URL YouTube avec une invite:

### Python

```
response = client.models.generate_content(
    model='models/gemini-2.0-flash',
    contents=types.Content(
        parts=[
            types.Part(
                file_data=types.FileData(file_uri='https://www.youtube.com/watch?v=9hE5-98ZeCg')
            ),
            types.Part(text='Please summarize the video in 3 sentences.')
        ]
    )
)

```


### JavaScript

```
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-pro" });
const result = await model.generateContent([
  "Please summarize the video in 3 sentences.",
  {
    fileData: {
      fileUri: "https://www.youtube.com/watch?v=9hE5-98ZeCg",
    },
  },
]);
console.log(result.response.text());

```


### Go

```
package main

import (
  "context"
  "fmt"
  "os"
  "google.golang.org/genai"
)

func main() {
  ctx := context.Background()
  client, err := genai.NewClient(ctx, nil)
  if err != nil {
      log.Fatal(err)
  }

  parts := []*genai.Part{
      genai.NewPartFromText("Please summarize the video in 3 sentences."),
      genai.NewPartFromURI("https://www.youtube.com/watch?v=9hE5-98ZeCg","video/mp4"),
  }

  contents := []*genai.Content{
      genai.NewContentFromParts(parts, genai.RoleUser),
  }

  result, _ := client.Models.GenerateContent(
      ctx,
      "gemini-2.0-flash",
      contents,
      nil,
  )

  fmt.Println(result.Text())
}

```


### REST

```
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[
            {"text": "Please summarize the video in 3 sentences."},
            {
              "file_data": {
                "file_uri": "https://www.youtube.com/watch?v=9hE5-98ZeCg"
              }
            }
        ]
      }]
    }' 2> /dev/null

```


Se reporter aux codes temporels du contenu
------------------------------------------

Vous pouvez poser des questions sur des moments spécifiques de la vidéo à l'aide de codes temporels au format `MM:SS`.

### Python

```
prompt = "What are the examples given at 00:05 and 00:10 supposed to show us?" # Adjusted timestamps for the NASA video

```


### JavaScript

```
const prompt = "What are the examples given at 00:05 and 00:10 supposed to show us?";

```


### Go

```
    prompt := []*genai.Part{
        genai.NewPartFromURI(currentVideoFile.URI, currentVideoFile.MIMEType),
         // Adjusted timestamps for the NASA video
        genai.NewPartFromText("What are the examples given at 00:05 and " +
            "00:10 supposed to show us?"),
    }

```


### REST

```
PROMPT="What are the examples given at 00:05 and 00:10 supposed to show us?"

```


Transcrire des vidéos et fournir des descriptions visuelles
-----------------------------------------------------------

Les modèles Gemini peuvent transcrire et fournir des descriptions visuelles du contenu vidéo en traitant à la fois la piste audio et les images. Pour les descriptions visuelles, le modèle échantillonne la vidéo à un taux de **1 image par seconde**. Ce taux d'échantillonnage peut avoir un impact sur le niveau de détail des descriptions, en particulier pour les vidéos dont les visuels changent rapidement.

### Python

```
prompt = "Transcribe the audio from this video, giving timestamps for salient events in the video. Also provide visual descriptions."

```


### JavaScript

```
const prompt = "Transcribe the audio from this video, giving timestamps for salient events in the video. Also provide visual descriptions.";

```


### Go

```
    prompt := []*genai.Part{
        genai.NewPartFromURI(currentVideoFile.URI, currentVideoFile.MIMEType),
        genai.NewPartFromText("Transcribe the audio from this video, giving timestamps for salient events in the video. Also " +
            "provide visual descriptions."),
    }

```


### REST

```
PROMPT="Transcribe the audio from this video, giving timestamps for salient events in the video. Also provide visual descriptions."

```


Personnaliser le traitement des vidéos
--------------------------------------

Vous pouvez personnaliser le traitement vidéo dans l'API Gemini en définissant des intervalles de coupure ou en fournissant un échantillonnage personnalisé de la fréquence d'images.

### Définir des intervalles de coupure

Vous pouvez découper une vidéo en spécifiant `videoMetadata` avec des décalages de début et de fin.

### Python

```
response = client.models.generate_content(
    model='models/gemini-2.5-flash-preview-05-20',
    contents=types.Content(
        parts=[
            types.Part(
                file_data=types.FileData(file_uri='https://www.youtube.com/watch?v=XEzRZ35urlk'),
                video_metadata=types.VideoMetadata(
                    start_offset='1250s',
                    end_offset='1570s'
                )
            ),
            types.Part(text='Please summarize the video in 3 sentences.')
        ]
    )
)

```


### Définir une fréquence d'images personnalisée

Vous pouvez définir un échantillonnage personnalisé de la fréquence d'images en transmettant un argument `fps` à `videoMetadata`.

### Python

```
# Only for videos of size <20Mb
video_file_name = "/path/to/your/video.mp4"
video_bytes = open(video_file_name, 'rb').read()

response = client.models.generate_content(
    model='models/gemini-2.5-flash-preview-05-20',
    contents=types.Content(
        parts=[
            types.Part(
                inline_data=types.Blob(
                    data=video_bytes,
                    mime_type='video/mp4'),
                video_metadata=types.VideoMetadata(fps=5)
            ),
            types.Part(text='Please summarize the video in 3 sentences.')
        ]
    )
)

```


Par défaut, une image par seconde (FPS) est échantillonnée à partir de la vidéo. Vous pouvez définir un faible FPS (< 1) pour les vidéos longues. Cela est particulièrement utile pour les vidéos principalement statiques (par exemple, des cours). Si vous souhaitez capturer plus de détails dans des visuels qui changent rapidement, envisagez de définir une valeur FPS plus élevée.

Formats vidéo acceptés
----------------------

Gemini est compatible avec les types MIME de formats vidéo suivants:

*   `video/mp4`
*   `video/mpeg`
*   `video/mov`
*   `video/avi`
*   `video/x-flv`
*   `video/mpg`
*   `video/webm`
*   `video/wmv`
*   `video/3gpp`

Détails techniques sur les vidéos
---------------------------------

*   **Modèles et contexte compatibles**: tous les modèles Gemini 2.0 et 2.5 peuvent traiter les données vidéo.
    *   Les modèles avec une fenêtre de contexte de deux millions de jetons peuvent traiter des vidéos d'une durée maximale de deux heures à la résolution multimédia par défaut ou de six heures à une résolution multimédia basse, tandis que les modèles avec une fenêtre de contexte d'un million de jetons peuvent traiter des vidéos d'une durée maximale d'une heure à la résolution multimédia par défaut ou de trois heures à une résolution multimédia basse.
*   **Traitement de l'API File**: lorsque vous utilisez l'API File, les vidéos sont échantillonnées à 1 image par seconde (FPS) et l'audio est traité à 1 kbit/s (canal unique). Des codes temporels sont ajoutés toutes les secondes.
    *   Ces tarifs sont susceptibles d'être modifiés à l'avenir pour améliorer les inférences.
*   **Calcul des jetons**: chaque seconde de vidéo est tokenisée comme suit :
    *   Images individuelles (échantillonnées à 1 FPS) :
        *   Si [`mediaResolution`](https://ai.google.dev/api/generate-content?hl=fr#MediaResolution) est défini sur "low" (bas), les images sont tokenisées à 66 jetons par image.
        *   Sinon, les images sont tokenisées à 258 jetons par image.
    *   Audio: 32 jetons par seconde.
    *   Les métadonnées sont également incluses.
    *   Total: environ 300 jetons par seconde de vidéo à la résolution multimédia par défaut, ou 100 jetons par seconde de vidéo à faible résolution multimédia.
*   **Format de code temporel**: lorsque vous faites référence à des moments spécifiques d'une vidéo dans votre requête, utilisez le format `MM:SS` (par exemple, `01:15` pendant 1 minute et 15 secondes).
*   **Bonnes pratiques** :
    *   Pour des résultats optimaux, n'utilisez qu'une seule vidéo par requête de requête.
    *   Si vous combinez du texte et une seule vidéo, placez la requête textuelle _après_ la partie vidéo dans le tableau `contents`.
    *   Notez que les séquences d'action rapides peuvent perdre des détails en raison du taux d'échantillonnage de 1 FPS. Si nécessaire, pensez à ralentir ces extraits.

Étape suivante
--------------

Ce guide explique comment importer des fichiers vidéo et générer des sorties textuelles à partir d'entrées vidéo. Pour en savoir plus, consultez les ressources suivantes :

*   [Instructions système](https://ai.google.dev/gemini-api/docs/text-generation?hl=fr#system-instructions) : les instructions système vous permettent d'orienter le comportement du modèle en fonction de vos besoins et de vos cas d'utilisation spécifiques.
*   [API Files](https://ai.google.dev/gemini-api/docs/files?hl=fr): découvrez comment importer et gérer des fichiers à utiliser avec Gemini.
*   [Stratégies d'invite de fichier](https://ai.google.dev/gemini-api/docs/files?hl=fr#prompt-guide): l'API Gemini prend en charge les invites avec des données textuelles, des images, des données audio et des données vidéo, également appelées invites multimodales.
*   [Conseils de sécurité](https://ai.google.dev/gemini-api/docs/safety-guidance?hl=fr): Parfois, les modèles d'IA générative produisent des résultats inattendus, comme des résultats inexacts, biaisés ou choquants. Le post-traitement et l'évaluation humaine sont essentiels pour limiter le risque de préjudice lié à ces sorties.