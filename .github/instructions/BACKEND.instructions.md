---
applyTo: "backend/**/*"
---

This project utilizes django 5.2 or higher, daisyUI5 and enforces CSP via the django-csp package.  
* Use {% load static %} for static files, not hardcoded paths
* Use {% url 'view_name' %} for internal links, not hardcoded URLs
* Always include {% csrf_token %} in forms
* Use Django's built-in template filters when available
* All JavaScript must use nonce="{{request.csp_nonce}}"
* Use addEventListener() instead of onclick attributes
* Event handlers must be in separate script blocks, not inline
* Use Django ModelForms when possible
* Include proper error handling in templates
* Use Django's form widgets with daisyUI classes
* Extend base templates using {% extends "path/to/base.html" %}
* Use {% include %} for reusable components
* Keep template logic minimal, use view context instead
* All template block tags must have the block name in the endblock tag



