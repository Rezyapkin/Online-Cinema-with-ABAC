from gevent import monkey

# it should be called as fast as it possible
monkey.patch_all()

from app import app  # noqa: F401, E402
