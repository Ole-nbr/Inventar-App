import { useHealth } from "../hooks/useHealth";

export function BackendStatus() {
  const { isPending, isError } = useHealth();

  if (isPending) return <p role="status">Prüfe Verbindung zum Backend …</p>;
  if (isError) return <p role="status">Backend ist nicht erreichbar.</p>;
  return <p role="status">Backend ist erreichbar.</p>;
}
