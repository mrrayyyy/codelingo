import type { Metadata } from "next";
import "@fontsource-variable/manrope";
import "@fontsource-variable/dm-sans";
import "./globals.css";

export const metadata: Metadata = { title: "CodeLingo — English from your everyday code", description: "Turn your own codebase into a personal English learning journey. Local-first learning for working developers." };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
