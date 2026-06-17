from db_connection import DB_connection

class AgentDB:
    def __init__(self):
        self.connection = DB_connection.get_connection()
        
        
    def create_agent(data):
        sql = """INSERT INTO agents VALUES()"""



    def get_all_agents():
        pass
    def get_agent_by_id(id):
        pass
    def update_agent(id, data):
        pass
    def deactivate_agent(id):
        pass
    def increment_completed(id):
        pass
    def increment_failed(id):
        pass
    def get_agent_performance(id):
        pass
    def count_active_agents():
        pass






#carte connection of db in the init?
#what has to be in init of agentdb
#data is just values?