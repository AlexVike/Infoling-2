from haystack.nodes import FARMReader


# Das Model deepset/gelectra-base-germanquad-distilled wird mit unseren Daten gefinetuned.
reader = FARMReader(model_name_or_path="deepset/gelectra-base-germanquad-distilled", use_gpu=True, num_processes=1)
data_dir = "QA/finetuning_data"

reader.train(data_dir=data_dir, train_filename="training_data_finetuning.json", use_gpu=True, n_epochs=1, save_dir="QA/my_model", num_processes=1)
# Das Model wird abgespeichert und für das Projekt verwendet.
reader.save(directory="QA/my_model")
new_reader = FARMReader(model_name_or_path="QA/my_model")