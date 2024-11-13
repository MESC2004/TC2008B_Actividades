/*
 * Miguel Enrique Soria A01028033
 * 06/11/2024
 * Script para generar un archivo .obj de un cilindro
 * hecho por triangulos en base a los valores
 * lados, radio y ancho en ese orden separado por espacios despues de
 * correr el script en la linea de comandos
 */

const fs = require("fs");

// Argumentos de linea de comando (separados por espacios)
// Valores por defecto (caras: 8, radio: 1, ancho: 0.5)
const sides = parseInt(process.argv[2]) || 8;
const radius = parseFloat(process.argv[3]) || 1;
const width = parseFloat(process.argv[4]) || 0.5;

// Validación de entrada (evita formas imposibles)
if (sides < 3 || sides > 360 || radius <= 0 || width <= 0) {
  console.error(
    "Valores inválidos. Asegúrate de que el número de lados esté entre 3 y 360, y que el radio y el ancho sean positivos.",
  );
  process.exit(1);
}

// listas para guardar los cálculos y luego añadirlos al archivo .obj
const vertices = [];
const faces = [];

// variable para obtener el step de incremento de angulo de acuerdo al numero de lados (Radianes)
const angleIncrement = (2 * Math.PI) / sides;

// generar vértices en el borde delantero y trasero de la rueda
for (let i = 0; i < sides; i++) {
  // calcula los vertices para cada paso del angulo
  const angle = i * angleIncrement;
  // Componentes x y y de cada vertice en el angulo
  const x = Math.cos(angle) * radius;
  const y = Math.sin(angle) * radius;

  // Vertices opuestos en la rueda
  vertices.push([x, y, width / 2]);
  vertices.push([x, y, -width / 2]);
}

// Vertices centrales en las tapas (centro de los circulos)
const frontCenterIndex = vertices.length;
const backCenterIndex = frontCenterIndex + 1;
vertices.push([0, 0, width / 2], [0, 0, -width / 2]);

// Calcular las caras
for (let i = 0; i < sides; i++) {
  // siguiuente vertice como indice hasta llegar al numero de lados
  const nextIndex = (i + 1) % sides;

  // Caras laterales (entre las tapas)
  faces.push([nextIndex * 2 + 2, nextIndex * 2 + 1, i * 2 + 1]);

  faces.push([i * 2 + 2, nextIndex * 2 + 2, i * 2 + 1]);

  // Caras frontal y trasera (tapas)
  faces.push([frontCenterIndex + 1, i * 2 + 1, nextIndex * 2 + 1]);

  faces.push([backCenterIndex + 1, nextIndex * 2 + 2, i * 2 + 2]);
}

// Crear y guardar el archivo OBJ

// string con datos
let objData = "# OBJ file\n";

vertices.forEach(
  // v antes de cada valor para indicar verices
  (v) =>
    // fs method from geeks4geeks
    (objData += `v ${v[0].toFixed(4)} ${v[1].toFixed(4)} ${v[2].toFixed(4)}\n`),
);

faces.forEach(
  // f antes de cada valor para indicar caras
  (f) => (objData += `f ${f[0]}//${f[0]} ${f[1]}//${f[1]} ${f[2]}//${f[2]}\n`),
);

// guardar contenido del string en archivo .obj
let filename = "cylinder.obj";
fs.writeFileSync(filename, objData);
console.log(`Archivo OBJ guardado como ${filename}`);
