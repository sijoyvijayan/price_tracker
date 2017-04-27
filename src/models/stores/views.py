from flask import Blueprint
from flask import json
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect

from src.models.stores.store import Store

import src.models.users.decorators as user_decorators

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')
def index():
    stores = Store.get_all_stores()
    return render_template('/stores/store_list.html', stores=stores)


@store_blueprint.route('/store/<string:store_id>')
def store_page(store_id):
    return render_template('/stores/store.html', store=Store.get_by_id(store_id))


@store_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_admin_access
def create_store():
    if request.method == 'POST':
        store_name = request.form['name']
        url_prefix = request.form['url_prefix']

        item_price_tag = request.form['item_price_tag']
        item_price_query = json.loads(request.form['item_price_query'])

        item_name_tag = request.form['item_name_tag']
        item_name_query = json.loads(request.form['item_name_query'])

        Store(name=store_name, url_prefix=url_prefix, tag_name=item_price_tag, query=item_price_query,
              item_name_tag=item_name_tag, item_name_query=item_name_query).save_to_mongo()
        return redirect(url_for('.index'))

    return render_template('/stores/create_store.html')


@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@user_decorators.requires_admin_access
def edit_store(store_id):
    store = Store.get_by_id(store_id)
    if request.method == 'POST':
        store_name = request.form['name']
        url_prefix = request.form['url_prefix']

        item_price_tag = request.form['item_price_tag']
        item_price_query = json.loads(request.form['item_price_query'])

        item_name_tag = request.form['item_name_tag']
        item_name_query = json.loads(request.form['item_name_query'])

        store.name = store_name
        store.url_prefix = url_prefix
        store.tag_name = item_price_tag
        store.query = item_price_query
        store.item_name_tag = item_name_tag
        store.item_name_query = item_name_query

        store.save_to_mongo()

        return redirect(url_for('.store_page', store_id=store._id))

    return render_template('/stores/edit_store.html', store=store)


@store_blueprint.route('/delete/<string:store_id>')
@user_decorators.requires_admin_access
def delete_store(store_id):
    Store.get_by_id(store_id).delete()
    return redirect(url_for('.index'))
