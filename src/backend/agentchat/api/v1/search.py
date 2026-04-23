"""
联网搜索接口
"""
from fastapi import APIRouter, Query, Body
from typing import Optional, Literal
from agentchat.schema.schemas import UnifiedResponseModel, resp_200, resp_500
from agentchat.tools.web_search.tavily_search.action import _tavily_search
from agentchat.tools.web_search.bocha_search.action import bocha_search
from loguru import logger

router = APIRouter(tags=["Search"])


@router.get("/search/tavily", response_model=UnifiedResponseModel)
async def search_with_tavily(
    query: str = Query(description="搜索关键词"),
    topic: Optional[str] = Query(default="general", description="搜索主题：general(通用)、news(新闻)、finance(财经)"),
    max_results: Optional[int] = Query(default=5, description="最大返回结果数量"),
    time_range: Optional[Literal["day", "week", "month", "year"]] = Query(default=None, description="时间范围")
):
    """
    使用 Tavily 进行联网搜索

    ## 参数说明
    - query: 搜索关键词（必填）
    - topic: 搜索主题，可选值：general(通用)、news(新闻)、finance(财经)
    - max_results: 最大返回结果数量，默认5条
    - time_range: 时间范围，可选值：day(一天)、week(一周)、month(一个月)、year(一年)

    ## 返回数据
    - 搜索结果列表，包含URL和内容摘要

    ## 示例
    ```
    GET /api/v1/search/tavily?query=人工智能&topic=general&max_results=5
    ```
    """
    try:
        result = _tavily_search(query, topic, max_results, time_range)

        logger.info(f"Tavily搜索成功: {query}")

        return resp_200(data={
            "query": query,
            "results": result
        })

    except Exception as e:
        logger.error(f"Tavily搜索失败: {e}")
        return resp_500(message=f"搜索失败: {str(e)}")


@router.post("/search/bocha", response_model=UnifiedResponseModel)
async def search_with_bocha(
    query: str = Body(description="搜索关键词"),
    count: int = Body(default=10, description="返回结果条数，范围1-50"),
    freshness: Literal["noLimit", "oneDay", "oneWeek", "oneMonth", "oneYear"] = Body(default="noLimit", description="时间范围"),
    summary: bool = Body(default=True, description="是否返回文本摘要"),
    include: Optional[str] = Body(default=None, description="限定搜索的网站域名"),
    exclude: Optional[str] = Body(default=None, description="排除的网站域名")
):
    """
    使用博查(Bocha)进行联网搜索

    ## 参数说明
    - query: 搜索关键词（必填）
    - count: 返回结果条数，范围1-50，默认10
    - freshness: 时间范围，默认noLimit，可选：oneDay、oneWeek、oneMonth、oneYear
    - summary: 是否返回文本摘要，默认True
    - include: 限定搜索的网站域名，多个用|或,分隔
    - exclude: 排除的网站域名，多个用|或,分隔

    ## 返回数据
    - 搜索结果列表，包含标题、URL、摘要、网站名称等

    ## 示例
    ```json
    {
      "query": "机器学习",
      "count": 10,
      "freshness": "oneWeek",
      "summary": true
    }
    ```
    """
    try:
        result = bocha_search.invoke({
            "query": query,
            "count": count,
            "freshness": freshness,
            "summary": summary,
            "include": include,
            "exclude": exclude
        })

        logger.info(f"Bocha搜索成功: {query}")

        return resp_200(data={
            "query": query,
            "results": result
        })

    except Exception as e:
        logger.error(f"Bocha搜索失败: {e}")
        return resp_500(message=f"搜索失败: {str(e)}")
