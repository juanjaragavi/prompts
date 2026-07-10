import urllib.request
import urllib.parse
import json
import base64
import email
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def refresh_token():
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
    refresh_token_value = os.environ.get('GOOGLE_REFRESH_TOKEN')
    if not client_id or not client_secret or not refresh_token_value:
        raise RuntimeError(
            'Missing required env vars: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN'
        )

    url = 'https://oauth2.googleapis.com/token'
    data = urllib.parse.urlencode({
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token_value,
        'grant_type': 'refresh_token'
    }).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST')
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        return res['access_token']

def send_email(access_token):
    msg = MIMEMultipart()
    msg['to'] = 'iban@jonhernandez.education'
    msg['from'] = 'juanamillo@gmail.com'
    msg['subject'] = 'Candidatura: Programador/a con enfoque Vibe Coding (IA) - Juan Miguel Jaramillo Gaviria'

    email_body = """Estimado Equipo de Selección,

Les escribo con gran entusiasmo para presentar mi candidatura al puesto de Programador/a con enfoque Vibe Coding (IA). Con más de 17 años de trayectoria en desarrollo web y diseño UI/UX, y tras haber dedicado los últimos 4 años de forma exclusiva a la Inteligencia Artificial Generativa y flujos de desarrollo ágiles asistidos por IA, considero que mi perfil se alinea perfectamente con su búsqueda de un programador rápido, creativo y con un excelente criterio visual.

Aunque actualmente resido en Bogotá, Colombia, mi pasión por la cultura y el ecosistema tecnológico de Barcelona es inmensa. Estoy plenamente abierto a discutir opciones de reubicación, estancias presenciales o un esquema que nos permita colaborar con el máximo nivel de compromiso y efectividad.

A continuación, detallo cómo mi experiencia responde directamente a sus requisitos:

- Desarrollo Web de Alta Velocidad (Vibe Coding): Mi flujo diario de trabajo está completamente automatizado y potenciado por herramientas como Cursor, Claude Sonnet, Bolt AI y v0.dev. Utilizo la IA no solo como un asistente de autocompletado, sino como un socio de co-creación que me permite diseñar y desarrollar landings, plataformas web y MVP completos en tiempo récord.
- Excelente Criterio Visual y de Negocio: Como cofundador y ex Director de Operaciones de la agencia digital FreshWorks (con operaciones en España, México y Colombia), he diseñado y liderado proyectos de alto impacto visual para marcas de renombre. Cuento con un sólido trasfondo en UI/UX, lo que me permite asegurar que el código generado por IA no solo funcione técnicamente, sino que mantenga una estética moderna, limpia y enfocada en la conversión.
- Dominio Técnico de Frameworks Modernos: Trabajo fluidamente en todo el stack web: HTML, CSS (incluyendo Tailwind CSS v4), JavaScript/TypeScript, React 19 y Next.js 15/16 (App Router). En mi rol reciente como AI Development Lead en TopNetworks Inc., diseñé e implementé un ecosistema SaaS completo (incluyendo Social Media Genius, un editor de contenido social con un canvas interactivo, y EmailGenius, un generador de correos con Vertex AI).
- Envío de Ejemplos de Proyectos Vibe Coding: Me encantaría programar una videollamada para compartirles mi pantalla y mostrarles en vivo herramientas complejas que he desarrollado en modalidad "vibe coding", demostrando mi velocidad de ejecución y toma de decisiones en tiempo real.

Adjunto mi currículum y portafolio para su consideración. Me encantaría disponer de 20 minutos para conversar sobre cómo mi enfoque AI-native puede acelerar la entrega de sus proyectos web y landings en Inteligencia Artificial.

Atentamente,

Juan Miguel Jaramillo Gaviria
info@juanjaramillo.tech | (+57) 305 420 6139
https://juanjaramillo.tech
https://www.linkedin.com/in/juan-jaramillo-ai/
https://github.com/juanjaragavi
"""
    msg.attach(MIMEText(email_body, 'plain'))

    # Attach resume PDF
    resume_path = '/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/Juan_Jaramillo_Resume_Vibe_Coding.pdf'
    with open(resume_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="Juan_Jaramillo_Resume_Vibe_Coding.pdf"')
        msg.attach(part)

    # Base64url encode the message
    raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')

    # Send message using Gmail API
    send_url = 'https://gmail.googleapis.com/gmail/v1/users/me/messages/send'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    req_data = json.dumps({'raw': raw_message}).encode('utf-8')
    req = urllib.request.Request(send_url, data=req_data, headers=headers, method='POST')
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

if __name__ == '__main__':
    print("Refreshing access token...")
    token = refresh_token()
    print("Sending application email...")
    result = send_email(token)
    print("Email sent successfully!")
    print(json.dumps(result, indent=2))
