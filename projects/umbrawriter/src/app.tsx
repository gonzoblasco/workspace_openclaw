import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { RouterProvider, createRouter } from '@tanstack/react-router'
import { RouteRuleLoaderFunction } from '@tanstack/react-router'

// Router configuration
const router = createRouter({
   routeRules: [
      {
         id: 'home',
         path: '/',
         loader: () => Promise.resolve({}),
         action: async ({ payload }) => { return {}; }
      },
      {
         id: 'beat-viewer',
         path: '/beat/:path',
         loader: RouteRuleLoaderFunction('loadBeat'),
         action: async ({ arg, payload }) => { return {}; }
      },
      {
         id: 'divergence-gen',
         path: '/diverge',
         loader: RouteRuleLoaderFunction('generateDivergence'),
         action: async ({ arg, payload }) => { return {}; }
      }
   ]
})

// Client setup
const queryClient = new QueryClient({
   defaultStatus: 'stale',
   defaultPendingState: null as Promise<any>[],
   defaultErrorState: () => new Error('Query error'),
   deplete: 1024 // Memory limit in bytes
})

function App() {
 return (
  <div className="min-h-screen bg-[var(--background)] text-[var(--foreground)]">
    <div className="container mx-auto max-w-[140ch] px-4 py-8">
      {/* Header */}
      <header className="mb-8 border-b border-border/20 pb-6">
        <h1 className="text-xl font-bold mb-2 text-accent-primary">
          UmbraWriter v0.1
        </h1>
        <p className="text-muted-foreground">
          Copiloto narrativo — Motor Dialógico v0.1
        </p>
      </header>

      {/* Main Navigation */}
      <nav className="flex flex-wrap gap-4 mb-8">
        <a href="/" className="px-3 py-2 rounded-md bg-accent-secondary/10 text-accent-primary hover:opacity-80 transition">
          Home
        </a>
        <a href="/beat/capitulo-01.md" className="px-3 py-2 rounded-md bg-accent-secondary/10 text-accent-primary hover:opacity-80 transition">
          Beat Viewer
        </a>
        <a href="/diverge" className="px-3 py-2 rounded-md bg-accent-secondary/10 text-accent-primary hover:opacity-80 transition font-medium">
          Diverge Engine
        </a>
      </nav>

      {/* Hero Content */}
      <main className="space-y-6">
        <div className="p-6 rounded-lg border border-border bg-accent-secondary/5 text-center">
          <h2 className="text-2xl font-bold mb-4 text-gradient-primary">
            ¿Dónde va esta historia?
          </h2>
          <p className="text-muted-foreground mb-6 max-w-[70ch] mx-auto">
            Referencie un file Beat, dig qué cambia, y obtendré 3 caminos divergentes con cargas dramáticas distintas.
          </p>

          <button
             onClick={() => router.navigate({ to: 'diverge' })}
             className="px-6 py-3 bg-accent-primary text-white font-bold rounded-lg hover:bg-accent-primary/80 transition-transform transform hover:scale-105"
          >
            Generar Divergencias
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 mt-8">
           <div className="p-4 rounded-lg bg-accent-secondary/10 text-center">
             <div className="text-2xl font-bold text-accent-primary mb-1">0</div>
             <div className="text-sm text-muted-foreground">Beats Loaded</div>
           </div>
           <div className="p-4 rounded-lg bg-accent-secondary/10 text-center">
             <div className="text-2xl font-bold text-accent-primary mb-1">∞</div>
             <div className="text-sm text-muted-foreground">Divergencias Generadas</div>
           </div>
           <div className="p-4 rounded-lg bg-accent-secondary/10 text-center">
             <div className="text-2xl font-bold text-accent-primary mb-1">3</div>
             <div className="text-sm text-muted-foreground">Path Options Per Turn</div>
           </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-12 pt-6 border-t border-border/20 text-center">
        <p className="text-xs text-muted-foreground">
          Kanam AI • 2026 • V0.1 Dialectic Engine
        </p>
      </footer>
    </div>
  </div >
 })
}

// Provider wrapping
export default function UmbraWriterApp() {
 return (
   <QueryClientProvider client={queryClient}>
     <RouterProvider router={router} />
   </QueryClientProvider>
 )
}