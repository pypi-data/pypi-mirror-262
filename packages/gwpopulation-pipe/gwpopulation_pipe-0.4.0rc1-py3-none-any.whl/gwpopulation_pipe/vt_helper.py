from dataclasses import dataclass, field
from pathlib import Path

import dill
import h5py
import numpy as np
from bilby.core.utils import logger

from gwpopulation.utils import xp
from gwpopulation.vt import GridVT, ResamplingVT
from .utils import get_path_or_local

N_EVENTS = np.nan


def dummy_selection(*args, **kwargs):
    return 1


def mass_only_scalar_calibrated_grid_vt(vt_file, model):
    selection = _mass_only_calibrated_grid_vt(
        vt_file=vt_file,
        model=model,
        calibration="scalar",
    )
    return selection


def mass_only_linear_calibrated_grid_vt(vt_file, model):
    selection = _mass_only_calibrated_grid_vt(
        vt_file=vt_file,
        model=model,
        calibration="linear",
    )
    return selection


def mass_only_quadratic_calibrated_grid_vt(vt_file, model):
    selection = _mass_only_calibrated_grid_vt(
        vt_file=vt_file,
        model=model,
        calibration="quadratic",
    )
    return selection


gaussian_mass_only_scalar_calibrated_grid_vt = mass_only_scalar_calibrated_grid_vt
gaussian_mass_only_linear_calibrated_grid_vt = mass_only_linear_calibrated_grid_vt
gaussian_mass_only_quadratic_calibrated_grid_vt = mass_only_quadratic_calibrated_grid_vt
broken_mass_only_scalar_calibrated_grid_vt = mass_only_scalar_calibrated_grid_vt
broken_mass_only_linear_calibrated_grid_vt = mass_only_linear_calibrated_grid_vt
broken_mass_only_quadratic_calibrated_grid_vt = mass_only_quadratic_calibrated_grid_vt


def _mass_only_calibrated_grid_vt(vt_file, model, calibration=None):
    import h5py

    model = model
    vt_data = dict()
    with h5py.File(vt_file) as _vt_data:
        vt_data["vt"] = _vt_data["vt_early_high"][:]
        if calibration is not None:
            vt_data["vt"] *= _vt_data[f"{calibration}_calibration"][:]
        vt_data["vt"] = xp.asarray(vt_data["vt"])
        vt_data["mass_1"] = xp.asarray(_vt_data["m1"][:])
        vt_data["mass_ratio"] = xp.asarray(_vt_data["q"][:])

    selection = GridVT(model=model, data=vt_data)
    return selection


@dataclass
class VTData:
    mass_1: np.ndarray
    mass_ratio: np.ndarray
    a_1: np.ndarray
    a_2: np.ndarray
    cos_tilt_1: np.ndarray
    cos_tilt_2: np.ndarray
    redshift: np.ndarray
    prior: np.ndarray
    total_generated: int
    analysis_time: float
    mass_2: np.ndarray = field(default=None, init=False)

    def append(self, other):
        self_sample_rate = self.analysis_time / self.total_generated
        other_sample_rate = other.analysis_time / other.total_generated
        self_weight = 2 * self_sample_rate / (self_sample_rate + other_sample_rate)
        other_weight = 2 * other_sample_rate / (self_sample_rate + other_sample_rate)
        for key in self.__dataclass_fields__:
            value = getattr(self, key)
            alt = getattr(other, key)
            if key == "mass_2":
                if value is None and alt is None:
                    continue
                elif value is not None and alt is not None:
                    setattr(self, key, np.concatenate([value, alt]))
                else:
                    raise ValueError("mass_2 is only defined for one VTData object")
            elif key in ["total_generated", "analysis_time"]:
                setattr(self, key, value + alt)
            elif key == "prior":
                setattr(
                    self,
                    key,
                    np.concatenate([value * self_weight, alt * other_weight]),
                )
            else:
                setattr(self, key, np.concatenate([value, alt]))

    def __add__(self, other):
        new = VTData(**self.__dict__)
        new += other
        return new

    def __iadd__(self, other):
        self.append(other)
        return self

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def items(self):
        return self.__dict__.items()

    def get(self, key, alt):
        return self.__dict__.get(key, alt)


def load_injection_data(vt_file, ifar_threshold=1, snr_threshold=11):
    """
    Load the injection file in the O3 injection file format.

    For mixture files and multiple observing run files we only
    have the full `sampling_pdf`.

    We use a different parameterization than the default so we require a few
    changes.

    - we parameterize the model in terms of primary mass and mass ratio and
      the injections are generated in primary and secondary mass. The Jacobian
      is `primary mass`.
    - we parameterize spins in spherical coordinates, neglecting azimuthal
      parameters. The injections are parameterized in terms of cartesian
      spins. The Jacobian is `1 / (2 pi magnitude ** 2)`.

    For O3 injections we threshold on FAR.
    For O1/O2 injections we threshold on SNR as there is no FAR
    provided by the search pipelines.

    Parameters
    ----------
    vt_file: str
        The path to the hdf5 file containing the injections.
    ifar_threshold: float
        The threshold on inverse false alarm rate in years. Default=1.
    snr_threshold: float
        The SNR threshold when there is no FAR. Default=11.

    Returns
    -------
    gwpop_data: dict
        Data required for evaluating the selection function.

    """
    logger.info(f"Loading VT data from {vt_file}.")
    if vt_file.endswith(".pkl"):
        with open(vt_file, "rb") as ff:
            data = dill.load(ff)
        for key, value in data.items():
            if isinstance(value, np.ndarray):
                data[key] = xp.asarray(value)
        return data

    with h5py.File(vt_file, "r") as ff:
        if "injections" in ff:
            data = ff["injections"]
            total_generated = int(data.attrs["total_generated"][()])
            analysis_time = data.attrs["analysis_time_s"][()] / 365.25 / 24 / 60 / 60
        elif "events" in ff:
            import pandas as pd

            data = pd.DataFrame(ff["events"][()]).to_dict(orient="list")
            data = {key: np.array(value) for key, value in data.items()}
            total_generated = int(ff.attrs["total_generated"][()])
            analysis_time = ff.attrs["total_analysis_time"][()] / 365.25 / 24 / 60 / 60
            if analysis_time == 0:
                analysis_time = 1 / 12
        else:
            raise KeyError(f"Unable to identify injections from {ff.keys()}")

        if "mass1_source" in data:
            mass_1_key = "mass1_source"
            mass_2_key = "mass2_source"
        else:
            mass_1_key = "mass_1_source"
            mass_2_key = "mass_2_source"
        if "redshift" in data:
            redshift_key = "redshift"
        else:
            redshift_key = "z"
        found = get_found_injections(data, ifar_threshold, snr_threshold)
        n_found = sum(found)
        if n_found == 0:
            raise ValueError("No sensitivity injections pass threshold.")
        gwpop_data = dict(
            mass_1=xp.asarray(data[mass_1_key][()][found]),
            mass_ratio=xp.asarray(
                data[mass_2_key][()][found] / data[mass_1_key][()][found]
            ),
            redshift=xp.asarray(data[redshift_key][()][found]),
            total_generated=total_generated,
            analysis_time=analysis_time,
        )
        for ii in [1, 2]:
            gwpop_data[f"a_{ii}"] = (
                xp.asarray(
                    data.get(f"spin{ii}x", np.zeros(n_found))[()][found] ** 2
                    + data.get(f"spin{ii}y", np.zeros(n_found))[()][found] ** 2
                    + data[f"spin{ii}z"][()][found] ** 2
                )
                ** 0.5
            )
            gwpop_data[f"cos_tilt_{ii}"] = (
                xp.asarray(data[f"spin{ii}z"][()][found]) / gwpop_data[f"a_{ii}"]
            )
        if "sampling_pdf" in data:
            gwpop_data["prior"] = (
                xp.asarray(data["sampling_pdf"][()][found])
                * xp.asarray(data[mass_1_key][()][found])
                * (2 * np.pi * gwpop_data["a_1"] ** 2)
                * (2 * np.pi * gwpop_data["a_2"] ** 2)
            )
        else:
            gwpop_data["prior"] = xp.exp(
                xp.sum(
                    [
                        xp.asarray(data[f"lnpdraw_{key}"][()][found])
                        for key in [
                            "mass1_source",
                            "mass2_source_GIVEN_mass1_source",
                            "z",
                            "spin1_magnitude",
                            "spin2_magnitude",
                            "spin1_polar_angle",
                            "spin2_polar_angle",
                        ]
                    ],
                    axis=0,
                )
            )
            gwpop_data["prior"] /= xp.sin(xp.arccos(gwpop_data["cos_tilt_1"]))
            gwpop_data["prior"] /= xp.sin(xp.arccos(gwpop_data["cos_tilt_2"]))
            gwpop_data["prior"] *= gwpop_data["mass_1"]
        if "v1_1ifo" in vt_file:
            gwpop_data["prior"] /= data["weights_1ifo"][()][found]
    return VTData(**gwpop_data)


def get_found_injections(data, ifar_threshold=1, snr_threshold=11):
    found = np.zeros_like(data["mass_1"], dtype=bool)
    if ifar_threshold is not None and "ifar" in any(
        [key.lower() for key in data.keys()]
    ):
        for key in data:
            if "ifar" in key.lower():
                found = found | (data[key] > ifar_threshold)
            if "name" in data.keys():
                gwtc1 = (data["name"] == b"o1") | (data["name"] == b"o2")
                found = found | (gwtc1 & (data["optimal_snr_net"] > snr_threshold))
        return found
    elif snr_threshold is not None:
        if "observed_phase_maximized_snr_net" in data.keys():
            found = found | (data["observed_phase_maximized_snr_net"] > snr_threshold)
        elif "observed_snr_net" in data.keys():
            found = found | (data["observed_snr_net"] > snr_threshold)
        return found
    else:
        raise ValueError("Cannot find keys to filter sensitivity injections.")


def injection_resampling_vt(vt_file, model, ifar_threshold=1, snr_threshold=11):
    import glob

    if "*" in vt_file:
        vt_files = glob.glob(vt_file)
        data = sum(
            [
                load_injection_data(
                    vt_file=get_path_or_local(filename),
                    ifar_threshold=ifar_threshold,
                    snr_threshold=snr_threshold,
                )
                for filename in vt_files
            ]
        )
    else:
        data = load_injection_data(
            vt_file=get_path_or_local(vt_file),
            ifar_threshold=ifar_threshold,
            snr_threshold=snr_threshold,
        )

    return ResamplingVT(model=model, data=data, n_events=N_EVENTS)


def injection_resampling_vt_no_redshift(
    vt_file, model, ifar_threshold=1, snr_threshold=11
):

    data = load_injection_data(
        vt_file=vt_file, ifar_threshold=ifar_threshold, snr_threshold=snr_threshold
    )
    data["prior"] = data["mass_1"] ** (-2.35 + 1) * data["mass_ratio"] ** 2

    return ResamplingVT(model=model, data=data, n_events=N_EVENTS)
