/**
 * Ejercicio 8.2 - cinco bloques, complejidad teorica y medida.
 *
 * A  getFirst      O(1) tiempo / O(1) espacio
 * B  buscar        O(n) peor / O(1) espacio
 * C  pares         O(n^2) / O(1)  -> a n=1e6 son 5e11 iteraciones: 5 dias
 * D  fib recursivo O(2^n) / O(n) espacio (pila)
 * E  new int[n]    O(n) tiempo / O(n) espacio
 *
 * D mide la razon de crecimiento real: si es 2^n, cada +1 de n duplica el
 * tiempo; si es el numero aureo, cada +1 multiplica por ~1,618.
 */
public class Bloques {

    static volatile long sumidero;

    // A
    static int getFirst(int[] a) { return a[0]; }

    // B
    static int buscar(int[] a, int x) {
        for (int i = 0; i < a.length; i++)
            if (a[i] == x) return i;
        return -1;
    }

    // C - no se ejecuta con n grande a proposito
    static long pares(int[] a) {
        long n = 0;
        for (int i = 0; i < a.length; i++)
            for (int j = i + 1; j < a.length; j++)
                n++;
        return n;
    }

    // D
    static int fib(int n) { return n <= 1 ? n : fib(n - 1) + fib(n - 2); }

    /** E: crear e inicializar un array de n ints. */
    static int[] nuevo(int n) { return new int[n]; }

    public static void main(String[] args) {

        // --- A: el costo fijo de una llamada, y el O(1) real
        int[] datos = new int[1_000_000];
        for (int k = 0; k < 20; k++) sumidero = getFirst(datos); // calentamiento
        long t0 = System.nanoTime();
        long acc = 0;
        for (int k = 0; k < 1_000_000; k++) acc += getFirst(datos);
        long tA = System.nanoTime() - t0;
        sumidero = acc;
        System.out.printf("A getFirst      n=1e6 llamadas: %8.2f ms total, %6.3f ns/llamada%n",
                tA / 1e6, (double) tA / 1e6);

        // --- B: lineal, peor caso (no esta), medido por elemento
        int[] rand = new int[1_000_000];
        java.util.Random rnd = new java.util.Random(1);
        for (int i = 0; i < rand.length; i++) rand[i] = rnd.nextInt();
        for (int k = 0; k < 5; k++) sumidero = buscar(rand, -1);
        long t1 = System.nanoTime();
        sumidero = buscar(rand, -1);
        long tB = System.nanoTime() - t1;
        System.out.printf("B buscar        n=1e6 peor caso: %8.2f ms, %6.3f ns/elemento%n",
                tB / 1e6, (double) tB / rand.length);

        // --- C: el conteo real de pares vs n^2
        System.out.println("C pares         conteo real vs n^2:");
        for (int n : new int[]{1_000, 10_000, 100_000}) {
            int[] v = new int[n];
            long p = pares(v);
            System.out.printf("                  n=%7d  pares=%15d  n^2/2=%15d  ratio=%.4f%n",
                    n, p, (long) n * (n - 1) / 2, (double) p / ((double) n * n));
        }
        // n=1e6 -> n(n-1)/2 iteraciones = ~5e11
        long n1 = 1_000_000L;
        double ops = n1 * (n1 - 1) / 2.0;
        System.out.println(String.format(
                "                  n=1e6 -> %.2e iteraciones; a 1 ns c/u = %.1f s (%.2f h)",
                ops, ops / 1e9, ops / 3.6e12));

        // --- D: la razon de crecimiento real de fib
        System.out.println("D fib recursivo razon entre n y n-1 (paso de 1):");
        long prev = 0;
        for (int n = 32; n <= 38; n++) {
            long s = System.nanoTime();
            long r = fib(n);
            long e = System.nanoTime() - s;
            sumidero = r;
            String razon = prev == 0 ? "" : String.format("  x%.3f", (double) e / prev);
            System.out.printf("                  fib(%2d)=%-10d %8.3f ms%s%n", n, r, e / 1e6, razon);
            prev = e;
        }
        System.out.println("                  (1.618 por paso = numero aureo; 2.0 seria 2^n puro)");

        // --- E: crear un array no es gratis
        for (int k = 0; k < 10; k++) nuevo(1000);
        long t2 = System.nanoTime();
        sumidero += nuevo(1_000_000)[0];
        long tE = System.nanoTime() - t2;
        System.out.printf("E new int[n]    n=1e6: %8.3f ms (el runtime escribe n ceros)%n", tE / 1e6);
    }
}
