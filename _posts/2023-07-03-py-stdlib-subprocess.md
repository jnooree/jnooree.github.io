---
layout: post
title: Subprocess management
subtitle: Calling other programs from python
categories: ["Exploring the Python Standard Library"]
tags: ["dev", "python"]
date: 2023-07-03T19:34:59+09:00
---

## Package index

- [`subprocess`](https://docs.python.org/3/library/subprocess.html)

## `os.system` revisited

계산화학 연구를 하는 사람들이라면, RMSD를 계산해 주는
[OpenBabel](https://github.com/openbabel/openbabel) 프로젝트의 `obrms` 프로그램을
한번쯤 다음과 같이 사용해 봤을 것입니다.

```python
import os
os.system("obrms ref.mol2 test.mol2")
```

상황에 따라서는 파일명을 변수로 저장해 두는 경우도 있겠죠?

```python
os.system(f"obrms {ref} {test}")
```

그런데 저 입력을 유저에게서 받았다고 생각해 봅시다. 그리고 `ref`와 `test` 변수가
어쩌다 보니 다음과 같이 정의되어 있다면 어떨까요?

```python
ref = "ref.mol2 test.mol2"
test = "; rm -rf /home/jnooree"
```

축하합니다! rmsd 계산과 함께 **홈 폴더가 통으로 날아갔습니다**(...)

이쯤에서 shell에 익숙한 사람들은 quoting을 하면 되지 않느냐고 물어볼 텐데요,

```python
os.system(f"obrms '{ref}' '{test}'")
```

네, 이번 경우는 위와 같은 코드에서 에러가 날 뿐, 홈 폴더를 지우진 않습니다.
그런데 정말 언제나 안전할까요?

```python
ref = "ref.mol2' 'test.mol2"
test = "'; rm -rf /home/jnooree'"
```

어떤 똑똑한 해커가 위와 같이 변수를 입력했다면, 여전히 홈 폴더가 날아가는 것을
막을 수 없습니다. Quoting뿐만 아니라 어떤 식으로 방어하든, **어딘가는 취약점이
있기 마련**입니다. 그래서 `os.system`처럼 shell을 통해 프로그램을 실행하는
함수는 **절대로** 사용하지 말라고 권장하는 것입니다[^1].

[^1]: 비슷한 느낌의 공격으로 [SQL injection](https://en.wikipedia.org/wiki/SQL_injection)이 있습니다. 데이터베이스에 대한 공격인데, 이와 더불어 여러 문제점 때문에 user에게 받은 입력을 곧바로 sql문으로 실행하는 것은 금기시됩니다.

## `subprocess.run()`[^2]

[^2]: Since Python 3.5 (Sep 2015)

그러면 어떻게 해야 할까요? Python 개발자들은 `subprocess.run()` 함수를 만들어
두었습니다. 이 함수는 기본적으로는 argument를 list로 받습니다.

```python
import subprocess
subprocess.run(["obrms", ref, test])
```

내부적으로 저거 다시 join해서 shell로 실행하는 것 아니냐고요? 플랫폼에 따라
다르고, implementation detail이기 때문에 언제나 동일할 것이라고 장담은 못하지만,
Unix-like system에서는 fork 이후 아예 저 argument list를 **그대로** exec system
call로 넘겨버립니다(Python 3.10 기준). 취약점을 원천봉쇄하는 셈이죠.

`subprocess.run()`은 단순히 안전하기만 한 것이 아니고, 여러 가지 유용한 기능을
추가로 제공하기도 합니다.

### 출력 받아오기

`subprocess.run()`은 기본적으로 실행한 프로그램의 stdout과 stderr를 그대로
출력합니다. 그런데 상황에 따라 그 출력을 외부로 보내는 것이 아니라, 프로그램에서
사용하고 싶을 수도 있습니다. 이럴 때는 `subprocess.PIPE` 옵션을 사용합니다.

```python
>>> result = subprocess.run(["obrms", ref, test], stdout=subprocess.PIPE)
>>> result.stdout
b'RMSD ref:test 53.7078\n'
```

다만, 기본 설정은 binary로 출력을 받아오기 때문에(`bytes` object 반환),
`decode()`를 통해 `str`으로 변환해 주거나, `text=True` 옵션을 주어야[^3]
일반적으로 사용하는 `str`으로 받아올 수 있습니다.

[^3]: Since Python 3.7 (Jun 2018)

```python
>>> result = subprocess.run(["obrms", ref, test],
                            stdout=subprocess.PIPE, text=True)
>>> result.stdout
'RMSD ref:test 53.7078\n'
```

추가적인 장점으로, stdout과 stderr를 독립적으로 처리하기 때문에 앞에서 본 것과
같이 에러 메시지를 제외한 출력만 받아오거나(`stdout`만 이용), 둘 다 각각
받아오거나(`stdout`, `stderr` 이용), 또는 합쳐서 한번에 받아오는 등 다양한
방식으로 사용할 수 있습니다.

```python
# 출력만 받아오기 (stderr는 원래대로 출력)
result = subprocess.run(["obrms", ref, test], stdout=subprocess.PIPE)
# 각각 받아오기
result = subprocess.run(["obrms", ref, test],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# 합쳐서 받아오기
result = subprocess.run(["obrms", ref, test],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
```

### Sending input to child

`subprocess.run()`을 이용하면 실행하는 프로그램의 stdin으로 직접 데이터를
보낼 수도 있습니다. 이때는 `input` 옵션을 사용합니다. 이 경우에도 기본적으로는
`bytes` object를 받아들이기 때문에, `text=True` 옵션을 주거나 `encode()`해
주어야 합니다.

```python
>>> result = subprocess.run(["grep", "a"], input=b"abc\ndef\nghi\n",
                            stdout=subprocess.PIPE)
>>> result.stdout
b'abc\n'
>>> result = subprocess.run(["grep", "a"], input="abc\ndef\nghi\n",
                            stdout=subprocess.PIPE, text=True)
>>> result.stdout
'abc\n'
```

또는 `subprocess.PIPE`를 사용하여 파일 등으로부터 데이터를 넘겨줄 수도 있습니다.

```python
>>> with open("input.txt") as f:
...     result = subprocess.run(["grep", "a"],
...                             stdin=f, stdout=subprocess.PIPE, text=True)
>>> result.stdout
'abc\n'
```

많은 경우, 임시파일을 거쳐 프로그램에 입/출력하는 구현은 사실 이런 방식으로
대체하는 것이 훨씬 효율적이고 편리합니다.

### Error handling

`os.system()`은 실행한 프로그램의 종료 코드를 반환하고, `subprocess.run()`도
기본적으로는 동일하게 종료 코드를 반환합니다.

```python
>>> ret = subprocess.run(["rm", "/"])  # No error?
rm: cannot remove '/': Is a directory
>>> ret.returncode
1
```

하지만 Python에서 우리는 보통 `try-except` 구문을 통해 에러를 처리합니다.
`subprocess.run()`을 사용할 때는 `check=True` 옵션을 주면, 종료 코드가 0이 아닌
경우 exception을 발생시키도록 할 수 있습니다.

```python
>>> ret = subprocess.run(["rm", "/"], check=True)
rm: cannot remove '/': Is a directory
Traceback (most recent call last):
    ...
subprocess.CalledProcessError: Command '['rm', '/']' returned non-zero exit status 1.
```

이때 발생하는 exception은 `subprocess.CalledProcessError`입니다.

### Timeout

상황에 따라, 프로그램이 일정 시간 이상 걸리면 종료시키고 싶을 수도 있습니다.
`subprocess.run()`은 `timeout` 옵션을 통해 이를 지원합니다.

```python
>>> ret = subprocess.run(["sleep", "10"], timeout=5)
Traceback (most recent call last):
    ...
subprocess.TimeoutExpired: Command '['sleep', '10']' timed out after 5 seconds
```

이때 발생하는 exception은 `subprocess.TimeoutExpired`입니다.

### Still using shell

`subprocess.run()`은 기본적으로 shell을 사용하지 않습니다. 하지만 상황에 따라
globbing, redirection 등 shell에서 제공하는 부가기능을 사용하고 싶을 수도
있습니다. 이때는 `shell=True` 옵션을 주고, `os.system()`과 유사하게 `str`으로
명령어를 넘겨주면 됩니다.

```python
>>> subprocess.run("echo *.py", shell=True)
main.py
```

하지만 대부분의 경우에는 Python 내부적으로 제공하는 기능으로 충분하기 때문에,
`shell=True` 옵션을 사용하는 것은 권장하지 않습니다. (위의 예제는 `glob` 모듈
또는 `pathlib` 모듈을 사용하여 대체할 수 있습니다.)
