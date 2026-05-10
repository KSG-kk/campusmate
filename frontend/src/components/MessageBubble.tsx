import { Loader2 } from "lucide-react";

type MessageBubbleProps = {
  role: "user" | "assistant";
  content: string;
  pending?: boolean;
};

export function MessageBubble({
  role,
  content,
  pending = false,
}: MessageBubbleProps) {
  const isUser = role === "user";
  const rowAlign = isUser ? "justify-end" : "justify-start";
  const bubbleColor = isUser
    ? "bg-slate-900 text-white rounded-br-md"
    : "bg-white border border-slate-100 rounded-bl-md";
  const pendingTone = pending
    ? "flex items-center gap-2 text-slate-500"
    : "";

  return (
    <div className={`flex my-3.5 animate-pop ${rowAlign}`}>
      <div
        className={`max-w-[min(720px,78%)] whitespace-pre-wrap leading-loose py-3.5 px-4 rounded-3xl shadow-md ${bubbleColor} ${pendingTone}`}
      >
        {pending && <Loader2 className="animate-spin" size={16} />}
        <span>{content}</span>
      </div>
    </div>
  );
}
