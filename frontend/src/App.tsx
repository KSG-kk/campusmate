import { useEffect, useMemo, useRef, useState } from "react";
import { BootScreen } from "./components/BootScreen";
import { Sidebar } from "./components/Sidebar";
import { MessageList } from "./components/MessageList";
import { Composer } from "./components/Composer";
import type { Mode, Msg } from "./types";

export function App() {
  const [mode, setMode] = useState<Mode | null>(null);
  const [messages, setMessages] = useState<Msg[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const sessionId = useMemo(() => crypto.randomUUID(), []);
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, loading]);

  async function send(text: string) {
    const question = text.trim();
    if (!question || !mode || loading) return;
    setError("");
    setLoading(true);
    setMessages((prev) => [
      ...prev,
      { role: "user", content: question },
      { role: "assistant", content: "正在思考中...", pending: true },
    ]);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: question,
          mode,
          session_id: sessionId,
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "请求失败");
      setMessages((prev) =>
        prev.map((m, i) =>
          i === prev.length - 1
            ? { role: "assistant", content: data.answer }
            : m,
        ),
      );
    } catch (e: any) {
      setMessages((prev) => prev.filter((m) => !m.pending));
      setError(e.message || "服务异常");
    } finally {
      setLoading(false);
    }
  }

  if (!mode) {
    return <BootScreen onSelectMode={setMode} />;
  }

  return (
    <main className="min-h-screen grid grid-cols-[320px_1fr] gap-[22px] p-6 max-md:grid-cols-1">
      <Sidebar
        mode={mode}
        onSwitchMode={() => {
          setMode(null);
          setMessages([]);
        }}
        onExampleClick={send}
        disabled={loading}
      />
      <section className="bg-white/85 backdrop-blur-lg border border-white/75 rounded-3xl shadow-2xl flex flex-col h-[calc(100vh-48px)] overflow-hidden animate-fadeUp">
        <MessageList messages={messages} bottomRef={bottomRef} />
        {error && (
          <div className="mx-[18px] mb-3 py-3 px-3.5 rounded-[14px] bg-red-50 text-red-700">
            {error}
          </div>
        )}
        <Composer onSubmit={send} disabled={loading} />
      </section>
    </main>
  );
}
