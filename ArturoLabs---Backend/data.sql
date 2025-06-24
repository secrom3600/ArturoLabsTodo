-- Script para crear la base de datos CN

  
-- Usar la base de datos CN

-- Tabla Tutor
CREATE TABLE IF NOT EXISTS tutor (
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

-- Tabla nino
CREATE TABLE IF NOT EXISTS nino (
    CI INT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    Fec_Nac DATE NOT NULL,
    sexo CHAR(1) NOT NULL,
    nacionalidad VARCHAR(100) NOT NULL,
    TutorCI INT NOT NULL,
    TutorDosCI INT NULL,
    edad INT,
    FOREIGN KEY (TutorCI) REFERENCES Tutor(CI),
    FOREIGN KEY (TutorDosCI) REFERENCES Tutor(CI)
);




---------------------------------------------------------------------------------trigger
-- Función para actualizar edad antes de INSERT o UPDATE
CREATE OR REPLACE FUNCTION actualizar_edad() RETURNS trigger AS $$
BEGIN
  NEW.edad := EXTRACT(YEAR FROM age(current_date, NEW.Fec_Nac));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que llama a la función antes de insertar o actualizar en nino
CREATE TRIGGER trg_actualizar_edad
BEFORE INSERT OR UPDATE ON nino
FOR EACH ROW
EXECUTE FUNCTION actualizar_edad();
-----------------------------------------------------------------------------------






CREATE TABLE IF NOT EXISTS autenticacion (
    id SERIAL PRIMARY KEY,
    Tutor_CI INT UNIQUE NOT NULL,
    Contrasenia VARCHAR(255) NOT NULL,
    fec_set DATE DEFAULT CURRENT_DATE,
    fec_cad DATE DEFAULT (CURRENT_DATE + INTERVAL '5 years'),
    
    -- Campos requeridos por Django
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP,

    FOREIGN KEY (Tutor_CI) REFERENCES Tutor(CI)
);

CREATE TABLE if not exists control_medico (
    ci INT NOT NULL,
    fecha DATE NOT NULL,
    edad SMALLINT NOT NULL,       
    peso DECIMAL(4, 1) NOT NULL,  
    talla DECIMAL(4, 1) NOT NULL, 
    PC BOOLEAN DEFAULT FALSE NOT NULL,
    PPL BOOLEAN DEFAULT FALSE NOT NULL,
    Complemento BOOLEAN DEFAULT FALSE NOT NULL,
    Hierro BOOLEAN DEFAULT FALSE NOT NULL,
    Vitamina_D BOOLEAN DEFAULT FALSE NOT NULL,
    cc DECIMAL(4, 1),    
    pas SMALLINT,        
    pad SMALLINT,
    PRIMARY KEY (ci, fecha),
    FOREIGN KEY (ci) REFERENCES nino(CI)
);

-- Tabla Responsable (Tabla de unión para la relación N:M entre Tutor y nino)


-- Constraints CHECK para fechas razonables (ejemplo básico)
ALTER TABLE Tutor
ADD CONSTRAINT CHK_Tutor_FecNac CHECK (Fec_Nac <= CURRENT_DATE);

ALTER TABLE nino
ADD CONSTRAINT CHK_nino_FecNac CHECK (Fec_Nac <= CURRENT_DATE);

ALTER TABLE autenticacion
ADD CONSTRAINT CHK_Contraseña_FecSet CHECK (fec_set <= CURRENT_TIMESTAMP);

ALTER TABLE autenticacion
ADD CONSTRAINT CHK_Contraseña_FecCad CHECK (fec_cad >= fec_set OR fec_cad IS NULL);

----Insertar 5 tutores de prueba
INSERT INTO Tutor (CI, Nombre, Apellido, Nacionalidad, Fec_Nac, sexo, Calle, num_puer, Localidad, email, Telefono)
VALUES
    (23481930, 'Luis', 'Suárez', 'Uruguaya', '1980-02-10', 'M', '18 de julio', '1895', 'Montevideo', 'luis.suarez@gmail.com', '099003456'),
    (29837465, 'Ana', 'Martínez', 'Uruguaya', '1979-07-22', 'F', 'Bulevar Artigas', '1203', 'Montevideo', 'ana.martinez@gmail.com', '098765432'),
    (31248795, 'Carlos', 'Pereira', 'Uruguaya', '1978-11-05', 'M', 'Rivera', '875', 'Salto', 'carlos.Pereira@gmail.com', '091234567'),
    (28765432, 'María', 'Pérez', 'Uruguaya', '1984-04-18', 'F', 'Avenida Italia', '456', 'Canelones', 'maria.perez@gmail.com', '092345678'),
    (35678921, 'Jorge', 'Fernández', 'Uruguaya', '1976-09-30', 'M', 'General Flores', '1020', 'Maldonado', 'jorge.fernandez@gmail.com', '093456789')
ON CONFLICT (CI) DO NOTHING;


---Asignar contraseñas
INSERT INTO autenticacion (Tutor_CI, Contrasenia, fec_set, fec_cad)
VALUES
    (23481930, 'LUIS1', '2025-04-29', '2026-04-29'),
    (29837465, 'Ana23', '2025-01-01', '2025-06-15'),
    (31248795, 'Carloss556', '2020-01-01', '2027-06-15' ),
    (28765432, 'María667', '2017-10-01', '2026-10-01'),
    (35678921, 'Jorge', '2022-10-01', '2027-10-01')
ON CONFLICT (Tutor_CI) DO NOTHING;      


----inserter 5 ninos de prueba

INSERT INTO nino (CI, Nombre, Apellido, Fec_Nac, sexo, nacionalidad, TutorCI, TutorDosCI)
VALUES
  -- Los 5 originales
  (52345678, 'Martina', 'Suárez', '2020-04-15', 'F', 'Uruguaya', 23481930, 29837465),
  (58912345, 'Benjamín', 'López', '2018-11-07', 'M', 'Uruguaya', 31248795, NULL),
  (61234567, 'Sofía', 'Pereira', '2019-06-21', 'F', 'Uruguaya', 29837465, 35678921),
  (63456789, 'Thiago', 'Dias', '2017-02-03', 'M', 'Uruguaya', 28765432, NULL),
  (65478901, 'Isabella', 'Fernández', '2022-09-29', 'F', 'Uruguaya', 35678921, 31248795),

  -- Hijos adicionales para que cada tutor tenga entre 2 y 5 niños
  (70000001, 'Lucas', 'Suárez', '2021-06-10', 'M', 'Uruguaya', 23481930, NULL),
  (70000002, 'Emma', 'Suárez', '2019-12-20', 'F', 'Uruguaya', 23481930, 29837465),
  (70000003, 'Joaquín', 'Suárez', '2022-07-08', 'M', 'Uruguaya', 23481930, NULL),

  (70000004, 'Valentina', 'Martínez', '2017-03-25', 'F', 'Uruguaya', 29837465, 35678921),
  (70000005, 'Agustín', 'Martínez', '2020-08-09', 'M', 'Uruguaya', 29837465, NULL),

  (70000006, 'Camila', 'Pereira', '2022-05-12', 'F', 'Uruguaya', 31248795, NULL),
  (70000007, 'Santiago', 'Pereira', '2015-10-01', 'M', 'Uruguaya', 31248795, NULL),

  (70000008, 'Bruno', 'Fernández', '2021-01-05', 'M', 'Uruguaya', 35678921, 28765432),
  (70000009, 'Florencia', 'Fernández', '2018-04-21', 'F', 'Uruguaya', 35678921, NULL),

  (70000010, 'Natalia', 'Pérez', '2020-11-19', 'F', 'Uruguaya', 28765432, NULL)
ON CONFLICT (CI) DO NOTHING;



INSERT INTO control_medico (ci, fecha, edad, peso, talla, PC, PPL, Complemento, Hierro, Vitamina_D, cc, pas, pad)
VALUES
-- CI: 52345678 (Martina - nacida 2020-04-15)
(52345678, '2025-04-15', 60, 17.0, 103.0, TRUE, TRUE, TRUE, TRUE, TRUE, 51.0, 102, 66),
(52345678, '2026-04-15', 72, 19.0, 108.2, TRUE, TRUE, TRUE, TRUE, TRUE, 52.5, 105, 68),

-- CI: 58912345 (Benjamín - nac. 2018-11-07)
(58912345, '2024-11-07', 72, 21.0, 110.0, TRUE, FALSE, TRUE, TRUE, FALSE, 53.0, 104, 69),
(58912345, '2025-11-07', 84, 23.0, 114.0, TRUE, FALSE, TRUE, TRUE, FALSE, 55.0, 106, 70),

-- CI: 61234567 (Sofía - nac. 2019-06-21)
(61234567, '2024-06-21', 60, 18.5, 105.0, TRUE, TRUE, TRUE, TRUE, TRUE, 52.0, 100, 68),
(61234567, '2025-06-21', 72, 20.0, 109.0, TRUE, TRUE, TRUE, TRUE, TRUE, 53.5, 104, 70),

-- CI: 63456789 (Thiago - nac. 2017-02-03)
(63456789, '2023-02-03', 72, 22.5, 111.0, TRUE, FALSE, FALSE, TRUE, FALSE, 53.5, 105, 70),
(63456789, '2025-02-03', 96, 26.0, 118.0, TRUE, FALSE, FALSE, TRUE, FALSE, 56.0, 110, 75)

-- CI: 65478901 (Isabella - nac. 2022-09-29) — todavía no cumple 5 años en 2025, se excluye por ahora
-- Alternativamente, podés dejarla sin controles o con uno futuro:
-- (65478901, '2027-09-29', 60, 17.0, 103.0, TRUE, TRUE, TRUE, TRUE, TRUE, 51.0, 100, 65)

-- Si querés mantener consistencia, podés dejarle uno:
--(65478901, '2027-09-29', 60, 17.0, 103.0, TRUE, TRUE, TRUE, TRUE, TRUE, 51.0, 100, 65)
ON CONFLICT (ci, fecha) DO NOTHING;