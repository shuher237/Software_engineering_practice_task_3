from app import app
from pyngrok import ngrok

import uvicorn
import nest_asyncio


ngrok_tunnel = ngrok.connect(8000)
print('Public URL:', ngrok_tunnel.public_url)
nest_asyncio.apply()
uvicorn.run(app, port=8000)
