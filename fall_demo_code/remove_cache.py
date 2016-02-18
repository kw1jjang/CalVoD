import db_manager
import helper

nodes_info = db_manager.get_all_nodes()
for each in nodes_info:
  if str(each.type_of_node) == 'cache':
    db_manager.remove_cache(each.ip, each.port)