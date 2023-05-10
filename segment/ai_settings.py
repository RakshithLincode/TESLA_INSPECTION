
SERVER_HOST = "localhost"

#Settings for MongoDB
MONGO_SERVER_HOST = SERVER_HOST
MONGO_SERVER_PORT = 27017
#MONGO_DB = "LIVIS"
MONGO_DB = "DEMO"
INSPECTION_DATA_COLLECTION = "inspection_summary"
MONGO_COLLECTION_PARTS = "parts"
MONGO_COLLECTIONS = {MONGO_COLLECTION_PARTS: "parts"}
WORKSTATION_COLLECTION = 'workstations'
PARTS_COLLECTION = 'parts'
SHIFT_COLLECTION = 'shift'
# PLAN_COLLECTION = 'plan'


# #Settings for Redis
REDIS_CLIENT_HOST = "localhost"
REDIS_CLIENT_PORT = 6379

# MONGO_DB = "Indo_trial"
# INSPECTION_DATA_COLLECTION = "inspection_summary"
# MONGO_COLLECTION_PARTS = "parts"
# MONGO_COLLECTIONS = {"MONGO_COLLECTION_PARTS": "parts" ,"INSPECTION_DATA_COLLECTION" :"inspection_summary" ,"SHIFT_COLLECTION" : 'shift'}
# WORKSTATION_COLLECTION = 'workstation'
# PARTS_COLLECTION = 'parts'
# SHIFT_COLLECTION = 'shift'

original_frame_keyholder = "original_frame"
predicted_frame_keyholder = "predicted_frame"

data_drive_path = ""