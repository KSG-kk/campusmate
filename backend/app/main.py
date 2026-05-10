from collections import defaultdict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import ChatRequest, ChatResponse, DebugInfo
from .router import route_question, local_answer
from .llm import deepseek_client

app = FastAPI(title="CampusMate API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions: dict[str, list[dict]] = defaultdict(list)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    route = route_question(req.message)
    local_text, sources, tools = local_answer(req.message, route)

    try:
        if req.mode == "local":
            answer = local_text
        else:
            answer = await deepseek_client.chat(
                user_message=req.message,
                history=sessions[req.session_id],
                context=local_text
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    sessions[req.session_id].append({"role": "user", "content": req.message})
    sessions[req.session_id].append({"role": "assistant", "content": answer})
    if len(sessions[req.session_id]) > 16:
        sessions[req.session_id] = sessions[req.session_id][-16:]

    return ChatResponse(
        answer=answer,
        debug=DebugInfo(mode=req.mode, route=route, sources=sources, tools=tools)
    )
