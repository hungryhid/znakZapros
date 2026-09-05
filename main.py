import fastapi
import uvicorn
import selectors
from database import base, engine
from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def lifespan(app):
    await startup()
    yield
    await shutdown()

async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)

async def shutdown():
    await engine.dispose()

app = fastapi.FastAPI(lifespan=lifespan)



@app.get("/")
def home():
    pass

def make_selector_loop() -> asyncio.AbstractEventLoop:
    return asyncio.SelectorEventLoop(selectors.SelectSelector())

async def main():
    config = uvicorn.Config(
        app=app, 
        host="127.0.0.1", 
        port=8000
    )
    server = uvicorn.Server(config)
    
    await server.serve()



if __name__ == "__main__":
    with asyncio.Runner(loop_factory=make_selector_loop) as runner:
        runner.run(main())
        
    
