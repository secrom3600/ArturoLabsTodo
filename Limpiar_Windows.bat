@echo off
echo Apagando Backend...
cd ArturoLabs---Backend
docker compose down

cd ..
echo Apagando Frontend...
cd ArturoLabs---Frontend
docker compose down

cd ..
echo Todo apagado y limpio.
pause