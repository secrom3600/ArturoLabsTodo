#!/bin/bash

echo "Levantando Backend..."
cd ArturoLabs---Backend || exit
docker compose up --build -d

cd ..
echo "Levantando Frontend..."
cd ArturoLabs---Frontend || exit
docker compose up --build -d

cd ..
echo "Todo levantado correctamente."