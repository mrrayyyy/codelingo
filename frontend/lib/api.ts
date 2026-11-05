import type { Vocab, UserProfile, PublicExercise, Feedback, PluginManifest } from "../../shared/plugins";
export type { Vocab, UserProfile, PublicExercise, Feedback, PluginManifest };
export interface Job { id: string; repo_id: string; status: string; progress: number; message: string }
export interface Repo { id: string; name: string; source_url: string | null; status: string; created_at: string; words: number; job: Job | null }
export interface Stats { total_words: number; mastered: number; due: number; streak: number; today_reviews: number; daily_goal: number; repos: number; activity: {date: string; count: number}[]; skills: Record<string, {score: number; attempts: number}>; topics: Record<string, number> }
export interface ReviewCard { vocab: Vocab; version: number; reviews: number; due: string }
export interface PluginStatus extends PluginManifest { available: boolean; unavailable_reason: string | null }

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api${path}`, { ...init, headers: init?.body instanceof FormData ? init.headers : { "Content-Type": "application/json", ...init?.headers } });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(typeof error.detail === "string" ? error.detail : "Please check your input and try again.");
  }
  return response.status === 204 ? undefined as T : response.json();
}
