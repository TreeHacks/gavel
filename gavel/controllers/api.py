from gavel import app
from gavel.models import *
import gavel.utils as utils
from flask import Response, send_file
from openpyxl import Workbook
from io import BytesIO
from tempfile import NamedTemporaryFile

def _dump_items(items):
    data = [['Mu', 'Sigma Squared', 'Name', 'Table', 'Floor', 'Categories', 'Description', 'Active']]
    data += [[
        str(item.mu),
        str(item.sigma_sq),
        item.name,
        item.location,
        item.floor,
        item.categories,
        item.description,
        item.active
    ] for item in items]
    return data

@app.route('/api/items.csv')
@app.route('/api/projects.csv')
@utils.requires_auth
def item_dump():
    items = Item.query.order_by(desc(Item.mu)).all()
    data = _dump_items(items)
    return Response(utils.data_to_csv_string(data), mimetype='text/csv')

@app.route('/api/items_by_category.xlsx')
@utils.requires_auth
def item_dump_by_category():
    items = Item.query.order_by(desc(Item.mu)).all()
    categories = utils.get_all_categories(items)
    wb = Workbook()
    ws = wb.active
    for row in _dump_items(items):
        ws.append(row)
    for category in categories:
        ws = wb.create_sheet(category.replace("*","").replace(":","").replace("/","").replace("\\","").replace("?","").replace("[","").replace("]",""))
        for row in _dump_items([item for item in items if category in item.get_categories()]):
            ws.append(row)
    out = BytesIO()
    wb.save(out)
    out.seek(0)
    return send_file(
        out,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        attachment_filename='items_by_category.xlsx', as_attachment=True
    )


@app.route('/api/annotators.csv')
@app.route('/api/judges.csv')
@utils.requires_auth
def annotator_dump():
    annotators = Annotator.query.all()
    data = [['Name', 'Email', 'Description', 'Secret']]
    data += [[
        str(a.name),
        a.email,
        a.description,
        a.secret
    ] for a in annotators]
    return Response(utils.data_to_csv_string(data), mimetype='text/csv')

@app.route('/api/decisions.csv')
@utils.requires_auth
def decisions_dump():
    decisions = Decision.query.all()
    data = [['Annotator ID', 'Winner ID', 'Loser ID', 'Time']]
    data += [[
        str(d.annotator.id),
        str(d.winner.id),
        str(d.loser.id),
        str(d.time)
    ] for d in decisions]
    return Response(utils.data_to_csv_string(data), mimetype='text/csv')
