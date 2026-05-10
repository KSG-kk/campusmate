import { Sparkles } from "lucide-react";
import type { Mode } from "../types";

const examples = [
  "图书馆借阅规则是什么？",
  "学生证怎么补办？",
  "补退选截止是什么时候？",
  "从今天到 2026-06-22 还有几天？",
  "教务处办公时间和电话是什么？",
];

type SidebarProps = {
  mode: Mode;
  onSwitchMode: () => void;
  onExampleClick: (text: string) => void;
  disabled?: boolean;
};

export function Sidebar({
  mode,
  onSwitchMode,
  onExampleClick,
  disabled = false,
}: SidebarProps) {
  return (
    <aside className="bg-white/85 backdrop-blur-lg border border-white/75 rounded-3xl shadow-2xl p-[22px] h-[calc(100vh-48px)] sticky top-6 max-md:h-auto max-md:static animate-fadeUp">
      <div className="flex gap-2.5 items-center font-extrabold text-slate-700">
        <Sparkles size={24} /> CampusMate
      </div>
      <div className="my-[22px] py-3.5 px-3.5 rounded-2xl bg-slate-50 text-slate-600">
        当前模式：
        <b>{mode === "deepseek" ? "DeepSeekv4flash" : "本地数据库"}</b>
      </div>
      <button
        onClick={onSwitchMode}
        className="w-full border border-slate-200 rounded-2xl py-3 px-3.5 my-[7px] text-center cursor-pointer transition bg-slate-900 text-white"
      >
        重新选择模式
      </button>
      <h3>示例问题</h3>
      {examples.map((x) => (
        <button
          key={x}
          onClick={() => onExampleClick(x)}
          disabled={disabled}
          className="w-full border border-slate-200 bg-white rounded-2xl py-3 px-3.5 my-[7px] text-left cursor-pointer transition hover:translate-x-1 hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-x-0 disabled:hover:bg-white"
        >
          {x}
        </button>
      ))}
    </aside>
  );
}
