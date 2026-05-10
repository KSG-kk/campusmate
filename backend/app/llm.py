import httpx
from .config import get_settings

SYSTEM_PROMPT = """
你是 CampusMate 校园助手 Agent。
要求：
1. 只围绕校园问答、办事流程、校历、学习生活提供帮助。
2. 优先依据提供的本地知识库片段和工具结果回答。
3. 如果资料不足，明确说“不确定”，不要编造。
4. 输出要清楚、简洁、有步骤。
"""

class DeepSeekClient:
    async def chat(self, user_message: str, history: list[dict], context: str) -> str:
        settings = get_settings()
        if not settings.deepseek_api_key:
            raise RuntimeError("未配置 DEEPSEEK_API_KEY，请在 backend/.env 中填写。")

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(history[-8:])
        messages.append({
            "role": "user",
            "content": f"本地上下文/工具结果：\n{context or '无'}\n\n用户问题：{user_message}"
        })

        url = settings.deepseek_base_url.rstrip("/") + "/chat/completions"
        payload = {
            "model": settings.deepseek_model,
            "messages": messages,
            "temperature": 0.3,
            "stream": False
        }
        headers = {"Authorization": f"Bearer {settings.deepseek_api_key}"}

        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]

deepseek_client = DeepSeekClient()
