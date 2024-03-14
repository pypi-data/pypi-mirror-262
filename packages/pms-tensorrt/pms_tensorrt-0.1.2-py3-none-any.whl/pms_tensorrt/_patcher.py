from dataclasses import dataclass
from typing import Iterable, List, Literal, Optional, Tuple

# for test
import cv2
import os
from loguru import logger
import numpy as np
import time


def pad_vector(
    vector: np.ndarray,
    overlap_length: int,
    mode: Literal[
        "edge",
        "mean",
        "median",
        "reflect",
        "symmetric",
    ] = "edge",
) -> np.ndarray:
    # create padding image
    padded_vector = np.pad(
        vector,
        pad_width=(
            (overlap_length, overlap_length),
            (overlap_length, overlap_length),
            (0, 0),
        ),
        mode=mode,
    )
    return padded_vector


@dataclass
class PatchPosition:
    target_pos: int
    target_length: int
    patch_length: int

    def __iter__(self):
        yield self.p1
        yield self.p2

    @property
    def p1(self) -> int:
        assert (
            self.target_pos < self.target_length
        ), f"ERROR, assert self.target_pos < self.target_length"
        return self.target_pos

    @property
    def p2(self) -> int:
        pos = self.target_pos + self.patch_length
        pos = pos if pos < self.target_length else self.target_length
        assert pos != self.p1, f"ERROR, pos != self.p1"
        return pos

    @property
    def dp(self) -> int:
        dp = self.p2 - self.p1
        assert dp > 0, f"ERROR, p1 and p2 are same. p1: {self.p1}, p2: {self.p2}"
        return dp

    @property
    def range(self) -> slice:
        return slice(self.p1, self.p2)


@dataclass
class PatchPositionXY:
    x: PatchPosition
    y: PatchPosition


class PatchPosXYCollection:
    def __init__(self, patch_pos_list: List[List[PatchPositionXY]]):
        self.patch_pos_list = patch_pos_list

    def __iter__(self):
        for poses in self.__patch_pos_list:
            for pos in poses:
                yield pos

    def __len__(self):
        return self.__size

    def __getitem__(self, idx):
        y = idx // self.__cols
        x = idx % self.__cols
        return self.__patch_pos_list[y][x]

    def get_patch(
        self,
        vector: np.ndarray,
    ) -> List[np.ndarray]:
        return [vector[pos.y.range, pos.x.range] for pos in self]

    def set_patch(
        self,
        vector: np.ndarray,
        patches: List[np.ndarray],
        overlab_length: int,
    ):
        for pos, patch in zip(self, patches, strict=True):  # inplace copy
            h, w, c = patch.shape
            vector[pos.y.range, pos.x.range] = patch[
                overlab_length : overlab_length + pos.y.dp,
                overlab_length : overlab_length + pos.x.dp,
            ]

    @property
    def patch_pos_list(self) -> List[List[PatchPositionXY]]:
        return self.__patch_pos_list

    @patch_pos_list.setter
    def patch_pos_list(self, patch_pos_list: List[List[PatchPositionXY]]):
        self.__rows = len(patch_pos_list)
        self.__cols = len(patch_pos_list[0])
        assert all([len(c) == self.__cols for c in patch_pos_list])
        self.__size = self.__rows * self.__cols
        self.__patch_pos_list = patch_pos_list

    @property
    def rows(self):
        return self.__rows

    @property
    def cols(self):
        return self.__cols

    @property
    def size(self):
        return self.__size

    @property
    def shape(self):
        return (self.rows, self.cols)

    @staticmethod
    def create(
        vector_shape: Tuple[int, int, int],
        patch_shape: Tuple[int, int, int],
        overlap_length: int,
    ):
        vector_height, vector_width, vector_c = vector_shape
        shape_height, shape_width, shape_c = patch_shape
        overlap_length = overlap_length
        pos_y = 0
        pos_x = 0
        patch_rows = 0
        patch_cols = 0
        pos_list: List[List[PatchPositionXY]] = []
        # loop for y
        while pos_y < vector_height - overlap_length * 2:
            pos_x = 0
            p_list_for_cols: List[PatchPositionXY] = []
            # loop for x
            while pos_x < vector_width - overlap_length * 2:
                p_list_for_cols.append(
                    PatchPositionXY(
                        PatchPosition(pos_x, vector_width, shape_width),
                        PatchPosition(pos_y, vector_height, shape_height),
                    )
                )
                pos_x = pos_x + shape_width - (overlap_length * 2)
                patch_cols += 1
            pos_list.append(p_list_for_cols)
            pos_y = pos_y + shape_height - (overlap_length * 2)
            patch_rows += 1
        return PatchPosXYCollection(patch_pos_list=pos_list)


class Patcher:

    def __init__(
        self,
        input_vector_shape: Tuple[int, int, int],
        input_patch_shape: Tuple[int, int, int],
        input_overlap_length: int,
        output_vector_shape: Tuple[int, int, int],
        output_patch_shape: Tuple[int, int, int],
        output_overlap_length: int,
    ) -> None:
        assert input_overlap_length > -1, "assert input_overlap_length > -1"
        assert output_overlap_length > -1, "assert output_overlap_length > -1"
        assert all(
            [e > 0 for e in input_patch_shape]
        ), "assert all([e > 0 for e in input_patch_shape])"
        assert all(
            [e > 0 for e in output_patch_shape]
        ), "assert all([e > 0 for e in output_patch_shape])"
        assert (
            len(input_patch_shape) == 3
        ), "assert len(input_patch_shape) == 3"  # only allow image-like vector
        assert (
            len(output_patch_shape) == 3
        ), "assert len(output_patch_shape) == 3"  # only allow image-like vector

        input_pos_collection = PatchPosXYCollection.create(
            vector_shape=input_vector_shape,
            patch_shape=input_patch_shape,
            overlap_length=input_overlap_length,
        )
        output_pos_collection = PatchPosXYCollection.create(
            vector_shape=output_vector_shape,
            patch_shape=output_patch_shape,
            overlap_length=0,
        )
        assert (
            input_pos_collection.shape == output_pos_collection.shape
        ), f"assert input_pos_collection.shape == output_pos_collection.shape | {input_pos_collection.shape} != {output_pos_collection.shape}"
        self._input_pos_collection = input_pos_collection
        self._output_pos_collection = output_pos_collection
        self._input_overlap_length = input_overlap_length
        self._output_overlap_length = output_overlap_length

    def slice(self, input_vector: np.ndarray):  # -> List[ndarray[Any, Any]]:
        return self._input_pos_collection.get_patch(input_vector)

    def merge(self, output_vector: np.ndarray, patches: List[np.ndarray]):
        self._output_pos_collection.set_patch(
            vector=output_vector,
            patches=patches,
            overlab_length=self._output_overlap_length,
        )
