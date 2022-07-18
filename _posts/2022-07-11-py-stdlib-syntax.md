---
layout: post
title: Advanced Python Syntax
subtitle: The python you might not have heard of
categories: ["Exploring the Python Standard Library"]
tags: [dev, python]
date: 2022-07-11T23:22:31.379445+09:00
---

## 혹시 이거 아시나요?

- [Triple quotes](#triple-quotes) ("docstrings")
- [_f_-string](#f-string) (formatted string literals)[^1]
- [Ternary operator](#ternary-operator)
- [`or` as a conditional statement](#or-as-a-conditional-statement)
- [Comprehensions](#comprehensions)
- [Assignment expression](#assignment-expression)[^2]
- [Loop-else construct](#loop-else-construct)

[^1]: Since Python 3.6 (Dec 2016)
[^2]: Since Python 3.8 (Oct 2019)

## Triple quotes

이런 걸 어딘가에서 많이 보셨을 겁니다.

```python
def foo():
    """
    This is a docstring.
    """
    pass
```

C나 다른 언어를 하다 오신 분의 경우에는 그냥 함수를 설명하는 주석(block comment)이겠거니 하고 넘기셨을 수도 있습니다만, 사실 Python에서는 triple-quoted string 역시 일반적인 string literal과 동일하게 사용 가능합니다. 그런데 왜 굳이 귀찮게 세번씩 쳐야 하냐고요?

```python
long_string = "A very long string with\n" \
    + "multiple lines\n" \
    + "and many words"
```

아마 그동안은 string literal 안에서 줄바꿈이 불가능하기 때문에 이렇게 쓰셨던 적이 많겠지만, 이렇게 작성하면 한눈에 잘 들어오지도 않을 뿐더러 속도도 느립니다. Triple-quoted string을 사용하면 다음과 같이 깔끔하게 표현이 가능합니다.

```python
long_string = """A very long string with
multiple lines
and many words"""
```

그냥 줄바꿈을 하는 대로 곧바로 반영되기 때문이죠. 첫 줄이 나머지랑 정렬이 안 돼서 영 마음에 안 드신다고요? 백슬래시(`\`)를 찍어서 드셔보세요.

```python
long_string = """\
A very long string with
multiple lines
and many words"""
```

물론 안에서 추가 줄바꿈을 하면 그대로 반영됩니다. 앞에 띄어쓰기를 포함하면 그것도 함께 포함됩니다. 그러니까 다음 예제를 실행하면...

```python
>>> long_string = """\

A very long string with
    multiple lines
    and many words"""
>>> print(long_string)

A very long string with
    multiple lines
    and many words
```

이런 식이 되는 셈이죠. 보통은 여러 출력에서 template string으로 많이 사용됩니다.

## _f_-string

프로그래밍에서 절대로 빼놓을 수 없는 편의기능을 한 개만 고르라면, string formatting을 고르는 사람도 꽤 있을 겁니다. Python은 전통적으로 C와 비슷한 `%`-formatting을 지원하지만, 이 방식은 1) **포맷할 자리와 값을 두 차례 전달하기 때문에 실수할 여지가 많다는 문제가 있고**, 2) 속도가 느립니다[^3]. 이후 등장한 string type의 `.format()` 메서드 역시 비슷한 문제를 공유합니다.

Python 3.6 버전에서 추가된 _f_-string[^4]을 사용하면 이런 문제를 깔끔하게 회피 가능합니다.

[^3]: 실수할 여지가 많다는 것이 더 큰 문제입니다. 어차피 둘 모두 충분히 빠르기 때문에 속도 이슈는 대부분의 경우 코드 실행 시간에 별다른 영향을 미치지 않습니다 ([Amdahl's law](https://en.wikipedia.org/wiki/Amdahl%27s_law)).
[^4]: String literal 앞에 `f` 표기를 붙이기 때문에 _f_-string이라고 불립니다. 정식 명칭은 [formatted string literal](https://docs.python.org/3/tutorial/inputoutput.html#tut-f-strings)입니다. 더 자세한 명세는 [이쪽](https://docs.python.org/3/reference/lexical_analysis.html#f-strings)을 참고하세요.

```python
name = "Nuri Jung"
print(f"My name is {name}")
```

말 그대로 literal이기 때문에 lazy evaluation[^5]이 일어나지 않습니다.

[^5]: 어떤 식의 값이 정의 시점이 아니라 사용 시점에 결정되는 것을 말합니다. 대표적인 lazy evaluation의 예시에는 `range()`가 있습니다.

```python
>>> name = "Nuri Jung"
>>> intro = f"My name is {name}"
>>> name = "John Doe"
>>> print(intro)
My name is Nuri Jung
```

기존에 되던 것들은 전부 됩니다.

```python
>>> result = [0, 1, 2]
>>> print(f"The result is {result}")
The result is [0, 1, 2]
```

`%f` formatting이 그리우신 분들을 위한 실수 포맷팅도 당연히 지원합니다.

```python
>>> num = 100 / 3
>>> print(f"The result is {num}")
The number is 33.33333333333336
>>> print(f"The result is {num:.3}")  # 유효숫자 기준입니다
The number is 33.3
>>> print(f"The result is {num:5.3}")
The number is  33.3
>>> print(f"The result is {num:05.3}")
The number is 033.3
>>> print(f"The result is {num:03.3}")  # 칸수는 "최소"입니다
The number is 33.3
>>> print(f"The result is {num:.3f}")  # f는 소수점 이하 자리수 기준입니다
The number is 33.333
```

### One more thing...

최근[^2]에는 더 좋아져서 이런 것도 지원합니다.

```python
>>> print(f"{num = :.3f}")
num = 33.333
```

### Benchmarks

아까 제가 느리다고 했는데, 얼마나 느린지 궁금하신 여러분들을 위해 벤치마크도 준비했습니다.

```python
# f-string
f"{s} {t}"
# string format
"{} {}".format(s, t)
# percent format
"%s %s" % (s, t)

# plus operator
s + " " + t
# string join
" ".join((s, t))
```

{% include image.html url="/assets/images/posts/exploring-python-stdlib/fstring-bench.png" description="Tested on M1 mac mini (2020), Python 3.10.5" %}

심하게는 두배 이상도 차이나네요? 물론 plus operator와 string join은 원래 formatting 용도로 만든게 아니니 공정한 비교는 아닙니다만, 그래도 궁금하실 여러분을 위해 넣어봤습니다.

### 실제 사용례

연구실 슬랙 봇 코드 중 일부를 가져왔습니다. 보시는 것처럼 template을 만들 때 triple-quoted string과 조합하면 유용하게 쓸 수 있습니다.

{% include image.html url="/assets/images/posts/exploring-python-stdlib/fstring-usage.png" caption='From the galaxybot <a href="https://github.com/seoklab/galaxybot/blob/205ef5fe5b7f57cb896b920829dded02a9bfeda4/galaxybot/automations/meeting.py#L210-L226">source code</a>' %}

## Ternary operator

다른 언어에 익숙한 분들은 Python을 처음 쓸 때 `?:` 연산자를 시도하고 장렬하게 `SyntaxError`와 함꼐 산화한 경험이 있으실 겁니다. 그렇다고 Python에 ternary operator가 없는 것은 아닙니다.

Ternary operator는 기본적으로는 다음과 같은 작업을 줄여서 쓰기 위해 도입되었습니다.

```python
if a >= 0:
    print(a)
else:
    print(-a)
```

딱 봐도 뭔가 반복이 많고, 단순한 작업인데도 네 줄이나 차지하네요. 이를 한 줄로 줄이기 위한 편리한 operator가 바로 ternary operator입니다.

```python
print(a if a >= 0 else -a)
```

항상 그렇듯이 Python 특유의 ~~변태적인~~ 문법이 눈에 띄는군요. 영어를 잘 하는 분이라면 그래도 좀더 직관적으로 와닿을지도 모르겠습니다. 영어 어순과 거의 동일하게 논리가 흘러가기 때문이죠[^6].

[^6]: 그렇다고 평가 순서까지 직관적인 것은 아닙니다. 조건문이 가장 먼저 실행되고, 조건문이 참이면 if 이전의 코드가, 거짓이면 else 이후의 코드가 실행됩니다.

좀 더 formal하게 정의하면, 다음 두 식의 실행 결과 `result`는 같습니다.

```python
# By conditional statement
if (expression):
    result = (if_true)
else:
    result = (if_false)

# By ternary operator
result = (if_true) if (expression) else (if_false)
```

## `or` as a conditional statement

이번에 보여드릴 것은 ternary operator랑 비슷하게 사용 가능한 기법입니다. 코딩하다 보면 다음과 같은 방식으로 처리해야 하는 경우가 꽤 많습니다.

```python
if a:
    foo = a
else:
    foo = b
```

물론 방금 나온 ternary operator를 사용하면 좀 더 줄일 수 있습니다.

```python
foo = a if a else b
```

하지만 정말 간단하게 처리하는 방법이 있는데, 바로 `or` operator를 응용하는 것입니다. 이는 `or` operator가 첫 번째 operand가 참인 경우 그 결과를 그대로 반환하고, 거짓인 경우 두 번째 operand를 그대로 반환하기 때문에 가능한 트릭입니다.

```python
foo = a or b
```

### 실제 사용례

연구실 코드에도 이와 같은 처리가 포함된 부분이 있습니다.

{% include image.html url="/assets/images/posts/exploring-python-stdlib/or-conditional-usage.png" caption='From the GalaxyPipe <a href="https://github.com/seoklab/GalaxyPipe/blob/1a696852206703c43181761a085c3f5e02673774/lib/Galaxy/config.py#L23-L24">source code</a>' %}

## Comprehensions

List comprehension 자체는 나름대로 유명하고 많이들 사용하는 편입니다.

```python
# For loop
squares = []
for x in range(10):
    squares.append(x**2)

# List comprehension
squares = [x**2 for x in range(10)]
```

그런데 전체 iterable에 대해 처리하는 경우가 아니라, 그 중 일부만을 처리하고 싶은 경우라면 어떻게 해야 하는지 막막하신 분들이 많습니다. 이럴 경우 `if`문을 맨 뒤에 붙여주면 됩니다.

```python
# For loop
squares = []
for x in range(10):
    if x % 2:
        squares.append(x**2)

# List comprehension
squares = [x**2 for x in range(10) if x % 2]
```

둘 모두를 경우에 따라 처리해야 한다면 앞에서 나왔던 ternary operator를 이용하면 됩니다.

```python
# For loop
squares = []
for x in range(10):
    if x % 2:
        squares.append(x**2)
    else:
        squares.append(-x**2)

# List comprehension
squares = [x**2 if x % 2 else -x**2 for x in range(10)]
```

당연히 list comprehension 뿐만 아니라 set comprehension, dictionary comprehension 등도 있습니다.

```python
# For loop
squares = []
for x in range(10):
    if x % 2:
        squares.append(x**2)

# Set comprehension
squares = {x**2 for x in range(10) if x % 2}
# Dictionary comprehension
squares = {x: x**2 for x in range(10) if x % 2}

# Tuple comprehension?
squares = (x**2 for x in range(10) if x % 2)
```

그러나 마지막과 같이 쓰면 tuple comprehension이 아니라 [generator expression](https://docs.python.org/3/reference/expressions.html#generator-expressions)[^7]이 됩니다. Tuple로 바꾸고 싶은 경우 tuple로 type casting해 줍시다.

[^7]: Lazy evaluation을 지원하는 iterator. 실제로 iteration을 할 때 (eg. for loop) 각각의 값이 계산된다.

```python
squares = tuple(x**2 for x in range(10) if x % 2)
```

## Assignment expression

Python에서 assignment문은 다른 많은 언어에서와는 달리 **expression이 아닙니다**[^8]. 즉, assignment문은 아무것도 반환하지 않습니다.

[^8]: [여기](https://docs.python.org/3/glossary.html#term-expression)를 참고하세요.

```python
# SyntaxError
if a = 1:
    print("a is 1")
```

하지만 대입과 동시에 조건을 확인하는 코드는 (다소 가독성이 떨어지는 문제가 생기는 경우도 있지만) 대부분의 while loop에서 상당히 유용하게 사용됩니다. 예를 들어 다음과 같은 코드는 만약 assignment문이 expression이었다면 가독성의 저하 없이도 덜 장황하게 짤 수 있습니다.

```python
# Without assignment expression
while True:
    flag = foo()
    if not flag
        break
    do_something(flag)

# If assignment statement were expression...
while flag = foo():
    do_something(flag)
```

그래서 Python 3.8에서는 assignment expression을 위한 Walrus operator(`:=`)를 도입합니다. 따라서 이제는 이렇게 사용이 가능합니다.

```python
while (flag := foo()):
    do_something(flag)
```

여기에서 괄호는 반드시 필요합니다. 괄호가 없는 경우 `SyntaxError`가 발생합니다.

### 실제 사용례

이번에도 연구실 슬랙 봇 코드를 가져왔습니다.

{% include image.html url="/assets/images/posts/exploring-python-stdlib/assignment-expression-usage.png" caption='From the galaxybot <a href="https://github.com/seoklab/galaxybot/blob/205ef5fe5b7f57cb896b920829dded02a9bfeda4/galaxybot/commands/meeting.py#L160-L167">source code</a>' %}

## Loop-else construct

많은 사람들의 인식과는 달리 Python은 있어야 할 것은 없고 없어도 되는 것은 있는 경우가 꽤 잦은, 독특한 언어입니다. Loop-else construct도 "없어도 되는" syntax의 예시인데요, 물론 꽤나 유용하게 사용되기는 하지만 이런 문법은 다른 언어에서는 찾아보기 어렵습니다.[^9]

[^9]: 이 syntax가 어쩌다 도입되었는지가 궁금하다면, 이 [stackoverflow 답변](https://stackoverflow.com/a/23748240)을 참고하세요.

```python
# For-else statement
for i in range(10):
    if i == 42:
        break
else:
    print("No answer")

# ...which is equivalent to:
found = False
for i in range(10):
    if i == 42:
        found = True
        break
if not found:
    print("No answer")
```

즉, loop의 정상적인 종료 시에만 (`break`이나 `return`등을 통해 loop이 끝나지 않는 경우에만) else문이 실행됩니다. Loop을 돌면서 특정 조건을 만족하는지 확인하고, 만족하지 않는 경우 예외 처리를 해야 하는 코드에서 유용하게 사용됩니다. 예시로는 for문만 들었지만, loop else construct라는 말에서도 볼 수 있듯이 while loop도 else문의 사용이 가능합니다.

## Wrap-up

**모를 법**한 Python syntax를 살펴봤습니다. 다음 포스트에서는 유용한 built-in에 대해 살펴보겠습니다. 원래는 하나의 글로 기획했는데 생각보다 길어져서 분리하게 되었네요.
