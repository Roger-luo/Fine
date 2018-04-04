import os
from .parser import Presentation
from flask import (Blueprint, current_app, render_template,
                   send_from_directory, url_for)


blueprint = Blueprint('fine', __name__)


@blueprint.route('/')
def index():
    meta = current_app.config.get('META')
    source_path = os.path.join(
        current_app.root_path,
        current_app.config['SOURCE_DIR']
    )

    contents = []
    for each in os.listdir(source_path):
        if each.endswith('.md'):
            path = os.path.join(source_path, each)
            with open(path, 'r') as f:
                pre = Presentation(f.read())

            configs = pre.meta
            configs['file'] = each[:-3]
            contents.append(configs)

    return render_template('index.html', contents=contents, meta=meta)


@blueprint.route('/media/<filename>')
def get_img(filename):
    media = os.path.join(current_app.root_path,
                         current_app.config.get('MEDIA_DIR'))
    return send_from_directory(media, filename)

@blueprint.route('/revealjs/<path:filename>')
def revealjs(filename):
    static_path = os.path.join(os.path.dirname(__file__), 'static/revealjs')
    return send_from_directory(static_path, filename)

@blueprint.route('/<name>/')
def presentation(name):
    defaults = current_app.config['REVEAL']
    md_extensions = current_app.config['MARKDOWN']
    configs = defaults['config']
    theme = defaults['theme']

    name, _ = os.path.splitext(name)
    filepath = os.path.join(
        current_app.root_path,
        current_app.config['SOURCE_DIR'],
        name + '.md'
    )

    with open(filepath, 'r') as f:
        pre = Presentation(**md_extensions)
        pre.parse(f.read())

    if 'reveal' in pre.meta:
        if 'config' in pre.meta['reveal']:
            configs.update(pre.meta['reveal']['config'])
        if 'theme' in pre.meta['reveal']:
            theme = pre.meta['reveal']['theme']

    theme = (url_for('fine.revealjs', filename='css/theme/') +
             theme + '.css')

    context = {
        'meta': pre.meta,
        'frames': pre.frames,
        'config': configs,
        'theme': theme,
    }
    return render_template('presentation.html', **context)
