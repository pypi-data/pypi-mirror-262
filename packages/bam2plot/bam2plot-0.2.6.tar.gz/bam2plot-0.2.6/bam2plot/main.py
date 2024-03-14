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
import argparse


class bcolors:
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    UNDERLINE = "\033[4m"


def print_green(text):
    print(f"{bcolors.OKGREEN}{text}{bcolors.ENDC}")


def print_warning(text):
    print(f"{bcolors.WARNING}{bcolors.UNDERLINE}{text}{bcolors.ENDC}")


def print_fail(text):
    print(f"{bcolors.FAIL}{bcolors.UNDERLINE}{text}{bcolors.ENDC}")


def print_blue(text):
    print(f"{bcolors.OKBLUE}{text}{bcolors.ENDC}")


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
    print_blue(f"[SUMMARIZE]: Coverage information for: {name}")
    print_blue(
        f"   [SUMMARIZE]: {np.mean(df['coverage'] == 0) * 100: .2f}% bases with 0 coverage"
    )
    print_blue(
        f"   [SUMMARIZE]: {np.mean(df['coverage'] <= threshold) * 100: .2f}% bases with a coverage under {threshold}X"
    )
    print_blue(f"   [SUMMARIZE]: median coverage: {df['coverage'].median(): .0f}X")
    print_blue(f"   [SUMMARIZE]: mean coverage: {df['coverage'].mean(): .0f}X")


def print_total_reference_info(df: pd.DataFrame, threshold: int) -> None:
    mean_coverage = df.coverage.mean()
    coverage_over_threshold = (
        sum(1 if x > threshold else 0 for x in df.coverage) / df.shape[0] * 100
    )
    print_blue(f"[SUMMARIZE]: Mean coverage of all basepairs: {mean_coverage: .1f}X")
    print_blue(
        f"[SUMMARIZE]: Percent bases with coverage above {threshold}X: {coverage_over_threshold: .1f}%"
    )


def plot_coverage(
    mpileup_df: pd.DataFrame,
    sample_name: str,
    threshold: int,
    rolling_window: int,
    log_scale: bool = False,
) -> matplotlib.figure.Figure:
    if log_scale:
        mpileup_df = mpileup_df.assign(
            coverage=lambda x: np.log10(x.coverage + 1)
        ).assign(Depth=lambda x: np.log10(x.Depth + 1))
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


def cli():
    parser = argparse.ArgumentParser(description="Plot your bam files!")
    parser.add_argument("-b", "--bam", required=True, help="bam file")
    parser.add_argument(
        "-o",
        "--outpath",
        required=False,
        default="bam2plots",
        help="Where to save the plots.",
    )
    parser.add_argument(
        "-w",
        "--whitelist",
        required=False,
        default=None,
        help="Only include these references/chromosomes.",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        required=False,
        default=3,
        help="Threshold of mean coverage depth",
    )
    parser.add_argument(
        "-r", "--rolling_window", required=False, default=10, help="Rolling window size"
    )
    parser.add_argument(
        "-i", "--index", required=False, default=False, help="Index bam file"
    )
    parser.add_argument(
        "-s",
        "--sort_and_index",
        required=False,
        default=False,
        help="Index and sort bam file",
    )
    parser.add_argument(
        "-z",
        "--zoom",
        required=False,
        default=False,
        help="Zoom into this region. Example: -z='100 2000'",
    )
    parser.add_argument(
        "-l", "--log_scale", required=False, default=False, help="Log scale of Y axis"
    )
    parser.add_argument(
        "-c",
        "--cum_plot",
        required=False,
        default=False,
        help="Generate cumulative plots of all chromosomes",
    )

    args = parser.parse_args()

    main(
        bam=args.bam,
        outpath=args.outpath,
        whitelist=args.whitelist,
        rolling_window=args.rolling_window,
        threshold=args.threshold,
        index=args.index,
        sort_and_index=args.sort_and_index,
        zoom=args.zoom,
        log_scale=args.log_scale,
        cum_plot=args.cum_plot,
    )


def if_sort_and_index(sort_and_index, index, bam):
    if not sort_and_index and not index:
        return run_perbase(bam)

    if sort_and_index:
        print_green("[INFO]: Sorting bam file")
        sort_bam(bam, new_name=SORTED_TEMP)
        print_green("[INFO]: Indexing bam file")
        index_bam(SORTED_TEMP, new_name=SORTED_TEMP_INDEX)
    if index:
        print_green("[INFO]: Indexing bam file")
        index_name = f"{bam}.bai"
        index_bam(bam, new_name=index_name)

    try:
        if sort_and_index:
            perbase = run_perbase(SORTED_TEMP)
        if index:
            perbase = run_perbase(bam)
    except:
        print_fail("[ERROR]: Could not run perbase on bam file")
        exit(1)
    finally:
        if sort_and_index:
            os.remove(SORTED_TEMP)
            os.remove(SORTED_TEMP_INDEX)
        if index:
            os.remove(index_name)

        return perbase


def process_dataframe(perbase, sort_and_index, index):
    try:
        print_green("[INFO]: Processing dataframe")
        df = perbase_to_df(perbase)
    except:
        print_fail("[ERROR]: Could not process dataframe")
        if not sort_and_index:
            print_warning(
                "[WARNING]: Is the file indexed? If not, run 'bam2plot <file.bam> -i True'"
            )
            print_warning(
                "[WARNING]: Is the file sorted? If not, run 'bam2plot <file.bam> -s True'"
            )
            exit(1)
        if not index:
            print_warning(
                "[WARNING]: Is the file indexed? If not, run 'bam2plot <file.bam> -i True'"
            )
            exit(1)

    return df


def main(
    bam,
    outpath,
    whitelist,
    rolling_window,
    threshold,
    index,
    sort_and_index,
    zoom,
    log_scale,
    cum_plot,
) -> None:
    print_green(f"[INFO]: Running bam2plot on {bam}!")
    if zoom:
        start = int(zoom.split(" ")[0])
        end = int(zoom.split(" ")[1])
        if start >= end:
            print_fail("[ERROR]: Start value of zoom must be lower than end value.")
            exit(1)

    if not Path(bam).exists():
        print_fail(f"[ERROR]: The file {bam} does not exist")
        exit(1)

    make_dir(outpath)
    sample_name = Path(bam).stem

    perbase = if_sort_and_index(sort_and_index, index, bam)

    df = process_dataframe(perbase, sort_and_index, index)

    print_total_reference_info(df, threshold)

    if whitelist:
        whitelist = [whitelist] if type(whitelist) == str else whitelist
        print_green(
            f"[INFO]: Only looking for references in the whitelist: {whitelist}"
        )
        df = df.loc[lambda x: x.id.isin(whitelist)]

    plot_number = df.id.nunique()
    if plot_number == 0:
        print_fail("[ERROR]: No reference to plot against!")
        exit(1)

    print_green(f"[INFO]: Generating {plot_number} plots:")
    out_file = f"{outpath}/{sample_name}_bam2plot"
    for reference in df.id.unique():
        mpileup_df = df.loc[lambda x: x.id == reference].assign(
            Depth=lambda x: x.coverage.rolling(rolling_window).mean()
        )
        if zoom:
            mpileup_df = mpileup_df.loc[lambda x: x.Position.between(start, end)]
            if mpileup_df.shape[0] == 0:
                print_warning("[WARNING]: No positions to plot after zoom")
                continue

        if mpileup_df.shape[0] == 0:
            print_warning("[WARNING]: No positions to plot")
            continue

        print_coverage_info(mpileup_df, threshold)

        plot = plot_coverage(
            mpileup_df,
            sample_name,
            threshold=threshold,
            rolling_window=rolling_window,
            log_scale=log_scale,
        )

        name = f"{out_file}_{reference}"
        plot.savefig(f"{name}.svg")
        plot.savefig(f"{name}.png")
        print_green(f"[INFO]: Plot for {reference} generated")

    print_green("[INFO]: Coverage plots done!")

    if cum_plot:
        print_green("[INFO]: Generating cumulative coverage plots for each reference")
        cum_plot = plot_cumulative_coverage_for_all(df)
        cum_plot_name = f"{outpath}/{Path(bam).stem}_cumulative_coverage"
        cum_plot.savefig(f"{cum_plot_name}.png")
        cum_plot.savefig(f"{cum_plot_name}.svg")
        print_green(f"[INFO]: Cumulative plot generated!")

    print_green(f"[INFO]: Plots location: {Path(outpath).resolve()}")
    exit(0)


if __name__ == "__main__":
    cli()
