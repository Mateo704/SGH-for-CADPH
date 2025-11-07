-- ========================================
-- BASE DE DATOS DE GESTIÓN ACADÉMICA
-- Versión corregida y normalizada
-- Compatible con MySQL Workbench
-- ========================================

CREATE DATABASE IF NOT EXISTS sghsena;
USE sghsena;

-- ========================================
-- TABLA DE ROLES Y USUARIOS
-- ========================================

CREATE TABLE Roles (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL
);

CREATE TABLE Usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo_documento VARCHAR(20),
    numero_documento VARCHAR(20) UNIQUE,
    especialidad VARCHAR(100),
    id_rol INT,
    FOREIGN KEY (id_rol) REFERENCES Roles(id_rol)
);

-- ========================================
-- TABLAS DE CONTRATOS
-- ========================================

CREATE TABLE Contratos (
    id_contrato INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    tipo_contrato VARCHAR(50),
    horas_por_cumplir INT DEFAULT 0,
    fecha_inicio DATE,
    fecha_fin DATE,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);

-- ========================================
-- TABLAS DE PROGRAMAS, FICHAS Y COMPETENCIAS
-- ========================================

CREATE TABLE Programas (
    id_programa INT AUTO_INCREMENT PRIMARY KEY,
    nombre_programa VARCHAR(150) NOT NULL
);

CREATE TABLE Fichas (
    id_ficha INT AUTO_INCREMENT PRIMARY KEY,
    nombre_ficha VARCHAR(100),
    id_programa INT NOT NULL,
    id_instructor_lider INT,
    FOREIGN KEY (id_programa) REFERENCES Programas(id_programa),
    FOREIGN KEY (id_instructor_lider) REFERENCES Usuarios(id_usuario)
);

CREATE TABLE Competencias (
    id_competencia INT AUTO_INCREMENT PRIMARY KEY,
    nombre_competencia VARCHAR(150) NOT NULL,
    especialidad VARCHAR(100)
);

CREATE TABLE Ficha_Competencia (
    id_ficha INT,
    id_competencia INT,
    PRIMARY KEY (id_ficha, id_competencia),
    FOREIGN KEY (id_ficha) REFERENCES Fichas(id_ficha),
    FOREIGN KEY (id_competencia) REFERENCES Competencias(id_competencia)
);

CREATE TABLE Resultados_Aprendizaje (
    id_resultado INT AUTO_INCREMENT PRIMARY KEY,
    nombre_resultado VARCHAR(200) NOT NULL,
    id_competencia INT NOT NULL,
    FOREIGN KEY (id_competencia) REFERENCES Competencias(id_competencia)
);

-- ========================================
-- TABLAS DE JORNADAS, AMBIENTES Y HORARIOS
-- ========================================

CREATE TABLE Jornadas (
    id_jornada INT AUTO_INCREMENT PRIMARY KEY,
    nombre_jornada VARCHAR(50) NOT NULL,
    hora_inicio TIME,
    hora_fin TIME
);

CREATE TABLE Ambientes (
    id_ambiente INT AUTO_INCREMENT PRIMARY KEY,
    nombre_ambiente VARCHAR(100) NOT NULL
);

CREATE TABLE Horarios (
    id_horario INT AUTO_INCREMENT PRIMARY KEY,
    id_ficha INT NOT NULL,
    id_instructor INT NOT NULL,
    id_ambiente INT NOT NULL,
    id_jornada INT NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    FOREIGN KEY (id_ficha) REFERENCES Fichas(id_ficha),
    FOREIGN KEY (id_instructor) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_ambiente) REFERENCES Ambientes(id_ambiente),
    FOREIGN KEY (id_jornada) REFERENCES Jornadas(id_jornada)
);

-- ========================================
-- REGISTRO DE HORAS CUMPLIDAS POR INSTRUCTOR
-- ========================================

CREATE TABLE Horas_Cumplidas (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    id_instructor INT NOT NULL,
    id_ficha INT NOT NULL,
    id_ambiente INT NOT NULL,
    horas_cumplidas INT DEFAULT 0,
    fecha DATE NOT NULL,
    FOREIGN KEY (id_instructor) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_ficha) REFERENCES Fichas(id_ficha),
    FOREIGN KEY (id_ambiente) REFERENCES Ambientes(id_ambiente)
);

-- ========================================
-- SISTEMA DE PERMISOS (opcional)
-- ========================================

CREATE TABLE Permisos (
    id_permiso INT AUTO_INCREMENT PRIMARY KEY,
    nombre_permiso VARCHAR(100) NOT NULL
);

CREATE TABLE Roles_Permisos (
    id_rol INT,
    id_permiso INT,
    PRIMARY KEY (id_rol, id_permiso),
    FOREIGN KEY (id_rol) REFERENCES Roles(id_rol),
    FOREIGN KEY (id_permiso) REFERENCES Permisos(id_permiso)
);

-- ========================================
-- DATOS INICIALES
-- ========================================

INSERT INTO Roles (nombre_rol) VALUES 
('Instructor'),
('Coordinador'),
('Root');

INSERT INTO Jornadas (nombre_jornada, hora_inicio, hora_fin) VALUES
('Mañana', '06:00:00', '12:00:00'),
('Tarde', '12:00:00', '18:00:00'),
('Noche', '18:00:00', '22:00:00');




--Datos de Prueva:
-- ========================================
-- USUARIOS (INSTRUCTORES Y COORDINADORES)
-- ========================================

INSERT INTO Usuarios (nombre, tipo_documento, numero_documento, especialidad, id_rol) VALUES
('Carlos López', 'CC', '10203040', 'Sistemas', 1),
('María Torres', 'CC', '10203041', 'Electricidad', 1),
('Andrés Gómez', 'CC', '10203042', 'Electrónica', 1),
('Laura Ramírez', 'CC', '10203043', 'Gestión Empresarial', 2),
('Admin Root', 'CC', '10000000', 'Administrador', 3);

-- ========================================
-- CONTRATOS DE INSTRUCTORES
-- ========================================

INSERT INTO Contratos (id_usuario, tipo_contrato, horas_por_cumplir, fecha_inicio, fecha_fin) VALUES
(1, 'Planta', 40, '2025-01-01', '2025-12-31'),
(2, 'Temporal', 30, '2025-03-01', '2025-09-30'),
(3, 'Catedrático', 20, '2025-02-15', '2025-12-15');

-- ========================================
-- PROGRAMAS DE FORMACIÓN
-- ========================================

INSERT INTO Programas (nombre_programa) VALUES
('Técnico en Sistemas'),
('Técnico en Electricidad Industrial'),
('Tecnólogo en Gestión Empresarial');

-- ========================================
-- FICHAS (GRUPOS DE APRENDICES)
-- ========================================

INSERT INTO Fichas (nombre_ficha, id_programa, id_instructor_lider) VALUES
('Ficha 2456789', 1, 1),
('Ficha 2456790', 2, 2),
('Ficha 2456791', 3, 4);

-- ========================================
-- COMPETENCIAS Y RESULTADOS DE APRENDIZAJE
-- ========================================

INSERT INTO Competencias (nombre_competencia, especialidad) VALUES
('Instalar y configurar sistemas operativos', 'Sistemas'),
('Diagnosticar y reparar circuitos eléctricos', 'Electricidad'),
('Diseñar estrategias empresariales', 'Gestión Empresarial');

INSERT INTO Ficha_Competencia (id_ficha, id_competencia) VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO Resultados_Aprendizaje (nombre_resultado, id_competencia) VALUES
('Instala sistemas operativos Windows y Linux', 1),
('Configura dispositivos de red básicos', 1),
('Identifica fallas en sistemas eléctricos trifásicos', 2),
('Diseña planes de mejora continua', 3);

-- ========================================
-- AMBIENTES Y JORNADAS
-- ========================================

INSERT INTO Ambientes (nombre_ambiente) VALUES
('Laboratorio de Sistemas'),
('Taller de Electricidad'),
('Sala de Emprendimiento');

-- Jornadas ya están insertadas más arriba

-- ========================================
-- HORARIOS DE CLASES
-- ========================================

INSERT INTO Horarios (id_ficha, id_instructor, id_ambiente, id_jornada, fecha, hora_inicio, hora_fin) VALUES
(1, 1, 1, 1, '2025-10-21', '07:00:00', '11:00:00'),
(2, 2, 2, 2, '2025-10-21', '13:00:00', '17:00:00'),
(3, 3, 3, 3, '2025-10-21', '18:00:00', '21:00:00');

-- ========================================
-- HORAS CUMPLIDAS POR INSTRUCTORES
-- ========================================

INSERT INTO Horas_Cumplidas (id_instructor, id_ficha, id_ambiente, horas_cumplidas, fecha) VALUES
(1, 1, 1, 4, '2025-10-21'),
(2, 2, 2, 4, '2025-10-21'),
(3, 3, 3, 3, '2025-10-21');

-- ========================================
-- PERMISOS (opcional)
-- ========================================

INSERT INTO Permisos (nombre_permiso) VALUES
('Ver reportes'),
('Editar horarios'),
('Administrar usuarios');

INSERT INTO Roles_Permisos (id_rol, id_permiso) VALUES
(1, 1), -- Instructor puede ver reportes
(2, 1), (2, 2), -- Coordinador puede ver y editar
(3, 1), (3, 2), (3, 3); -- Root tiene todos


--Consultas:
-- Ver todos los usuarios con su rol
SELECT u.id_usuario, u.nombre, r.nombre_rol
FROM Usuarios u
JOIN Roles r ON u.id_rol = r.id_rol;

-- Ver todos los programas con su instructor líder
SELECT f.nombre_ficha, p.nombre_programa, u.nombre AS instructor_lider
FROM Fichas f
JOIN Programas p ON f.id_programa = p.id_programa
JOIN Usuarios u ON f.id_instructor_lider = u.id_usuario;

-- Ver competencias por ficha
SELECT f.nombre_ficha, c.nombre_competencia
FROM Ficha_Competencia fc
JOIN Fichas f ON fc.id_ficha = f.id_ficha
JOIN Competencias c ON fc.id_competencia = c.id_competencia;


-- Ver horario completo por instructor
SELECT u.nombre AS instructor, f.nombre_ficha, a.nombre_ambiente, j.nombre_jornada, h.fecha, h.hora_inicio, h.hora_fin
FROM Horarios h
JOIN Usuarios u ON h.id_instructor = u.id_usuario
JOIN Fichas f ON h.id_ficha = f.id_ficha
JOIN Ambientes a ON h.id_ambiente = a.id_ambiente
JOIN Jornadas j ON h.id_jornada = j.id_jornada
ORDER BY h.fecha, h.hora_inicio;

-- Ver total de horas programadas por instructor
SELECT u.nombre, SUM(TIMESTAMPDIFF(HOUR, h.hora_inicio, h.hora_fin)) AS horas_programadas
FROM Horarios h
JOIN Usuarios u ON h.id_instructor = u.id_usuario
GROUP BY u.nombre;


-- Ver total de horas cumplidas por instructor
SELECT u.nombre, SUM(hc.horas_cumplidas) AS total_horas_cumplidas
FROM Horas_Cumplidas hc
JOIN Usuarios u ON hc.id_instructor = u.id_usuario
GROUP BY u.nombre;

-- Comparar horas cumplidas vs contrato
SELECT u.nombre,
       c.horas_por_cumplir,
       IFNULL(SUM(hc.horas_cumplidas), 0) AS horas_realizadas,
       (c.horas_por_cumplir - IFNULL(SUM(hc.horas_cumplidas), 0)) AS horas_pendientes
FROM Contratos c
JOIN Usuarios u ON c.id_usuario = u.id_usuario
LEFT JOIN Horas_Cumplidas hc ON hc.id_instructor = u.id_usuario
GROUP BY u.nombre, c.horas_por_cumplir;
-- ========================================


