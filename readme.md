# Flyweight

Flyweight is a lightweight commandline tool for building CDNs using Amazon S3 and CloudFront.

### How it works

Flyweight starts by looking for tags in your git repos that match [SemVer](http://semver.org/) version numbers. Flyweight enumerates these tags and pulls assets like images, css, and javascript out of git and pushes them into namespaced, versioned paths in S3, like this:

	/somejslib/1.2.0/my.js
	/somejslib/1.2.1/my.js

Flyweight is built for write-once behavior, so it sets long expires headers and will not modify existing versions on your CDN.

### Dependencies

- python 2.7
- git
- [`s3cmd`](http://s3tools.org/s3cmd), which can be installed via pip, brew, apt-get, yum or manually

### Configuration

Configuration is managed through some very simple settings in `config.py`.

```python
bucket = "flyweight"

repos = [
    {"url":"git@github.com:cbednarski/flyweight-test1.git"},
    {"url":"git@github.com:cbednarski/skyrim-alchemy.git"}
]
```

### Usage

	$ python flyweight.py

We recommend using something like Jenkins to run Flyweight on a regular cadence or trigger off of commits into your repositories.