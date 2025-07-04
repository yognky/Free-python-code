from http.server import BaseHTTPRequestHandler, HTTPServer

host = "0.0.0.0"
port = 8080

# === HTML BERITA DARK MODE ===
html_berita = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Yongky Cyber News</title>
    <style>
        body {
            background-color: #121212;
            color: #f1f1f1;
            font-family: Arial, sans-serif;
            padding: 40px;
            line-height: 1.7;
        }
        h1 {
            color: #ffffff;
        }
        .card {
            background: #1e1e1e;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 0 10px #00000055;
        }
        a {
            color: #66b2ff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>📰 Yongky Cyber News</h1>
    <div class="card">
        <h2>[TEROBOSAN] Python Tools Anti-DDoS Gratis!</h2>
        <p>Yongky telah merilis tool anti-DDoS gratis bersumber Python yang dapat digunakan untuk melindungi server publik dari serangan Layer 7. <a href="#">Cek selengkapnya &raquo;</a></p>
    </div>
    <div class="card">
        <h2>[BARU] Deteksi Backdoor JS Otomatis</h2>
        <p>Tool analisa JavaScript berbasis AI kini tersedia gratis! Deteksi spyware dan fungsi tersembunyi hanya dalam 1 klik. <a href="#">Pelajari di sini &raquo;</a></p>
    </div>
</body>
</html>
"""

# === HANDLER SERVER ===
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"📥 GET dari {self.client_address[0]} ke {self.path}")
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_berita.encode('utf-8'))

if __name__ == "__main__":
    print(f"🚀 Server berita aktif di http://{host}:{port}")
    server = HTTPServer((host, port), RequestHandler)
    server.serve_forever()
