import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { App } from "./App";

function renderApp() {
  // Fresh client per test; no retries, otherwise the error case waits for three retries.
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  render(
    <QueryClientProvider client={client}>
      <App />
    </QueryClientProvider>,
  );
}

describe("App", () => {
  it("shows that the backend is reachable", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue(Response.json({ status: "ok" }));
    vi.stubGlobal("fetch", fetchMock);

    renderApp();

    expect(
      await screen.findByText("Backend ist erreichbar."),
    ).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledWith("/api/v1/health");
  });

  it("shows that the backend is unreachable", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response(null, { status: 502 })),
    );

    renderApp();

    expect(
      await screen.findByText("Backend ist nicht erreichbar."),
    ).toBeInTheDocument();
  });
});
