# Prompt

We are currently working on the WordPress CMS UI for Actualoft's website, Actualoft.com. Our client has two specific requests.

First, they need an LLM-powered chatbot agent plugin with BYOK functionality. The plugin must accept Google AI Studio API keys that start with "AIza..." The instructions or system prompt must be updatable, and the plugin must have a WhatsApp integration feature. The plugin must be free or updated via a paid subscription. The basic set of instructions is below:

```markdown ACTUALOFT-assistant-system-prompt
<!-- ACTUALOFT-assistant-system-prompt.md -->

Eres el asistente virtual de Actualoft, una empresa colombiana especializada en la fabricación y comercialización de muebles de madera para el hogar con sede en Bogotá. Tu nombre es "Loft".

Tu misión es ayudar a los clientes con:

- Información sobre los productos disponibles: alcobas, comedores, salas modulares, chaise longue, muebles auxiliares y más.
- Consultas sobre precios, materiales y disponibilidad.
- Asesoría en diseño y decoración de interiores.
- Información sobre puntos de venta y entrega inmediata en Bogotá.
- Agendar citas o derivar al equipo comercial.

Tono: Amable, profesional y cercano. Habla siempre en español colombiano. Usa un lenguaje cálido pero formal.

Normas importantes:

- Si no sabes la respuesta exacta, invita al cliente a contactar directamente a Actualoft.
- No inventes precios ni disponibilidad de productos.
- Siempre finaliza ofreciendo ayuda adicional.
- Fecha y hora actual: {DATE_TIME}.
```

Second, analyze the current structure of the products' location and organization in this instance of the WordPress CMS configured for Actualoft. We saw that the products are located on the blogs, but we need to identify any additional configurations or plugins that generate shortcodes to display products.

This research is necessary because our client's second requirement is a plugin that replaces the WordPress dashboard with a screen showing "aliases" or "direct access" to the two functionalities the client will use most: product listings and chatbot configuration and instructions. The plugin will display links to the settings of other plugins on the initial WordPress screen.

Your task is to find, install, activate, and fully configure the two required plugins. The client's goal is to have a chatbot agent on the front end of the Actualoft.com website to serve client requests. When he logs in, he wants to see the options he uses most on the first screen of the Actualoft.com CMS WP Admin main dashboard.

Lastly, research the entire WordPress CMS area as well as the Actualoft front-end UI. Look for additional information about the company and its products, primarily luxury furniture, to complete the 'Loft' system prompt. 'Loft' is an LLM-based agent that will address the needs of leads and page visitors.
