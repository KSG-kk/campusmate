import { useState } from "react";
import { Send } from "lucide-react";

type ComposerProps = {
  onSubmit: (text: string) => void;
  disabled?: boolean;
  placeholder?: string;
};

export function Composer({
  onSubmit,
  disabled = false,
  placeholder = "输入问题，比如：学生证怎么补办？",
}: ComposerProps) {
  const [input, setInput] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const text = input.trim();
    if (!text || disabled) return;
    onSubmit(text);
    setInput("");
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="flex gap-3 p-[18px] border-t border-slate-100 bg-white/70"
    >
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder={placeholder}
        className="flex-1 border border-slate-200 rounded-2xl py-[15px] px-4 text-base outline-none transition focus:border-slate-400 focus:ring-4 focus:ring-slate-400/20"
      />
      <button
        disabled={disabled || !input.trim()}
        className="w-[52px] rounded-2xl bg-slate-900 text-white grid place-items-center cursor-pointer transition disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Send size={18} />
      </button>
    </form>
  );
}
