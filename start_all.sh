dame todo esto para bat
#!/bin/bash

# Ir a Frontend y levantar docker-compose
echo "Starting Frontend..."
cd ArturoLabs---Frontend/portal_gestion_carne || { echo "Frontend folder not found!"; exit 1; }
docker-compose up -d

# Volver a la carpeta base
cd ../../../

# Ir a Backend y levantar docker-compose
echo "Starting Backend..."
cd ArturoLabs---Backend || { echo "Backend folder not found!"; exit 1; }
docker-compose up -d

# Volver a la carpeta base
cd ../

echo "Both Frontend and Backend started!"

pause