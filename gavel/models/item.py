from gavel.models import db
import gavel.crowd_bt as crowd_bt
from sqlalchemy.orm.exc import NoResultFound

view_table = db.Table('view',
    db.Column('item_id', db.Integer, db.ForeignKey('item.id')),
    db.Column('annotator_id', db.Integer, db.ForeignKey('annotator.id'))
)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    floor = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    categories = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    viewed = db.relationship('Annotator', secondary=view_table)
    prioritized = db.Column(db.Boolean, default=False, nullable=False)

    mu = db.Column(db.Float)
    sigma_sq = db.Column(db.Float)

    def __init__(self, name, location, url, description, categories):
        self.name = name
        self.location, self.floor = self.calculate_initial_floor(location)
        self.url = url
        self.description = description
        self.categories = categories
        self.mu = crowd_bt.MU_PRIOR
        self.sigma_sq = crowd_bt.SIGMA_SQ_PRIOR

    def calculate_initial_floor(self, location):
        if table <= 125:
            return str(table), "1st Floor, Outside Hallways"
        elif table <= 162: # 301-337
            return str(table - 125 + 300), "1st Floor, Outside Hallways"
        else: # 401-XXX
            return str(table - 162 + 400), "1st Floor, Outside Hallways"
    
    def get_categories(self):
        return [category.strip() for category in (self.categories or "").split(",") if category.strip() != ""]

    @classmethod
    def by_id(cls, uid):
        if uid is None:
            return None
        try:
            item = cls.query.get(uid)
        except NoResultFound:
            item = None
        return item
