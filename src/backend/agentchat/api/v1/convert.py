"""
文件格式转换接口
"""
from fastapi import APIRouter, Body, UploadFile, File
from agentchat.schema.schemas import UnifiedResponseModel, resp_200, resp_500
from agentchat.tools.convert_to_pdf.action import _convert_to_pdf
from agentchat.tools.convert_to_docx.action import _convert_to_docx
from loguru import logger

router = APIRouter(tags=["Convert"])


@router.post("/convert/to-pdf", response_model=UnifiedResponseModel)
async def convert_docx_to_pdf(
    file_url: str = Body(description="DOCX文件的URL地址")
):
    """
    将 DOCX 文件转换为 PDF

    ## 参数说明
    - file_url: DOCX文件的URL地址（必填）

    ## 返回数据
    - 转换后的PDF文件下载链接

    ## 支持格式
    - docx, doc, odt, rtf, txt, html, htm, xls, xlsx, ods, ppt, pptx, odp

    ## 示例
    ```json
    {
      "file_url": "https://example.com/document.docx"
    }
    ```
    """
    try:
        result = _convert_to_pdf(file_url)

        if "解析成功" in result:
            logger.info(f"文件转换成功: {file_url}")
            return resp_200(data={"message": result})
        else:
            logger.error(f"文件转换失败: {result}")
            return resp_500(message=result)

    except Exception as e:
        logger.error(f"文件转换异常: {e}")
        return resp_500(message=f"文件转换失败: {str(e)}")


@router.post("/convert/to-docx", response_model=UnifiedResponseModel)
async def convert_pdf_to_docx(
    file_url: str = Body(description="PDF文件的URL地址")
):
    """
    将 PDF 文件转换为 DOCX

    ## 参数说明
    - file_url: PDF文件的URL地址（必填）

    ## 返回数据
    - 转换后的DOCX文件下载链接

    ## 示例
    ```json
    {
      "file_url": "https://example.com/document.pdf"
    }
    ```
    """
    try:
        result = _convert_to_docx(file_url)

        if "解析成功" in result:
            logger.info(f"文件转换成功: {file_url}")
            return resp_200(data={"message": result})
        else:
            logger.error(f"文件转换失败: {result}")
            return resp_500(message=result)

    except Exception as e:
        logger.error(f"文件转换异常: {e}")
        return resp_500(message=f"文件转换失败: {str(e)}")
