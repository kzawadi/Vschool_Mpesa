from waitress import serve
import app

serve(app.app, port=80, threads=8)
