import os
import tarfile
import StringIO
import base64
import tempfile
import importlib
import shutil

def make_tarfile_string(source_dir):
    f = StringIO.StringIO()
    with tarfile.open(mode="w:gz", fileobj=f) as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    archive = f.getvalue()
    return base64.encodestring(archive)

def save_tensorflow_graph(sess):
    import tensorflow as tf
    from tensorflow.contrib.session_bundle import exporter

    f = tempfile.mkdtemp(suffix="_yhat")
    saver = tf.train.Saver(sharded=True)
    model_exporter = exporter.Exporter(saver)
    model_exporter.init(sess.graph.as_graph_def())
    model_exporter.export(f, tf.constant(1), sess)

    b64_tarfile = make_tarfile_string(f)
    shutil.rmtree(f)
    return b64_tarfile

def _find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def load_tensorflow_graph(s):
    from tensorflow.contrib.session_bundle import session_bundle

    dest = tempfile.mkdtemp(suffix="_yhat")
    s = base64.decodestring(s)
    f = StringIO.StringIO(s)
    tar = tarfile.open(mode="r:gz", fileobj=f)
    tar.extractall(path=dest)
    graphdir = os.path.dirname(_find_file("export.meta", dest))
    graphdirectory = os.path.join(dest, graphdir)

    return session_bundle.load_session_bundle_from_path(graphdirectory)

def save_spark_model(sc, model):
    f = tempfile.mkdtemp(suffix="_yhat")
    model.save(sc, f)
    b64_tarfile = make_tarfile_string(f)
    b64_tarfile = "%s|%s|%s" % (model.__module__, model.__class__.__name__, b64_tarfile)
    shutil.rmtree(f)
    return b64_tarfile

def load_spark_model(sc, s):
    dest = tempfile.mkdtemp(suffix="_yhat")
    lib, classname, s = s.split("|")
    s = base64.decodestring(s)
    f = StringIO.StringIO(s)
    tar = tarfile.open(mode="r:gz", fileobj=f)
    tar.extractall(path=dest)
    modeldir = os.listdir(dest)[0] # i know, i know. shame on me.
    modeldirectory = os.path.join(dest, modeldir)
    # i see you judging me
    exec("from %s import %s" % (lib, classname))
    return eval("%s.load(sc, '%s')" % (classname, modeldirectory))
