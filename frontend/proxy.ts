import { timingSafeEqual } from "node:crypto";
import { NextRequest, NextResponse } from "next/server";

function equal(a: string, b: string): boolean {
  const left = Buffer.from(a), right = Buffer.from(b);
  return left.length === right.length && timingSafeEqual(left, right);
}

/** Single-user cloud access. All app routes and data requests require auth. */
export function proxy(request: NextRequest) {
  const password = process.env.WORKSPACE_PASSWORD;
  if (!password) return NextResponse.next(); // Local loopback development only.
  const path = request.nextUrl.pathname;
  if (path === "/api/health" && request.method === "GET") return NextResponse.next();
  const key = request.headers.get("x-api-key") || "";
  // Only remote-worker routes accept machine credentials; no generic API bypass.
  if (path.startsWith("/api/cloud/jobs/") && process.env.API_KEY && equal(key, process.env.API_KEY)) return NextResponse.next();
  const authorization = request.headers.get("authorization") || "";
  const expected = "Basic " + Buffer.from(`codelingo:${password}`).toString("base64");
  if (equal(authorization, expected)) return NextResponse.next();
  return new NextResponse("Sign in to your CodeLingo workspace.", {
    status: 401,
    headers: { "WWW-Authenticate": 'Basic realm="CodeLingo", charset="UTF-8"', "Cache-Control": "no-store" },
  });
}

export const config = { matcher: ["/((?!_next/static|_next/image|favicon.ico|monaco).*)"] };
