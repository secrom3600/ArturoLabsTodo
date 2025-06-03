-- Script para crear la base de datos CN

  
-- Usar la base de datos CN
\c ArturoLabsDB

-- Tabla Tutor
CREATE TABLE IF NOT EXISTS Tutor (
    CI INT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    Nacionalidad VARCHAR(100) NOT NULL,
    Fec_Nac DATE NOT NULL,
    sexo CHAR(1) NOT NULL,
    Calle VARCHAR(100),
    num_puer VARCHAR(10),
    Localidad VARCHAR(100),
    email VARCHAR(100),
    Telefono VARCHAR(20),
    OAuth BOOLEAN,
    codigo_2fa VARCHAR(100),
    verificado BOOLEAN DEFAULT FALSE

);

-- Tabla Niño
CREATE TABLE IF NOT EXISTS Niño (
    CI INT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    Fec_Nac DATE NOT NULL,
    sexo CHAR(1) NOT NULL,
    nacionalidad VARCHAR(100) NOT NULL,
    TutorCI INT NOT NULL,
    tutordosci INT NULL,

    FOREIGN KEY (TutorCI) REFERENCES Tutor(CI),
    FOREIGN KEY (TutorDosCI) REFERENCES Tutor(CI)
);

CREATE TABLE IF NOT EXISTS autenticacion (
    Tutor_CI INT PRIMARY KEY,
    Contrasenia VARCHAR(255) NOT NULL,
    fec_set DATE DEFAULT CURRENT_DATE,
    fec_cad DATE DEFAULT (CURRENT_DATE + INTERVAL '5 years'),
    FOREIGN KEY (Tutor_CI) REFERENCES Tutor(CI)
);

-- Tabla Responsable (Tabla de unión para la relación N:M entre Tutor y Niño)


-- Constraints CHECK para fechas razonables (ejemplo básico)
ALTER TABLE Tutor
ADD CONSTRAINT CHK_Tutor_FecNac CHECK (Fec_Nac <= CURRENT_DATE);

ALTER TABLE Niño
ADD CONSTRAINT CHK_Niño_FecNac CHECK (Fec_Nac <= CURRENT_DATE);

ALTER TABLE autenticacion
ADD CONSTRAINT CHK_Contraseña_FecSet CHECK (fec_set <= CURRENT_TIMESTAMP);

ALTER TABLE autenticacion
ADD CONSTRAINT CHK_Contraseña_FecCad CHECK (fec_cad >= fec_set OR fec_cad IS NULL);

----Insertar 5 tutores de prueba
INSERT INTO Tutor (CI, Nombre, Apellido, Nacionalidad, Fec_Nac, sexo, Calle, num_puer, Localidad, email, Telefono)
VALUES
    ('23481930', 'Luis', 'Suárez', 'Uruguaya', '1980-02-10', 'M', '18 de julio', '1895', 'Montevideo', 'luis.suarez@gmail.com', '099003456'),
    ('29837465', 'Ana', 'Martínez', 'Uruguaya', '1979-07-22', 'F', 'Bulevar Artigas', '1203', 'Montevideo', 'ana.martinez@gmail.com', '098765432'),
    ('31248795', 'Carlos', 'Pereira', 'Uruguaya', '1978-11-05', 'M', 'Rivera', '875', 'Salto', 'carlos.Pereira@gmail.com', '091234567'),
    ('28765432', 'María', 'Pérez', 'Uruguaya', '1984-04-18', 'F', 'Avenida Italia', '456', 'Canelones', 'maria.perez@gmail.com', '092345678'),
    ('35678921', 'Jorge', 'Fernández', 'Uruguaya', '1976-09-30', 'M', 'General Flores', '1020', 'Maldonado', 'jorge.fernandez@gmail.com', '093456789')
ON CONFLICT (CI) DO NOTHING;


---Asignar contraseñas
INSERT INTO autenticacion (Tutor_CI, Contrasenia, fec_set, fec_cad)
VALUES
    ('23481930', 'LUIS1', '2025-04-29', '2026-04-29'),
    ('29837465', 'Ana23', '2025-01-01', '2025-06-15'),
    ('31248795', 'Carloss556', '2020-01-01', '2027-06-15' ),
    ('28765432', 'María667', '2017-10-01', '2026-10-01'),
    ('35678921', 'Jorge', '2022-10-01', '2027-10-01')
ON CONFLICT (Tutor_CI) DO NOTHING;      


----inserter 5 niños de prueba

INSERT INTO Niño (CI, Nombre, Apellido, Fec_Nac, sexo, nacionalidad, TutorCI, TutorDosCI)
VALUES
  ('52345678', 'Martina', 'Suárez', '2020-04-15', 'F', 'Uruguaya', 23481930, 29837465),
  ('58912345', 'Benjamín', 'López', '2018-11-07', 'M', 'Uruguaya', 31248795, NULL),
  ('61234567', 'Sofía', 'Pereira', '2019-06-21', 'F', 'Uruguaya', 29837465, 35678921),
  ('63456789', 'Thiago', 'Dias', '2017-02-03', 'M', 'Uruguaya', 28765432, NULL),
  ('65478901', 'Isabella', 'Fernández', '2022-09-29', 'F', 'Uruguaya', 35678921, 31248795)
ON CONFLICT (CI) DO NOTHING;


