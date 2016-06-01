def document(app):
    for r in app.router.routes():
        print(r.method)
        print(r._resource)
        print(r.handler)
        print(r.handler.__doc__)
        print(getattr(r.handler, "_input_schema"))
        print(getattr(r.handler, "_output_schema"))

    return app
