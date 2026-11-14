import { useHealth } from "../hooks/useHealth";

// Full class names only: Tailwind cannot detect classes built at runtime.
const STATUS = {
  pending: { dot: "bg-gray-400", text: "Prüfe Verbindung zum Backend …" },
  error: { dot: "bg-red-500", text: "Backend ist nicht erreichbar." },
  success: { dot: "bg-green-500", text: "Backend ist erreichbar." },
} as const;

export function BackendStatus() {
  const { status } = useHealth();
  const { dot, text } = STATUS[status];

  return (
    <p role="status" className="flex items-center gap-2 text-sm text-gray-600">
      <span aria-hidden="true" className={`size-2.5 rounded-full ${dot}`} />
      {text}
    </p>
  );
}
