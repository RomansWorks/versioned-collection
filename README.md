![Build Status](https://img.shields.io/github/actions/workflow/status/RomansWorks/versioned-collection/build-library)
![Coverage Status](https://img.shields.io/codecov/c/github/RomansWorks/versioned-collection)
![GitHub](https://img.shields.io/github/license/RomansWorks/versioned-collection)
![PyPI version](https://img.shields.io/pypi/v/versioned-collection)
![Python version](https://img.shields.io/badge/python-3.10-blue.svg)


# (Remote) Versioned Collection

## Why

While working with LLMs I wanted to version my prompts and load them consistently whether from local files or from an online resource. The abstraction goes beyond LLMs and prompts, and is basically a versioned collection of objects, e.g. texts, images, feature flags, etc.

(a specificially LLMs related library is [prompt-base](https://github.com/RomansWorks/prompt-base) which will be released later, based on this library).

NOTE: This library does not automatically manage the versions of each mutation of items. It only manages the version of the collection as a whole.


## How

The library abstracts over storage and versioning. The main object is the `Collection` class, which is a glorified dictionary with pluggable storage and versioning implementations. `Item`s in the collection can be accessed by `key` or by a value hash (content based lookup). 

The collection itself can be loaded from a storage such that we don't need to know anything about the actual storage format and protocols at the site of the collection usage. For example, we can load a collection from a local file, a remote URL, a git repository, a database - and thiscan be configured vie env vars, logic or any other runtime or buildtime mechanism.

## Usage

### Loading a collection

Here's a simple way to load a collection:

```python
from versioned_collection import Collection, CollectionStore

collection = CollectionStore.load(url="path/to/collection")
```

The `url` can be a local file path (using `file://` scheme), or remote URL. I'll add more storage options in the future if need arises (`github`, `sqlite`, `api`, etc.)

Loading from the the internet requires installing the optional `aiohttp` dependency:

```bash
poetry install --extras http
```

### Accessing items

Once we have a collection we can access items by key or by hash:

```python
item = collection["my.item"]
item = collection.get("my.item")
item = collection.get_by_hash("my.item.hash")
```

See the `tests/` folder for examples of usage. 

### Creating a collection

A collection can be created from a list of items:

```python
collection = Collection(items=[Item(key="my.item", value="my item value")])
```

### Adding items to a collection

Items can be added to a collection:

```python
collection.add(Item(key="my.item", value="my item value"))
```

### Removing items from a collection

Items can be removed from a collection:

```python
collection.remove("my.item")
```

### Saving a collection

A collection can be saved to a storage:

```python
collection.save(url="path/to/collection")
```

### Versioning

The currently implemented scheme assumes that the version is part of the collection file. 

If you have a use case where the versioning should happen outside of the file (for example, as happens with `git`), please let me know in the issues. 

### Storage

The currently implemented storage is a single file per-collection, either JSON or YAML. 

Both files are human readable and more importantly their diff is human readable.

If there's a need to add file-per-item storage please let me know in the issues. 

# Roadmap and Contributing

This library would stay small. Further work on this library is pending feedback from the community in the issues. 

I currently plan to add the following capabilities:

- [ ] - Support watch on a collection (i.e. file watch) and change notification callback.
- [ ] - A `link` content type to support nested loading.
- [ ] - Lazy loading for `link` values. 

Please let me know if you want me to add additional storage options or features.

## Contributing

Please feel free to open issues, especially before opening pull requests. I'll add a mandatory CLA in the future. 


