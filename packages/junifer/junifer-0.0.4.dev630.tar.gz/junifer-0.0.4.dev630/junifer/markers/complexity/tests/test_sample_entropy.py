"""Provide test for sample entropy."""

# Authors: Amir Omidvarnia <a.omidvarnia@fz-juelich.de>
#          Synchon Mandal <s.mandal@fz-juelich.de>
# License: AGPL

from pathlib import Path

import pytest


pytest.importorskip("neurokit2")

from junifer.datareader import DefaultDataReader  # noqa: E402
from junifer.markers.complexity import SampleEntropy  # noqa: E402
from junifer.storage import SQLiteFeatureStorage  # noqa: E402
from junifer.testing.datagrabbers import (  # noqa: E402
    SPMAuditoryTestingDataGrabber,
)


# Set parcellation
PARCELLATION = "Schaefer100x17"


def test_compute() -> None:
    """Test SampleEntropy compute()."""
    with SPMAuditoryTestingDataGrabber() as dg:
        # Fetch element
        element = dg["sub001"]
        # Fetch element data
        element_data = DefaultDataReader().fit_transform(element)
        # Initialize the marker
        marker = SampleEntropy(parcellation=PARCELLATION)
        # Compute the marker
        feature_map = marker.fit_transform(element_data)
        # Assert the dimension of timeseries
        assert feature_map["BOLD"]["data"].ndim == 2


def test_get_output_type() -> None:
    """Test SampleEntropy get_output_type()."""
    marker = SampleEntropy(parcellation=PARCELLATION)
    assert marker.get_output_type("BOLD") == "vector"


def test_store(tmp_path: Path) -> None:
    """Test SampleEntropy store().

    Parameters
    ----------
    tmp_path : pathlib.Path
        The path to the test directory.

    """
    with SPMAuditoryTestingDataGrabber() as dg:
        # Fetch element
        element = dg["sub001"]
        # Fetch element data
        element_data = DefaultDataReader().fit_transform(element)
        # Initialize the marker
        marker = SampleEntropy(parcellation=PARCELLATION)
        # Create storage
        storage = SQLiteFeatureStorage(
            uri=tmp_path / "test_sample_entropy.sqlite"
        )
        # Compute the marker and store
        marker.fit_transform(input=element_data, storage=storage)
