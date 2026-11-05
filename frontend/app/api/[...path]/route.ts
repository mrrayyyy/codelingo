import { NextRequest } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
const LIMIT = 22 * 1024 * 1024;

async function proxy(request: NextRequest, context: { params: Promise<{ path: string[] }> }) {
  const { path } = await context.params;
  if (path.some(p => p === "." || p === ".." || p.includes("/"))) return new Response("Invalid path", { status: 400 });
  if (!["GET", "HEAD"].includes(request.method)) {
    const origin = request.headers.get("origin");
    if (origin) {
      try {
        if (new URL(origin).host !== request.headers.get("host")) return Response.json({ detail: "Cross-origin request denied" }, { status: 403 });
      } catch {
        return Response.json({ detail: "Invalid request origin" }, { status: 403 });
      }
    }
  }
  let body: Uint8Array | undefined;
  if (request.body && !["GET", "HEAD"].includes(request.method)) {
    const reader = request.body.getReader();
    const chunks: Uint8Array[] = [];
    let length = 0;
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      length += value.length;
      if (length > LIMIT) { await reader.cancel(); return Response.json({ detail: "Upload exceeds 20 MiB" }, { status: 413 }); }
      chunks.push(value);
    }
    body = new Uint8Array(length);
    let offset = 0;
    for (const chunk of chunks) { body.set(chunk, offset); offset += chunk.length; }
  }
  try {
    const response = await fetch(`${process.env.API_URL || "http://127.0.0.1:8000"}/${path.map(encodeURIComponent).join("/")}${request.nextUrl.search}`, {
      method: request.method,
      headers: { "X-API-Key": process.env.API_KEY || "local-development-key", "Content-Type": request.headers.get("content-type") || "application/json" },
      body: body as BodyInit | undefined, cache: "no-store", signal: AbortSignal.timeout(120_000),
    });
    const headers = new Headers();
    for (const name of ["content-type", "content-disposition"]) { const value = response.headers.get(name); if (value) headers.set(name, value); }
    headers.set("Cache-Control", "no-store");
    return new Response(response.body, { status: response.status, headers });
  } catch {
    return Response.json({ detail: "The CodeLingo API is unavailable. Start the backend and try again." }, { status: 503 });
  }
}

export { proxy as GET, proxy as POST, proxy as PATCH, proxy as DELETE };
