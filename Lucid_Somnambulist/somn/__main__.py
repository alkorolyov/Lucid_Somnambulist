##Something
import sys
import logging
import pickle
from time import time
from sys import argv
from argparse import ArgumentParser

import pandas as pd

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s',
                    level=logging.DEBUG,
                    datefmt='%d-%m-%Y %I:%M:%S')

use_msg = """
Welcome to the somn command-line interface. 

[NORMAL USE] To make predictions from pre-trained models, use:
predict [project ID with pre-trained models] [model set ID of specific pre-trained models]  [new prediction ID]

[POWER USER USE] To retrain models, two steps are required: generating a particular set of partitions, then optimizing hyperparameters
partition-wise. These are separated so that custom preprocessing or features can be incorporated at the partition step,
and custom modeling changes can be incorporated or tested at the modeling step. New data for training should be 
incorporated into the dataset_yields.hdf5 file for inclusion in the retraining process.

To create new partitions, use:
partition [project ID, new or old project with no partitions] 

To train a new model set on partitions, use:
learn [project ID with partitions] [new ID for model set]
"""


def _run_predictions(args):
    """
    parse options for predict CLI

    Wrapper that runs main() from predict workflow

    ProjectID, model set ID, and new identifier for predictions are required arguments

    """
    opts = args.options
    from somn.workflows.predict import main as predict

    predict(args=opts)
    print(
        f"Finished generating predictions for project {opts[0]}, model set {opts[1]}, called {opts[2]}."
    )


def _train_models(args):
    """
    Wrapper that trains new models from CLI arguments.
    """
    opts = args.options
    from somn.workflows.learn import main as learn

    try:
        learn(args=opts)
    except:
        raise Warning(
            f"Looks like {opts} in the learning workfow led to an error. Check if job trained any partitions, \
and if it did, then try re-starting the job with the same input arguments (known memory leak in Keras backend can cause this) \
Otherwise, check input arguments to ensure that a valid project ID was passed."
        )


def _generate_partitions(args):
    """
    Wrapper that generates partitions

    DEV - checked for "last" and "new" operation.
    """
    opts = args.options
    ## DEV
    logging.debug(opts)

    start = time()
    from somn.workflows.partition import main as partition, get_precalc_sub_desc
    from somn.workflows.calculate import main as calc_sub
    from somn.workflows.calculate import preprocess
    from copy import deepcopy
    from somn.util.project import Project
    logging.debug(f'partition imports {time() - start: .3f}s')

    ## IDENTIFY OR CREATE AND INSTANTIATE PROJECT ##
    if opts[0] == "new":
        assert len(opts) >= 2
        project = Project()
        project.save(identifier=opts[1])  ####DEV####
    else:
        try:
            project = Project.reload(how=opts[0])
        except:
            raise Exception(
                "Must pass valid identifier or 'last' to load project. Can also say 'new' and give an identifier"
            )
    ## CHECK FOR OPTIONAL VALIDATION FLAG - USE AS TEMPLATE TO INTRODUCE MORE OPTIONS LATER ##
    if "val" in opts:
        val_schema = opts[opts.index("val") + 1]
    else:
        val_schema = "vi_to"
    # print("DEV - val_schema: ", val_schema)
    logging.debug(f"val_schema: {val_schema}")
    assert val_schema in [
        "to_vi",
        "vi_to",
        "random",
        "vo_to",
        "to_vo",
        "noval_to",
        "to_noval",
    ]
    ## BEGINNING PREP - LOAD STATIC DATA/PREREQUISITES TO DESCRIPTORS
    start = time()
    (
        amines,
        bromides,
        dataset,
        handles,
        unique_couplings,
        a_prop,
        br_prop,
        base_desc,
        solv_desc,
        cat_desc,
    ) = preprocess.load_data(optional_load="maxdiff_catalyst")
    logging.debug(f'preprocess.load_data() {time() - start:.3f}s')

    # DEBUG
    # return


    start = time()
    # Checking project status to make sure sub descriptors are calculated
    sub_desc = get_precalc_sub_desc()
    if not sub_desc:  # Need to calculate
        real, rand = calc_sub(
            project, optional_load="maxdiff_catalyst", substrate_pre=("corr", 0.95)
        )
        sub_am_dict, sub_br_dict, cat_desc, solv_desc, base_desc = real
    else:  # Already calculated descriptors, just fetching them
        sub_am_dict, sub_br_dict, rand = sub_desc
        real = (sub_am_dict, sub_br_dict, cat_desc, solv_desc, base_desc)
    combos = pickle.loads(
        pickle.dumps(unique_couplings, -1)
    )  # This is a guide for building the partitions out - really, any set of combinations can be specified.
    # The amine_bromide individual elements in this list will direct out-of-sample partitioning (if relevant in val_schema).
    # Any specific set of out-of-sample partitions can be designed and introduced here. This *could* be an optional input from
    # the user (e.g. a csv file with a list of items in it).
    import os

    logging.debug(f'get_precalc_sub_desc() {time() - start:.3f}s')

    # print(pd.DataFrame(combos).to_string())
    outdir = deepcopy(f"{project.partitions}/")
    os.makedirs(outdir + "real/", exist_ok=True)
    # os.makedirs(outdir + "rand/", exist_ok=True)
    realout = outdir + "real/"
    # randout = outdir + "rand/"
    logging.debug("partition()")
    project.combos = combos
    project.unique_couplings = unique_couplings
    project.dataset = dataset
    partition(
        project,
        val_schema=val_schema,
        vt=0,
        mask_substrates=True,
        rand=rand,
        real=real,
        serialize_rand=False,
    )
    print(
        f"Finished calculating partitions for {project.unique}, stored at {project.partitions}."
    )


def _calculate_parse_options(args):
    """
    parse options
    """
    ...


def _add_parse_options(args):
    """
    parse options
    """
    ...


def _visualize_parse_options(args):
    """
    parse options
    """
    ...


helpblock = f"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ SOMN CLI ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use the somn CLI, select an operation (e.g. add, calculate, partition, learn, or predict) followed by the
operation-specific arguments. Documentation should describe the required arguments.

Here is a simple summary/guide:

{use_msg}"""


def main():
    logging.debug("module")
    parser = ArgumentParser(usage=use_msg)
    parser.add_argument(
        nargs="?",
        choices=[
            "predict",
            "partition",
            "learn",
            "add",
            "calculate",
            "visualize",
            "help",
        ],
        dest="operation",
        default="help",
    )
    parser.add_argument(
        dest="options",
        nargs="*",
        default=False,
    )
    args = parser.parse_args()

    logging.debug(f"command line args: {args}")

    if args.operation == "predict":  ## Make predictions
        try:
            _run_predictions(args)
        except:
            raise Warning(
                f"Looks like handling the predict workflow with the arguments: [{args.options}] failed. \
Check that a project ID, model set ID, and a new identifier are present (in that order)."
            )
    elif args.operation == "help":
        print(helpblock)
    elif args.operation == "learn":  ## Train models
        try:
            _train_models(args)
        except:
            raise Warning(
                f"Looks like handling arguments for model training failed with {args.options}. \
Ensure that a project ID and a new, unique model set ID are being passed (in that order)."
            )
    elif args.operation == "partition":  ## Generate partitions
        try:
            _generate_partitions(args)
        except:
            raise Warning(
                f"Looks like handling the partition arguments {args.options} led to an error. \
Ensure that project ID is provided, or specify 'new'."
            )
    elif args.operation in ["add", "calculate", "visualize"]:
        raise Exception(
            f"DEV - {args.operation} implementation through CLI is under development"
        )


if __name__ == "__main__":
    pass
    # sys.argv[1:] = ['partition', 'new', 'test_proj'] # run once
    # sys.argv[1:] = ['learn', 'last', 'test_exp']

    # smi BrC1=NC=C(C)C(Cl)=C1 el
    # smi CC1C(C)NCCO1 nuc
    sys.argv[1:] = ['predict', 'last', 'test_exp', 'test_pred']
    main()
