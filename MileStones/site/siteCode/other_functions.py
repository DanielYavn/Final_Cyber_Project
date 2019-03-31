from siteCode import app
import os


def download_and_remove(path, user_filename):
    # path = os.path.join(app.instance_path, filename)

    def generate():
        with open(path, "rb") as f:
            yield f.read()
            # yield from f

        os.remove(path)

    r = app.response_class(generate(), mimetype='text/csv')
    r.headers.set('Content-Disposition', 'attachment', filename=user_filename)
    return r
