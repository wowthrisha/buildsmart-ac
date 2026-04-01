import ast
import os
import glob
import re

def get_models_fields():
    models = {}
    if not os.path.exists('app/models.py'): return models
    
    code = open('app/models.py').read()
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            fields = []
            for child in node.body:
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name):
                            if isinstance(child.value, ast.Call):
                                fname = getattr(child.value.func, 'id', '') or getattr(child.value.func, 'attr', '')
                                if fname in ['Column', 'relationship']:
                                    fields.append(target.id)
            if fields:
                # very basic lower case mapping
                model_key = node.name.lower()
                models[model_key] = fields
    return models

def audit_templates_for_fields(models):
    mismatches = []
    count = 1
    html_files = glob.glob('app/templates/**/*.html', recursive=True)
    
    # manual model hint mapping due to typical variable names
    # e.g., 'project.client_name' -> accesses Project table
    var_to_model = {
        'project': 'project',
        'p': 'project',
        'user': 'user',
        'client': 'user',
        'architect': 'user',
        'current_user': 'user',
        'payment': 'payment',
        'doc': 'document',
        'document': 'document',
        'plot': 'plot',
        'meeting': 'meeting',
        'activity': 'activitylog',
        'log': 'activitylog'
    }
    
    for f in html_files:
        content = open(f).read()
        
        # find {{ obj.field }} or {% if obj.field %}
        # Also could catch obj.field() if it's a method
        accesses = set(re.findall(r'([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)(?!\()', content))
        
        for obj, field in accesses:
            # ignore common jinja/flask builtins
            if obj in ['request', 'session', 'config', 'url_for', 'loop', 'g']: continue
            if field in ['id', 'created_at', 'updated_at', 'length', 'append', 'keys', 'values', 'items', 'update']: continue
            
            model_name = var_to_model.get(obj.lower(), obj.lower())
            if model_name in models:
                if field not in models[model_name] and not field.startswith('get_'):
                    mismatches.append(f"""╔══════════════════════════════════════════════╗
║ FIELD MISMATCH #{count}                            ║
╠══════════════════════════════════════════════╣
║ Template       : {f}
║ Template uses  : {{{{{obj}.{field}}}}}
║ Model reality  : FIELD DOES NOT EXIST ON '{model_name.capitalize()}'
║ Type mismatch  : N/A
║ Runtime error  : AttributeError / jinja silent error
║ Fix            : Update template to use a valid field, or add column to models.py
╚══════════════════════════════════════════════╝""")
                    count += 1
    
    return mismatches

mismatches = audit_templates_for_fields(get_models_fields())

out = open('docs/AUDIT_REPORT.md', 'a')
out.write("## ═══ PASS 4 — MODEL & TEMPLATE FIELD MISMATCH AUDIT ═══\n\n")
for m in mismatches:
    out.write(m + "\n\n")
out.write(f"PASS 4 COMPLETE. {len(mismatches)} field mismatches found.\n\n")
out.close()
