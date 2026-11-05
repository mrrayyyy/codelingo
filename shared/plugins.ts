/** JSON contracts equivalent to backend/app/contracts.py. Answers stay server-side. */
export type Skill = "reading" | "listening" | "speaking" | "writing" | "review" | "workplace";
export type Service = "tts" | "stt" | "llm" | "dictionary";
export interface Context { text: string; file_path: string; line_number: number; kind: string }
export interface Vocab {
  id: string; lemma: string; part_of_speech: string; frequency: number; cefr: string;
  cefr_estimated: boolean; ipa: string | null; definition: string | null;
  tags: string[]; rank: number; contexts: Context[];
}
export interface UserProfile { native_language: string; target_level: string; daily_goal: number; tts_voice: string }
export interface PluginManifest { id: string; version: string; title: string; skills: Skill[]; services: Service[] }
export interface PublicExercise<Payload extends object = Record<string, unknown>> {
  id: string; plugin_id: string; vocab_id: string; kind: string; prompt: string;
  payload: Payload;
}
export interface Exercise<Payload extends object = Record<string, unknown>, Key extends object = Record<string, unknown>> extends PublicExercise<Payload> { answer_key: Key }
export type DictationExercise = Exercise<{ voice: string; audio_available: boolean }, { transcript: string }> & { kind: "dictation" };
export interface Feedback { score: number; explanation: string; corrections: string[]; reference: string | null }
export interface LearningPlugin {
  manifest: PluginManifest;
  generate(vocabulary: Vocab[], profile: UserProfile): Promise<Exercise[]>;
  grade(exercise: Exercise, answer: { text: string }): Promise<Feedback>;
}
export interface TTSAdapter { synthesize(text: string, voice: string): Promise<Uint8Array> }
export interface STTAdapter { transcribe(audio: Uint8Array, filename: string): Promise<string> }
export interface LLMAdapter { gradeWriting(prompt: string, answer: string): Promise<Feedback> }
export interface DictionaryAdapter { lookup(lemma: string): Promise<{ definition: string | null; ipa: string | null; source: string }> }
