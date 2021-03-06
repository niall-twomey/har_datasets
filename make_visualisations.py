from src import load_datasets_metadata
from src import load_pipelines_metadata
from src import load_visualisations_metadata
from src import pipeline_importer
from src import randomised_order
from src import visualisation_importer


def main():
    datasets = load_datasets_metadata()
    chains = load_pipelines_metadata()
    visualisations = load_visualisations_metadata()

    for dataset_name in randomised_order(datasets.keys()):
        if dataset_name != "anguita2013":
            continue
        for chain_name in randomised_order(chains.keys()):
            chain = pipeline_importer(chain_name, name=dataset_name)
            for visualisation_name in randomised_order(visualisations.keys()):
                print(dataset_name, chain_name, visualisation_name)
                visualisation_importer(visualisation_name, parent=chain).evaluate_outputs()


if __name__ == "__main__":
    main()
