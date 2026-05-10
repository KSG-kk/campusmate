export type Mode = "deepseek" | "local";

export type Msg = {
  role: "user" | "assistant";
  content: string;
  pending?: boolean;
};
