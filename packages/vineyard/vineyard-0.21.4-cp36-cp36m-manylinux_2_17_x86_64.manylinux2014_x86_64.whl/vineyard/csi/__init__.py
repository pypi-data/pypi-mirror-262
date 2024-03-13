#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020-2023 Alibaba Group Holding Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
from typing import Any

import vineyard


def _find_vineyard_socket(path):
    current_dir = path
    while current_dir != "/":
        socket_path = os.path.join(current_dir, "vineyard.sock")
        if os.path.exists(socket_path):
            return socket_path
        current_dir = os.path.dirname(current_dir)
    return None


def write(
    value: Any,
    path: str,
):
    """
    Write python value to vineyard.
    Notice, the API is only used for CSI driver.

    Parameters:
        path: str
            The path that represents a vineyard object.

    .. code:: python

        >>> arr = np.arange(8)
        >>> vineyard.write(arr)
    """
    socket_path = _find_vineyard_socket(path)

    if socket_path is None:
        raise FileNotFoundError(
            f"The given path is not generated by vineyard CSI driver: {path}"
        )

    client = vineyard.connect(socket_path)
    client.put(value, persist=True, name=path)


def read(
    path: str,
):
    """
    Read vineyard object from path, and return python value.
    Notice, the API is only used for CSI driver.

    Parameters:
        path: str
            The path that represents a vineyard object.

    .. code:: python

        >>> arr = vineyard.read('/a/b/c/d/f')
        >>> arr
        array([0, 1, 2, 3, 4, 5, 6, 7])

    Returns:
        A python object that return by the resolver, by resolving an vineyard object.
    """
    socket_path = _find_vineyard_socket(path)

    if socket_path is None:
        raise FileNotFoundError(
            f"The given path is not generated by vineyard CSI driver: {path}"
        )

    client = vineyard.connect(socket_path)
    return client.get(name=path)
