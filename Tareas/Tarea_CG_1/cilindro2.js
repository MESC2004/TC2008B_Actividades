/*
 * Miguel Enrique Soria A01028033
 * Script para generar un archivo .obj de un cilindro
 * hecho por triangulos en base a los valores
 * lados, radio y ancho en ese orden separado por espacios despues de
 * correr el script en la linea de comandos
 */

const fs = require("fs");

// Argumentos de linea de comando (separados por espacios)
const sides = parseInt(process.argv[2]) || 8;
const radius = parseFloat(process.argv[3]) || 1;
const width = parseFloat(process.argv[4]) || 0.5;

// Validación de entrada
if (sides < 3 || sides > 360 || radius <= 0 || width <= 0) {
  console.error(
    "Valores inválidos. Asegúrate de que el número de lados esté entre 3 y 360, y que el radio y el ancho sean positivos.",
  );
  process.exit(1);
}

// listas para guardar los cálculos y luego añadirlos al archivo .obj
const vertices = [];
const normals = [];
const faces = [];

// Incremento del ángulo
const angleIncrement = (2 * Math.PI) / sides;

// Generar vértices en el borde delantero y trasero de la rueda
for (let i = 0; i < sides; i++) {
  // calcula los vertices para cada paso del angulo
  const angle = i * angleIncrement;
  const x = Math.cos(angle) * radius;
  const y = Math.sin(angle) * radius;

  // Vertices opuestos en la rueda
  vertices.push([x, y, width / 2]);
  vertices.push([x, y, -width / 2]);
}

// Vertices centrales en las tapas
const frontCenterIndex = vertices.length + 1;
const backCenterIndex = frontCenterIndex + 1;
vertices.push([0, 0, width / 2], [0, 0, -width / 2]); // Centros

// Calcular las caras
for (let i = 0; i < sides; i++) {
  const nextIndex = (i + 1) % sides;

  // Caras laterales (normales hacia afuera)
  faces.push([2 * i + 1, 2 * nextIndex + 1, 2 * i + 2]);
  faces.push([2 * nextIndex + 1, 2 * nextIndex + 2, 2 * i + 2]);

  // Normales de las caras laterales
  // const nx = Math.cos(angleIncrement);
  // const ny = Math.sin(angleIncrement);
  // normals.push([nx, ny, 0]);

  // Caras frontal y trasera
  faces.push([2 * i + 1, 2 * nextIndex + 1, frontCenterIndex]); // Frontal
  faces.push([2 * nextIndex + 2, 2 * i + 2, backCenterIndex]); // Trasera

  // Normales para caras frontal y trasera
  // normals.push([0, 0, 1]); // Frente (hacia el eje positivo Z)
  // normals.push([0, 0, -1]); // Parte trasera (hacia el eje negativo Z)
}

for (let i = 0; i < sides; i++) {
  const normalAngle = (2 * Math.PI * i) / sides;
  const nx = Math.cos(normalAngle);
  const ny = Math.sin(normalAngle);
  normals.push([nx, ny, 0]);
}

normals.push([0, 0, 1]);
normals.push([0, 0, -1]);

// Crear y guardar el archivo OBJ
let objData = "# OBJ file\n";
vertices.forEach(
  // v antes de cada valor para indicar verices
  (v) =>
    // fs method from geeks4geeks
    (objData += `v ${v[0].toFixed(4)} ${v[1].toFixed(4)} ${v[2].toFixed(4)}\n`),
);
normals.forEach(
  // vn antes de cada valor para indicar vectores normales
  (n) =>
    (objData += `vn ${n[0].toFixed(4)} ${n[1].toFixed(4)} ${n[2].toFixed(4)}\n`),
);

faces.forEach((f, idx) => {
  const normalIdx =
    idx < faces.length - 2 * sides
      ? 1
      : normals.length - (idx < faces.length - sides ? 1 : 0);
  // f antes de cada valor para indicar caras
  objData += `f ${f[0]}//${normalIdx} ${f[1]}//${normalIdx} ${f[2]}//${normalIdx}\n`;
});

fs.writeFileSync("cylinder.obj", objData);
console.log("Archivo OBJ guardado como wheel.obj");
