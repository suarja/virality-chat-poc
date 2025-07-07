# Using files  |  Gemini API  |  Google AI for Developers

[Passer au contenu principal](#main-content)

- [Modèles](https://ai.google.dev/gemini-api/docs)
  - [Documentation de l'API Gemini](https://ai.google.dev/gemini-api/docs)
  - [Documentation de référence de l'API](https://ai.google.dev/api)
  - [Liste de recettes](https://github.com/google-gemini/cookbook)
  - [Communauté](https://discuss.ai.google.dev/c/gemini-api/)
- Solutions
- Aide au codage
- Showcase
- Communauté

- [Aperçu](https://ai.google.dev/api)
- [Versions de l'API](https://ai.google.dev/gemini-api/docs/api-versions)
- Capacités
- [Modèles](https://ai.google.dev/api/models)
- [Génération de contenu...](https://ai.google.dev/api/generate-content)
- [API Live](https://ai.google.dev/api/live)
- [Jetons](https://ai.google.dev/api/tokens)
- [Fichiers](https://ai.google.dev/api/files)
- [Mise en cache](https://ai.google.dev/api/caching)
- [Embeddings](https://ai.google.dev/api/embeddings)

- [Toutes les méthodes](https://ai.google.dev/api/all-methods)

- Références du SDK
- [Python](https://googleapis.github.io/python-genai/)
- [Go](https://pkg.go.dev/google.golang.org/genai)
- [TypeScript](https://googleapis.github.io/js-genai/)
- [Java](https://googleapis.github.io/java-genai/javadoc/)

L'API Gemini permet d'importer des fichiers multimédias séparément de l'entrée de la requête, ce qui vous permet de réutiliser vos contenus multimédias dans plusieurs requêtes et requêtes. Pour en savoir plus, consultez le guide [Générer des requêtes avec des contenus multimédias](https://ai.google.dev/gemini-api/docs/prompting_with_media?hl=fr).

- [Point de terminaison](#body.HTTP_TEMPLATE)
- [Corps de la requête](#body.request_body)
  - [Représentation JSON](#body.request_body.SCHEMA_REPRESENTATION)
- [Corps de la réponse](#body.response_body)
  - [Représentation JSON](#body.CreateFileResponse.SCHEMA_REPRESENTATION)
- [Exemple de requête](#body.codeSnippets)
  - [Image](#body.codeSnippets.group)
  - [Audio](#body.codeSnippets.group_1)
  - [Texte](#body.codeSnippets.group_2)
  - [Vidéo](#body.codeSnippets.group_3)
  - [PDF](#body.codeSnippets.group_4)

Crée un objet `File`.

### Point de terminaison

- URI d'importation, pour les demandes d'importation de médias:

post `https://generativelanguage.googleapis.com/upload/v1beta/files`

- URI de métadonnées, pour les requêtes de métadonnées uniquement:

post `https://generativelanguage.googleapis.com/v1beta/files`

### Corps de la requête

Le corps de la requête contient des données présentant la structure suivante :

`file` `` object (`[File](https://ai.google.dev/api/files?hl=fr#File)`) ``

Facultatif. Métadonnées du fichier à créer.

### Exemple de requête

### Image

### Python

### Node.js

### Go

### Coquille Rose

### Audio

### Python

### Node.js

### Go

### Coquille Rose

### Texte

### Python

### Node.js

### Go

### Coquille Rose

### Vidéo

### Python

### Node.js

### Go

### Coquille Rose

### PDF

### Python

### Corps de la réponse

Réponse pour `media.upload`.

Si la requête aboutit, le corps de la réponse contient des données qui ont la structure suivante :

`file` `` object (`[File](https://ai.google.dev/api/files?hl=fr#File)`) ``

Métadonnées du fichier créé.

| Représentation JSON                                  |
| ---------------------------------------------------- |
| urltomarkdowncodeblockplaceholder00.8351799866849756 |

## Méthode: files.get

- [Point de terminaison](#body.HTTP_TEMPLATE)
- [Paramètres de chemin d'accès](#body.PATH_PARAMETERS)
- [Corps de la requête](#body.request_body)
- [Corps de la réponse](#body.response_body)
- [Exemple de requête](#body.codeSnippets)
  - [Basic](#body.codeSnippets.group)

Récupère les métadonnées de l'`File` donné.

### Point de terminaison

get `https://generativelanguage.googleapis.com/v1beta/{name=files/*}`

### Paramètres de chemin d'accès

`name` `string`

Obligatoire. Nom du `File` à obtenir. Exemple: `files/abc-123` Il se présente sous la forme `files/{file}`.

### Corps de la requête

Le corps de la requête doit être vide.

### Exemple de requête

### Python

### Node.js

### Go

### Coquille Rose

### Corps de la réponse

Si la requête aboutit, le corps de la réponse contient une instance de `[File](https://ai.google.dev/api/files?hl=fr#File)`.

## Méthode: files.list

- [Point de terminaison](#body.HTTP_TEMPLATE)
- [Paramètres de requête](#body.QUERY_PARAMETERS)
- [Corps de la requête](#body.request_body)
- [Corps de la réponse](#body.response_body)
  - [Représentation JSON](#body.ListFilesResponse.SCHEMA_REPRESENTATION)
- [Exemple de requête](#body.codeSnippets)
  - [Basic](#body.codeSnippets.group)

Répertorie les métadonnées des `File` appartenant au projet à l'origine de la requête.

### Point de terminaison

get `https://generativelanguage.googleapis.com/v1beta/files`

### Paramètres de requête

`pageSize` `integer`

Facultatif. Nombre maximal de `File` à renvoyer par page. Si aucune valeur n'est spécifiée, la valeur par défaut est 10. La valeur maximale de `pageSize` est 100.

`pageToken` `string`

Facultatif. Jeton de page reçu d'un appel `files.list` précédent.

### Corps de la requête

Le corps de la requête doit être vide.

### Exemple de requête

### Python

### Node.js

### Go

### Coquille Rose

### Corps de la réponse

Réponse pour `files.list`.

Si la requête aboutit, le corps de la réponse contient des données qui ont la structure suivante :

Champs

`files[]` `` object (`[File](https://ai.google.dev/api/files?hl=fr#File)`) ``

Liste des `File`.

`nextPageToken` `string`

Jeton pouvant être envoyé en tant que `pageToken` dans un appel `files.list` ultérieur.

| Représentation JSON                                   |
| ----------------------------------------------------- |
| urltomarkdowncodeblockplaceholder10.15061210167246752 |

## Méthode: files.delete

- [Point de terminaison](#body.HTTP_TEMPLATE)
- [Paramètres de chemin d'accès](#body.PATH_PARAMETERS)
- [Corps de la requête](#body.request_body)
- [Corps de la réponse](#body.response_body)
- [Exemple de requête](#body.codeSnippets)
  - [Basic](#body.codeSnippets.group)

Supprime la `File`.

### Point de terminaison

delete `https://generativelanguage.googleapis.com/v1beta/{name=files/*}`

### Paramètres de chemin d'accès

`name` `string`

Obligatoire. Nom du `File` à supprimer. Exemple: `files/abc-123` Il se présente sous la forme `files/{file}`.

### Corps de la requête

Le corps de la requête doit être vide.

### Exemple de requête

### Python

### Node.js

### Go

### Coquille Rose

### Corps de la réponse

Si la requête aboutit, le corps de la réponse est un objet JSON vide.

## Ressource REST : fichiers

- [Ressource: Fichier](#File)
  - [Représentation JSON](#File.SCHEMA_REPRESENTATION)
- [VideoFileMetadata](#VideoFileMetadata)
  - [Représentation JSON](#VideoFileMetadata.SCHEMA_REPRESENTATION)
- [État](#State)
- [Source](#Source)
- [Méthodes](#METHODS_SUMMARY)

## Ressource: Fichier

Fichier importé dans l'API. Identifiant suivant: 15

Champs

`name` `string`

Immuable. Identifiant. Nom de la ressource `File`. L'ID (nom sans le préfixe "files/") peut contenir jusqu'à 40 caractères alphanumériques en minuscule ou des tirets (-). L'ID ne peut pas commencer ni se terminer par un tiret. Si le nom est vide lors de la création, un nom unique est généré. Exemple : `files/123-456`

`displayName` `string`

Facultatif. Nom à afficher lisible par l'humain pour le `File`. Le nom à afficher ne doit pas dépasser 512 caractères, espaces compris. Exemple: "Image de bienvenue"

`mimeType` `string`

Uniquement en sortie. Type MIME du fichier.

`sizeBytes` `string ([int64](https://developers.google.com/discovery/v1/type-format?hl=fr) format)`

Uniquement en sortie. Taille du fichier, en octets.

Uniquement en sortie. Code temporel de création de l'`File`.

Utilise la norme RFC 3339, où la sortie générée est toujours normalisée avec le suffixe Z et utilise 0, 3, 6 ou 9 chiffres décimaux. Les décalages autres que "Z" sont également acceptés. Exemples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` ou `"2014-10-02T15:01:23+05:30"`.

Uniquement en sortie. Code temporel de la dernière mise à jour de l'`File`.

Utilise la norme RFC 3339, où la sortie générée est toujours normalisée avec le suffixe Z et utilise 0, 3, 6 ou 9 chiffres décimaux. Les décalages autres que "Z" sont également acceptés. Exemples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` ou `"2014-10-02T15:01:23+05:30"`.

`expirationTime` `` string (`[Timestamp](https://protobuf.dev/reference/protobuf/google.protobuf/#timestamp)` format) ``

Uniquement en sortie. Code temporel de suppression de l'`File`. Ne doit être défini que si l'`File` est programmé pour expirer.

Utilise la norme RFC 3339, où la sortie générée est toujours normalisée avec le suffixe Z et utilise 0, 3, 6 ou 9 chiffres décimaux. Les décalages autres que "Z" sont également acceptés. Exemples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` ou `"2014-10-02T15:01:23+05:30"`.

`sha256Hash` `string ([bytes](https://developers.google.com/discovery/v1/type-format?hl=fr) format)`

Uniquement en sortie. Hachage SHA-256 des octets importés.

Chaîne encodée en base64.

`uri` `string`

Uniquement en sortie. URI de l'`File`.

`downloadUri` `string`

Uniquement en sortie. URI de téléchargement de l'`File`.

Uniquement en sortie. État de traitement du fichier.

Uniquement en sortie. État d'erreur si le traitement du fichier a échoué.

`metadata` `Union type`

Métadonnées du fichier. `metadata` ne peut être qu'un des éléments suivants :

Uniquement en sortie. Métadonnées d'une vidéo.

| Représentation JSON                                  |
| ---------------------------------------------------- |
| urltomarkdowncodeblockplaceholder20.8199430865486983 |

Métadonnées d'une vidéo `File`.

`videoDuration` `` string (`[Duration](https://protobuf.dev/reference/protobuf/google.protobuf/#duration)` format) ``

Durée de la vidéo.

Durée en secondes avec neuf chiffres au maximum après la virgule et se terminant par "`s`". Exemple : `"3.5s"`

| Représentation JSON                                   |
| ----------------------------------------------------- |
| urltomarkdowncodeblockplaceholder30.14714751521074465 |

## État

États du cycle de vie d'un fichier.

- Enums: STATE_UNSPECIFIED
  - Valeur par défaut. Cette valeur est utilisée si l'état est omis.
- Enums: PROCESSING
  - Le fichier est en cours de traitement et ne peut pas encore être utilisé pour l'inférence.
- Enums: ACTIVE
  - Le fichier est traité et disponible pour l'inférence.
- Enums: FAILED
  - Échec du traitement du fichier.

## Source

| Enums              |                                                       |
| ------------------ | ----------------------------------------------------- |
| SOURCE_UNSPECIFIED | Utilisé si la source n'est pas spécifiée.             |
| UPLOADED           | Indique que le fichier est importé par l'utilisateur. |
| GENERATED          | Indique que le fichier est généré par Google.         |

## État

- [Représentation JSON](#SCHEMA_REPRESENTATION)

Le type `Status` définit un modèle d'erreur logique adapté aux différents environnements de programmation, y compris les API REST et RPC. Il est utilisé par le protocole [gRPC](https://github.com/grpc). Chaque message `Status` contient trois éléments de données : un code d'erreur, un message d'erreur et les détails de l'erreur.

Pour en savoir plus sur ce modèle d'erreur et sur son utilisation, consultez le [Guide de conception d'API](https://cloud.google.com/apis/design/errors?hl=fr).

Champs

`code` `integer`

Code d'état, qui doit être une valeur d'énumération de `google.rpc.Code`.

`message` `string`

Message d'erreur destiné au développeur, qui doit être en anglais. Tout message d'erreur destiné aux utilisateurs doit être localisé et envoyé dans le champ `[google.rpc.Status.details](https://ai.google.dev/api/files?hl=fr#FIELDS.details)`, ou localisé par le client.

`details[]` `object`

Liste de messages comportant les détails de l'erreur. Il existe un ensemble commun de types de message utilisable par les API.

Objet contenant des champs d'un type arbitraire. Un champ supplémentaire `"@type"` contient un URI identifiant le type. Exemple : `{ "id": 1234, "@type": "types.example.com/standard/id" }`.

| Représentation JSON                                  |
| ---------------------------------------------------- |
| urltomarkdowncodeblockplaceholder40.9510605368785843 |

Sauf indication contraire, le contenu de cette page est régi par une licence [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/), et les échantillons de code sont régis par une licence [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). Pour en savoir plus, consultez les [Règles du site Google Developers](https://developers.google.com/site-policies?hl=fr). Java est une marque déposée d'Oracle et/ou de ses sociétés affiliées.

Dernière mise à jour le 2025/06/12 (UTC).
