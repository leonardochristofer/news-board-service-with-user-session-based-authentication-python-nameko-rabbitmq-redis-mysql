import news_board.dependencies as dependencies

from nameko.rpc import rpc

class NewsBoardService:

    name = 'news_board_service'

    database = dependencies.Database()

    # Create
    @rpc
    def add_news(self, newsTitle, newsDetail, fileUrl, createdAt):
        news = self.database.add_news(newsTitle, newsDetail, fileUrl, createdAt)
        return news

    # Read
    @rpc
    def get_all_news(self):
        news = self.database.get_all_news()
        return news

    @rpc
    def get_news_by_id(self, newsId):
        news = self.database.get_news_by_id(newsId)
        return news

    @rpc
    def download_file_by_id(self, newsId):
        news = self.database.download_file_by_id(newsId)
        return news

    # Update
    @rpc
    def edit_news(self, newsId, newsTitle, newsDetail, fileUrl, updatedAt):
        news = self.database.edit_news(newsId, newsTitle, newsDetail, fileUrl, updatedAt)
        return news

    # Delete
    @rpc
    def delete_news(self, newsId):
        news = self.database.delete_news(newsId)
        return news