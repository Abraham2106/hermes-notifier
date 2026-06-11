# Hermes Notifier - Monitor de Gmail Multi-Keyword

Revisa periodicamente tu cuenta de Gmail buscando correos que contengan cualquiera de los terminos que elijas y te avisa por Telegram cuando llega uno nuevo.

Puedes monitorear tantas palabras o frases como quieras (ej. "oferta de trabajo", "notificacion urgente", "alerta de servidor", etc.).

Para ver los diagramas UML detallados de la estructura y flujo de ejecucion del proyecto, consulta el archivo [ARCHITECTURE.md](file:///c:/Users/solan/Documents/Personal/Automatas/hermes-notifier/ARCHITECTURE.md).

---

## 1. Crear credenciales de Google (una sola vez)

1. Ve a https://console.cloud.google.com/ y crea un proyecto.
2. Activa la Gmail API (menu "APIs y servicios" -> "Biblioteca" -> busca "Gmail API" -> habilitar).
3. Configura la pantalla de consentimiento OAuth (tipo "Externo", agregando tu correo como usuario de prueba).
4. Crea credenciales: "APIs y servicios" -> "Credenciales" -> "Crear credenciales" -> "ID de cliente de OAuth" -> tipo "Aplicacion de escritorio".
5. Copia el client_id y client_secret.

---

## 2. Obtener el refresh token (una sola vez)

1. Rellena las variables `GMAIL_CLIENT_ID` y `GMAIL_CLIENT_SECRET` en tu archivo `.env` (puedes copiar el archivo `.env.example` como plantilla).
2. Ejecuta el script de configuracion:
   ```bash
   setup.bat
   ```
3. Ejecuta el script para obtener el token:
   ```bash
   get_refresh_token.bat
   ```
4. Se abrira tu navegador para iniciar sesion y autorizar la lectura de Gmail. El script guardara de forma automatica y segura tu `GMAIL_REFRESH_TOKEN` en tu archivo `.env` sin imprimirlo en la terminal.


---

## 3. Configurar bot de Telegram

1. En Telegram, habla con @BotFather, envia el comando `/newbot` y sigue los pasos para obtener tu `TELEGRAM_BOT_TOKEN`.
2. Escribe cualquier mensaje a tu nuevo bot.
3. Visita en tu navegador:
   `https://api.telegram.org/bot<TU_TOKEN>/getUpdates`
   y busca el campo `"chat":{"id": ...}` para obtener tu `TELEGRAM_CHAT_ID`.

---

## 4. Definir palabras clave

La variable de entorno `GMAIL_KEYWORDS` acepta una lista de terminos separados por comas. El bot monitoreara cada uno de forma independiente.

Ejemplos:

| Caso de Uso | Valor de GMAIL_KEYWORDS |
|---|---|
| Buscar avisos del trabajo | `oferta, empleo, contratacion` |
| Monitoreo de servidores | `error 500, caida de servicio, database failure` |
| Alertas por asunto | `subject:urgente, subject:alerta` |

---

## 5. Guia para subir a Railway

Sigue estos pasos para desplegar el bot en Railway y mantenerlo ejecutandose de manera continua:

### Paso 5.1 - Inicializar Repositorio y Subir a GitHub
Abre una terminal en el directorio del proyecto y ejecuta los siguientes comandos:
```bash
git init
git add .
git commit -m "Despliegue inicial de Hermes Notifier"
```
Crea un repositorio vacio en tu cuenta de GitHub (ej. `hermes-notifier`) y sube el codigo:
```bash
git remote add origin https://github.com/TU_USUARIO/hermes-notifier.git
git branch -M main
git push -u origin main
```

### Paso 5.2 - Desplegar en Railway
1. Ingresa a https://railway.app/ e inicia sesion con tu cuenta de GitHub.
2. Haz clic en "New Project" -> "Deploy from GitHub repo".
3. Selecciona tu repositorio `hermes-notifier`.

### Paso 5.3 - Configurar Variables de Entorno en Railway
En la seccion de variables (Variables) del servicio creado en Railway, agrega los siguientes campos:

| Variable | Valor |
|---|---|
| `GMAIL_CLIENT_ID` | Tu ID de cliente de Google Cloud |
| `GMAIL_CLIENT_SECRET` | Tu Secreto de cliente de Google Cloud |
| `GMAIL_REFRESH_TOKEN` | Tu Refresh Token obtenido en el paso 2 |
| `TELEGRAM_BOT_TOKEN` | El token entregado por BotFather |
| `TELEGRAM_CHAT_ID` | Tu Chat ID de Telegram |
| `GMAIL_KEYWORDS` | Lista de palabras clave separadas por comas |
| `POLL_INTERVAL_SECONDS` | Intervalo de revision (ej. 120) |

### Paso 5.4 - Agregar Volumen para Persistencia
Para evitar que el bot repita notificaciones cuando el contenedor de Railway se reinicie:
1. En tu proyecto de Railway, haz clic en "Add a service" -> "Volume".
2. Configura el Mount Path en: `/data`
3. El bot guardara de forma automatica el historial de correos vistos en esta ruta.

---

## 6. Buenas Prácticas de Seguridad

Para garantizar el correcto funcionamiento y proteger tus credenciales, sigue estas recomendaciones:

- **Protección del archivo `.env`**: Este archivo contiene credenciales extremadamente sensibles (secreto de cliente de Google y tokens de Telegram). Nunca lo agregues al control de versiones (Git). El archivo ya se encuentra incluido en el `.gitignore`.
- **Rotación de tokens**: Se recomienda rotar tus credenciales de Google y el token del bot de Telegram periódicamente o de forma inmediata si sospechas que han sido expuestos.
- **Acceso exclusivo al volumen en Railway**: Si despliegas en Railway, asegúrate de restringir el acceso a tu proyecto únicamente a personal autorizado, ya que el volumen almacena el historial de identificadores procesados.
- **Minimización de permisos**: Al configurar tus credenciales en Google Cloud Console, asegúrate de utilizar únicamente el alcance `gmail.readonly` para restringir el acceso a sólo lectura de correos.
- **Validación automática**: El sistema realiza comprobaciones en el inicio para evitar la ejecución con credenciales por defecto/placeholders y limita los tiempos de consulta (`POLL_INTERVAL_SECONDS >= 10`) para prevenir bloqueos por Rate Limit.

---

## Ejecución Local

Si deseas correrlo localmente para realizar pruebas:
```bash
start.bat
```

