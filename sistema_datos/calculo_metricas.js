import { lista_de_ventas } from "./datos_ventas.js";

export function calcular_total_ventas() {
  let total = 0;

  for (let i = 0; i < lista_de_ventas.length; i++) {
    total = total + lista_de_ventas[i].precio_producto;
  }

  return total;
}

export function calcular_cantidad_ventas() {
  return lista_de_ventas.length;
}

export function calcular_ticket_promedio() {
  let total = calcular_total_ventas();
  let cantidad = calcular_cantidad_ventas();

  if (cantidad === 0) {
    return 0;
  }

  return total / cantidad;
}
