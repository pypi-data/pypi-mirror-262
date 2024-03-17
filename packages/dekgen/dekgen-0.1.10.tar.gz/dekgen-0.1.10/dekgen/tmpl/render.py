import os
from dektools.yaml import yaml
from dektools.dict import dict_merge
from dektools.attr import object_path_update
from .template import TemplateWide


class RenderTemplate(TemplateWide):
    file_ignore_tpl = [f"../{x}" for x in TemplateWide.file_ignore_tpl]
    file_ignore_override = [f"../{x}" for x in TemplateWide.file_ignore_override]
    file_ignore = [f"../{x}" for x in TemplateWide.file_ignore]


def render_path(dest, src, files=None, updated=None, **kwargs):
    data = {}
    path_values = os.path.join(src, 'values.yaml')
    if os.path.isfile(path_values):
        data = dict(Values=yaml.load(path_values))
    if files:
        for f in files:
            strict = True
            if f.startswith('?'):
                f = f[1:]
                strict = False
            if not strict and not os.path.isfile(f):
                continue
            dict_merge(data, dict(Values=yaml.load(f)))
    if updated:
        object_path_update(data, updated)
    if os.path.isdir(dest) or os.path.isdir(src):
        RenderTemplate(data, **kwargs).render_dir(dest, os.path.join(src, 'templates'))
    elif os.path.isfile(src):
        RenderTemplate(data, **kwargs).render_file(dest, src)
