import user_access.dependencies as dependencies

from nameko.rpc import rpc

class UserAccessService:

    name = 'user_access_service'

    database = dependencies.Database()

    @rpc
    def add_user(self, userAccount, userPassword):
        user = self.database.add_user(userAccount, userPassword)
        return user

    @rpc
    def get_user(self, userAccount, userPassword):
        user = self.database.get_user(userAccount, userPassword)
        return user