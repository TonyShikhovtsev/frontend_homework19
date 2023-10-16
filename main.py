from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    """
    Класс определяющий обработку запросов пользователя

    """
    def __get_html_content(self):
        """Метод получения html разметки из файла index.html"""
        file_path = "index.html"

        try:
            with open(file_path, "r") as file:
                html_content = file.read()
                return html_content
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден.")
            return None
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return None


    def do_GET(self):
        """
        Функция обработки входящих GET-запросов
        """
        query_components = parse_qs(urlparse(self.path).query)
        print(query_components)
        page_content = self.__get_html_content()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(page_content, "utf-8"))

if __name__ == "__main__":
    # Инициализация веб-сервера
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")
