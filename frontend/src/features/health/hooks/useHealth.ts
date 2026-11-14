import { useQuery } from "@tanstack/react-query";

import type { components } from "../../../api/types";

type HealthRead = components["schemas"]["HealthRead"];

async function fetchHealth(): Promise<HealthRead> {
  const response = await fetch("/api/v1/health");
  if (!response.ok)
    throw new Error(`Health check failed with HTTP ${response.status}`);
  return (await response.json()) as HealthRead;
}

export function useHealth() {
  return useQuery({ queryKey: ["health"], queryFn: fetchHealth });
}
