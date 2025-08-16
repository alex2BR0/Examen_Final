# Usar imagen base de nginx
FROM nginx:alpine

# Copiar archivos estáticos
COPY . /usr/share/nginx/html/

# Copiar configuración personalizada de nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Exponer puerto
EXPOSE 3000

# Comando para ejecutar nginx
CMD ["nginx", "-g", "daemon off;"]
