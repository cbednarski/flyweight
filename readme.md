# Flyweight

Flyweight is a lightweight commandline tool for building CDNs using Amazon S3 and CloudFront.

[![Build Status](https://travis-ci.org/cbednarski/flyweight.png)]
(https://travis-ci.org/cbednarski/flyweight)

### How it works

Flyweight starts by looking for tags in your git repos that match [SemVer](http://semver.org/) version numbers. Flyweight enumerates these tags and pulls assets like images, css, and javascript out of git and pushes them into namespaced, versioned paths in S3, like this:

	/somejslib/1.2.0/my.js
	/somejslib/1.2.1/my.js

Flyweight is built for write-once behavior, so it sets long expires headers and will not modify existing versions on your CDN.

### Dependencies

All optional dependencies are recommended.

- python 2.7
- git
- [`s3cmd`](http://s3tools.org/s3cmd), available via pip, brew, apt-get, yum or manual install
- (optional) [python-magic](http://pypi.python.org/pypi/python-magic/), avilable via pip
- (optional) [YUI Compressor](https://github.com/yui/yuicompressor/downloads), used to minify css and js before upload.

### Configuration

Configuration is managed through some very simple settings in `config.py`.

```python
bucket = "flyweight"
yui = "yuicompressor-2.4.7.jar"

repos = [
    {"url":"git@github.com:cbednarski/flyweight-test1.git"},
    {"url":"git@github.com:cbednarski/skyrim-alchemy.git"}
]
```

### Usage

	$ python flyweight.py

We recommend using something like Jenkins to run Flyweight on a regular cadence or trigger off of commits into your repositories.

### YUI

You can optionally use YUI to minify your javascript and css files. Simply add the path for your `yuicompressor.x.y.z.jar` to `config.py`. Input and output files have the same names, so this feature should be completely transparent to your users.

The YUI compression happens during the source-to-output copy stage, so it will not minify existing versions. Use `--force` or delete the appropriate folder(s) to minify an already-deployed version.