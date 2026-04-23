"""
论文检索接口
"""
from fastapi import APIRouter, Query
from agentchat.schema.schemas import UnifiedResponseModel, resp_200, resp_500
from agentchat.tools.arxiv.action import _get_arxiv
from loguru import logger

router = APIRouter(tags=["Arxiv"])


@router.get("/arxiv/search", response_model=UnifiedResponseModel)
async def search_arxiv(
    query: str = Query(description="搜索关键词，例如：machine learning、deep learning")
):
    """
    在 Arxiv 上搜索论文

    ## 参数说明
    - query: 搜索关键词（必填），支持英文关键词

    ## 返回数据
    - 相关论文的详细信息，包括标题、作者、摘要、发布日期等

    ## 示例
    ```
    GET /api/v1/arxiv/search?query=machine learning
    ```
    """
    try:
        result = _get_arxiv(query)

        logger.info(f"Arxiv搜索成功: {query}")

        return resp_200(data={
            "query": query,
            "papers": result
        })

    except Exception as e:
        logger.error(f"Arxiv搜索失败: {e}")
        return resp_500(message=f"搜索论文失败: {str(e)}")
