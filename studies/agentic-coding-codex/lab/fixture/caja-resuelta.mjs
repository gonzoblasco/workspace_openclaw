const PRECIO = 250;
const IVA = 21;
let total = 0;

function vender(cantidad) {
  total += PRECIO * cantidad * (1 + IVA / 100);
  return total;
}

vender(2);
vender(3);
console.log(total);
