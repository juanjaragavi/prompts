# Document

<Context>

### Environment
* **Server:** Google Cloud Platform (GCP) Compute Engine VM
* **OS:** Ubuntu 22.04 LTS
* **Services:** Apache2 (configured as a reverse proxy), `pm2`

### Existing Project Template
An existing Next.js application (`uk.topfinanzas.com`) is deployed in `/var/www/html/uk` and managed by `pm2`. Its Apache configuration, `uk.topfinanzas.com.conf`, will be used as the template for a new project deployment.

This configuration handles HTTP to HTTPS redirection, SSL termination, static asset serving (`/_next/static`), WebSocket proxying, and reverse proxying to the Next.js application process.

### Template File: `uk.topfinanzas.com.conf`
```apache
<VirtualHost *:80>
    ServerName uk.topfinanzas.com
    ServerAdmin juan.jaramillo@topfinanzas.co
    
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

    RewriteEngine on
    RewriteCond %{SERVER_NAME} =uk.topfinanzas.com
    RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
</VirtualHost>

<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName uk.topfinanzas.com
    ServerAdmin juan.jaramillo@topfinanzas.co

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

    ProxyRequests Off
    ProxyPreserveHost On

    # Next.js static files handling
    Alias "/_next/static" "/var/www/html/uk/.next/static"
    <Directory "/var/www/html/uk/.next/static">
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
        
        # Set correct MIME types for Next.js static files
        AddType application/javascript .js
        AddType text/css .css
        AddType application/json .json
        AddType image/svg+xml .svg
        AddType image/png .png
        AddType image/jpeg .jpg .jpeg
        AddType image/gif .gif
        AddType application/font-woff .woff
        AddType application/font-woff2 .woff2
    </Directory>

    # Next.js application proxy for all other paths
    ProxyPass /_next/static !
    ProxyPass / http://localhost:3004/
    ProxyPassReverse / http://localhost:3004/

    # WebSocket support for Next.js
    RewriteEngine On
    RewriteCond %{HTTP:Upgrade} websocket [NC]
    RewriteCond %{HTTP:Connection} upgrade [NC]
    RewriteRule ^/?(.*) "ws://localhost:3004/$1" [P,L]

    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set X-XSS-Protection "1; mode=block"

    Include /etc/letsencrypt/options-ssl-apache.conf
    SSLCertificateFile /etc/letsencrypt/live/[uk.topfinanzas.com/fullchain.pem](https://uk.topfinanzas.com/fullchain.pem)
    SSLCertificateKeyFile /etc/letsencrypt/live/[uk.topfinanzas.com/privkey.pem](https://uk.topfinanzas.com/privkey.pem)
</VirtualHost>
</IfModule>
````

</Context>

<Task>

### Objective

Configure and deploy a new Next.js project (`kardtrust.com`) on the same server by creating a new Apache virtual host based on the provided `uk.topfinanzas.com.conf` template.

### New Project Specifications

  * **Installation Directory:** `/var/www/html/kardtrust`
  * **Application Port:** `3006` (The application will run on `http://localhost:3006`)
  * **Domain:** `kardtrust.com` (The DNS A record already points to the virtual machine's IP address)

### Requirements

1.  **Apache Configuration:** Create a new virtual host file for `kardtrust.com`, adapting the template. All references to `uk.topfinanzas.com`, `/var/www/html/uk`, and port `3004` must be updated to match the new project's specifications.
2.  **Process Management:** Configure `pm2` to manage the new Next.js application from its directory (`/var/www/html/kardtrust`), ensuring it runs persistently and restarts on server reboot.
3.  **SSL Provisioning:** Install a new Let’s Encrypt SSL certificate for the `kardtrust.com` domain and update the new virtual host configuration to use the certificate files.

</Task>