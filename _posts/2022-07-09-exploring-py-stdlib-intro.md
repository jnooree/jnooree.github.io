---
layout: post
title: Exploring the Python Standard Library
subtitle: Introduction
categories: ["Exploring the Python Standard Library"]
tags: [dev, python]
date: 2022-07-09T23:51:56.003835+09:00
---

> "The standard library saves programmers from having to reinvent the wheel."  
> ― Bjarne Stroustrup, father of the C++ programming language

## Preface

초보 개발자들이 저지르기 가장 쉬운 실수는 바로 **내가 필요로 하는 기능이 이미 구현되어 있는지 모르는 것**이다. 개발을 하면서 경험이 쌓이면 "어 이거 어디서 봤던 것 같은데" 라든가, "이건 누가 만들어뒀을 법 한데" 같은 감이 생기지만, 처음부터 이런 관심법을 쓰기는 쉽지 않기 때문이다.

이 시리즈를 만들게 된 계기도 비슷한 *실수*를 연구실에서 많이 접했기 때문이다. Python의 모든 라이브러리를 다루는 것은 불가능하므로, 이 시리즈에서는 Python을 깔자마자 사용 가능한 Python stdandard library의 유용한 모듈을 둘러보도록 하겠다. 앞으로 총 6개의 글이 계획되어 있으며, 각각 다음과 같은 내용을 다룬다.

1. Advanced Python syntax
2. More about built-ins
3. Path manipulation
4. `collections` (containers)
5. Subprocess management
6. Miscellaneous useful modules

## Notes

이 시리즈는 2022년 7월 8일 [연구실](https://seoklab.org)에서 진행했던 동 제목의 [온라인 세미나](https://drive.google.com/drive/folders/18SDWiRlrd2Ya47MItXZEs2JRZbFjvblr?usp=sharing)의 내용을 기반으로 한다.
