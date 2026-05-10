import { Database, Sparkles } from "lucide-react";
import type { Mode } from "../types";

type BootScreenProps = {
  onSelectMode: (mode: Mode) => void;
};

export function BootScreen({ onSelectMode }: BootScreenProps) {
  return (
    <main className="min-h-screen grid place-items-center p-7">
      <section className="w-full max-w-[880px] bg-white/80 backdrop-blur-lg border border-white/75 rounded-3xl p-[38px] shadow-2xl animate-fadeUp">
        <div className="flex gap-2.5 items-center font-extrabold text-slate-700">
          <Sparkles size={28} /> CampusMate
        </div>
        <h1 className="text-[44px] mt-6 mb-2.5 max-md:text-4xl font-bold">
          启动前请选择运行方式
        </h1>
        <p className="leading-loose text-slate-500">
          你可以选择 DeepSeek 模型回答，或只使用本地数据库检索。项目中只保留
          DeepSeekv4flash 这一种模型，不在前端硬编码 API Key。
        </p>
        <div className="grid grid-cols-2 gap-[18px] mt-7 max-md:grid-cols-1">
          <button
            onClick={() => onSelectMode("deepseek")}
            className="border border-slate-200 bg-white rounded-3xl p-6 text-left cursor-pointer flex flex-col gap-2.5 transition shadow-md hover:-translate-y-1.5 hover:shadow-xl"
          >
            <Sparkles />
            <b className="text-xl">使用 DeepSeek 模型</b>
            <span className="text-slate-500 leading-relaxed">
              后端读取 .env，通过 DeepSeekv4flash 生成更自然的回答。
            </span>
          </button>
          <button
            onClick={() => onSelectMode("local")}
            className="border border-slate-200 bg-white rounded-3xl p-6 text-left cursor-pointer flex flex-col gap-2.5 transition shadow-md hover:-translate-y-1.5 hover:shadow-xl"
          >
            <Database />
            <b className="text-xl">使用本地数据库</b>
            <span className="text-slate-500 leading-relaxed">
              不调用模型，只基于本地知识库和工具返回结果。
            </span>
          </button>
        </div>
      </section>
    </main>
  );
}
