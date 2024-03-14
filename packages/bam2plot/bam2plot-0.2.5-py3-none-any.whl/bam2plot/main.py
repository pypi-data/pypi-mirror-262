from pathlib import Path
import subprocess
import fire
import pysam
import pandas as pd
from io import StringIO
import _io
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import os
import platform
import pandas
import matplotlib.ticker as mtick
import numpy as np


# for windows users
if platform.system() == "Windows":
    matplotlib.use("Agg")

sns.set_theme()


SORTED_TEMP = "TEMP112233.sorted.bam"
SORTED_TEMP_INDEX = f"{SORTED_TEMP}.bai"

COVERAGE_VALUES = [
    0,
    1,
    5,
    10,
    15,
    20,
    25,
    30,
    40,
    70,
    100,
]


def sort_bam(bam: str, new_name: str) -> None:
    pysam.sort("-o", new_name, bam)


def index_bam(bam: str, new_name: str) -> None:
    pysam.index(bam, new_name)


def run_perbase(bam: str) -> _io.StringIO:
    return StringIO(
        subprocess.check_output(
            f"perbase only-depth {bam}", shell=True, stderr=subprocess.DEVNULL
        ).decode(errors="ignore")
    )


def perbase_to_df(perbase: _io.StringIO) -> pd.DataFrame:
    return (
        pd.read_csv(
            perbase,
            sep="\t",
        )
        .rename(columns={"REF": "id", "POS": "Position", "DEPTH": "coverage"})
        .assign(coverage=lambda x: x.coverage.fillna(0))
        .assign(n_bases=lambda x: x.END - x.Position)
    )


def print_coverage_info(df: pd.DataFrame, threshold: int) -> None:
    name = df.iloc[0].id
    print(f"Coverage information for: {name}")
    print(f"{np.mean(df['coverage'] == 0) * 100: .2f}% bases with 0 coverage")
    print(
        f"{np.mean(df['coverage'] <= threshold) * 100: .2f}% bases with a coverage under {threshold}X"
    )
    print(f"median coverage: {df['coverage'].median(): .0f}X")
    print(f"mean coverage: {df['coverage'].mean(): .0f}X")


def print_total_reference_info(df: pd.DataFrame, threshold: int) -> None:
    mean_coverage = df.coverage.mean()
    coverage_over_threshold = (
        sum(1 if x > threshold else 0 for x in df.coverage) / df.shape[0] * 100
    )
    print(f"Mean coverage of all basepairs: {mean_coverage: .1f}X")
    print(
        f"Percent bases with coverage above {threshold}X: {coverage_over_threshold: .1f}%"
    )


def plot_coverage(
    mpileup_df: pd.DataFrame,
    sample_name: str,
    threshold: int,
    rolling_window: int,
    log_scale: bool = False,
) -> matplotlib.figure.Figure:
    if log_scale:
        mpileup_df = (
                mpileup_df
                .assign(coverage=lambda x: np.log10(x.coverage + 1))
                .assign(Depth=lambda x: np.log10(x.Depth + 1))
        )
        threshold = np.log10(threshold)

    mean_coverage = mpileup_df.coverage.mean()
    coverage = (
        sum(1 if x > threshold else 0 for x in mpileup_df.coverage)
        / mpileup_df.shape[0]
        * 100
    )

    coverage_plot = plt.figure(figsize=(15, 8))
    sns.lineplot(data=mpileup_df, x="Position", y="Depth")
    zero = plt.axhline(y=0, color="red")
    zero.set_label("Zero")
    mean = plt.axhline(y=mean_coverage, color="green")
    mean.set_label(f"Mean coverage: {mean_coverage: .1f}X")
    plt.legend(loc="upper right")
    plt.title(
        f"Percent bases with coverage above {threshold}X: {coverage: .1f}% | Rolling window: {rolling_window} nt"
    )
    plt.suptitle(f"Ref: {mpileup_df.iloc[0].id} | Sample: {sample_name}")
    plt.close()
    return coverage_plot


def coverage_for_value(df: pd.DataFrame, COVERAGE: int):
    number_of_bases = df.n_bases.sum()
    _id = df.id.iloc[0]
    percent = (
        df.loc[lambda x: x.coverage >= COVERAGE].n_bases.sum() / number_of_bases * 100
    )
    return pd.DataFrame(
        {
            "coverage": [COVERAGE],
            "percent": [percent],
            "id": [_id],
        }
    )


def coverage_for_many_values(df: pd.DataFrame, values) -> pd.DataFrame:
    dfs = []
    for coverage in values:
        coverage_df = coverage_for_value(df, coverage)
        dfs.append(coverage_df)
    return pd.concat(dfs, ignore_index=True)


def plot_cumulative_coverage_for_all(perbase_df: pd.DataFrame):
    all_coverage = pd.concat(
        [
            coverage_for_many_values(
                perbase_df.loc[lambda x: x.id == ref], COVERAGE_VALUES
            )
            for ref in perbase_df.id.unique()
        ]
    )
    grid = sns.FacetGrid(all_coverage, col="id", height=2.5, col_wrap=5)
    grid.map_dataframe(sns.lineplot, x="coverage", y="percent")
    plt.close()
    return grid.fig


def make_dir(outpath: str) -> None:
    outpath = Path(outpath)
    if not outpath.exists():
        outpath.mkdir(parents=True)


def cli(
    bam: str,
    outpath: str = "",
    whitelist: list = None,
    rolling_window: int = 10,
    threshold: int = 3,
    index: bool = False,
    sort_and_index: bool = False,
    zoom: bool | str = False,
    log_scale: bool = False,
    cum_plot: bool = False,
) -> None:
    if zoom:
        start = int(zoom.split(" ")[0])
        end = int(zoom.split(" ")[1])
        if start >= end:
            print("Start value of zoom must be lower than end value.")
            exit(1)

    if not Path(bam).exists():
        print(f"The file {bam} does not exist")
        exit(1)

    if outpath == "":
        outpath = "bam2plot"
        make_dir(outpath)
    else:
        make_dir(outpath)

    sample_name = Path(bam).stem

    if sort_and_index:
        print("Sorting bam file")
        sort_bam(bam, new_name=SORTED_TEMP)
        print("Indexing bam file")
        index_bam(SORTED_TEMP, new_name=SORTED_TEMP_INDEX)
        perbase = run_perbase(SORTED_TEMP)
        os.remove(SORTED_TEMP)
        os.remove(SORTED_TEMP_INDEX)
    else:
        if index:
            print("Indexing bam file")
            index_name = f"{bam}.bai"
            index_bam(bam, new_name=index_name)
        perbase = run_perbase(bam)
        if index:
            os.remove(index_name)

    try:
        print("-----------------------------")
        print("Processing dataframe")
        df = perbase_to_df(perbase)
    except pandas.errors.EmptyDataError as e:
        print("Error while processing bam")
        if not sort_and_index:
            print("Is the file indexed? If not, run 'bam2plot <file.bam> -i True'")
            print("Is the file sorted? If not, run 'bam2plot <file.bam> -s True'")
            exit(1)
        if not index:
            print("Is the file indexed? If not, run 'bam2plot <file.bam> -i True'")
            exit(1)
    print("-----------------------------")
    print("")

    print("-----------------------------")
    # Average coverage for total reference
    print_total_reference_info(df, threshold)
    print("-----------------------------")
    print("")

    print("-----------------------------")
    # filter the df to wanted ref or chromosomes:
    if whitelist:
        whitelist = [whitelist] if type(whitelist) == str else whitelist
        print(f"Only looking for references in the whitelist: {whitelist}")
        df = df.loc[lambda x: x.id.isin(whitelist)]

    plot_number = df.id.nunique()
    if plot_number == 0:
        print("No reference to plot against!")
        exit(1)

    print(f"Generating {plot_number} plots:")
    print("-----------------------------")
    print("")
    out_file = f"{outpath}/{sample_name}_bam2plot"
    for reference in df.id.unique():
        mpileup_df = df.loc[lambda x: x.id == reference].assign(
            Depth=lambda x: x.coverage.rolling(rolling_window).mean()
        )
        if zoom:
            mpileup_df = mpileup_df.loc[lambda x: x.Position.between(start, end)]
            if mpileup_df.shape[0] == 0:
                print("No positions to plot after zoom")
                continue
                #exit(1)
                
        if mpileup_df.shape[0] == 0:
            print("No positions to plot")
            continue
            #exit(1)

        print("-----------------------------")
        print_coverage_info(mpileup_df, threshold)

        plot = plot_coverage(
            mpileup_df, sample_name, threshold=threshold, rolling_window=rolling_window, log_scale=log_scale
        )

        name = f"{out_file}_{reference}"
        plot.savefig(f"{name}.svg")
        plot.savefig(f"{name}.png")
        print(f"Plot for {reference} generated")
        print("-----------------------------")
        print("")

    print("-----------------------------")
    print("Coverage plots done!")
    print("-----------------------------")
    print("")

    print("-----------------------------")
    if cum_plot:
        print("Generating cumulative coverage plots for each reference")
        cum_plot = plot_cumulative_coverage_for_all(df)
        cum_plot_name = f"{outpath}/{Path(bam).stem}_cumulative_coverage"
        cum_plot.savefig(f"{cum_plot_name}.png")
        cum_plot.savefig(f"{cum_plot_name}.svg")
        print(f"Cumulative plot generated!")
        print("-----------------------------")
        print("")

    print("-----------------------------")
    print("Plots done!")
    print(f"Plots location: {Path(outpath).resolve()}")
    print("-----------------------------")
    print("")
    exit(0)


def run() -> None:
    fire.Fire(cli)
