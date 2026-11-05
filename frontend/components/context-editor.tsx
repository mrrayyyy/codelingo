"use client";
import dynamic from "next/dynamic";
import { useEffect, useRef } from "react";
import type { editor } from "monaco-editor";
import type { Vocab } from "@/lib/api";

type Monaco = typeof import("monaco-editor");
let monacoPromise: Promise<Monaco> | undefined;
function loadMonaco(): Promise<Monaco> {
  monacoPromise ??= new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = "/monaco/editor.js";
    script.onload = () => resolve((globalThis as unknown as { CodeLingoMonaco: Monaco }).CodeLingoMonaco);
    script.onerror = () => { monacoPromise = undefined; reject(new Error("Could not load the local context editor")); };
    document.head.appendChild(script);
  });
  return monacoPromise;
}

const Monaco = dynamic(async () => {
  const { default: Editor, loader } = await import("@monaco-editor/react");
  // Serve our ESM bundle and workers locally, including patched dependencies.
  (globalThis as { MonacoEnvironment?: unknown }).MonacoEnvironment = {
    getWorker: () => new Worker("/monaco/editor.worker.js"),
  };
  const monaco = await loadMonaco();
  loader.config({ monaco });
  return Editor;
}, { ssr: false, loading: () => <div className="editor-loading">Loading context editor…</div> });

export default function ContextEditor({ word }: { word: Vocab }) {
  const ref = useRef<editor.IStandaloneCodeEditor | null>(null);
  const decorations = useRef<editor.IEditorDecorationsCollection | null>(null);
  const context = word.contexts[0];
  function highlight() {
    const instance = ref.current;
    if (!instance) return;
    const matches = instance.getModel()?.findMatches(word.lemma, false, false, false, null, true) || [];
    decorations.current?.clear();
    decorations.current = instance.createDecorationsCollection(matches.map(match => ({ range: match.range, options: { inlineClassName: "vocab-highlight" } })));
  }
  useEffect(() => { highlight(); }, [word.id]); // eslint-disable-line react-hooks/exhaustive-deps
  if (!context) return <p className="muted">No context remains. Import a repository to add examples.</p>;
  return <div className="context-editor"><link rel="stylesheet" href="/monaco/editor.css"/><div className="editor-toolbar"><span className="dot green" /><code>{context.file_path}:{context.line_number}</code><span>original context</span></div>
    <Monaco height="145px" language="plaintext" value={context.text} onMount={instance => { ref.current = instance; highlight(); }} onChange={highlight}
      options={{ readOnly: true, domReadOnly: true, minimap: { enabled: false }, lineNumbers: n => String(context.line_number + n - 1), fontSize: 13, fontFamily: "ui-monospace, SFMono-Regular, monospace", wordWrap: "on", scrollBeyondLastLine: false, automaticLayout: true, folding: false, lineDecorationsWidth: 5, overviewRulerLanes: 0, renderLineHighlight: "none", padding: { top: 18 }, contextmenu: false }} />
  </div>;
}
