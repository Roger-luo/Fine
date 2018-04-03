import os
import yaml
import jinja2

from flask import Flask as BaseFlask, Config as BaseConfig
from .blueprints import blueprint


class Config(BaseConfig):

    def from_yaml(self, config_file):
        env = os.environ.get('FLASK_ENV', 'development')
        self['ENVIRONMENT'] = env.lower()

        with open(config_file) as f:
            c = yaml.load(f)

        c = c.get(env, c)

        for key in c:
            self[key.upper()] = c[key]


class Fine(BaseFlask):

    def __init__(self, import_name, **kwargs):
        super(Fine, self).__init__(import_name, **kwargs)
        self.register_blueprint(blueprint)
        self.load_default_config()

        # load templates in both project and user folders
        self.jinja_loader = jinja2.ChoiceLoader([
            self.jinja_loader,
            jinja2.FileSystemLoader([
                os.path.join(os.path.dirname(__file__), 'templates')
            ])
        ])

    def load_default_config(self):
        root_path = os.path.dirname(__file__)
        config_path = os.path.join(root_path, 'config.yml')
        if not os.path.isfile(config_path):
            return
        self.config.from_yaml(config_path)

    def load_config(self, filename='config.yml'):
        root_path = self.root_path
        config_path = os.path.join(root_path, filename)
        if not os.path.isfile(config_path):
            return
        self.config.from_yaml(config_path)

    def make_config(self, instance_relative=False):
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return Config(root_path, self.default_config)
