from fastapi import FastAPI, applications
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from fastapi.openapi.docs import get_swagger_ui_html
from contextlib import asynccontextmanager


from geeked import Geeked


def swagger_monkey_patch(*args, **kwargs):
    """
    Wrap the function which is generating the HTML for the /docs endpoint and
    overwrite the default values for the swagger js and css.
    """
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url="static/swagger/swagger-ui-bundle.min.js",
        swagger_css_url="static/swagger/swagger-ui.min.css"
    )


applications.get_swagger_ui_html = swagger_monkey_patch


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="./static"), name="static")

# 设置允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许的 HTTP 请求方法
    allow_headers=["*"],  # 允许所有标头
    expose_headers=["x-request-id"],
)


@app.get("/")
async def root():
    return {"message": "live"}


class GtParams(BaseModel):
    captcha_id: str = Field(
        default="6ba6b71b4f3958a1c69ad839ba47836b", title="captcha_id", max_length=128
    )
    risk_type: str = Field(
        default="slide", title="验证码的类别,icon,sign,slide三种类别", max_length=128
    )
    proxy: str = Field(default="", title="请求的代理", max_length=128)
    referer: str = Field(default="", title="referer", max_length=128)
    user_agent: str = Field(default="", title="user_agent", max_length=128)


#  caa87cc3faeac1b7fd942fbbe6ef6ca0 f15827325743@163.com
#  6ba6b71b4f3958a1c69ad839ba47836b geetest


@app.post("/api/geetest/v4/verify")
async def GeetestV4Verify(item: GtParams):
    """
    极验验证码4.0接口 verify 接口
    验证码参考demo地址:https://gt4.geetest.com/demov4/index-en.html
    """
    geetest_result = {}
    try:
        geeked = Geeked(
            captcha_id=item.captcha_id,
            risk_type=item.risk_type,
            proxy=item.proxy,
            verify=False,
        )
        geetest_result = geeked.solve()
        geetest_result["status"] = 200 * 100
    except Exception as e:
        geetest_result["error_info"] = str(e)
        geetest_result["status"] = 0
    return {"geetest_result": geetest_result}


# https://decodecaptcha.com/system/onlinetest/?lang=zh

# https://github.com/pysunday/sdenv

# https://ip.zhengbingdong.com/