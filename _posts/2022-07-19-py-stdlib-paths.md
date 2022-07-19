---
layout: post
title: Manipulating paths in Python
subtitle: The beauty of the object-oriented paths
categories: ["Exploring the Python Standard Library"]
tags: ["dev", "python"]
date: 2022-07-19T20:44:20.440788+09:00
---

## Package index

- [`pathlib`](https://docs.python.org/3/library/pathlib.html)[^1]
- [`shutil`](https://docs.python.org/3/library/shutil.html)
- [`tempfile`](https://docs.python.org/3/library/tempfile.html)

[^1]: Since Python 3.4 (Mar 2014)

## Object-oriented filesystem paths

이 글을 읽고 나면, 여러분이 작성하시는 코드는 대부분 이 줄을 포함하게 될 겁니다.

```python
from pathlib import Path
```

### What is `pathlib`?

Python 개발자들이 붙인 부제가 아주 잘 설명하고 있듯이, `pathlib`은 object-oriented filesystem path(`Path`)를 제공합니다. 다른 말로 하면, 이 라이브러리를 사용하면 파일 및 경로를 별도의 object로 다룰 수 있게 됩니다.

### Path object initialization

모든 object는 어떤 식으로든지 생성되어야 합니다. `Path` object를 생성하는 방법은 여러 가지가 있습니다만, 자주 사용되는 방법은 다음과 같습니다.

```python
# p points to any/path/you/want
p = Path("any/path/you/want")
# Also works with segments
p = Path("any", "path", "you", "want")
# Current working directory
p = Path.cwd()
# Home directory; since 3.5 (Sep 2015)
p = Path.home()
# Home directory of user jnooree; since 3.5 (Sep 2015)
p = Path.home("~jnooree")
```

### Properties of Path object

대부분의 object는 property도 가지죠. `Path` object의 경우에는 다음과 같은 유용한 property를 가집니다.

```python
>>> p = Path("any", "path", "you", "want")
>>> p
PosixPath('any/path/you/want')
>>> p.parts
['any', 'path', 'you', 'want']
>>> p.parent
PosixPath('any/path/you')
>>> p.parents[1]
PosixPath('any/path')
>>> p.parents[2:]  # Since 3.10 (Oct 2021)
(PosixPath('any'), PosixPath('.'))
>>> p = Path("foo/bar.dir")
>>> p.name
'bar.dir'
>>> p.stem
'bar'
>>> p.suffix
'.dir'
```

이들 중에서는 특히 `Path.parent`, `Path.name`, `Path.stem` 등이 굉장히 자주, 또 유용하게 사용됩니다.

### Path manipulations

이제 `Path` object를 어떻게 다루는지도 살펴봅시다.

```python
>>> p = Path("foo/bar.dir")
>>> p / "baz.txt"
PosixPath('foo/bar.dir/baz.txt')
>>> p.joinpath("baz", "qux.txt")
PosixPath('foo/bar.dir/baz/qux.txt')
>>> p.with_name("quux")
PosixPath('foo/quux')
>>> p.with_stem("quz")  # Since 3.9 (Oct 2020)
PosixPath('foo/quz.dir')
>>> p.with_suffix(".d")
PosixPath('foo/bar.d')
>>> p.resolve()  # Make path absolute
PosixPath('/home/jnooree/foo/bar.dir')
>>> p.resolve(strict=True)  # Since 3.6 (Dec 2016)
FileNotFoundError: [Errno 2] No such file or directory: ...
```

이것만으로도 대부분의 경로와 관련된 상황을 전부 커버 가능합니다.

특히 `Path.with_suffix()` method는 같은 이름의 다른 형식 파일을 생성할 때 유용한데요, computational chemistry 쪽에서는 파일 형식 변환을 자주 하기 때문에 굉장히 많이 쓰입니다. Python 3.9에 추가된 `Path.with_stem()`는 반대로 파일 형식을 유지한 채로 전/후처리를 거친 파일의 이름을 약간만 바꿔주고 싶을 때 유용합니다. 예를 들면 다음과 같은 식으로요.

```python
sdf = Path("foo.sdf")
mol2 = sdf.with_suffix(".mol2")  # foo.mol2
mol2_3d = mol2.with_stem(f"{mol2.stem}_3d")  # foo_3d.mol2
```

### Querying metadata

파일이 실제로 디스크에 존재하는지 ~~폰파일은 아닌지~~ 확인하는 등, 해당 경로의 metadata를 확인하는 method도 유용하게 사용 가능합니다.

```python
p = Path("foo/bar.txt")
# Check if the path exists
p.exists()
# Check if the path exists and is a directory (or a symlink to a directory)
p.is_dir()
# Check if the path exists and is a file (or a symlink to a file)
p.is_file()
# Check if the path is an absolute path
p.is_absolute()
```

### Directory related operations

Bash나 zsh 등의 shell에서는 어떤 디렉토리 내부의 모든 파일에 대해 무언가를 실행하는 것이 용이하지만, Python에서 비슷한 방식으로 작업하기는 그리 간단하지 않습니다. `pathlib`이 여기에서도 구원투수로 등판합니다.

```python
d = Path("foo/bar")
# Equivalent to mkdir foo/bar
d.mkdir()
# Equivalent to mkdir -p foo/bar; since 3.5 (Sep 2015)
d.mkdir(parents=True, exist_ok=True)
# Iterator of directory contents
for p in d.iterdir(): ...
# Iterator of directory contents, matching a glob pattern
for p in d.glob("*.txt"): ...
# Recursive globbing is also supported
for p in d.glob("**/*.txt"): ...
```

### File related operations

디렉토리가 있으면 파일도 있어야겠죠?

```python
text = Path("foo/bar.txt")
# Equivalent to open(text)
with text.open() as f:
    for line in f:
        ...

# Whole file contents as a string; since 3.5 (Sep 2015)
content = text.read_text()
# Write a string to a file; since 3.5 (Sep 2015)
text.write_text("Hello, world!\n")
```

물론 첫 번째 예시에서 `Path.open()` method 대신 기존과 동일하게 built-in `open()` 함수를 사용해도 됩니다[^2]. 두번째 예시의 경우 간단한 파일 입출력에서 아주 유용하게 사용 가능합니다. 단, `Path.write_text()`는 항상 write mode로 파일을 열기 때문에 동일한 파일에 여러 번 호출하면 **안 됩니다**. `Path.read_text()`는 매우 큰 파일에 대해 실행할 경우 메모리 문제가 발생할 수 있다는 것도 기억해 두면 좋습니다.

[^2]: `open()`뿐만 아니라, Python standard library에서 제공하는 대부분의 함수나 method에서 경로와 관련된 argument에는 `str` 타입과 `Path` 타입을 모두 사용할 수 있습니다.

### Moving files around

또 shell에서는 쉽지만 Python에서 어려운 작업이 파일/디렉토리를 이동하거나 삭제하는 것인데요, 일부 작업은 `Path` object로 실행 가능합니다.

```python
p = Path("foo/bar")
# Rename foo/bar to baz (cannot overwrite directory)
p.rename("baz")
# Force rename foo/bar to baz
p.replace("baz")

# For files:
# Equivalent to rm foo/bar
p.unlink()
# Equivalent to rm -f foo/bar; since 3.8 (Oct 2019)
p.unlink(missing_ok=True)

# For *empty* directories:
# Equivalent to rmdir foo/bar
p.rmdir()
```

이보다 복잡한 파일 및 디렉토리 복사/이동/삭제 작업은 `pathlib` 모듈만으로는 불가능합니다.

## High-level file operations

그래서 많은 사람들이 이런 코드를 사용합니다.

```python
import os

os.system("rm -rf foo/bar")
```

그러나 `os.system()` 함수는 되도록이면 사용을 지양하는 것이 좋습니다.

### What's wrong with `os.system()`?

가장 큰 문제는 별도의 보호장치가 없다는 것입니다. 예를 들어, 코딩 중에 다음과 같이 오타를 냈다고 생각해 봅시다.

```python
#                 ↓ Oops!
p = "/home/jnooree /foo/bar"
os.system(f"rm -rf {p}")
```

축하합니다! 여러분의 **홈 폴더가 통째로 사라졌군요**. 이런 일이 실제로는 절대로 일어나지 않는다고 생각하신다면, 안타깝게도 틀렸습니다. 아주 유명한 사례로, Ubuntu에서 특정 오픈소스 패키지를 설치하면 설치 과정에서 `/usr` 디렉토리를 ~~친절하게도~~ [통째로 삭제해서 컴퓨터를 아주 깨끗하게 만들어 줬던 적이 있습니다](https://github.com/MrMEEE/bumblebee-Old-and-abbandoned/issues/123)[^3]. 해당 사례에서도 space 하나가 문제가 되었죠.

[^3]: 리눅스에서 `/usr` 디렉토리는 과장 좀 보태면 윈도의 `C` 드라이브와 비슷한 역할을 합니다. 전부 날려먹었으니 시스템이 통으로 망가지고 ~~가정이 무너지고 사회가 무너지고~~ 부팅이 안 되는건 당연하겠죠?

그래서 `os.system()`과 같이 주어진 문자열을 아무런 처리 없이 곧바로 실행하는 함수는 쓰지 않는 것이 좋습니다. 추가적인 논의는 이후 게시할 `subprocess` 모듈을 다루는 글에서 보실 수 있습니다.

### The rescue: `shutil`

저런 일 당하지 말라고 Python에는 `shutil` 모듈이 포함되어 있습니다. 앞서 언급했던 `pathlib` 모듈로는 불가능한 파일 및 디렉토리 복사/이동/삭제 작업에 특화되어 있는 모듈이죠.

```python
import shutil

# Copy file data and permission
shutil.copy("src.txt", "dst.txt")
# Copy file dat and metadata (modified time, ...)
shutil.copy2("src.txt", "dst.txt")
# cp -a src dst, except raises error if dst exists
shutil.copytree("src", "dst")
# rsync -a src/ dst/; since 3.8 (Oct 2019)
shutil.copytree("src", "dst", dirs_exist_ok=True)
# rm -r src
shutil.rmtree("src")
```

### Generate temporary files and directories

코딩을 하다 보면 가끔 임시로 사용하는 파일이나 디렉토리를 생성해야 하는 경우가 있습니다. 보통은 이런 방식을 사용하실 텐데요, 다른 사용자나 프로세스가 동일한 이름의 파일이나 디렉토리를 수정하려고 시도할 수 있기 때문에 권장하지 않습니다.

```python
# Temporary file
with open("temp.txt", "w") as f: ...

# Temporary directory
os.mkdir("temp")
...
os.system("rm -rf temp")
```

대신 임시 파일 또는 디렉토리를 **최대한 안전하게** 생성해 주는 `tempfile` 모듈을 사용하세요.

```python
import tempfile

# "Safe" way to write to a temporary file
with tempfile.TemporaryFile("w") as f: ...

# If file name should be used afterwards, then
with tempfile.NamedTemporaryFile("w") as f:
    foo(f.name)
    ...

# For temporary directories; since 3.2 (Feb 2011)
with tempfile.TemporaryDirectory() as dirname:
    ...
```

해당 context를 벗어나면 자동으로 생성했던 임시 파일 또는 디렉토리(와 그 안에 있는 모든 것)를 삭제합니다.
