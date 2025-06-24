@echo off
echo Levantando Backend...
cd ArturoLabs---Backend
docker compose up --build -d

cd ..
echo Levantando Frontend...
cd ArturoLabs---Frontend
docker compose up --build -d

cd ..
echo Todo levantado correctamente.
pause