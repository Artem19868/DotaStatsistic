from models import Item
import os
import json

class ItemManager:
    def __init__(self, items_ids: list):
        self.items_ids = items_ids
        self.items_data = self._load_items_data()
        self.items_by_id = {}
        self._create_items_mapping_by_id()

    def _load_items_data(self):
        items_data_path = os.path.join(os.path.dirname(__file__), 'constants', 'items.json')
        with open(items_data_path,'r',encoding='utf-8') as f:
            data = json.load(f)
            return list(data.values())
        
    def _create_items_mapping_by_id(self):
        self.items_by_id = {item['id']: item for item in self.items_data}

    def get_item_model(self, item_id):
        if item_id == 0:
            return Item()
        else:
            item = Item(id=item_id,
                        price=self.items_by_id.get(item_id).get('cost'),
                        image_url=self.items_by_id.get(item_id).get('img'),
                        display_name=self.items_by_id.get(item_id).get('dname'))
            return item