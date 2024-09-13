// middleware.js
import { NextResponse } from "next/server";
export function middleware(req) {
  const mode = process.env.NODE_ENV;

  if (
    req.nextUrl.pathname.startsWith("/components") &&
    mode !== "development"
  ) {
    return NextResponse.redirect(new URL("/", req.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: "/components/:path*",
};
