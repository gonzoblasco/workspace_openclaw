/**
 * Ejercicio 8.4 - la pregunta de entrevista:
 *   "Esto esta lento con 100.000 registros. Por que y como lo mejorarías?"
 *
 * Tres soluciones, tres perfiles de costo:
 *   fuerza bruta  O(n^2) tiempo, O(1) espacio
 *   hashset       O(n) promedio,  O(n) espacio
 *   sort          O(n log n),     O(log n) (o O(1) si el array se puede mutar)
 *
 * Se mide el PEOR caso de cada una (sin duplicado: se recorre todo) porque
 * es el que decide el tiempo en produccion.
 */
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;

public class Duplicado {

    static volatile boolean sumidero;

    /** O(n^2) tiempo, O(1) espacio. */
    static boolean fuerza(int[] a) {
        for (int i = 0; i < a.length; i++)
            for (int j = i + 1; j < a.length; j++)
                if (a[i] == a[j]) return true;
        return false;
    }

    /** O(n) promedio, O(n) espacio. */
    static boolean hashset(int[] a) {
        HashSet<Integer> vistos = new HashSet<>(a.length * 2);
        for (int x : a) {
            if (!vistos.add(x)) return true; // add devuelve false si ya estaba
        }
        return false;
    }

    /** O(n log n), O(1) espacio adicional si se permite mutar el array. */
    static boolean ordenando(int[] original) {
        int[] a = original.clone(); // el clone es O(n); sin el, se muta el input
        Arrays.sort(a);
        for (int i = 1; i < a.length; i++)
            if (a[i] == a[i - 1]) return true;
        return false;
    }

    static double ms(int[] datos, int reps, int modo) {
        long mejor = Long.MAX_VALUE;
        for (int r = 0; r < reps; r++) {
            long t0 = System.nanoTime();
            for (int k = 0; k < 3; k++) {
                boolean b = switch (modo) {
                    case 0 -> fuerza(datos);
                    case 1 -> hashset(datos);
                    default -> ordenando(datos);
                };
                sumidero = b;
            }
            mejor = Math.min(mejor, System.nanoTime() - t0);
        }
        return mejor / 1e6 / 3;
    }

    public static void main(String[] args) {
        int[] tamanos = {10_000, 100_000, 200_000};
        Random rnd = new Random(42);

        System.out.printf("%10s %14s %14s %14s %10s%n",
                "n", "fuerza (ms)", "hashset (ms)", "sort (ms)", "speedup");
        System.out.println("-".repeat(68));

        double[] prev = new double[3];
        for (int n : tamanos) {
            // sin duplicado: todos los valores distintos -> peor caso
            int[] datos = new int[n];
            for (int i = 0; i < n; i++) datos[i] = i;

            for (int k = 0; k < 3; k++) { fuerza(new int[]{1, 2}); hashset(new int[]{1, 2}); ordenando(new int[]{1, 2}); }

            double f = ms(datos, 3, 0);
            double h = ms(datos, 15, 1);
            double s = ms(datos, 15, 2);

            System.out.printf("%10d %14.4f %14.5f %14.4f %9.0fx%n", n, f, h, s, f / h);
            prev[0] = f; prev[1] = h; prev[2] = s;
        }

        System.out.println();
        System.out.println("Duplicar n de 100k a 200k: cuanto se multiplica cada tiempo");
        System.out.println("  fuerza  x4   -> O(n^2)");
        System.out.println("  hashset x2   -> O(n)");
        System.out.println("  sort    x2.x -> O(n log n)");

        // memoria del set, medida de verdad
        int n = 200_000;
        int[] datos = new int[n];
        for (int i = 0; i < n; i++) datos[i] = i;
        Runtime rt = Runtime.getRuntime();
        System.gc();
        long antes = rt.totalMemory() - rt.freeMemory();
        HashSet<Integer> s = new HashSet<>(n * 2);
        for (int x : datos) s.add(x);
        long despues = rt.totalMemory() - rt.freeMemory();
        System.out.printf("%nHashSet con %d enteros: +%.1f MB de heap (~%.0f bytes/entrada)%n",
                n, (despues - antes) / 1e6, (double) (despues - antes) / n);
        if (s.size() < 0) System.out.println(); // keep-alive
    }
}
