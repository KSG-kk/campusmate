import type { RefObject } from "react";
import { MessageBubble } from "./MessageBubble";
import type { Msg } from "../types";

type MessageListProps = {
  messages: Msg[];
  bottomRef: RefObject<HTMLDivElement | null>;
};

export function MessageList({ messages, bottomRef }: MessageListProps) {
  return (
    <div className="flex-1 overflow-auto p-[26px] scroll-smooth">
      {messages.length === 0 && (
        <div className="text-center text-slate-400 mt-[25vh]">
          选择左侧示例，或输入你的校园问题。
        </div>
      )}
      {messages.map((m, i) => (
        <MessageBubble
          key={i}
          role={m.role}
          content={m.content}
          pending={m.pending}
        />
      ))}
      <div ref={bottomRef} />
    </div>
  );
}
