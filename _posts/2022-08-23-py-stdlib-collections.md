---
layout: post
title: Collections
subtitle: Useful & efficient container datatypes
categories: ["Exploring the Python Standard Library"]
tags: ["dev", "python"]
date: 2022-08-23T14:35:05.830804+09:00
---

## Package index

- [`collections`](https://docs.python.org/3/library/collections.html)

## `defaultdict`

### A common workflow

어떤 리스트를 특정 조건을 만족하는 더 작은 리스트로 나누는 작업은 상당히 빈번하게 일어납니다. 대개는 아래와 같이 작성하게 되죠.

```python
l = [("yellow", 1), ("blue", 2), ("yellow", 3), ...]
d = {}
for color, value in l:
    if color not in d:
        d[color] = [value]
    else:
        d[color].append(value)
```

### A better workflow

그러나 위와 같은 방식은 비교적 덜 자주 일어나는 "새로운 key를 만나는 경우"를 위해 모든 원소에 대해 조건문을 실행한다는 단점이 있습니다. 이를 개선하는 방법은 try-except 문을 통해 `KeyError`를 [처리하는 것입니다](https://docs.python.org/3.5/glossary.html#term-eafp).

```python
l = [("yellow", 1), ("blue", 2), ("yellow", 3), ...]
d = {}
for color, value in l:
    try:
        d[color].append(value)
    except KeyError:
        d[color] = [value]
```

### The best workflow

그러나 가장 좋은 방법은 애초에 python 코드를 적게 작성하는 것입니다. 이를 위해 `defaultdict`를 [사용할 수 있습니다](https://docs.python.org/3/library/collections.html#collections.defaultdict). 코드가 전체적으로 훨씬 깔끔해지고 가독성이 높아지는 것을 볼 수 있습니다.

```python
from collections import defaultdict

l = [("yellow", 1), ("blue", 2), ("yellow", 3), ...]
d = defaultdict(list)
for color, value in l:
    d[color].append(value)
```

`defaultdict`는 `dict`의 subclass이기 때문에 `dict`의 모든 메서드를 사용할 수 있습니다.

### Benchmarks

위의 세 가지 방법의 속도를 비교해보았습니다. `defaultdict`를 이용하면 최대 10%정도 속도 향상이 있는데, 이는 `defaultdict`는 [C로 구현되어 있기 때문입니다](https://github.com/python/cpython/blob/1499d73b3e02878850c007fa7298bb62f6c5a9a1/Modules/_collectionsmodule.c#L1955-L2269). 코드가 깔끔해지는 것 외에도 속도 향상까지 얻을 수 있는 셈이죠.

{% include image.html url="/assets/images/posts/exploring-python-stdlib/defaultdict-bench.png" description="Tested on M1 mac mini (2020), Python 3.10.5" %}

## `Counter`

### Counting occurrences

또 다른 자주 있는 작업은 리스트 원소의 빈도수를 세는 것입니다. 보통은 이렇게 작성하는 경우가 많습니다.

```python
l = ["foo", "bar", "bar", "baz", ...]
c = {}
for item in l:
    if item not in c:
        c[item] = 1
    else:
        c[item] += 1
```

### Oh, `defaultdict`, my `defaultdict`

물론 앞서 소개했던 `defaultdict`를 이용하면 더 깔끔하게 작성할 수 있습니다.

```python
from collections import defaultdict

l = ["foo", "bar", "bar", "baz", ...]
c = defaultdict(int)
for item in l:
    c[item] += 1
```

### Use _the_ right tool

하지만 이런 작업은 워낙 자주 사용되어서 모든 것을 아예 자동으로 처리해주는 `Counter`가 [준비되어 있습니다](https://docs.python.org/3/library/collections.html#collections.Counter).[^1]

[^1]: Available since Python 3.1 (Jun 2009).

```python
from collections import Counter

l = ["foo", "bar", "bar", "baz", ...]
c = Counter(l)
```

`Counter` 역시 `dict`의 subclass이기 때문에 `dict`의 모든 method를 사용할 수 있습니다. 또한 `Counter`는 `most_common` 등의 유용한 method를 제공한다는 추가적인 장점도 있습니다.

```python
>>> c.most_common()
[('bar', 10), ('foo', 7), ('baz', 3), ...]
```

### Benchmarks

위의 세 방법과 더불어 exception으로 처리한 방법까지 총 네 가지에 대해 속도를 비교해 보았습니다.

{% include image.html url="/assets/images/posts/exploring-python-stdlib/counter-bench.png" description="Tested on M1 mac mini (2020), Python 3.10.5" %}

지금까지 중 가장 드라마틱한 차이로, 2배 이상 빨라지는 것을 확인할 수 있습니다. 이것 역시 `Counter`의 핵심 부분이 [C로 구현되어 있기 때문이죠](https://github.com/python/cpython/blob/d6259c58cbb48b8f3fbd70047f004ea19fe91e86/Modules/_collectionsmodule.c#L2271-L2388).
