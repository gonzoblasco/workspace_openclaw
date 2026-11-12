/**
 * Ejercicio 8.3 - la misma tarea, dos algoritmos.
 *
 * 1. Busqueda lineal (array desordenado).
 * 2. Busqueda binaria (array ordenado).
 * 3. Medicion con System.nanoTime() sobre varios N.
 *
 * La pregunta del modulo no es "cual es mas rapido" sino "cuanto crece cada
 * uno". Por eso el benchmark corre con varios N y ademas mide el costo por
 * operacion: si ns/op no crece con n, la complejidad es lineal.
 *
 * Leccion de la primera version (ver RESULTADOS.md): con N >= 100.000 la
 * busqueda lineal se comporta como si fuera O(1), porque el JIT vectoriza el
 * loop y recorre la memoria a decenas de GB/s. La teoria no cambia; la
 * maquina se vuelve demasiado rapida para verla con cronometro. La version
 * con -Xint (interprete, sin JIT) si muestra la forma.
 *
 * Compilar:  javac Busqueda.java
 * Ejecutar:  java Busqueda          (con JIT)
 *            java -Xint Busqueda    (sin JIT, para ver la forma)
 */
import java.util.Arrays;
import java.util.Random;

public class Busqueda {

    // volatile: impide que el JIT borre el loop por "resultado no usado".
    static volatile long sumidero;

    /** O(n) peor caso: si el elemento no esta, recorre todo. */
    static int lineal(int[] a, int objetivo) {
        for (int i = 0; i < a.length; i++) {
            if (a[i] == objetivo) return i;
        }
        return -1;
    }

    /** O(log n): cada paso descarta la mitad del rango vivo. */
    static int binaria(int[] ordenado, int objetivo) {
        int lo = 0, hi = ordenado.length - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2; // no (lo+hi)/2: desborda con arrays grandes
            if (ordenado[mid] == objetivo) return mid;
            if (ordenado[mid] < objetivo) lo = mid + 1;
            else hi = mid - 1;
        }
        return -1;
    }

    static void correrLineal(int[] a, int veces, int objetivo) {
        long acc = 0;
        for (int k = 0; k < veces; k++) acc += lineal(a, objetivo);
        sumidero = acc;
    }

    static void correrBinaria(int[] ordenado, int veces, int objetivo) {
        long acc = 0;
        for (int k = 0; k < veces; k++) acc += binaria(ordenado, objetivo);
        sumidero = acc;
    }

    static double medianaMs(int[] datos, int veces, boolean binaria, int objetivo, int muestras) {
        double[] t = new double[muestras];
        for (int s = 0; s < muestras; s++) {
            long t0 = System.nanoTime();
            if (binaria) correrBinaria(datos, veces, objetivo);
            else correrLineal(datos, veces, objetivo);
            t[s] = (System.nanoTime() - t0) / 1e6 / veces;
        }
        Arrays.sort(t);
        return t[muestras / 2];
    }

    public static void main(String[] args) {
        boolean jit = !java.lang.management.ManagementFactory
                .getRuntimeMXBean().getInputArguments().toString().contains("-Xint");

        int[] tamanos = {1_000, 10_000, 100_000, 1_000_000};
        int repeticiones = 20, muestras = 15;
        Random rnd = new Random(42);

        System.out.printf("modo: %s%n%n", jit ? "JIT (compilado)" : "interprete (-Xint)");
        System.out.printf("%10s %14s %14s %12s %12s%n",
                "n", "lineal (ms)", "binaria (ms)", "ns/elem", "veces mas");
        System.out.println("-".repeat(66));

        for (int n : tamanos) {
            int[] datos = new int[n];
            for (int i = 0; i < n; i++) datos[i] = rnd.nextInt();
            int[] ordenado = datos.clone();
            Arrays.sort(ordenado);

            for (int i = 0; i < 5; i++) { correrLineal(datos, 1, -1); correrBinaria(ordenado, 1, -1); }

            double mejorCaso = medianaMs(datos, repeticiones, false, datos[0], muestras);
            double peorCaso = medianaMs(datos, repeticiones, false, -1, muestras);
            double bin = medianaMs(ordenado, repeticiones, true, -1, muestras);

            System.out.printf("%10d %14.4f %14.6f %12.4f %12.0fx%n",
                    n, peorCaso, bin, (peorCaso - mejorCaso) * 1e6 / n,
                    peorCaso / Math.max(bin, 1e-9));
        }

        System.out.println();
        System.out.println("'ns/elem' = (peorCaso - mejorCaso) * 1e6 / n: el costo de UN elemento.");
        System.out.println("Plano entre tamanos -> O(n). No es que el algoritmo cambie:");
        System.out.println("es que el costo por elemento no crece.");
    }
}
