import base64
import os
import shutil
import tarfile
import tempfile
from io import BytesIO

def _find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def make_tarfile_string(source_dir):
    f = open("/tmp/faketar.tar.gz", "wb")
    with tarfile.open(mode="w:gz", fileobj=f) as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    f.close()
    archive = open("/tmp/faketar.tar.gz", "rb").read()
    return base64.encodestring(archive)

def save_tensorflow_graph(sess):
    """
    save_tensorflow_graph will save a tensorflow graph as a base64 encoded tar
    file string and return it
    """
    import tensorflow as tf

    tempdir = tempfile.mkdtemp(suffix="_yhat")
    checkpoint_dest = os.path.join(tempdir, "session.checkpoint")
    saver = tf.train.Saver()
    saver.save(sess, checkpoint_dest)
    b64_tarfile = make_tarfile_string(checkpoint_dest).decode()
    shutil.rmtree(tempdir)
    return b64_tarfile

def load_tensorflow_graph(s):
    """
    load_tensorflow_graph will load a tensorflow session from a base64 encoded
    string
    """
    import tensorflow as tf
    # if we don't have bytes already, try to convert
    if not isinstance(s, bytes):
        try:
            s = s.encode()
        except Exception:
            print("Please supply a file opened in binary mode, open(model, 'rb')")
    dest = tempfile.mkdtemp(suffix="_yhat")
    s = base64.decodestring(s)
    f = BytesIO(s)
    tar = tarfile.open(mode="r:gz", fileobj=f)
    tar.extractall(path=dest)
    checkpoint_file = _find_file("session.checkpoint", dest)
    sess = tf.InteractiveSession()
    saver = tf.train.Saver()
    saver.restore(sess, checkpoint_file)
    return sess, None

def save_spark_model(sc, model):
    """
    save_spark_model will take a spark context and a spark model, and return a
    base64 encoded string containing the model name, model class, and a tar
    containing the spark model
    """
    f = tempfile.mkdtemp(suffix="_yhat")
    model.save(sc, f)
    b64_tarfile = make_tarfile_string(f).decode()
    b64_tarfile = "%s|%s|%s" % (model.__module__, model.__class__.__name__, b64_tarfile)
    shutil.rmtree(f)
    return b64_tarfile

def load_spark_model(sc, s):
    """
    load_spark_model takes the base64 encoded bytes generated with
    save_spark_model and loads it into the current python session.
    """
    # if we don't have bytes already, try to convert
    if not isinstance(s, bytes):
        try:
            s = s.encode()
        except Exception:
            print("Please supply a file opened in binary mode, open(model, 'rb')")
    dest = tempfile.mkdtemp(suffix="_yhat")
    lib, classname, s = s.split(b"|")
    # Sometimes the padding is wrong on this, so fix it here
    s += b'=' * (-len(s) % 4)
    s = base64.decodestring(s)
    f = BytesIO(s)
    tar = tarfile.open(mode="r:gz", fileobj=f)
    tar.extractall(path=dest)
    modeldir = os.listdir(dest)[0] # i know, i know. shame on me.
    modeldirectory = os.path.join(dest, modeldir)
    # i see you judging me
    exec("from %s import %s" % (lib.decode(), classname.decode()))
    return eval("%s.load(sc, '%s')" % (classname.decode(), modeldirectory))
