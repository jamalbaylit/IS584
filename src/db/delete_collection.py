from config import *
if __name__=="__main__":
    collection_name = DB_DOC_COLLECTION_NAME
    dbclient.collections.delete(collection_name)
    # dbclient.collections.delete_all()
    dbclient.close()