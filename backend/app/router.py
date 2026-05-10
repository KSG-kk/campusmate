import re
from .kb import kb
from .tools import search_calendar_event, calculate_date_gap, lookup_office_hours, today_iso


def route_question(message: str) -> str:
    m = message
    has_kb = any(k in m for k in ["图书馆", "借阅", "学生证", "补办", "选课", "退课", "宿舍", "报修", "流程", "规则"])
    has_tool = any(k in m for k in ["还有几天", "多少天", "什么时候", "校历", "截止", "办公室", "办公时间", "电话", "地点", "教务处", "事务中心", "后勤"])
    if has_kb and has_tool:
        return "mixed"
    if has_tool:
        return "tool"
    if has_kb:
        return "kb"
    return "direct"


def run_tools(message: str) -> list[dict]:
    results: list[dict] = []

    if any(k in message for k in ["校历", "什么时候", "截止", "开学", "考试", "暑假", "五一"]):
        keyword = ""
        for k in ["补退选", "开学", "期末", "暑假", "五一"]:
            if k in message:
                keyword = k
                break
        results.append(search_calendar_event(keyword or message[:20]))

    if any(k in message for k in ["办公时间", "电话", "地点", "办公室", "教务处", "学生事务中心", "后勤"]):
        office = ""
        for k in ["教务处", "学生事务中心", "后勤服务中心", "后勤"]:
            if k in message:
                office = "后勤服务中心" if k == "后勤" else k
                break
        results.append(lookup_office_hours(office or message))

    if any(k in message for k in ["还有几天", "多少天", "相差几天"]):
        dates = re.findall(r"\d{4}-\d{1,2}-\d{1,2}", message)
        if len(dates) >= 2:
            start, end = dates[0], dates[1]
        elif len(dates) == 1:
            start, end = today_iso(), dates[0]
        else:
            start, end = today_iso(), "2026-06-22"
        results.append(calculate_date_gap(start, end))

    return results


def local_answer(message: str, route: str) -> tuple[str, list[dict], list[dict]]:
    sources = kb.search(message) if route in ["kb", "mixed", "direct"] else []
    tools = run_tools(message) if route in ["tool", "mixed"] else []

    parts = []
    if sources:
        parts.append("我在本地知识库里找到了这些信息：")
        for idx, doc in enumerate(sources, 1):
            parts.append(f"{idx}. {doc['title']}：{doc['content']} 来源：{doc['source']}")
    if tools:
        if parts:
            parts.append("")
        for item in tools:
            parts.append(format_tool_result(item))
    if not sources and not tools:
        parts.append("本地数据库没有找到足够依据。你可以切换到 DeepSeek 模式，让模型基于通用能力回答；或者补充本地知识库资料。")
    return "\n".join(parts), sources, tools

def format_tool_result(item: dict) -> str:
    """把工具返回的机器结构 dict 转成适合用户阅读的自然语言。"""
    tool_name = item.get("tool")

    if tool_name == "search_calendar_event":
        matches = item.get("matches", [])
        if not matches:
            keyword = item.get("input", "相关事项")
            return f"我没有在校历里找到“{keyword}”相关安排。"

        lines = ["我在校历里查到了以下安排："]
        for event in matches:
            name = event.get("name", "未命名事项")
            date = event.get("date", "日期未注明")
            desc = event.get("description", "暂无说明")
            lines.append(f"- {name}：{date}，{desc}")
        return "\n".join(lines)

    if tool_name == "calculate_date_gap":
        start = item.get("start_date", "开始日期")
        end = item.get("end_date", "结束日期")
        days = item.get("days")
        if days is None:
            return "日期计算失败，请检查日期格式是否为 YYYY-MM-DD。"
        if days < 0:
            return f"从 {start} 到 {end} 已经过去 {abs(days)} 天。"
        if days == 0:
            return f"{end} 就是今天。"
        return f"从 {start} 到 {end} 还有 {days} 天。"

    if tool_name == "lookup_office_hours":
        if item.get("error"):
            return f"我没有找到“{item.get('office', '该部门')}”的办公信息。"
        office = item.get("office", "相关部门")
        hours = item.get("hours", "未注明")
        phone = item.get("phone", "未注明")
        location = item.get("location", "未注明")
        return f"{office}的办公信息如下：\n- 办公时间：{hours}\n- 电话：{phone}\n- 地点：{location}"

    return "查询完成，但暂时无法格式化这类结果。"
