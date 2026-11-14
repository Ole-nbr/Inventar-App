import { BackendStatus } from "./features/health/components/BackendStatus";

export function App() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 bg-gray-50 p-4 text-gray-900">
      <h1 className="text-3xl font-semibold">Inventar-App</h1>
      <BackendStatus />
    </main>
  );
}
