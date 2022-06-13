import json

from nameko.web.handlers import http
from werkzeug.wrappers import Response
from nameko.rpc import RpcProxy

from datetime import datetime

from gateway.session import SessionProvider

class GatewayService:

    name = "gateway_service"

    user_access_rpc = RpcProxy('user_access_service')

    news_board_rpc = RpcProxy('news_board_service')

    session_provider = SessionProvider()

    # Have to login first
    @http('POST', '/logout')
    def logout(self, request):
        cookies = request.cookies
        if cookies:
            session_data = self.session_provider.delete_session(cookies['sessionId'])
            response = Response('Logged Out Successfully')
            return response
        else:
            response = Response('Bad Request')
            return response

    @http('POST', '/add-news')
    def add_news(self, request):
        cookies = request.cookies
        if cookies:
            createdAt = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            data = request.json
            result = self.news_board_rpc.add_news(data['newsTitle'], data['newsDetail'], data['fileUrl'], createdAt)
            return result
        else:
            response = Response('You Will Need To Login First')
            return response

    @http('POST', '/edit-news')
    def edit_news(self, request):
        cookies = request.cookies
        if cookies:
            updatedAt = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            data = request.json
            result = self.news_board_rpc.edit_news(data['newsId'], data['newsTitle'], data['newsDetail'], data['fileUrl'], updatedAt)
            return result
        else:
            response = Response('You Will Need To Login First')
            return response

    @http('POST', '/delete-news')
    def delete_news(self, request):
        cookies = request.cookies
        if cookies:
            data = request.json
            result = self.news_board_rpc.delete_news(data['newsId'])
            return result
        else:
            response = Response('You Will Need To Login First')
            return response

    # Does not have to login first
    @http('POST', '/register')
    def add_user(self, request):
        data = request.json
        result = self.user_access_rpc.add_user(data['userAccount'], data['userPassword'])
        return result

    @http('POST', '/login')
    def get_user(self, request):
        data = request.json
        result = self.user_access_rpc.get_user(data['userAccount'], data['userPassword'])
        response = ""
        if result:
            session_id = self.session_provider.set_session(result)
            response = Response(str(result))
            response.set_cookie('sessionId', session_id)
            return response
        else:
            return response + "Invalid Login"

    @http('GET', '/get-all-news')
    def get_all_news(self, request):
        result = self.news_board_rpc.get_all_news()
        return json.dumps(result)

    @http('POST', '/get-news-by-id')
    def get_news_by_id(self, request):
        data = request.json
        result = self.news_board_rpc.get_news_by_id(data['newsId'])
        return json.dumps(result)

    @http('POST', '/download-file-by-id')
    def download_file_by_id(self, request):
        data = request.json
        result = self.news_board_rpc.download_file_by_id(data['newsId'])
        return json.dumps(result)
